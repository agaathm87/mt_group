"""Build and solve the PyPSA energy model.

Hydrogen extension based on the final course model
---------------------------------------------------
Lines marked with ``# [H2]`` were added or changed for the hydrogen study.
Everything else is the P06 course model. Without the new keyword arguments,
``model_run`` behaves exactly as before (Gurobi, no scenario constraint).

New keyword arguments of ``model_run``:
    solver_name     'gurobi'
    solver_options  dict passed to the solver; default depends on the solver
    scenario        dict with scenario settings (see model.make_scenario), or None for the
                    plain course model
    results_dir     folder for the solver log
"""

import os

import numpy as np
import pandas as pd
import pypsa

# Logging to control running log output
import logging
logging.getLogger("pypsa").setLevel(logging.ERROR)
logging.getLogger("linopy").setLevel(logging.ERROR)
logging.getLogger("gurobipy").setLevel(logging.ERROR)

from .preprocessing import (
    preprocess_demand,
    preprocess_supply,
    preprocess_technologies,
    int_extrapolate
)

# ============================================================
# MODEL HELPER FUNCTIONS
# ============================================================

def annuity(disc_rate, life):
    return disc_rate / (1.0 - 1.0 / (1.0 + disc_rate) ** life)

def investment_cost(technology, year, techs_d, rt):
    capex = techs_d.at[(technology,'CAPEX'),year]
    fom = techs_d.at[(technology,'FOM'),year]
    lt = techs_d.at[(technology,'Lifetime'),year]
    return (capex*annuity(rt, lt) + fom) # (€/activity output unit)


def techs_by_type(techs_s, t):
    """Retrieve a list with all techs of type t (e.g link, generator, etc.)"""
    types = techs_s.query("Parameter=='Type'").reset_index()
    return list(types[types['Value']==t]['Technology'].unique())

#     - ```def get_topology(t)```:
def get_topology(techs_s, technology):
    """returns a df with the inputs and outputs of technology, with t's buses as index"""
    techdf = techs_s.loc[(technology,slice(None)),:].reset_index()
    techdf = techdf[techdf.Parameter.str.startswith('bus')].set_index('Parameter')
    return techdf

#     - ```def start_year(t)```:
def start_year(techs_s, technology, years):
    """if a start-year is specified returns it, otherwise default to years[0]"""
    try:
        sy = techs_s.at[(technology,'Start year'),'Value']
    except KeyError:
        sy = years[0]
    return sy


def static_value(techs_s, technology, parameter, default=None):  # [H2]
    """Return a static parameter (e.g. 'Max hours') or a default if it is not in the database."""
    try:
        return float(techs_s.at[(technology, parameter), 'Value'])
    except (KeyError, ValueError, TypeError):
        return default


def get_cap_constraints(t, years, cn):
    """
    Returns a df with any user-defined constraints (cn) on capacity for tech t.
    The base year is only used to set up fixed capacity bounds. This is not extrapolated to future years.
    Any min/max constraints set for future years are inter/extrapolated.
    Returns a NaN df if there are no constraints for t.
    """

    # Set up empty df
    df = pd.DataFrame(columns=['Technology','Type']+years)
    df.Technology = [t] * 2
    df.Type = ['min','max']
    df = df.set_index(['Technology','Type'])

    # Fill it with user-defined constraints from the technologies input table
    df.loc[:,:] = cn.loc[:,:]

    # The base year is only used to set up fixed capacity bounds, we don't want to extrapolate those to future years.
    # We only want to int/extrapolate if there are user-constraints on max or min cap limits after the base year:
    # Slice df for years > base year, and store index of non-nan values
    df_idx = df.loc[:,[y for y in years if ((y>years[0]) and (y in df.columns))]]
    idx = np.where(df_idx.notna())

    # If there are no non-nan values, return df as it is:
    if len(df_idx.iloc[idx[0],idx[1]])==0:
        ret = df

    # otherwise int-extrapolate:
    else:
        ret = int_extrapolate(df, years)

    return ret


def default_solver_options(solver_name, results_dir):  # [H2]
    """Return the course Gurobi options."""
    return {"LogFile": os.path.join(results_dir, "solver_run.log"),
            "LogToConsole": 0,
            "TimeLimit": 43200}

# ============================================================
# MAIN MODEL FUNCTION
# ============================================================

