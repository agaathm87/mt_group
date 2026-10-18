# Energy transition model with hydrogen
by *Agaath de Vries​, Māra Učelniece​, and Josefina Rodríguez Zuloaga​*

This folder contains an energy transition model with a hydrogen extension.
Hydrogen is represented as a fixed industrial demand of 1.3 Mt per year,
served by grey hydrogen, blue hydrogen, and grid electrolysis. The 2020
reformers are represented as existing capacity.

- **Hydrogen is a demand.** It is 1.3 Mt/yr for refineries and ammonia (Elzenga et al., 2025), the same in every period and scenario and flat over the hours.
- **Three end-use technologies** feed that demand directly:
  - SMR (grey): gas → hydrogen + CO₂ to the air;
  - SMR + CCS (blue): gas → hydrogen + a little CO₂ to the air + CO₂ stored (the storage is capped);
  - electrolyser (green): grid electricity → hydrogen.
  The reformers that exist in 2020 are the 2020 stock.

- **Water is not modelled.** The scenarios limit how much **electrolyser capacity** can be built, in the capacity constraints of the technology table. **The base is the scenario without water scarcity.**

- **Green levers, off by default**: electrolysers on desalinated seawater, outside the water limit (`desal`); a production subsidy per kg of electrolytic hydrogen (`h2_production_subsidy`); a minimum share of electrolytic hydrogen (`green_mandate`).
- **Real Dutch input data** are the default (research report *Dutch hydrogen model input data*). All money values are in 2024 euros.

| Scenario | Short name | Meaning |
|---|---|---|
| S1 | **Base** | No electrolyser capacity limit |
| S2 | **Medium** | Electrolyser capacity capped at 50% of the S1 reference  |
| S3 | **Scarce** | No electrolyser capacity |




## Quick start
```bash
pip install pypsa==1.3.0 openpyxl matplotlib gurobipy
python build_h2_database.py                  # (re)builds input_databases/h2_nl from the final course database
python run_batch.py S1 S2 S3                 # the three scenarios (S1 first: it sets the water of S2)
python run_batch.py                          # all 40 configured runs (S2_mandate is infeasible by design)
```
For the normal workflow, open `interface.ipynb` and run its cells from top to
bottom. Set `RUN_ALL_SCENARIOS = True` to solve the configured registry and
set `RUN_ALL_FIGURES = True` to generate plots through the interface. The
plots are written to `results/plots/presentation/`, `results/plots/apa/`, and
`results/plots/` for system plots.
The published workflow uses Gurobi. A valid Gurobi license is required.
The model uses 15-hour representative steps; two independent runs can go in
parallel when each is configured to use one solver thread.
- All runs are saved in `results/runs/`, so the notebook and the figure scripts load them without solving.
- `docs/results_summary.md` has the main numbers of this package, written from the runs.


## Running from the interface

Open `interface.ipynb` in VS Code or Jupyter with the configured Python
environment, then run the notebook cells from top to bottom:

1. The setup cell imports the model and the plotting functions from
   `figures/plots`.
2. Keep `RUN_ALL_SCENARIOS = False` to load existing
   `results/runs/*.nc` files. Set it to `True` to solve the complete
   `run_batch.py` registry; set `RERUN = True` to force fresh solves.
3. Set `RUN_ALL_FIGURES = True` in the final plotting cell to generate
   figures from the saved runs. Outputs are written to
   `results/plots/presentation/`, `results/plots/apa/`, and `results/plots/`
   for system plots.

The interface is the user-facing workflow: it runs scenarios through
`run_batch.py`, loads saved PyPSA networks, and calls the modules in
`figures/plots`. The plot modules do not need to be run as a separate package.


## Implementation answers

### Topology changes

`build_h2_database.py`
creates a package-local hydrogen bus and the fixed `industrial_h2` demand,
then adds `SMR`, `SMR CCS`, `Electrolyser`, and the calibrated
`SMR - existing` link. This package also retains optional hydrogen storage;
the additions variant extends the hydrogen topology further with dedicated
renewable electrolysis and pink electrolysis. These are database topology
changes; the optimisation routine remains the same generic PyPSA model in
`energy_model/model.py`.

### Data obtained and changed

`input_databases/default` is copied and extended to create
`input_databases/h2_nl`. The default course database remains untouched.
Hydrogen demand, Dutch technology costs, efficiencies, lifetimes, and
emissions are added by `build_h2_database.py`. This published copy is the
without-additions H2 model: it does not include dedicated pure-green or pink
hydrogen routes. Hydrogen storage is available as an optional H2 technology
and is enabled by the default settings; individual scenarios can disable it
with `h2_storage=False`.

