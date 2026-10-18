# h2_constraints.py  
#    ← make_extra_functionality(), store_shadow_prices(), _annual_flow()

import numpy as np
import pandas as pd
import xarray as xr

from .h2_presets import (
    H2_STORAGE, ELECTROLYSIS, ELECTROLYSIS_GRID, H2_LOAD, BATTERY
)
from .h2_scenario import resolve, water_limited_electrolyser_techs, electrolyser_techs

__all__ = ['make_extra_functionality', 'store_shadow_prices'] 

# --------------------------------------------------------------------------
# 4. Extra constraints (added to the optimisation problem)
# --------------------------------------------------------------------------

def _annual_flow(n, links, period, sns, eff_attr='efficiency'):
    """Linear expression: weighted annual flow of `links` in `period` at the port of eff_attr (per year)."""
    m = n.model
    p = m['Link-p']
    name_dim = [d for d in p.dims if d != 'snapshot'][0]
    pos = np.where(sns.get_level_values(0) == period)[0]
    w = n.snapshot_weightings.generators.iloc[pos].values            # hours per snapshot
    eff = n.links.loc[links, eff_attr].values
    coeff = np.outer(w, eff)                                          # (snapshot, link)
    sel = p.isel(snapshot=pos).sel({name_dim: list(links)})
    return (sel * coeff).sum()


def _capacity_cap(n, component, carriers, period, cap, name):
    """Sum of capacity of all active, extendable assets of these carriers <= cap (MW or MWh)."""
    c = {'Link': n.links, 'Generator': n.generators, 'Store': n.stores, 'StorageUnit': n.storage_units}[component]
    attr = 'e_nom' if component == 'Store' else 'p_nom'
    act = n.get_active_assets(component, period)
    names = [i for i in c.index[c.carrier.isin(carriers) & c[f'{attr}_extendable']] if act.get(i, False)]
    if not names:
        return
    var = n.model[f'{component}-{attr}']
    fixed = float(c.loc[c.carrier.isin(carriers) & ~c[f'{attr}_extendable'] & act.reindex(c.index, fill_value=False),
                        attr].sum())
    n.model.add_constraints(var.sel({var.dims[0]: names}).sum() <= cap - fixed, name=name)


def make_extra_functionality(scen):
    """Return a function for n.optimize(extra_functionality=...).

    The scenario limit itself is NOT here: it is a capacity constraint of the technology table (see above).
    """

    def extra_functionality(n, sns):
        periods = sns.get_level_values(0).unique()

        # CO2 storage capacity (MtCO2/yr captured, all CCS technologies together)
        cap = resolve('co2_storage_cap', scen.get('co2_storage_cap'))
        if cap is not None:
            ccs = n.links.index[n.links.get('bus3', pd.Series('', index=n.links.index)) == 'CO2 storage']
            for y in periods:
                if y in cap and len(ccs):
                    n.model.add_constraints(_annual_flow(n, ccs, y, sns, 'efficiency3') <= cap[y] * 1e6,
                                            name=f'CO2-storage_cap-{y}')

        # Build limits per period (electrolysers, offshore wind, nuclear) and the H2 storage that can exist (option)
        caps = list(resolve('capacity_caps', scen.get('capacity_caps')) or [])
        hcap = resolve('h2_storage_cap', scen.get('h2_storage_cap'))
        if scen.get('h2_storage') and hcap is not None:
            caps.append(dict(name='H2 storage', component='Store', carriers=H2_STORAGE, cap=hcap))
        for c in caps:
            for y in periods:
                if y in c['cap']:
                    _capacity_cap(n, c['component'], c['carriers'], y, c['cap'][y],
                                  name=f"Cap-{c['name'].replace(' ', '_')}-{y}")

        # Green lever: a minimum share of the hydrogen made by electrolysis (all electrolysers), per period
        mandate = scen.get('green_mandate') or {}
        if mandate:
            ely = n.links.index[n.links.carrier.isin(ELECTROLYSIS)]
            w_all = n.snapshot_weightings.generators
            for y in periods:
                share = mandate.get(y, mandate.get(str(y)))
                if not share:
                    continue
                sl = sns.get_level_values(0) == y
                p_set = n.get_switchable_as_dense('Load', 'p_set')[H2_LOAD]
                demand = float((p_set[sl] * w_all[sl]).sum())                             # MWh/yr in period y
                n.model.add_constraints(_annual_flow(n, ely, y, sns, 'efficiency') >= float(share) * demand,
                                        name=f'Green-mandate-{y}')

        # (1) Freshwater: the joint limit on grid electrolysers per vintage.
        total = scen.get('_electrolyser_cap_total_mw_h2') or {}
        techs = water_limited_electrolyser_techs(scen)
        if total and len(techs) > 1 and scen.get('electrolyser_limit_on', 'capacity') == 'capacity':
            var = n.model['Link-p_nom']
            ext = set(n.links.index[n.links.p_nom_extendable])
            for y, cap in total.items():
                names = [f'{t}_{y}' for t in techs if f'{t}_{y}' in ext]
                if not names:
                    continue
                eff = xr.DataArray([float(n.links.at[l, 'efficiency']) for l in names], coords={var.dims[0]: names})
                n.model.add_constraints((var.sel({var.dims[0]: names}) * eff).sum() <= cap,
                                        name=f'Electrolyser-total-cap-{y}')

        # Over-dimensioned plant with its own plant reference: water caps the hourly hydrogen output of all
        # electrolysers together at the MW that the water reference allows (the vintages still in use)
        water = scen.get('_electrolyser_water_mw_h2') or {}
        if water:
            p = n.model['Link-p']
            name_dim = [d for d in p.dims if d != 'snapshot'][0]
            ely_all = list(n.links.index[n.links.carrier.isin(electrolyser_techs(scen))])
            life = {int(v): float(n.links.at[f'{ELECTROLYSIS_GRID[0]}_{v}', 'lifetime'])
                    if f'{ELECTROLYSIS_GRID[0]}_{v}' in n.links.index else 25.0 for v in water}
            for y in periods:
                act = n.get_active_assets('Link', y)
                names = [l for l in ely_all if act.get(l, False)]
                if not names:
                    continue
                cap = sum(v for vy, v in water.items() if int(vy) <= y < int(vy) + life[int(vy)])
                pos = np.where(sns.get_level_values(0) == y)[0]
                eff = xr.DataArray(n.links.loc[names, 'efficiency'].values.astype(float), coords={name_dim: names})
                n.model.add_constraints((p.isel(snapshot=pos).sel({name_dim: names}) * eff).sum(name_dim) <= cap,
                                        name=f'Electrolyser-water-output-{y}')

        # (3b) Maximum battery power in each period (MW, summed over all active vintages)
        if scen['battery'] and scen['battery_max_mw'] is not None:
            for y in periods:
                _capacity_cap(n, 'StorageUnit', BATTERY, y, scen['battery_max_mw'], name=f'Battery-max_power-{y}')

    return extra_functionality