def model_run(db_dir, years, t_res, passenger_cars_cf, rt, rs,
              solver_name='gurobi', solver_options=None,      # [H2]
              scenario=None, results_dir='results'):          # [H2]
    """
    Build and solve the energy model.

    Parameters
    ----------
    db_dir
        Folder containing the input database.
    years
        Model periods.
    t_res
        Intra-year temporal resolution.
    passenger_cars_cf
        Conversion factor for passenger cars.
    rt
        Technical discount rate.
    rs
        Social discount rate.
    solver_name, solver_options          [H2]
        Solver to use. The published model uses Gurobi.
    scenario                             [H2]
        None (plain course model) or a scenario dict from model.make_scenario().
    results_dir                          [H2]
        Folder for the solver log.

    Returns
    -------
    pypsa.Network
        The optimized PyPSA network.
    """

    # --------------------------
    # 1. PREPROCESS INPUT DATA
    # --------------------------

    # Call the preprocessing functions and store their outputs.

    demands, demand_profiles_prj = preprocess_demand(
            db_dir, years, t_res
        )
    resources, resources_pars, ren_profiles = preprocess_supply(
            db_dir, years, t_res
        )

    techs_s, techs_d, cn = preprocess_technologies(
            db_dir, years, passenger_cars_cf
        )

    # [H2] The scenario changes the input data before the network is built: the largest electrolyser capacity
    #      per vintage goes into the capacity constraints (cn), and sensitivities change prices and costs
    #      (CO2 price, gas price, electrolyser CAPEX or subsidy, battery cost/duration).
    if scenario is not None:
        techs_s, techs_d, resources_pars, cn = apply_scenario_inputs(
            techs_s, techs_d, resources_pars, cn, scenario, years)

    # --------------------------
    # 2. CREATE PYPSA NETWORK
    # --------------------------

    # Create the network and define snapshots/model periods.

    n = pypsa.Network()

    # Define snapshots and investment periods from demand profiles index:
    n.set_snapshots(demand_profiles_prj.index,
                    default_snapshot_weightings=t_res)

    n.investment_periods = years

    # Set the legth of each period:
    n.investment_period_weightings['years'] = list(np.diff(years)) + [list(np.diff(years))[-1]] # the last period gets the same delta as the second last

    # Set the weight of each period on the objective function.
    # For this we use a "social" discount rate rs=1%
    # (lower than the "technical" discout rate rt used for annuitization):
    T = 0
    for period, nyears in n.investment_period_weightings.years.items():
        discounts = [(1 / (1 + rs) ** t) for t in range(T, T + nyears)]
        n.investment_period_weightings.at[period, 'objective'] = sum(discounts)
        T += nyears



    # --------------------------
    # 3. ADD MODEL COMPONENTS
    # --------------------------

    # From the demand dataframes: add all buses and corresponding loads

    # Add demand buses and corresponding carrier
    for b in demands.Bus.unique():
        n.add("Bus", b, carrier=demands[demands.Bus==b]['Carrier'].values[0])

    # Add loads, with the right demand bus from the demand dataframe
    # and the right profile from the demand_profiles_prj dataframe
    for d in demands.index:
        n.add("Load", d,
            bus=demands.at[d,'Bus'],
            p_set=demand_profiles_prj.loc[:,d].values)

    # From the resources dataframe: Loop over all resources and distinguish three separate cases
    #     - For Secondary resources add a bus
    #     - For Reserves add a bus and a store
    #     - For Emissions add a bus, a store and a maximum limit

    for s in resources['Resource'].unique():

        # for secondary resources add a bus
        if resources[resources.Resource==s]['Type'].values[0] == 'Secondary':
            n.add("Bus", s, carrier = resources[resources.Resource==s]['Carrier'].values[0])

        #  for reserves add a bus...
        elif resources[resources.Resource==s]['Type'].values[0] == 'Reserve':
            n.add("Bus", s, carrier=resources[resources.Resource==s]['Carrier'].values[0])

            # ... and a store
            n.add(
                "Store",
                s,
                carrier = resources[resources.Resource==s]['Carrier'].values[0],
                bus = s,
                # Max energy in the store at any given time:
                e_nom = resources_pars[(resources_pars.Resource==s) & (resources_pars.Parameter=='Reserves')][years[0]].values[0],
                # Initial energy in the store (it's a reserve, so we set it equal to e_nom)
                e_initial = resources_pars[(resources_pars.Resource==s) & (resources_pars.Parameter=='Reserves')][years[0]].values[0],
                # Whether the model can optimize e_nom
                e_nom_extendable = False,
                # Whether the stored energy has to return to e_initial at the end of a period
                e_cyclic = False,
                )

        # For emissions add a bus...
        elif resources[resources.Resource==s]['Type'].values[0] == 'Emissions':
            n.add("Bus", s, carrier=resources[resources.Resource==s]['Carrier'].values[0])

            # ... an upper value to limit maximum cumulated emissions at any snapshot within a given year...
            co2_max_profile = pd.Series(index=n.snapshots, dtype=float)
            for y in years:
                co2_max_profile.loc[y] = resources_pars[(resources_pars.Resource==s) &\
                                                        (resources_pars.Parameter=='Budget')][y].values[0]

            # ... and a store
            n.add(
                "Store",
                s,
                carrier=resources[resources.Resource==s]['Carrier'].values[0],
                bus=s,
                # For CO2 we add e_nom as a normalized value...
                e_nom=1,
                # ... and then we set the yearly max cumulated emissions relative to e_nom
                e_max_pu = co2_max_profile,
                e_initial=0,
                e_nom_extendable=False,
                e_cyclic=False,
                )


    # Loop over periods to add all technologies, distinguishing three separate cases:
    #     - Generators - loop through all generators and add them to the network
    #     - Links - loop over all links, check type of link (nr of inputs and outputs), and add to the network
    #     - Storage Units - loop over all storage units and add them to the network
    #     - [H2] Stores - energy storage with a separate energy capacity (the H2 storage option)


    # [H2] In the course code, a technology whose start year lies after y is still added in loop year y,
    #      with build_year = start year but with the costs and fuel/CO2 prices of year y. 'SMR CCS_2020' is then
    #      built in 2030 but pays 2020 gas and CO2 prices for its whole lifetime. In scenario runs these
    #      early copies are skipped (setting skip_early_vintages, default True); the plain course model keeps them.
    skip_early = scenario is not None and scenario.get('skip_early_vintages', True)

    def too_early(t, y):
        return skip_early and y < int(start_year(techs_s, t, years))

    # Loop over model years to add all technologies:
    for y in years:
        print(y)

        # We use techs_by_type to distinguish generators, links and storage units

        # Generators:
        for t in techs_by_type(techs_s, 'Generator'):
            if too_early(t, y):  # [H2]
                continue
            bus0 = techs_s.at[(t,'bus0'), 'Value'] # bus0 as carrier
            bus1 = techs_s.at[(t,'bus1'), 'Value'] # bus1 as bus

            # Retrieve any user-defined capacity constraints for this technology/vintage
            cap_constraints = get_cap_constraints(t, years, cn)

            n.add(
                'Generator',
                f'{t}_{y}',
                carrier = techs_s.at[(t,'Carrier'),'Value'] if (t,'Carrier') in techs_s.index else bus0,  # [H2] own carrier (dedicated wind/solar option)
                bus = bus1,
                p_nom_extendable = True,
                p_max_pu = ren_profiles[bus0].values, # apply renewable profiles as max availability factors
                build_year = max([start_year(techs_s,t,years),y]),  # make sure t won't be built before its start_year
                capital_cost = investment_cost(t, y, techs_d, rt),
                marginal_cost = techs_d.at[(t,'VOM'),y],
                lifetime = techs_d.at[(t,'Lifetime'),y],
                efficiency = techs_d.at[(t,'Efficiency'),y],
                # capacity constraints (NaN -> PyPSA treats as unconstrained: p_nom_max=inf, p_nom_min=0)
                p_nom_max = cap_constraints.at[(t,'max'),y],
                p_nom_min = cap_constraints.at[(t,'min'),y],
                )

        # Links:
        for t in techs_by_type(techs_s,'Link'):
            if too_early(t, y):  # [H2]
                continue

            # "existing" technologies may only be installed in the base year (they represent the
            # 2020 stock, with CAPEX=0 and a short lifetime); skip them in all later vintages.
            if ('existing' in t) and (y > years[0]):
                continue

            # Retrieve any user-defined capacity constraints for this technology/vintage
            cap_constraints = get_cap_constraints(t, years, cn)

            # First, get the link topology dataframe
            topology = get_topology(techs_s, t)

            # Second, check if a cost is specified for any of the buses in the link
            bus_cost = {}
            for b in topology.index:
                try:
                    bus_cost[b] = resources_pars[(resources_pars.Resource==topology.at[b,'Value']) &\
                                                (resources_pars.Parameter=='Price')][y].values[0]
                # In case there are no costs specified and an error is raised, set the costs to 0:
                except IndexError:
                    bus_cost[b] = 0
                except KeyError:
                    bus_cost[b] = 0

            # 1. Simple link, one input one output (two  buses)
            if len(topology)==2:
                n.add(
                    'Link',
                    f'{t}_{y}',
                    carrier = t, # for links we will use the technology name as carrier (it helps sorting out the results)
                    bus0 = topology.at['bus0','Value'], # input bus
                    bus1 = topology.at['bus1','Value'], # output bus
                    p_nom_extendable = True,
                    build_year = max([start_year(techs_s,t,years),y]),
                    capital_cost = investment_cost(t, y, techs_d, rt) * techs_d.at[(t,'Efficiency'), y], # for links costs are expressed in €/activity unit input
                    marginal_cost = techs_d.at[(t,'VOM'), y] + bus_cost['bus0'] + bus_cost['bus1']*techs_d.at[(t,'Efficiency'), y], # VOM + any costs associated with the inputs or the outputs
                    lifetime = techs_d.at[(t,'Lifetime'), y],
                    efficiency = techs_d.at[(t,'Efficiency'), y],
                    # capacity constraints are given in output units -> divide by efficiency to express them per unit of input (p_nom)
                    p_nom_max = cap_constraints.at[(t,'max'),y] / techs_d.at[(t,'Efficiency'), y],
                    p_nom_min = cap_constraints.at[(t,'min'),y] / techs_d.at[(t,'Efficiency'), y],
                    )

            # 2. Link with three buses (e.g. links with emissions)
            elif len(topology)==3:
                # Such a link will have two efficiencies:
                eff1 = techs_d.at[(t,'Efficiency'), y]
                eff2 = techs_d.at[(t,topology.at['bus2','Efficiency_link']), y]

                n.add(
                    'Link',
                    f'{t}_{y}',
                    carrier = t,
                    bus0 = topology.at['bus0','Value'],
                    bus1 = topology.at['bus1','Value'],
                    bus2 = topology.at['bus2','Value'],
                    p_nom_extendable = True,
                    build_year = max([start_year(techs_s,t,years),y]),
                    capital_cost = investment_cost(t, y, techs_d, rt) * techs_d.at[(t,'Efficiency'), y],
                    marginal_cost = techs_d.at[(t,'VOM'), y] + bus_cost['bus0'] + bus_cost['bus1']*eff1 + bus_cost['bus2']*eff2,
                    lifetime = techs_d.at[(t,'Lifetime'), y],
                    efficiency = eff1,
                    efficiency2 = eff2,
                    p_nom_max = cap_constraints.at[(t,'max'),y] / techs_d.at[(t,'Efficiency'), y],
                    p_nom_min = cap_constraints.at[(t,'min'),y] / techs_d.at[(t,'Efficiency'), y],
                    )

            # 3. Link with four buses: CCS technologies.
            #    bus0 = input, bus1 = main output, bus2 = CO2 emitted to the atmosphere (not captured),
            #    bus3 = CO2 captured and sent to storage. The Efficiency_link column tells us which
            #    dynamic parameter feeds each extra output (Emissions -> bus2, Captured CO2 -> bus3).
            elif len(topology)==4:
                # Such a link has three efficiencies (main output + the two CO2 streams):
                eff1 = techs_d.at[(t,'Efficiency'), y]
                eff2 = techs_d.at[(t,topology.at['bus2','Efficiency_link']), y]
                eff3 = techs_d.at[(t,topology.at['bus3','Efficiency_link']), y]

                n.add(
                    'Link',
                    f'{t}_{y}',
                    carrier = t,
                    bus0 = topology.at['bus0','Value'], # input
                    bus1 = topology.at['bus1','Value'], # main output
                    bus2 = topology.at['bus2','Value'], # CO2 to atmosphere (not captured)
                    bus3 = topology.at['bus3','Value'], # CO2 captured and stored
                    p_nom_extendable = True,
                    build_year = max([start_year(techs_s,t,years),y]),
                    capital_cost = investment_cost(t, y, techs_d, rt) * techs_d.at[(t,'Efficiency'), y],
                    marginal_cost = techs_d.at[(t,'VOM'), y] + bus_cost['bus0'] + bus_cost['bus1']*eff1 + bus_cost['bus2']*eff2 + bus_cost['bus3']*eff3,
                    lifetime = techs_d.at[(t,'Lifetime'), y],
                    efficiency = eff1,
                    efficiency2 = eff2,
                    efficiency3 = eff3,
                    p_nom_max = cap_constraints.at[(t,'max'),y] / techs_d.at[(t,'Efficiency'), y],
                    p_nom_min = cap_constraints.at[(t,'min'),y] / techs_d.at[(t,'Efficiency'), y],
                    )

        # StorageUnits
        for t in techs_by_type(techs_s,'StorageUnit'):
            if too_early(t, y):  # [H2]
                continue
            # [H2] optional battery settings for sensitivities 3a-c (capacity limit, duration)
            cap_constraints = get_cap_constraints(t, years, cn)
            n.add(
                'StorageUnit',
                f'{t}_{y}',
                bus = techs_s.at[(t,'bus0'), 'Value'],
                carrier = t,
                capital_cost = investment_cost(t,y,techs_d,rt),
                marginal_cost = techs_d.at[(t,'VOM'), y],                    # [H2] (0 for the battery)
                efficiency_store = techs_d.at[(t,'Efficiency'), y],
                efficiency_dispatch = techs_d.at[(t,'Efficiency'), y],
                build_year = max([start_year(techs_s,t,years),y]),
                lifetime = techs_d.at[(t,'Lifetime'), y],                    # [H2] was missing (default: infinite)
                max_hours = static_value(techs_s, t, 'Max hours', 1.0),      # [H2] PyPSA default is 1 h
                p_nom_max = cap_constraints.at[(t,'max'),y],                  # [H2] NaN -> unconstrained
                p_nom_min = cap_constraints.at[(t,'min'),y],                  # [H2]
                p_nom_extendable=True,
                cyclic_state_of_charge=True,
            )

        # [H2] Stores: storage with its own energy capacity (the H2 storage option, salt caverns).
        #      CAPEX/FOM are per unit of energy capacity (€/kWh -> €/MWh after preprocessing).
        #      Charging and discharging are free and lossless (no separate compressor is modelled).
        for t in techs_by_type(techs_s, 'Store'):
            if too_early(t, y):  # [H2]
                continue
            n.add(
                'Store',
                f'{t}_{y}',
                bus = techs_s.at[(t,'bus0'), 'Value'],
                carrier = t,
                e_nom_extendable = True,
                e_cyclic = True,
                capital_cost = investment_cost(t, y, techs_d, rt),
                build_year = max([start_year(techs_s,t,years),y]),
                lifetime = techs_d.at[(t,'Lifetime'), y],
            )


    # [H2] Scenario settings that act on the built network:
    #      - fuel and CO2 prices per period instead of per vintage (setting period_prices)
    #      - what the hydrogen demand is used for (feedstock on top, or fuel taken out of the HTP demand)
    if scenario is not None:
        apply_network_settings(n, scenario, techs_d, resources_pars, years)

    # --------------------------
    # 4. SOLVE MODEL
    # --------------------------

    n.sanitize()

    # [H2] solver choice and the extra constraints (CO2-storage cap, build limits, battery cap)
    os.makedirs(results_dir, exist_ok=True)
    if solver_options is None:
        solver_options = default_solver_options(solver_name, results_dir)
    extra = make_extra_functionality(scenario) if scenario is not None else None

    status, condition = n.optimize(multi_investment_periods=True,
            solver_name=solver_name,
            log_to_console=False,
            include_objective_constant=False,
            solver_options=solver_options,
            extra_functionality=extra,          # [H2]
            )

    # [H2] keep the scenario settings and the shadow prices (electrolyser limit, CO2-storage cap) on the network
    n.meta = {**n.meta, 'scenario': dict(scenario) if scenario is not None else None, 'rt': rt, 'rs': rs}
    if scenario is not None and status == 'ok':
        store_shadow_prices(n)

    print("\n")
    print(f"Model Status: {status}")
    print(f"Termination Condition: {condition}")
    print(f"Objective value: {n.objective}")

    return n

