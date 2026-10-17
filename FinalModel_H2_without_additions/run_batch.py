"""Run a list of runs on the final course model with the hydrogen extension and save each network to
results/runs/<name>.nc (runs already on disk are skipped).

Usage:  python run_batch.py S1 S2 S3 ...        (names from RUNS below; no names = all runs)
        SOLVER=gurobi python run_batch.py ...    (the course solver; the default here is HiGHS, which is free)

The three scenarios (meeting with Francesco, 14 Oct; base = 100%, group 15 Oct): one dimension, water availability.
  S1 Base     no water scarcity: the cost-optimal electrolyser capacity
  S2 Medium   electrolyser capacity at most 50% of what Base WITHOUT additions builds (all electrolysers together)
  S3 Scarce   no electrolysers
Two packages run the same list (energy_model/package.py):
  * without additions: SMR, SMR + CCS and the grid electrolyser;
  * with additions: the same runs with hydrogen storage, the pure green route and pink hydrogen on in every run, plus
    runs that show what the additions do (S*_noadd: none of them, the same as the package without additions;
    S*_storage, S*_green, S*_pink: one of them).
The limits are fixed in MW by Base without additions (S1, or S1_noadd in the package with additions), for every run:
the water that is available does not change when costs change or technologies are added. The limit is on all
electrolysers together (MW of hydrogen output per vintage), whatever their power source. All runs use
input_databases/h2_nl of this package.
"""
import json
import os
import sys
import time
import warnings

warnings.filterwarnings('ignore')
from energy_model import model_run, make_scenario
from energy_model.hydrogen import electrolyser_reference
from energy_model.package import ADDITIONS, SET_NAME

SOLVER = 'highs'
YEARS, T_RES, CARS_CF, RT, RS = [2020, 2030, 2040, 2050], 15, 40 * 0.1, 0.07, 0.01
DB = 'input_databases//h2_nl'        # final course database + hydrogen + real Dutch data (research report)


BASE_NOADD = 'S1_noadd' if ADDITIONS else 'S1'     # Base without additions: it sets the water (MW) in both packages


def ref(run=BASE_NOADD):
    """The limits of a Medium run refer to the electrolyser capacity of Base without additions, so that the water
    available is the same in MW in every run of both packages."""
    return dict(electrolyser_reference=f'from:{run}')


MANDATE = {2040: 0.6, 2050: 0.6}     # minimum share of the hydrogen made by electrolysis (green lever)
NOADD = dict(h2_storage=False, pure_green=False, pink=False)      # package with additions: switch them all off
ONLY_STORAGE = dict(pure_green=False, pink=False)                 # ... or keep only one of them
ONLY_GREEN = dict(h2_storage=False, pink=False)
ONLY_PINK = dict(h2_storage=False, pure_green=False)

