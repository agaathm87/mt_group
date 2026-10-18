# Final course model + hydrogen extension: the package without additions

This is one model: the **final course model** (FinalModel) with its hydrogen extension.

**Two packages run the same analysis**:
- `FinalModel_H2_without_additions`: SMR, SMR + CCS and the grid electrolyser serve the hydrogen demand;
- `FinalModel_H2_with_additions`: the same, plus hydrogen storage, the pure green route and pink hydrogen in every run.

**This is the package without additions.** The water limit is the same in MW in both packages, so their results can be compared one to one.

- **Hydrogen is a demand.** It is 1.3 Mt/yr for refineries and ammonia (Elzenga et al., 2025), the same in every period and scenario and flat over the hours.
- **Three end-use technologies** feed that demand directly:
  - SMR (grey): gas → hydrogen + CO₂ to the air;
  - SMR + CCS (blue): gas → hydrogen + a little CO₂ to the air + CO₂ stored (the storage is capped);
  - electrolyser (green): grid electricity → hydrogen.

  The reformers that exist in 2020 are the 2020 stock.
- **Water is not modelled.** The scenarios limit how much **electrolyser capacity** can be built, in the capacity constraints of the technology table. **The base is the scenario without water scarcity.**
- **No additions in this package.** Hydrogen storage, the pure green route (own wind and solar) and pink hydrogen (own nuclear plant) are in the package with additions (`FinalModel_H2_with_additions`), which runs the same analysis with them in every run.
- **Green levers, off by default**: electrolysers on desalinated seawater, outside the water limit (`desal`); a production subsidy per kg of electrolytic hydrogen (`h2_production_subsidy`); a minimum share of electrolytic hydrogen (`green_mandate`).
- **Real Dutch input data** are the default (research report *Dutch hydrogen model input data*). All money values are in 2024 euros.

| Scenario | Short name | Water | (1) Electrolyser capacity |
|---|---|---|---|
| S1 | **Base** | no scarcity: desalinated seawater | no limit: the cost-optimal capacity |
| S2 | **Medium** | medium: electrolysis is process water (category 3) | at most 50% of what Base without additions builds: 2,473 MW of hydrogen output in 2050, for all electrolysers together |
| S3 | **Scarce** | high: electrolysis is ordinary industry (category 4) | none |

## Quick start
```bash
pip install pypsa==1.3.0 highspy openpyxl matplotlib       # gurobipy if you use Gurobi
python build_h2_database.py                  # (re)builds input_databases/h2_nl from the final course database
python run_batch.py S1 S2 S3                 # the three scenarios (S1 first: it sets the water of S2)
python run_batch.py                          # all 30 runs of this package (the 60% mandate in Medium is infeasible)
```
For the normal workflow, open `interface.ipynb` and run its cells from top to
bottom. Set `RUN_ALL_SCENARIOS = True` to solve the configured registry and
set `RUN_ALL_FIGURES = True` to generate plots through the interface. The
plots are written to `results/plots/presentation/`, `results/plots/apa/`, and
`results/plots/` for system plots.
`run_batch.py` uses HiGHS (free) by default; `SOLVER=gurobi python run_batch.py ...` uses the course solver.
- A run takes 2–6 minutes with HiGHS (15-hour steps). Two runs can go in parallel (one thread each).
- All runs are saved in `results/runs/`, so the notebook and the figure scripts load them without solving.
- `docs/results_summary.md` has the main numbers of this package, written from the runs.

## Using the model
```python
from energy_model import model_run, make_scenario
from energy_model.model import electrolyser_reference
args = ('input_databases//h2_nl', [2020, 2030, 2040, 2050], 15, 4.0, 0.07, 0.01)
n_S1 = model_run(*args, solver_name='highs', scenario=make_scenario('S1'))            # Base (no limit)
ref = electrolyser_reference(n_S1)          # MW of hydrogen output per technology and vintage, e.g. {'Electrolyser': {'2050': 4946}}
n_S2 = model_run(*args, solver_name='highs', scenario=make_scenario('S2', electrolyser_reference=ref))   # Medium
n_S3 = model_run(*args, solver_name='highs', scenario=make_scenario('S3'))            # Scarce
```
Settings of `make_scenario()` that the group may want to change:

| Setting | Default | Meaning |
|---|---|---|
| `electrolyser_cap_share` | S1: None, S2: 0.5, S3: 0.0 | largest electrolyser capacity as a share of what Base without additions builds (Scarce at 10%: `0.1` with a reference) |
| `h2_storage`, `pure_green`, `pink` | False | not in this package (the package with additions has them); setting one to True gives an error |
| `electrolyser_subsidy`, `electrolyser_capex` | 0, central | (2a) cheaper electrolysers, e.g. a 20% subsidy or `'low'` |
| `co2_price` | `'central'` | (2b) `'zero'`, `'low'`, `'central'`, `'high'`, `'stress'` or your own `{year: €/t}` |
| `battery_cost_factor`, `battery_max_mw`, `battery_max_hours` | 1.0, None, None (4 h) | (3a–c) batteries: cost multiplier, largest total power, hours of storage |
| `h2_demand_use` | `'feedstock'` | `'feedstock'`: the hydrogen demand comes on top of the course demands; `'htp_fuel'`: it replaces part of the industrial high-temperature heat demand |
| `h2_demand_mt` | 1.3 Mt every period | a demand path, e.g. `'high'` (1.3 / 1.3 / 2.5 / 3.3 Mt) |
| `electrolyser_limit_on`, `electrolyser_plant_reference` | `'capacity'`, None | `'output'`: the electrolysers of Base are built, but water allows only the output of Medium (the oversized plant) |
| `desal`, `desal_cost_eur_per_kg` | False, 0.03 | green lever: an electrolyser on desalinated seawater (or effluent), outside the water limit, at this extra cost per kg of hydrogen (research report: €0.01–0.03/kg) |
| `h2_production_subsidy` | 0.0 | green lever: € per kg of hydrogen from every electrolyser (CfD/H2Global-type); a transfer, added back by `economic_cost()` |
| `green_mandate` | None | green lever: `{year: share}`, e.g. `{2040: 0.6, 2050: 0.6}`: at least this share of the hydrogen from electrolysis (RED III-type). Infeasible under a water limit unless `desal=True` |

## Implementation answers

### Topology changes

Yes, the hydrogen study extends the course topology. `build_h2_database.py`
creates a package-local hydrogen bus and the fixed `industrial_h2` demand,
then adds `SMR`, `SMR CCS`, `Electrolyser`, and the calibrated
`SMR - existing` link. The additions variant extends this further with
hydrogen storage, dedicated renewable electrolysis, and pink electrolysis.
These are database topology changes; the optimisation routine remains the
same generic PyPSA model in `energy_model/model.py`.

### Data obtained and changed

The source database is `input_databases/default`; it is copied to
`input_databases/h2_nl` and extended with the hydrogen demand and technology
data. The source database is not modified. The hydrogen demand is 1.3 Mt/year,
and the Dutch cost, efficiency, emissions, price, and lifetime assumptions are
written into the generated H2 database and documented in the build script.

The canonical `input_databases/h2_nl` remains shared, while the runner creates
and uses `input_databases/scenarios/<name>/` for every run. Each snapshot
contains a `scenario_manifest.json` with the source fingerprint and resolved
scenario settings. `model.py` still applies parameters to in-memory copies,
so the fast workflow is preserved while each run has a reproducible structural
input and configuration. A changed canonical database automatically refreshes
the snapshots.

### Parameter changes for each scenario

`run_batch.py` contains the shared 40-run registry. It changes parameters such
as electrolyser capacity limits, electrolyser subsidy/CAPEX, infrastructure
subsidy, CO2 price paths, battery cost and duration, hydrogen storage and its
cost multiplier, desalinated-water electrolysis, hydrogen production subsidy,
the hydrogen end use, and the green-hydrogen mandate. The additions package
also varies the availability of storage, dedicated renewable electrolysis, and
pink electrolysis. These values are passed to `make_scenario()` and applied
in memory; they do not overwrite the database.

### Key model outputs and results