# ============================================================
# HYDROGEN EXTENSION
# ============================================================

"""Hydrogen extension of the final course model.

The set-up agreed with Francesco (meeting of 14 October):

* Hydrogen is a DEMAND, not a secondary resource: 'industrial_h2' on the bus 'Hydrogen', 1.3 Mt/yr in every period
  and scenario (Elzenga et al., 2025), with a flat hourly profile.
* Three END-USE technologies feed that demand directly (links, see build_h2_database.py):
      SMR (grey)          Gas supply  -> Hydrogen + CO2 atmosphere
      SMR CCS (blue)      Gas supply  -> Hydrogen + CO2 atmosphere (not captured) + CO2 storage
      Electrolyser (green) Electricity -> Hydrogen
  plus 'SMR - existing', the reformers that exist in 2020 (course convention for the existing stock).
* The scenarios lie on one dimension: water availability. Water itself is not modelled. Instead the scenario
  limits how much ELECTROLYSER CAPACITY can be built, in the capacity constraints of the technology table:
      S1 Base       no water scarcity (100%): the cost-optimal electrolyser capacity (the reference run)
      S2 Medium     medium water scarcity: at most 50% of the electrolyser capacity that S1 builds (per vintage)
      S3 Scarce     high water scarcity: no electrolysers (0%)
  The rest of the hydrogen demand is met by gas-based hydrogen (grey or blue, whichever is cheaper).
* H2 storage (group, 15 Oct): optional salt-cavern storage on the hydrogen bus.
* Within each scenario, green levers and hydrogen-storage cost are optional sensitivities.
* GREEN LEVERS within the water scenarios (16 Oct), off by default: desal (electrolysers on desalinated seawater,
  outside the water limit, at 0.01-0.03 €/kg extra), h2_production_subsidy (€/kg of electrolytic hydrogen) and
  green_mandate (a minimum share of electrolytic hydrogen per period, RED III-type).

This module holds:
* SCENARIOS, SHORT_NAMES        the three scenarios
* presets                       CO2_PRICES (ETS1), CO2_PRICES_ETS2 (household gas and petrol cars, from 2028),
                                GAS_PRICES, ELY_CAPEX, ... (Dutch input data and cited sources);
                                the central values are the defaults, the other values are sensitivities
* make_scenario()               one run = a scenario plus any sensitivities and data settings
* electrolyser_reference()      the electrolyser capacity per technology and vintage of a solved run (the S1 reference)
* apply_scenario_inputs()       changes the input data (incl. the capacity constraints) before the network is built
* apply_network_settings()      prices per period, the use of the hydrogen demand, a demand path
* make_extra_functionality()    CO2-storage cap, build-rate caps, battery cap
* store_shadow_prices()         saves shadow prices on the network

Water USE is reported afterwards as an output (h2_results.water_use).
"""

import numpy as np
import pandas as pd
import xarray as xr

# Set this switch to False to exclude hydrogen storage from rebuilt databases and
# from the default scenario settings. Individual runs can still override it with
# h2_storage=True or h2_storage=False.
STORAGE = True