The canonical `input_databases/h2_nl` remains shared, while the runner creates
and uses `input_databases/scenarios/<name>/` for every run. Each snapshot
contains a `scenario_manifest.json` with the source fingerprint and resolved
settings. `model.py` still applies parameters to in-memory copies, preserving
the fast workflow while making each run's structural input reproducible.

### Parameter changes for each scenario

The `run_batch.py` registry changes electrolyser capacity, subsidies and
CAPEX, infrastructure subsidy, CO2 price, battery cost and duration,
hydrogen storage sensitivities, desalinated-water electrolysis, hydrogen production
subsidy, hydrogen end use, and the green-hydrogen mandate. These are scenario
settings applied in memory through `make_scenario()` and the H2 scenario
modules.

### Key model outputs and results

Saved networks in `results/runs/*.nc` are the primary results. The result and
plot modules derive hydrogen route balances, capacity, full-load hours, costs,
CO2, gas use, electricity mix, water use, storage, and policy indicators.


## What is where

### Main files

- `energy_model/model.py`: course-model construction and optimization.
- `energy_model/h2_presets.py`: H₂ constants, price paths, defaults, and scenario presets.
- `energy_model/h2_scenario.py`: scenario settings and input changes.
- `energy_model/h2_constraints.py`: additional H₂, water, storage, and capacity constraints.
- `figures/plots/h2_results.py`: result calculations.
- `build_h2_database.py`: builds `input_databases/h2_nl`.
- `figures/plots/`: analysis and plotting modules used by the interface.
- `results/plots/`: generated slide, report, and system plots.
- `run_batch.py`: scenario registry and batch runner.
- `interface.ipynb`: interactive model interface.
- `results/solver_run.log`: example solver log.

### Green levers and storage

The optional experiments retained in this package are:

- `desal`: electrolysis using alternative water outside the capacity limit;
- `h2_production_subsidy`: an operating subsidy per kilogram of hydrogen;
- `infrastructure_subsidy`: a 20% or 40% capital subsidy for electrolyser infrastructure;
- `green_mandate`: a minimum electrolytic-hydrogen share;
- `h2_storage`: hydrogen storage in salt caverns;
- `h2_storage_cost_factor`: storage-cost sensitivity.

Storage is controlled by the `STORAGE` switch near the top of
`energy_model/h2_presets.py`. Individual runs can override it with
`h2_storage=True` or `h2_storage=False`. The selected runs are defined in
`run_batch.py`.


| File | Content |
|---|---|
| `interface.ipynb` | **Main notebook**: the course interface (settings, course plots, check against the course model) plus the hydrogen study of this package: the database, the scenarios, the policy story, Sankeys, the variations, the green levers and the figures. `html/interface.html` is the executed notebook. |
| `energy_model/model.py`, `preprocessing.py` | Final course model and data preprocessing. |
| `energy_model/h2_presets.py`, `h2_scenario.py`, `h2_constraints.py` | Hydrogen defaults, scenario input changes, and additional constraints. |
| `figures/plots/h2_results.py`, `h2_plots.py`, `h2_sankey.py` | Output tables (incl. `policy_table`, `economic_cost`), plots, hydrogen Sankey diagrams. |
| `figures/plots/presentation.py` | **The figures for the slides and the report**: slide style (the template's content box) and APA style (6.5 inches wide, text 8 pt or more), all in colour. Also the tables `Table_key_numbers` and `Table_green_levers` next to the APA figures. |
| `figures/plots/system_plots.py` | Whole-system plots and the course's quick plots. |
| `input_databases/default` | The final course database, untouched. |
| `input_databases/h2_nl` | Canonical hydrogen database of this package. |
| `input_databases/scenarios/<name>` | Run-specific database snapshot and scenario manifest. |
| `run_batch.py` | The 40 configured runs, including the intentionally infeasible `S2_mandate`, and the cached runner. |
| `docs/results_summary.md` | The main numbers of this package, written from its runs. |
| `docs/model_notes.md` | What the meetings changed; checks against the final model and the sources; results; suggested report text (written for both packages). |
| `docs/report_tables_check.md` | What changes in Tables 1–3 of the report. |
| `docs/Dutch hydrogen model input data.md` | Research report: the real input data, ranges and sources. |
| `figures_document/` | Presentation-ready document diagrams: the model overview, Figure 1 (scenario matrix), Figure 2 (verdringingsreeks), and Figure 3 (model structure), with one PNG output per diagram and the source scripts. |
| `results/` | Solved runs (`runs/`) and generated plots (`plots/presentation/` for slides, `plots/apa/` for the report). |