# name: (scenario, settings)
RUNS = {
    # ---- the three scenarios ----
    'S1': ('S1', {}),
    'S2': ('S2', ref()),
    'S3': ('S3', {}),
    # ---- (2a) cheaper electrolysers: a subsidy of 20% (Francesco's example) or 40%, and the low cost path ----
    'S1_sub20': ('S1', dict(electrolyser_subsidy=0.2)), 'S2_sub20': ('S2', dict(ref(), electrolyser_subsidy=0.2)),
    'S1_sub40': ('S1', dict(electrolyser_subsidy=0.4)), 'S2_sub40': ('S2', dict(ref(), electrolyser_subsidy=0.4)),
    'S1_capexlow': ('S1', dict(electrolyser_capex='low')), 'S2_capexlow': ('S2', dict(ref(), electrolyser_capex='low')),
    # ---- (2b) CO2 price paths: low (170 €/t in 2050) and high (500 €/t) ----
    'S1_co2low': ('S1', dict(co2_price='low')), 'S2_co2low': ('S2', dict(ref(), co2_price='low')),
    'S3_co2low': ('S3', dict(co2_price='low')),
    'S1_co2high': ('S1', dict(co2_price='high')), 'S2_co2high': ('S2', dict(ref(), co2_price='high')),
    'S3_co2high': ('S3', dict(co2_price='high')),
    # ---- (3a, 3c) batteries where electrolysis is limited: half the cost, 8 hours instead of 4 ----
    'S2_battery_cheap': ('S2', dict(ref(), battery_cost_factor=0.5)),
    'S2_battery_8h': ('S2', dict(ref(), battery_max_hours=8)),
    # ---- Scarce at 10% instead of 0% (Francesco: "zero or ten percent") ----
    'S3_10pct': ('S3', dict(ref(), electrolyser_cap_share=0.1)),
    # ---- the over-dimensioned plant: the electrolysers of Base are built, then water allows only Medium's water ----
    #   (without additions: the plant of S1 at 50% of its output; with additions: the plant of S1 of that package,
    #   whose hourly output is capped at the same MW as Medium)
    'S2_oversized': ('S2', dict(ref(), electrolyser_limit_on='output', **(
        dict(electrolyser_plant_reference='from:S1') if ADDITIONS else {}))),
    # ---- the decision on what the hydrogen is for: fuel for high-temperature heat instead of feedstock ----
    'S1_htp_fuel': ('S1', dict(h2_demand_use='htp_fuel')),
    # ---- green levers within the water scenarios (16 Oct) ----
    # alternative water: electrolysers on desalinated seawater, outside the water limit (0.03 €/kg; x10 = 0.30 €/kg)
    'S2_desal': ('S2', dict(ref(), desal=True)), 'S3_desal': ('S3', dict(desal=True)),
    'S3_desal_x10': ('S3', dict(desal=True, desal_cost_eur_per_kg=0.30)),
    # an operating subsidy per kg of electrolytic hydrogen (CfD / H2Global / SDE++-type)
    'S1_prod1': ('S1', dict(h2_production_subsidy=1.0)), 'S2_prod1': ('S2', dict(ref(), h2_production_subsidy=1.0)),
    'S1_prod2': ('S1', dict(h2_production_subsidy=2.0)), 'S2_prod2': ('S2', dict(ref(), h2_production_subsidy=2.0)),
    # a green-hydrogen mandate: 60% of the hydrogen from electrolysis from the 2040 period (RED III: 60% by 2035;
    # its 42% for 2030 cannot be met with the build limit of 3 GW). Medium and Scarce cannot meet it on their own water.
    'S1_mandate': ('S1', dict(green_mandate=MANDATE)), 'S2_mandate': ('S2', dict(ref(), green_mandate=MANDATE)),
    'S2_desal_mandate': ('S2', dict(ref(), desal=True, green_mandate=MANDATE)),
    'S3_desal_mandate': ('S3', dict(desal=True, green_mandate=MANDATE)),
}
if ADDITIONS:
    RUNS.update({
        # ---- what the additions do: none of them (= the package without additions), or one of them ----
        'S1_noadd': ('S1', NOADD), 'S2_noadd': ('S2', dict(NOADD, **ref())), 'S3_noadd': ('S3', NOADD),
        'S1_storage': ('S1', ONLY_STORAGE), 'S2_storage': ('S2', dict(ONLY_STORAGE, **ref())),
        'S3_storage': ('S3', ONLY_STORAGE),
        'S1_green': ('S1', ONLY_GREEN), 'S2_green': ('S2', dict(ONLY_GREEN, **ref())), 'S3_green': ('S3', ONLY_GREEN),
        'S1_pink': ('S1', ONLY_PINK), 'S2_pink': ('S2', dict(ONLY_PINK, **ref())), 'S3_pink': ('S3', ONLY_PINK),
        # ---- (2c) H2 storage three times as expensive ----
        'S1_storage_x3': ('S1', dict(h2_storage_cost_factor=3.0)),
        'S2_storage_x3': ('S2', dict(ref(), h2_storage_cost_factor=3.0)),
        # ---- strict green: no grid electrolyser; green hydrogen only from dedicated wind + solar (RFNBO-type) ----
        'S1_green_only': ('S1', dict(grid_electrolysis=False)),
    })
# The 60% mandate in Medium (S2_mandate) has no solution: water allows electrolysers for at most 50% of the demand.
INFEASIBLE = {'S2_mandate': 'the water of Medium allows electrolysis for at most 50% of the hydrogen'}


def _reference(settings, solver):
    """Replace 'from:<run>' by the electrolyser capacity per vintage of that run (solving it first if needed)."""
    for key in ('electrolyser_reference', 'electrolyser_plant_reference'):
        ref = settings.get(key)
        if isinstance(ref, str) and ref.startswith('from:'):
            import pypsa
            path = run(ref[5:], solver)
            settings[key] = electrolyser_reference(pypsa.Network(path))
    return settings


def run(name, solver=SOLVER, rerun=False, t_res=T_RES):
    path = os.path.join('results', 'runs', f'{name}.nc')
    if os.path.exists(path) and not rerun:
        print(f'{name}: already on disk')
        return path
    base, settings = RUNS[name]
    settings = _reference(dict(settings), solver)
    t = time.time()
    opts = {'threads': 1, 'time_limit': 7200.0} if solver == 'highs' else {'Threads': 1, 'TimeLimit': 7200}
    n = model_run(DB, YEARS, t_res, CARS_CF, RT, RS, solver_name=solver, solver_options=opts,
                  scenario=make_scenario(base, label=name, **settings),
                  results_dir=os.path.join('results', 'logs'))
    if n.loads_t.p.empty:                      # infeasible or not solved: do not save
        print(f'{name}: NOT solved (infeasible?) - nothing saved')
        return None
    os.makedirs(os.path.dirname(path), exist_ok=True)
    n.export_to_netcdf(path)
    caps = (n.meta.get('scenario') or {}).get('_electrolyser_caps_mw_h2')
    if caps:
        print(f'{name}: electrolyser limit per vintage (MW of H2 output): {json.dumps(caps)}')
    print(f'{name}: solved in {time.time() - t:.0f} s')
    return path


if __name__ == '__main__':
    solver = os.environ.get('SOLVER', SOLVER)
    print(f'Package {SET_NAME}: {len(RUNS)} runs')
    for name in (sys.argv[1:] or [r for r in RUNS if r not in INFEASIBLE]):     # infeasible ones only when named
        run(name, solver)