# Names of the hydrogen technologies in the database (technologies.xlsx)
ELECTROLYSIS_GRID = ['Electrolyser']                   # green: grid electricity
ELECTROLYSIS_SEAWATER = ['Electrolyser - seawater']    # green on desalinated seawater: OUTSIDE the water limit (lever)
ELECTROLYSIS = ELECTROLYSIS_GRID + ELECTROLYSIS_SEAWATER
GREY = ['SMR', 'SMR - existing']                       # grey (new and the 2020 stock)
BLUE = ['SMR CCS']                                     # blue
H2_PRODUCTION = ELECTROLYSIS + GREY + BLUE
H2_STORAGE = ['H2 storage']                            # salt caverns (option)
OPTION_TECHS = {'h2_storage': H2_STORAGE, 'desal': ELECTROLYSIS_SEAWATER}
KG_PER_MWH_H2 = 1000 / 33.33                           # kg of hydrogen per MWh (LHV)
BATTERY = ['Battery']
H2_BUS = 'Hydrogen'                                    # the demand bus of 'industrial_h2'
H2_LOAD = 'industrial_h2'
MWH_PER_T_H2 = 33.33                                   # lower heating value
MWH_PER_KG = MWH_PER_T_H2 / 1000

# --------------------------------------------------------------------------
# Scenario parameter (1): water availability for electrolysis
#   electrolyser_cap_share = largest electrolyser capacity, as a share of what the cost-optimal run (S1) builds.
#   None = no limit. 0 = no electrolysers. The base is the scenario without water scarcity (group, 15 Oct).
# --------------------------------------------------------------------------
SCENARIOS = {
    'S1': dict(label='S1 Base (no water scarcity)', electrolyser_cap_share=None),
    'S2': dict(label='S2 Medium (medium water scarcity)', electrolyser_cap_share=0.5),
    'S3': dict(label='S3 Scarce (high water scarcity)', electrolyser_cap_share=0.0),
}
SHORT_NAMES = {'S1': 'Base', 'S2': 'Medium', 'S3': 'Scarce'}     # short names for plots and tables (feedback)
REFERENCE_SCENARIO = 'S1'                                         # the cost-optimal run the caps refer to

# --------------------------------------------------------------------------
# Presets based on Dutch input data and cited sources (October 2026).
# All money values in 2024 euros (the report's convention). Price bases are converted with the Dutch HICP
# (Eurostat HICP, annual averages as published by CBS): 2021 +2.8%, 2022 +11.6%, 2023 +4.1%, 2024 +3.2%, 2025 +3.0%.
#   nominal 2020 -> €2024: x 1.2325          €2025 -> €2024: / 1.030
# 2020 = the observed value of 2020, expressed in 2024 euros.
# --------------------------------------------------------------------------
EUR2024_PER_EUR2020 = 1.028 * 1.116 * 1.041 * 1.032      # = 1.2325
EUR2024_PER_EUR2025 = 1 / 1.030
# EU ETS1 CO2 price (€/tCO2). 2020: auction average 24.61 nominal (Umweltbundesamt) = 30.3 €2024.
# 2030 band = PBL KEV 2025 (75-138, central 111, €2024); 2040-2050 = synthesis of Enerdata (2025, 2026),
# TYNDP 2024 and WLO 2025 (see report).
CO2_PRICES = {
    'zero':    {2020: 0,    2030: 0,   2040: 0,   2050: 0},
    'low':     {2020: 30.3, 2030: 75,  2040: 130, 2050: 170},
    'central': {2020: 30.3, 2030: 110, 2040: 180, 2050: 250},
    'high':    {2020: 30.3, 2030: 140, 2040: 270, 2050: 500},
    'stress':  {2020: 30.3, 2030: 140, 2040: 450, 2050: 630},
}
# EU ETS2 CO2 price (€/tCO2) for fuel burnt in buildings and road transport: here the household gas boilers and
# the petrol cars (ETS2_TECHS). ETS2 starts with the emissions of 2028, so 2020 = 0 (no EU carbon price on household
# gas and petrol). PBL (2026c, p. 17; 2025 prices): low 57 €/t = the price-stability trigger, kept flat ("loopt niet
# op in de tijd"); middle 86 in 2030 (futures price Dec-2028 of 71, +10%/yr); high 135 in 2030, +10%/yr.
# 2040 = 2030 x 1.1^10 for middle and high (223, 350). 2050: converges with ETS1.
# Stress = the ETS1 stress values from 2040. Converted to €2024 (/1.030). Industry, power and hydrogen stay in ETS1.
CO2_PRICES_ETS2 = {
    'zero':    {2020: 0, 2030: 0,   2040: 0,   2050: 0},
    'low':     {2020: 0, 2030: 55,  2040: 55,  2050: 170},
    'central': {2020: 0, 2030: 83,  2040: 217, 2050: 250},
    'high':    {2020: 0, 2030: 131, 2040: 340, 2050: 500},
    'stress':  {2020: 0, 2030: 131, 2040: 450, 2050: 630},
}
ETS2_TECHS = ['Residential gas boiler', 'Residential gas boiler - existing', 'ICE car', 'ICE car - existing']
# Natural gas (TTF) in €/MWh LHV (= €/MWh HHV x 1.11). 2020: ACER annual average 9.7 HHV nominal = 13.3 LHV €2024.
# 2030 band = PBL KEV 2025 (15-47 HHV, central 24, €2024); 2040-2050 from WLO 2025, REF2020, IEA (see report).
GAS_PRICES = {
    'low':       {2020: 13.3, 2030: 16.7, 2040: 15.5, 2050: 14.4},
    'central':   {2020: 13.3, 2030: 26.6, 2040: 28.9, 2050: 27.8},
    'high':      {2020: 13.3, 2030: 52.2, 2040: 44.4, 2050: 42.2},
    'shock2030': {2020: 13.3, 2030: 80.0, 2040: 44.4, 2050: 42.2},   # Sept-Oct 2026 level (~72 HHV)
}
# Electrolyser system CAPEX (€/kW_e, installed, excluding grid). IEA GHR 2025, EHO 2025, TNO 2024.
ELY_CAPEX = {
    'low':     {2020: 1800, 2030: 1250, 2040: 800,  2050: 500},
    'central': {2020: 2200, 2030: 1650, 2040: 1250, 2050: 1000},
    'high':    {2020: 3100, 2030: 2500, 2040: 1800, 2050: 1400},
}
# CO2 transport and storage tariff (€/tCO2). Porthos max 47.10; Aramis 67-72 (Algemene Rekenkamer 2024).
CO2_TS_PRICES = {
    'zero':    {2020: 0,  2030: 0,  2040: 0,  2050: 0},
    'low':     {2020: 45, 2030: 45, 2040: 30, 2050: 25},
    'central': {2020: 55, 2030: 55, 2040: 45, 2050: 40},
    'high':    {2020: 75, 2030: 75, 2040: 70, 2050: 65},
}
# CO2 storage capacity (MtCO2/yr): Porthos 2.5 from 2027, Aramis 5-7.5 at launch, up to 22.
CO2_STORAGE_CAPS = {
    'low':     {2030: 2.5,  2040: 10, 2050: 10},
    'central': {2030: 10,   2040: 22, 2050: 25},
    'high':    {2030: 10,   2040: 25, 2050: 25},
}
# H2 storage option: salt-cavern storage that can exist (MWh): first HyStock cavern ~2031 (0.22 TWh),
# 4 caverns 0.67-0.9 TWh mid-2030s, 1.5-10 TWh in 2050 (Gasunie; KGG 2025; TNO 2020).
H2_STORAGE_CAPS = {
    'low':     {2030: 0.0,    2040: 0.67e6, 2050: 1.5e6},
    'central': {2030: 0.22e6, 2040: 0.9e6,  2050: 5e6},
    'high':    {2030: 0.9e6,  2040: 3e6,    2050: 10e6},
}
# Build limits per period (MW of p_nom: input power for links, output for generators), summed over all active vintages.
# Each period stands for 10 years (2030 = 2030-2039). These are limits on how fast things can be built in the
# Netherlands; they are not the water limit of the scenarios.
#   Electrolysers: 1.2 GW funded for 2030, 3-4 GW by 2035, NPE 15-20 GW in 2040, up to 40 GW 2050.
#   Offshore wind: 21 GW roadmap (~2032), 30-40 GW in 2040, up to 70 GW in 2050.
#   Nuclear: Borssele (512 MW_e) only until the late 2030s; up to 7 GW_e by 2050 (input = output / 0.4).
CAPACITY_CAPS = {
    'central': [
        dict(name='Electrolysers', component='Link', carriers=ELECTROLYSIS,
             cap={2030: 3000, 2040: 20000, 2050: 40000}),
        dict(name='Offshore wind', component='Generator', carriers=['Wind offshore', 'Wind offshore - dedicated'],
             cap={2030: 21000, 2040: 40000, 2050: 70000}),
        dict(name='Nuclear', component='Link', carriers=['Nuclear plant', 'Nuclear plant - dedicated'],
             cap={2030: 512 / 0.4, 2040: 2712 / 0.4, 2050: 7000 / 0.4}),
    ],
}
CAPACITY_CAPS['low'] = [
    {**CAPACITY_CAPS['central'][0], 'cap': {2030: 1200, 2040: 15000, 2050: 14000}},
    {**CAPACITY_CAPS['central'][1], 'cap': {2030: 10200, 2040: 21000, 2050: 40000}},
    {**CAPACITY_CAPS['central'][2], 'cap': {2030: 512 / 0.4, 2040: 512 / 0.4, 2050: 512 / 0.4}},
]
# Hydrogen demand (Mt/yr). Fixed 1.3 Mt in the scenarios (Elzenga et al., 2025); 'high' is a variation
# (Francesco: "of course you can do a variation where the demand is different", after the three scenarios run).
H2_DEMAND = {
    'fixed':  {2020: 1.3, 2030: 1.3, 2040: 1.3, 2050: 1.3},
    'low':    {2020: 1.3, 2030: 0.8, 2040: 1.3, 2050: 1.3},
    'high':   {2020: 1.3, 2030: 1.3, 2040: 2.5, 2050: 3.3},
}
# Water use by route, litres per kg H2 (consumption incl. treatment and cooling; report Table "water"):
# electrolysis 17.5-22.3 (IRENA 2023), SMR 8-12.5, SMR + CCS 24-32. Output only.
WATER_L_PER_KG = {'electrolysis': 22.0, 'SMR': 10.0, 'SMR CCS': 28.0}

