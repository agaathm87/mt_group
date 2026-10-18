"""Exploratory modelling: a large set of plausible futures, run with the EMA Workbench (Kwakkel, 2017).

XLRM frame (research report, section "Designing an ensemble"):
  X  uncertainties  UNCERTAINTIES below; ranges from the research report (low-high, 2024 euros)
  L  levers         the scenario parameter (1), water availability: S1 Base, no limit (the cost-optimal electrolyser
                   capacity), S2 Medium, at most 50% of the electrolyser capacity that S1 builds IN THE SAME FUTURE,
                   S3 Scarce, no electrolysers
  R  relationships  the final course model + hydrogen (set-up of 14 Oct: a fixed hydrogen demand served by SMR,
                   SMR CCS and electrolysers) with the Dutch database (h2_nl), coarser time steps (T_RES) for speed
  M  metrics        OUTCOMES below

Each path-type uncertainty (CO2 price, gas price, electrolyser cost, ...) is ONE index between 0 (low path)
and 1 (high path), so a future never zig-zags between low and high values over time.
The share of futures in which something happens is not a probability (no distributions are assumed).

    python -m energy_model.ensemble 96 2         # 96 futures x 3 policies, 2 processes (resumable)

In each future S1 runs first, because the limit of S2 is a share of the electrolyser capacity that S1 builds.
"""

import json
import os
import sys
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

from energy_model.model import (make_scenario, electrolyser_reference, CO2_PRICES, CO2_PRICES_ETS2, GAS_PRICES, ELY_CAPEX,
                       CO2_STORAGE_CAPS, H2_DEMAND, CAPACITY_CAPS, MWH_PER_KG)

ROOT = Path(__file__).resolve().parents[2]
DB = str(ROOT / 'input_databases' / 'h2_nl')
OUT = ROOT / 'results' / 'ensemble'
YEARS = [2020, 2030, 2040, 2050]
T_RES = 73                 # hours per time step in the ensemble (120 steps per year; 15 h in the main runs)
CARS_CF, RS = 4.0, 0.01

# name: (low, high, unit, meaning)
UNCERTAINTIES = {
    'co2_index':       (0.0, 1.0, '-', 'EU ETS CO2 path: 0 = low (75/130/170 €/t), 1 = high (140/270/500 €/t); '
                                       'ETS2 (household gas, petrol cars) moves with it: 57/148/170 to 135/350/500'),
    'gas_index':       (0.0, 1.0, '-', 'TTF gas path: 0 = low (17/16/14 €/MWh), 1 = high (52/44/42 €/MWh)'),
    'ely_capex_index': (0.0, 1.0, '-', 'Electrolyser CAPEX path: 0 = low (1250/800/500 €/kW), 1 = high (2500/1800/1400)'),
    'co2_ts_price':    (25.0, 75.0, '€/t', 'CO2 transport and storage tariff (Porthos 47, Aramis 67-72)'),
    'co2_storage_index': (0.0, 1.0, '-', 'CO2 storage capacity: 0 = 2.5/10/10 Mt/yr, 1 = 10/25/25 Mt/yr'),
    'offshore_capex_factor': (0.875, 1.08, 'x', 'offshore wind CAPEX (2100-2600 €/kW in 2030 vs 2400 central)'),
    'res_capex_factor': (0.7, 1.25, 'x', 'solar PV and onshore wind CAPEX multiplier (DEA range)'),
    'h2_demand_index': (0.0, 1.0, '-', 'H2 demand: 0 = 0.8/1.3/1.3 Mt, 1 = 1.3/2.5/3.3 Mt (2030/2040/2050)'),
    'ely_build_index': (0.0, 1.0, '-', 'electrolyser build limit: 0 = 1.2/15/14 GW, 1 = 3/20/40 GW'),
    'wacc':            (0.03, 0.10, '-', 'technical discount rate (annuities)'),
    'dummy':           (0.0, 1.0, '-', 'not used by the model: threshold for "no influence" in feature scoring'),
}
POLICIES = ['S1', 'S2', 'S3']          # S1 first: S2 needs its electrolyser capacity


def _interp(low, high, i):
    return {y: low[y] + i * (high[y] - low[y]) for y in low}