The primary outputs are the solved PyPSA networks in `results/runs/*.nc`.
`figures/plots/h2_results.py` gathers and aggregates hydrogen-route production,
electrolyser capacity and full-load hours, system cost, CO2 emissions and
storage, gas use, electricity mix, water use, and policy indicators.
`h2_plots.py`, `h2_sankey.py`, `system_plots.py`, and `presentation.py`
generate figures from those saved networks. The document figures are
separate from these run-based figures.

### Staged plan and preliminary tests

1. Rebuild `input_databases/h2_nl` and verify the required sheets and files.
2. Check the topology: `Hydrogen`, `industrial_h2`, `SMR`, `SMR CCS`,
   `Electrolyser`, and `SMR - existing`.
3. Solve S1 first, derive the S2 electrolyser reference from S1, and then
   solve S2 and S3. Check that the capacity limits have the intended effect.
4. Run the sensitivity registry only after the three base scenarios pass.
   The expected infeasible case is `S2_mandate`, which is not saved.
5. Load the saved networks with `h2_results.py`, generate aggregate tables
   and figures, and compare the results with the base scenario.

This staged approach tests database construction, topology, scenario
parameters, and outputs separately before expensive full sensitivity runs.

## What is where
| File | Content |
|---|---|
| `interface.ipynb` | **Main notebook**: the course interface (settings, course plots, check against the course model) plus the hydrogen study of this package: the database, the scenarios, the policy story, Sankeys, the variations, the green levers and the figures. `html/interface.html` is the executed notebook. |
| `energy_model/model.py`, `preprocessing.py` | Final course model; our changes are marked `# [H2]`. |
| `energy_model/model.py` | Scenarios (electrolyser capacity limits), additions, levers, real data (central values are the defaults), cost variations, prices per period, extra constraints. |
| `figures/plots/h2_results.py`, `h2_plots.py`, `h2_sankey.py` | Output tables (incl. `policy_table`, `economic_cost`), plots, hydrogen Sankey diagrams. |
| `figures/plots/presentation.py` | **The figures for the slides and the report**: slide style (the template's content box) and APA style (6.5 inches wide, text 8 pt or more), all in colour. Also the tables `Table_key_numbers` and `Table_green_levers` next to the APA figures. |
| `figures/plots/system_plots.py` | Whole-system plots and the course's quick plots. |
| `figures/plots/ensemble.py`, `ensemble_analysis.py` | Scenario ensemble (EMA Workbench); not rerun. |
| `input_databases/default` | The final course database, untouched. |
| `input_databases/h2_nl` | Canonical hydrogen database of this package. |
| `input_databases/scenarios/<name>` | Run-specific database snapshot and scenario manifest. |
| `run_batch.py` | The runs of this package (30 that solve, plus the 60% mandate in Medium, which is infeasible) and a cached runner. |
| `docs/results_summary.md` | The main numbers of this package, written from its runs. |
| `docs/model_notes.md` | What the meetings changed; checks against the final model and the sources; results; suggested report text (written for both packages). |
| `docs/report_tables_check.md` | What changes in Tables 1–3 of the report. |
| `docs/Dutch hydrogen model input data.md` | Research report: the real input data, ranges and sources. |
| `figures_document/` | Report figures in colour (APA), drawn for this package: Figure 1 (scenario matrix), Figure 2 (verdringingsreeks), Figure 3 (model structure); `--bw` gives black and white, `--slide` a slide version (Figures 1 and 2; for Figure 3 the slide version is `P_impl_model_structure`). Also the course overview with our extension (slide size). |
| `results/` | Solved runs (`runs/`) and generated plots (`plots/presentation/` for slides, `plots/apa/` for the report). |

## Checks
- **Course model.** With `input_databases/default` and no scenario, the objective is 2.1292789279e12 (HiGHS), identical to the final course model.
- **The two packages.** Base without additions has the same objective in both packages, so the package without additions and the `_noadd` runs of the package with additions are the same model.
- **Sources.** Every input that differs from the course database is listed with its source in `docs/model_notes.md`.
- **The scenario limit** is written into the capacity constraints (the course's own table) and printed by `run_batch.py`. Medium allows 2,473 MW of hydrogen output (3.5 GW of electricity input) in 2050, half of Base without additions.