PRESETS = {
    'co2_price': CO2_PRICES, 'co2_price_ets2': CO2_PRICES_ETS2, 'gas_price': GAS_PRICES, 'electrolyser_capex': ELY_CAPEX,
    'co2_storage_price': CO2_TS_PRICES, 'co2_storage_cap': CO2_STORAGE_CAPS, 'h2_storage_cap': H2_STORAGE_CAPS,
    'capacity_caps': CAPACITY_CAPS, 'h2_demand_mt': H2_DEMAND,
}

DEFAULTS = dict(
    label=None,
    # --- scenario parameter (1): water availability -> electrolyser capacity ---
    electrolyser_cap_share=None,   # None = no limit (cost-optimal, S1); 0.5 = half of the reference capacity; 0 = none
    electrolyser_reference=None,   # {technology: {year: MW of H2 output}} built per vintage in the reference run (the
                                   #   central S1), from electrolyser_reference(n_S1); needed when 0 < electrolyser_cap_share
    cap_from=2030,                 # first vintage that the scenario limits (electrolysers start in 2030)
    electrolyser_limit_scope='total',  # 'total': the limit is on all electrolysers together (MW of hydrogen output per
                                   #   vintage), share x the total of the reference run: the same water whatever the
                                   #   power source; 'per_technology': each electrolyser <= share x its own reference
    electrolyser_limit_on='capacity',  # 'capacity': water limits how big the electrolyser can be (the scenarios);
                                   # 'output': the plant is built as big as in the reference run (S1), but water lets
                                   #   it run at no more than electrolyser_cap_share of its capacity in any hour (the
                                   #   "over-dimensioned plant" story of Francesco: build for abundant water, then a drought)
    electrolyser_plant_reference=None,  # with 'output': the plant to build ({technology: {year: MW of H2}}, e.g. of
                                   #   the Base run); the water then caps the hourly output of all
                                   #   electrolysers together at share x electrolyser_reference (the same water in MW)
    # --- optional hydrogen storage ---
    h2_storage=STORAGE,            # H2 storage in salt caverns (a Store on the hydrogen bus)
    h2_storage_cap='central',      # MWh of H2 storage that can exist (key of H2_STORAGE_CAPS or {year: MWh}); None = no cap
    h2_storage_cost_factor=1.0,    # (2c) multiplier on H2 storage CAPEX and FOM
    grid_electrolysis=True,        # False = no grid electrolyser: green hydrogen only from the pure green route
                                   #   (a strict reading of the EU rules for renewable hydrogen, RFNBO)
    # --- green levers within the water scenarios (16 Oct) ---
    desal=False,                   # alternative water: an electrolyser on desalinated seawater (or treated waste
                                   #   water), outside the verdringingsreeks, so NOT limited by the water scenario
    desal_cost_eur_per_kg=0.03,    # levelised cost of alternative water per kg H2
    h2_production_subsidy=0.0,     # €/kg of hydrogen from electrolysis (all electrolysers): an operating subsidy,
                                   #   CfD / H2Global / SDE++-type; a transfer, added back in the economic cost
    green_mandate=None,            # {year: minimum share of the hydrogen made by electrolysis}, e.g. {2040: 0.6,
                                   #   2050: 0.6} (RED III: 42% RFNBO in industry by 2030, 60% by 2035)
    # --- the hydrogen demand (Francesco: decide what this hydrogen is used for) ---
    h2_demand_use='feedstock',     # 'feedstock': refineries and ammonia, a separate demand ON TOP of the course demands
                                   # 'htp_fuel':  hydrogen burnt for high-temperature heat; the industrial HTP demand is
                                   #              reduced by the heat this hydrogen delivers (H2 x furnace efficiency)
    h2_demand_mt=None,             # key of H2_DEMAND or {year: Mt}; None = database (1.3 Mt every period)
    # --- sensitivities: cost variations within the scenarios ---
    electrolyser_subsidy=0.0,      # (2a) share of electrolyser CAPEX paid by subsidy, 0-0.8 (OWE)
    infrastructure_subsidy=0.0,    # share of electrolyser infrastructure CAPEX paid by subsidy, 0-0.8
    electrolyser_capex=None,       # (2a) 'low'/'central'/'high' or {year: €/kW_e}; None = database
    co2_price='central',           # (2b) key of CO2_PRICES, number, {year: price}, or None (= database)
    co2_price_scope='all',         # 'all': every emission pays (ETS-like); 'h2': only the SMR routes pay
    co2_price_ets2='auto',         # price for household gas boilers and petrol cars (ETS2_TECHS): key of
                                   #   CO2_PRICES_ETS2, number or {year: price}; 'auto' = the ETS2 path with the same
                                   #   name as co2_price (or the ETS1 price if co2_price is not a preset name);
                                   #   None = they pay ETS1
    capex_factors=None,            # {technology: multiplier on CAPEX}, e.g. {'SMR CCS': 1.2}
    battery=True,                  # (3) include batteries at all (course model; not used for hydrogen)
    battery_cost_factor=1.0,       # (3a) multiplier on battery CAPEX
    battery_max_mw=None,           # (3b) maximum total battery power in any period (MW)
    battery_max_hours=None,        # (3c) hours of storage per MW (None = database: 4 h in h2_nl)
    # --- data and model settings ---
    gas_price='central',           # key of GAS_PRICES or {year: €/MWh}; None = database
    gas_reserve=None,              # MWh of gas for ALL periods together; None = database
    co2_storage_price='central',   # €/tCO2 transport + storage (key, number or dict); None = database
    co2_storage_cap='central',     # MtCO2/yr captured (key or {year: Mt}); None = no cap
    capacity_caps='central',       # build limits: key of CAPACITY_CAPS or a list of dicts; None = no caps
    period_prices=True,            # True: fuel and CO2 prices of each PERIOD (not of the build year)
    storage_cyclic_per_period=True,  # batteries return to their start level within EACH period
    skip_early_vintages=True,      # do not add copies of a technology before its start year (see model.py)
    vom_scale=1.0,                 # multiplier on ALL variable O&M costs (1 = database as is)
)