def scenario_settings(policy, reference=None, **x):
    """Translate one future (x) and one policy into make_scenario() settings.
    reference: the electrolyser capacity per vintage of S1 in the same future (needed for S2)."""
    caps_lo, caps_hi = CAPACITY_CAPS['low'], CAPACITY_CAPS['central']
    ely_caps = _interp(caps_lo[0]['cap'], caps_hi[0]['cap'], x['ely_build_index'])
    caps = [dict(caps_hi[0], cap=ely_caps), caps_hi[1], caps_hi[2]]
    extra = dict(electrolyser_reference=reference) if policy == 'S2' else {}
    return make_scenario(
        policy, label=policy, **extra,
        co2_price=_interp(CO2_PRICES['low'], CO2_PRICES['high'], x['co2_index']),
        co2_price_ets2=_interp(CO2_PRICES_ETS2['low'], CO2_PRICES_ETS2['high'], x['co2_index']),
        gas_price=_interp(GAS_PRICES['low'], GAS_PRICES['high'], x['gas_index']),
        electrolyser_capex=_interp(ELY_CAPEX['low'], ELY_CAPEX['high'], x['ely_capex_index']),
        co2_storage_price=float(x['co2_ts_price']),
        co2_storage_cap=_interp(CO2_STORAGE_CAPS['low'], CO2_STORAGE_CAPS['high'], x['co2_storage_index']),
        capex_factors={'Wind turbine - offshore': x['offshore_capex_factor'],
                       'Solar PV': x['res_capex_factor'], 'Wind turbine - onshore': x['res_capex_factor']},
        h2_demand_mt=_interp(H2_DEMAND['low'], H2_DEMAND['high'], x['h2_demand_index']),
        capacity_caps=caps,
    )


OUTCOMES = ['green_share_2040', 'green_share_2050', 'green_twh_2050', 'blue_twh_2050', 'grey_twh_2050',
            'ely_gw_2050', 'ely_flh_2050', 'lcoh_green_2050', 'h2_price_2050', 'gas_2050', 'system_cost_bn',
            'cum_co2_mt', 'co2_2050', 'co2_h2_2050', 'water_2050', 'electricity_price_2050', 'infeasible']


def evaluate(n):
    """Scalar outcomes of one solved network."""
    from .h2_results import summary, cumulative_co2
    s = summary(n).loc[2050]
    s40 = summary(n).loc[2040]
    return dict(
        green_share_2040=float(np.nan_to_num(s40['Green share (%)'])),
        green_share_2050=float(np.nan_to_num(s['Green share (%)'])),
        green_twh_2050=float(s['Green H2 total (TWh/yr)']),
        blue_twh_2050=float(s['Blue (SMR + CCS)']),
        grey_twh_2050=float(s['Grey (SMR)']),
        ely_gw_2050=float(s['Electrolyser capacity (GW_el)']),
        ely_flh_2050=float(s['Electrolyser full-load hours (h/yr)']),
        lcoh_green_2050=float(s['LCOH Green (grid electrolysis) (€/kg)']),
        h2_price_2050=float(s['H2 price, mean (€/kg)']),
        gas_2050=float(s['Gas use, total (TWh/yr)']),
        system_cost_bn=float(n.objective / 1e9),
        cum_co2_mt=float(cumulative_co2(n)),
        co2_2050=float(s['CO2 total (Mt/yr)']),
        co2_h2_2050=float(s['CO2 from H2 production (Mt/yr)']),
        water_2050=float(s['Water for H2 (Mm3/yr)']),
        electricity_price_2050=float(s['Electricity price, mean (€/MWh)']),
        infeasible=0.0,
    )