def make_scenario(base='S1', preset=None, **settings):
    """Return the settings for one run, e.g. make_scenario('S3', co2_price='high').

    base is 'S1' (Base), 'S2' (Medium), 'S3' (Scarce) or None (no limit, the same as S1).
    S2 needs the electrolyser capacity of the central S1 run:
    make_scenario('S2', electrolyser_reference=electrolyser_reference(n_S1))
    Hydrogen storage and the green levers are optional settings.
    The defaults are the central Dutch values used to build input_databases/h2_nl.
    preset: None or 'nl' (the same; 'nl' is accepted so older scripts keep working).
    """
    scen = dict(DEFAULTS)
    if preset not in (None, 'nl'):
        raise KeyError(f'Unknown preset {preset!r}')
    scen['preset'] = 'nl'
    if base is not None:
        scen.update(SCENARIOS[base])
        scen['scenario'] = base
    unknown = set(settings) - set(DEFAULTS)
    if unknown:
        raise KeyError(f'Unknown scenario settings: {sorted(unknown)}')
    scen.update(settings)
    if scen['label'] is None:
        scen['label'] = base or 'no limit'
    return scen


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def resolve(key, value):
    """Turn a preset name into its values (dict or list); leave numbers/dicts/lists as they are."""
    if isinstance(value, str):
        return PRESETS[key][value]
    return value


def _per_year(value, years, key=None):
    """Scalar, preset name or {year: value} dict -> pd.Series over the model years (interpolated)."""
    if isinstance(value, str):
        value = PRESETS[key or 'co2_price'][value]
    if isinstance(value, dict):
        s = pd.Series({int(k): v for k, v in value.items()}, dtype=float)
        s = s.reindex(sorted(set(s.index) | set(years))).interpolate(method='index').ffill().bfill()
        return s.loc[years]
    return pd.Series(float(value), index=years)


def _has(techs_d, tech, par):
    return (tech, par) in techs_d.index


def _set_resource(resources_pars, resource, parameter, values, years):
    row = (resources_pars.Resource == resource) & (resources_pars.Parameter == parameter)
    resources_pars.loc[row, years] = values


def _disable(techs_s, techs):
    for t in techs:
        if (t, 'Type') in techs_s.index:
            techs_s.loc[(t, 'Type'), 'Value'] = 'Disabled'   # techs_by_type() then skips it


# --------------------------------------------------------------------------
# 1. The scenario: electrolyser capacity in the capacity constraints
# --------------------------------------------------------------------------

def electrolyser_reference(n):
    """{technology: {year: MW of hydrogen OUTPUT capacity}} that a solved run builds per electrolyser vintage.

    Use it on the cost-optimal run (the central S1) and pass it to
    make_scenario(..., electrolyser_reference=...). Values below 1 MW are solver noise and count as 0.
    """
    out = {}
    for name, l in n.links[n.links.carrier.isin(ELECTROLYSIS)].iterrows():
        t, y = l.carrier, str(int(l.build_year))
        out.setdefault(t, {})
        out[t][y] = out[t].get(y, 0.0) + float(l.p_nom_opt) * float(l.efficiency)
    return {t: {y: (v if v > 1.0 else 0.0) for y, v in sorted(d.items())} for t, d in out.items()}


def _per_tech(ref):
    """Accept the reference as {technology: {year: MW}} or, for one electrolyser, as {year: MW}."""
    if not ref:
        return {}
    if all(isinstance(v, dict) for v in ref.values()):
        return ref
    return {ELECTROLYSIS_GRID[0]: ref}


def electrolyser_techs(scen):
    """The grid electrolyser and, when enabled, the alternative-water lever."""
    return ((ELECTROLYSIS_GRID if scen.get('grid_electrolysis', True) else [])
            + (ELECTROLYSIS_SEAWATER if scen.get('desal') else []))


def water_limited_electrolyser_techs(scen):
    """Electrolysers whose capacity is constrained by freshwater availability."""
    return ELECTROLYSIS_GRID if scen.get('grid_electrolysis', True) else []


def electrolyser_total_cap(scen, years):
    """{year: MW of H2 output} allowed for freshwater-limited electrolysers."""
    share = scen.get('electrolyser_cap_share')
    if share is None or scen.get('electrolyser_limit_scope', 'total') != 'total':
        return None
    ref = _per_tech(scen.get('electrolyser_reference'))
    out = {}
    for y in years:
        if y < scen.get('cap_from', 2030):
            continue
        tot = sum(float(d.get(str(y), d.get(y, 0.0)) or 0.0) for d in ref.values()) if float(share) > 0 else 0.0
        out[y] = float(share) * tot
    return out


def electrolyser_caps(scen, years):
    """{technology: {year: MW of hydrogen output}} that the scenario allows per electrolyser vintage, or None.

    Freshwater availability limits grid electrolysis. Desalinated-water
    electrolysis is an alternative-water lever and remains outside this cap.
    * scope 'total' (default): freshwater-limited electrolysers together may be
      at most the share of the total electrolyser capacity of the reference run.
      Each freshwater-limited technology gets that total as its own capacity
      constraint; when several are enabled, make_extra_functionality() adds the
      joint limit.
    * scope 'per_technology': each freshwater-limited electrolyser may be at
      most the share of what the reference run builds of it.
    """
    share = scen.get('electrolyser_cap_share')
    if share is None:
        return None
    share = float(share)
    ref = _per_tech(scen.get('electrolyser_reference'))
    techs = water_limited_electrolyser_techs(scen)
    total = electrolyser_total_cap(scen, years)
    if total is not None:
        if share > 0 and not ref:
            raise ValueError(
                f"Scenario {scen.get('label')!r} limits the electrolysers to {share:.0%} of the cost-optimal capacity, so "
                "it needs that capacity: make_scenario(..., electrolyser_reference=electrolyser_reference(n_S1)).")
        return {t: dict(total) for t in techs}
    if share > 0:
        missing = [t for t in techs if t not in ref]
        if missing:
            raise ValueError(
                f"Scenario {scen.get('label')!r} limits the electrolysers to {share:.0%} of the cost-optimal capacity, so "
                f"it needs that capacity for {missing}: make_scenario(..., electrolyser_reference="
                f"electrolyser_reference(n_S1)), where n_S1 is the solved S1 (Base) run "
                f"(electrolyser_limit_scope='per_technology': S1 with the same options).")
    caps = {}
    for t in techs:
        caps[t] = {}
        for y in years:
            if y < scen.get('cap_from', 2030):
                continue
            r = 0.0 if share == 0 else float(ref[t].get(str(y), ref[t].get(y, 0.0)) or 0.0)
            caps[t][y] = share * r
    return caps


def _set_capacity_constraint(cn, tech, kind, values, years):
    """Write a min or max row {year: MW of output} into the capacity constraints (course table, per vintage)."""
    row = pd.DataFrame([[np.nan] * len(cn.columns)], columns=cn.columns,
                       index=pd.MultiIndex.from_tuples([(tech, kind)], names=cn.index.names))
    if 'Unit' in row.columns:
        row['Unit'] = 'MW'
    for y in years:
        if y in values and y in row.columns:
            row[y] = float(values[y])
    cn = pd.concat([cn.drop(index=(tech, kind), errors='ignore'), row])
    return cn.sort_index()


# --------------------------------------------------------------------------
# 2. Input changes (before the network is built)
# --------------------------------------------------------------------------

def apply_scenario_inputs(techs_s, techs_d, resources_pars, cn, scen, years):
    """Apply the scenario (electrolyser capacity) and the data settings and sensitivities to the input data.

    Note: techs_d is already in €/MW and €/MWh here (preprocessing multiplied by 1e3).
    """
    techs_s, techs_d, resources_pars, cn = techs_s.copy(), techs_d.copy(), resources_pars.copy(), cn.copy()

    # Options (off by default): the technologies of an option that is not switched on are disabled
    for option, techs in OPTION_TECHS.items():
        if not scen.get(option, False):
            _disable(techs_s, techs)
    if not scen.get('grid_electrolysis', True):
        _disable(techs_s, ELECTROLYSIS_GRID)

    # (1) Freshwater availability: the largest grid-electrolyser capacity per vintage.
    limit_on = scen.get('electrolyser_limit_on', 'capacity')
    if limit_on == 'capacity':
        caps = electrolyser_caps(scen, years)
        if caps is not None:
            for t, c in caps.items():
                cn = _set_capacity_constraint(cn, t, 'max', c, years)
            scen['_electrolyser_caps_mw_h2'] = {t: {str(y): float(v) for y, v in c.items()}
                                                for t, c in caps.items()}       # kept on n.meta
            total = electrolyser_total_cap(scen, years)
            if total is not None:
                scen['_electrolyser_cap_total_mw_h2'] = {str(y): float(v) for y, v in total.items()}
    elif limit_on == 'output':
        # the plant (min = max per vintage): electrolyser_plant_reference, or else the reference run itself. The water
        # limit: p_max_pu = share (apply_network_settings), or, with a separate plant, an hourly cap on the output of all
        # electrolysers together at share x the water reference (make_extra_functionality)
        ref = _per_tech(scen.get('electrolyser_plant_reference') or scen.get('electrolyser_reference'))
        if not ref:
            raise ValueError("electrolyser_limit_on='output' needs electrolyser_reference (the plant of the S1 run)")
        if scen.get('electrolyser_plant_reference'):
            water = _per_tech(scen.get('electrolyser_reference'))
            share = float(scen.get('electrolyser_cap_share') or 0.0)
            scen['_electrolyser_water_mw_h2'] = {
                str(y): share * sum(float(d.get(str(y), d.get(y, 0.0)) or 0.0) for d in water.values())
                for y in years if y >= scen.get('cap_from', 2030)}
        fixed = {}
        for t in electrolyser_techs(scen):
            size = {y: float(ref.get(t, {}).get(str(y), 0.0) or 0.0) for y in years if y >= scen.get('cap_from', 2030)}
            cn = _set_capacity_constraint(cn, t, 'max', size, years)
            cn = _set_capacity_constraint(cn, t, 'min', size, years)
            fixed[t] = {str(y): v for y, v in size.items()}
        scen['_electrolyser_fixed_mw_h2'] = fixed
    else:
        raise ValueError("electrolyser_limit_on must be 'capacity' or 'output'")

    # (2c) H2 storage cost (option)
    for t in H2_STORAGE:
        for par in ('CAPEX', 'FOM'):
            if _has(techs_d, t, par):
                techs_d.loc[(t, par), years] = techs_d.loc[(t, par), years].values * scen.get('h2_storage_cost_factor', 1.0)

    # VOM convention check (applies to every technology, so the comparison stays like-for-like)
    if scen.get('vom_scale', 1.0) != 1.0:
        vom = techs_d.index.get_level_values('Parameter') == 'VOM'
        techs_d.loc[vom, years] = techs_d.loc[vom, years].values * scen['vom_scale']

    # (2a) Electrolyser CAPEX path (€/kW_e -> €/kW_H2 output via the efficiency), then the subsidy
    if scen.get('electrolyser_capex') is not None:
        capex_e = _per_year(scen['electrolyser_capex'], years, 'electrolyser_capex') * 1e3  # €/MW_e
        for t in ELECTROLYSIS:
            if _has(techs_d, t, 'CAPEX'):
                eff = techs_d.loc[(t, 'Efficiency'), years].values.astype(float)
                old = techs_d.loc[(t, 'CAPEX'), years].values.astype(float)
                new = capex_e.values / eff
                techs_d.loc[(t, 'CAPEX'), years] = new
                if _has(techs_d, t, 'FOM'):   # FOM is a share of CAPEX, keep that share
                    techs_d.loc[(t, 'FOM'), years] = techs_d.loc[(t, 'FOM'), years].values * new / old
    sub = _per_year(scen['electrolyser_subsidy'], years)
    infrastructure_sub = _per_year(scen['infrastructure_subsidy'], years)
    total_sub = 1 - (1 - sub) * (1 - infrastructure_sub)
    scen['_subsidy_eur_per_mw_h2'] = {}          # kept on n.meta, used by h2_results.subsidy_cost()
    scen['_infrastructure_subsidy_eur_per_mw_h2'] = {}
    scen['_capex_eur_per_mw_h2'] = {}            # electrolyser CAPEX before the subsidy (investment outputs)
    for t in ELECTROLYSIS:
        if _has(techs_d, t, 'CAPEX'):
            capex = techs_d.loc[(t, 'CAPEX'), years].values.astype(float)
            scen['_capex_eur_per_mw_h2'][t] = {str(y): float(v) for y, v in zip(years, capex)}
            scen['_subsidy_eur_per_mw_h2'][t] = {str(y): float(v) for y, v in zip(years, capex * total_sub.values)}
            scen['_infrastructure_subsidy_eur_per_mw_h2'][t] = {
                str(y): float(v) for y, v in zip(years, capex * infrastructure_sub.values)
            }
            techs_d.loc[(t, 'CAPEX'), years] = capex * (1 - total_sub.values)

    # Green levers: the cost of desalinated water and an operating subsidy per kg, both as variable cost (VOM, € per
    # MWh of electricity INPUT = € per kg x kg per MWh of hydrogen x efficiency)
    for t in ELECTROLYSIS:
        if not (_has(techs_d, t, 'VOM') and _has(techs_d, t, 'Efficiency')):
            continue
        eff = techs_d.loc[(t, 'Efficiency'), years].values.astype(float)
        add = np.zeros(len(years))
        if t in ELECTROLYSIS_SEAWATER:
            add += float(scen.get('desal_cost_eur_per_kg', 0.0)) * KG_PER_MWH_H2 * eff
        add -= float(scen.get('h2_production_subsidy', 0.0)) * KG_PER_MWH_H2 * eff
        if add.any():
            techs_d.loc[(t, 'VOM'), years] = techs_d.loc[(t, 'VOM'), years].values.astype(float) + add
    scen['_prod_subsidy_eur_per_mwh_h2'] = float(scen.get('h2_production_subsidy', 0.0)) * KG_PER_MWH_H2

    # (2b) CO2 price (€/tCO2). The database row is called "CO2 atmosphere / Price".
    if scen['co2_price'] is not None:
        price = _per_year(scen['co2_price'], years, 'co2_price')
        if scen['co2_price_scope'] == 'all':
            _set_resource(resources_pars, 'CO2 atmosphere', 'Price', price.values, years)
        elif scen['co2_price_scope'] == 'h2':
            for t in GREY + BLUE:
                if _has(techs_d, t, 'Emissions'):
                    techs_d.loc[(t, 'VOM'), years] = (techs_d.loc[(t, 'VOM'), years].values
                                                      + price.values * techs_d.loc[(t, 'Emissions'), years].values)
        else:
            raise ValueError("co2_price_scope must be 'all' or 'h2'")

    # Natural gas price path and reserve
    if scen.get('gas_price') is not None:
        _set_resource(resources_pars, 'Gas supply', 'Price',
                      _per_year(scen['gas_price'], years, 'gas_price').values, years)
    if scen.get('gas_reserve') is not None:
        _set_resource(resources_pars, 'Gas supply', 'Reserves', float(scen['gas_reserve']), years)

    # CO2 transport and storage cost (€/tCO2 captured), applies to every CCS technology
    if scen.get('co2_storage_price') is not None:
        _set_resource(resources_pars, 'CO2 storage', 'Price',
                      _per_year(scen['co2_storage_price'], years, 'co2_storage_price').values, years)

    # CAPEX multipliers per technology (cost variations)
    for t, f in (scen.get('capex_factors') or {}).items():
        if _has(techs_d, t, 'CAPEX'):
            techs_d.loc[(t, 'CAPEX'), years] = techs_d.loc[(t, 'CAPEX'), years].values * float(f)

    # (3) Batteries
    for t in BATTERY:
        if not scen['battery']:
            _disable(techs_s, [t])
            continue
        hours = scen['battery_max_hours']
        factor = scen['battery_cost_factor']
        if hours is not None:
            base_hours = float(techs_s.at[(t, 'Max hours'), 'Value']) if (t, 'Max hours') in techs_s.index else 1.0
            techs_s.loc[(t, 'Max hours'), 'Value'] = hours
            # the database CAPEX is for a battery of base_hours; scale it with the energy capacity
            factor = factor * hours / base_hours
        if _has(techs_d, t, 'CAPEX'):
            techs_d.loc[(t, 'CAPEX'), years] = techs_d.loc[(t, 'CAPEX'), years].values * factor

    return techs_s, techs_d, resources_pars, cn


# --------------------------------------------------------------------------
# 3. Changes to the built network
# --------------------------------------------------------------------------