def run_future(water_case='S1', future_id=-1, reference=None, **x):
    """Build, solve and evaluate one future under one policy. Returns (outcomes, electrolyser reference).
    For S2, `reference` is the electrolyser capacity per vintage of S1 in the same future."""
    warnings.filterwarnings('ignore')
    import logging
    logging.getLogger('pypsa').setLevel(logging.ERROR)
    logging.getLogger('linopy').setLevel(logging.ERROR)
    from energy_model.model import model_run
    t0 = time.time()
    x = {k: x[k] for k in UNCERTAINTIES}
    scen = scenario_settings(water_case, reference=reference, **x)
    ref = None
    tmp = OUT / 'logs' / f'pid{os.getpid()}'
    tmp.mkdir(parents=True, exist_ok=True)
    try:
        import contextlib, io
        with contextlib.redirect_stdout(io.StringIO()):
            n = model_run(DB, YEARS, T_RES, CARS_CF, float(x['wacc']), RS, solver_name='highs',
                          solver_options={'threads': 1, 'time_limit': 1800.0}, scenario=scen,
                          results_dir=str(tmp))
        out = evaluate(n)
        ref = electrolyser_reference(n)
    except Exception as e:                       # infeasible or failed run: keep the batch going
        out = {k: np.nan for k in OUTCOMES}
        out['infeasible'] = 1.0
        print('run failed:', water_case, repr(e)[:200], file=sys.stderr)
    # write every run to a CSV as soon as it is done, so nothing is lost if the batch stops
    row = {'scenario': future_id, 'policy': water_case, **x, **out, 'seconds': round(time.time() - t0, 1),
           'ely_reference': json.dumps(ref) if ref is not None else ''}
    path = OUT / 'runs_log.csv'
    pd.DataFrame([row]).to_csv(path, mode='a', header=not path.exists(), index=False)
    return out, ref


def design(n_futures=96, seed=42):
    """Latin hypercube sample of the uncertainties (scipy), saved as results/ensemble/design.csv."""
    from scipy.stats import qmc
    u = qmc.LatinHypercube(d=len(UNCERTAINTIES), seed=seed).random(n_futures)
    lo = np.array([v[0] for v in UNCERTAINTIES.values()])
    hi = np.array([v[1] for v in UNCERTAINTIES.values()])
    df = pd.DataFrame(lo + u * (hi - lo), columns=list(UNCERTAINTIES))
    df.insert(0, 'scenario', range(n_futures))
    OUT.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT / 'design.csv', index=False)
    return df


def _task(args):
    """All policies still to do for one future, S1 first (its electrolyser capacity sets the limit of S2)."""
    fid, policies, x, ref = args
    for p in POLICIES:
        if p not in policies:
            continue
        if p == 'S2' and ref is None:          # S1 failed in this future: S2 cannot be defined
            continue
        _, r = run_future(p, future_id=fid, reference=ref if p == 'S2' else None, **x)
        if p == 'S1':
            ref = r
    return fid


def run_ensemble(n_futures=96, n_processes=2, seed=42):
    """Run every future under the three policies (full factorial, needed for regret).

    Resumable: futures x policies already in results/ensemble/runs_log.csv are skipped, so the
    batch can be stopped and started again. The EMA Workbench is used for the analysis (ensemble_analysis.py).
    """
    from multiprocessing import Pool
    OUT.mkdir(parents=True, exist_ok=True)
    d = pd.read_csv(OUT / 'design.csv') if (OUT / 'design.csv').exists() else design(n_futures, seed)
    done, refs = set(), {}
    if (OUT / 'runs_log.csv').exists():
        log = pd.read_csv(OUT / 'runs_log.csv')
        done = set(zip(log['scenario'], log['policy']))
        for _, r in log[(log.policy == 'S1') & log.ely_reference.notna()].iterrows():
            refs[int(r.scenario)] = json.loads(r.ely_reference) if r.ely_reference else None
    tasks = []
    for _, r in d.iterrows():
        todo = [p for p in POLICIES if (int(r.scenario), p) not in done]
        if todo:
            tasks.append((int(r.scenario), todo, {k: float(r[k]) for k in UNCERTAINTIES}, refs.get(int(r.scenario))))
    print(f'{sum(len(t[1]) for t in tasks)} runs to do in {len(tasks)} futures ({len(done)} already done)', flush=True)
    t0 = time.time()
    with Pool(n_processes, maxtasksperchild=4) as pool:
        for i, _ in enumerate(pool.imap_unordered(_task, tasks), 1):
            if i % 5 == 0:
                print(f'{i}/{len(tasks)} futures, {time.time() - t0:.0f} s', flush=True)
    return load_ensemble()


def load_ensemble(path=None):
    """Load the ensemble table: one row per future (column 'scenario') x policy (S1/S2/S3)."""
    df = pd.read_csv(Path(path) if path else OUT / 'runs_log.csv')
    df = df.drop_duplicates(['scenario', 'policy'], keep='last').sort_values(['scenario', 'policy'])
    return df.reset_index(drop=True)


if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 96
    procs = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    df = run_ensemble(n, procs)
    print(df.groupby('policy')[['green_share_2050', 'system_cost_bn', 'cum_co2_mt']].describe().T)