def ets2_price(scen, years):
    """ETS2 price per period (pd.Series, €/tCO2) for ETS2_TECHS, or None if they pay the ETS1 price."""
    v = scen.get('co2_price_ets2', 'auto')
    if v is None or scen.get('co2_price') is None or scen.get('co2_price_scope', 'all') != 'all':
        return None
    if isinstance(v, str) and v == 'auto':
        v = scen['co2_price'] if isinstance(scen['co2_price'], str) else None
        if v not in CO2_PRICES_ETS2:
            return None          # own ETS1 values: households and cars pay the same price
    return _per_year(v, years, 'co2_price_ets2')


def set_period_prices(n, resources_pars, years, overrides=None):
    """Let every link pay the fuel, CO2 and CO2-storage prices of the PERIOD it operates in.

    The course code fixes these prices at the build year of each vintage (a 2030 SMR would pay the
    2030 CO2 price until 2060). Here the static marginal cost is split into VOM (vintage) and bus
    prices (period), and a time-varying marginal cost is set per snapshot.
    overrides: {link carrier: {bus: pd.Series of prices per year}}, e.g. the ETS2 price on the
    'CO2 atmosphere' bus for the household gas boilers and petrol cars.
    """
    price = resources_pars[resources_pars.Parameter == 'Price'].set_index('Resource')[years].astype(float)
    per = n.snapshots.get_level_values(0)
    overrides = overrides or {}
    mc = {}
    for name, l in n.links.iterrows():
        try:
            y = int(name.rsplit('_', 1)[1])
        except (IndexError, ValueError):
            continue
        buses = [(l.bus0, 1.0), (l.bus1, l.efficiency)]
        for i in (2, 3):
            b = l.get(f'bus{i}', '')
            if isinstance(b, str) and b:
                buses.append((b, l[f'efficiency{i}']))
        priced = [(b, f) for b, f in buses if b in price.index]
        if not priced or y not in years:
            continue
        vom = l.marginal_cost - sum(price.at[b, y] * f for b, f in priced)   # the build-year prices of model.py
        own = overrides.get(l.carrier, {})
        mc[name] = vom + sum((own[b] if b in own else price.loc[b]).loc[per].values * f for b, f in priced)
    if mc:
        n.links_t.marginal_cost = pd.DataFrame(mc, index=n.snapshots)


def apply_network_settings(n, scen, techs_d, resources_pars, years):
    """Settings that act on the built network: prices per period, the use of the hydrogen demand, demand path."""
    ets2 = ets2_price(scen, years)
    overrides = {t: {'CO2 atmosphere': ets2} for t in ETS2_TECHS} if ets2 is not None else None
    if scen.get('period_prices', False):
        set_period_prices(n, resources_pars, years, overrides)
    elif ets2 is not None:       # prices of the build year: swap the ETS1 part for the ETS2 price of that year
        co2 = resources_pars[(resources_pars.Resource == 'CO2 atmosphere')
                             & (resources_pars.Parameter == 'Price')][years].astype(float).iloc[0]
        for name in n.links.index[n.links.carrier.isin(ETS2_TECHS) & (n.links.bus2 == 'CO2 atmosphere')]:
            y = int(name.rsplit('_', 1)[1])
            n.links.at[name, 'marginal_cost'] += (ets2[y] - co2[y]) * n.links.at[name, 'efficiency2']
    if ets2 is not None:
        n.meta = {**n.meta, 'co2_price_ets2': {str(y): float(v) for y, v in ets2.items()}}

    # Storage cycles within each period. PyPSA 1.3 defaults to one cycle over the whole horizon, which lets a
    # battery or the H2 store fill in the 2040 representative year and empty in 2050.
    if scen.get('storage_cyclic_per_period', True):
        if len(n.storage_units):
            n.storage_units['cyclic_state_of_charge_per_period'] = True
        if len(n.stores):
            ext = n.stores.e_nom_extendable          # only built storage, not the fuel reserves or CO2 stores
            n.stores.loc[ext, 'e_cyclic_per_period'] = True

    # Over-dimensioned plant: water lets the electrolysers run at no more than this share of their capacity
    if (scen.get('electrolyser_limit_on', 'capacity') == 'output' and scen.get('electrolyser_cap_share') is not None
            and not scen.get('electrolyser_plant_reference')):
        ely = n.links.index[n.links.carrier.isin(ELECTROLYSIS)]
        n.links.loc[ely, 'p_max_pu'] = float(scen['electrolyser_cap_share'])

    per = n.snapshots.get_level_values(0)
    if scen.get('h2_demand_mt') is not None and H2_LOAD in n.loads.index:
        mt = _per_year(scen['h2_demand_mt'], years, 'h2_demand_mt')
        mw = mt * 1e6 * MWH_PER_T_H2 / 8760.0                      # flat MW
        n.loads_t.p_set[H2_LOAD] = mw.loc[per].values

    # What the hydrogen demand is used for (Francesco, 14 Oct):
    #   feedstock (refineries, ammonia): a separate demand stream on top of the course demands, nothing subtracted;
    #   fuel for high-temperature heat: subtract the heat it delivers from the industrial HTP demand.
    use = scen.get('h2_demand_use', 'feedstock')
    if use == 'htp_fuel' and H2_LOAD in n.loads.index and 'industrial_htp' in n.loads.index:
        eff = float(techs_d.at[('Industrial HTP - fossil - existing', 'Efficiency'), years[0]])
        red = n.loads_t.p_set[H2_LOAD] * eff               # MW of heat that this hydrogen delivers in a furnace
        htp = n.loads_t.p_set['industrial_htp']
        if (htp - red).min() < 0:
            raise ValueError('The hydrogen demand is larger than the industrial HTP demand')
        n.loads_t.p_set['industrial_htp'] = htp - red
        n.meta = {**n.meta, 'htp_reduction_twh': {str(y): float((red[per == y] * n.snapshot_weightings.generators[
            per == y]).sum() / 1e6) for y in years}}
    elif use not in ('feedstock', 'htp_fuel'):
        raise ValueError("h2_demand_use must be 'feedstock' or 'htp_fuel'")


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


def store_shadow_prices(n):
    """Save shadow prices on n.meta.

    * CO2-storage cap (€/tCO2 per year of capacity, € of that year).
    * Electrolyser capacity limit of the scenario (per capped vintage): the value of one more kW of electrolyser
      (hydrogen output) capacity, as a present value over its lifetime (€/kW_H2, discounted like the objective).
      This is what the system would gain if water allowed a slightly larger electrolyser.
    """
    co2, ely = {}, {}
    if getattr(n, 'model', None) is None:
        return {}
    w = n.investment_period_weightings.objective
    for name in n.model.constraints:
        if name.startswith('CO2-storage_cap-'):
            # value of one more tonne per year of CO2 storage capacity (€/tCO2), in € of that year
            y = int(name.rsplit('-', 1)[1])
            co2[str(y)] = abs(float(n.model.constraints[name].dual)) / w.loc[y]
    for name in n.model.constraints:
        if name.startswith('Electrolyser-total-cap-'):
            # joint limit on all electrolysers (MW of hydrogen output): € per kW of hydrogen output
            y = name.rsplit('-', 1)[1]
            ely.setdefault('total', {})[y] = abs(float(n.model.constraints[name].dual)) / 1e3
    caps = ((n.meta or {}).get('scenario') or {}).get('_electrolyser_caps_mw_h2') or {}
    if caps and 'Link-ext-p_nom-upper' in n.model.constraints:
        dual = n.model.constraints['Link-ext-p_nom-upper'].dual.to_series()
        for t, c in caps.items():
            for y, cap in c.items():
                name = f'{t}_{y}'
                # only where the limit allows some capacity: a limit of 0 MW (S3, or a vintage the reference did not
                # build) gives a dual that is not unique, so it is not reported
                if cap > 1.0 and name in dual.index and name in n.links.index:
                    # dual per MW of input (p_nom); per kW of hydrogen output: / efficiency / 1000
                    ely.setdefault(t, {})[y] = abs(float(dual[name])) / float(n.links.at[name, 'efficiency']) / 1e3
    n.meta = {**n.meta, 'co2_storage_cap_shadow_price': co2, 'electrolyser_cap_shadow_price_eur_per_kw_h2': ely}
    return {'co2': co2, 'electrolyser': ely}
