# Hydrogen Extension

Hydrogen extension of the final course model.

---

## Overview

Hydrogen is modelled as a **demand**, not a secondary resource:
- `industrial_h2` on the bus `Hydrogen`
- **1.3 Mt/yr** in every period and scenario *(Elzenga et al., 2025)*
- Flat hourly profile

---

## End-Use Technologies

Three technologies feed hydrogen demand directly (Links, see `build_h2_database.py`), plus the existing stock:

| Technology | Input | Output |
|---|---|---|
| SMR (grey) | Gas supply | Hydrogen + CO₂ atmosphere |
| SMR CCS (blue) | Gas supply | Hydrogen + CO₂ atmosphere (uncaptured) + CO₂ storage |
| Electrolyser (green) | Electricity | Hydrogen |
| SMR - existing | — | Existing reformers in 2020 (course convention) |

---

## Scenarios

Scenarios vary along one dimension: **water availability**. Water itself is not modelled — instead, each scenario constrains how much electrolyser capacity can be built (per vintage):

| Scenario | Water Availability | Electrolyser Capacity Limit |
|---|---|---|
| **S1 Base** | No scarcity (100%) | Cost-optimal (reference run) |
| **S2 Medium** | Medium scarcity | ≤ 50% of S1 capacity per vintage |
| **S3 Scarce** | High scarcity | No electrolysers (0%) |

Remaining hydrogen demand is met by gas-based hydrogen (grey or blue, whichever is cheaper).

---

## Storage

Optional **salt-cavern storage** on the hydrogen bus *(added by group, 15 Oct)*.

---

## Green Levers *(off by default, 16 Oct)*

Optional sensitivities within each water scenario:

| Lever | Description |
|---|---|
| `desal` | Electrolysers on desalinated seawater, outside the water limit, at 0.01–0.03 €/kg extra cost |
| `h2_production_subsidy` | Subsidy in €/kg of electrolytic hydrogen |
| `green_mandate` | Minimum share of electrolytic hydrogen per period (RED III-type) |

---

## Module Contents

| Component | Description |
|---|---|
| `SCENARIOS`, `SHORT_NAMES` | The three water-availability scenarios |
| `presets` | Central values and sensitivities: `CO2_PRICES` (ETS1), `CO2_PRICES_ETS2` (household gas & petrol cars, from 2028), `GAS_PRICES`, `ELY_CAPEX`, … |
| `make_scenario()` | Defines one run = scenario + any sensitivities and data settings |
| `electrolyser_reference()` | Electrolyser capacity per technology and vintage of a solved S1 run |
| `apply_scenario_inputs()` | Modifies input data (incl. capacity constraints) before the network is built |
| `apply_network_settings()` | Sets prices per period, hydrogen demand, and demand path |
| `make_extra_functionality()` | CO₂-storage cap, build-rate caps, battery cap |
| `store_shadow_prices()` | Saves shadow prices on the network |

---

## Notes

- Water **use** is reported as an output after solving: `h2_results.water_use`
- Input data sources and cited values are documented in `presets`


----------------

# Final course model with hydrogen (published H2 copy)

This folder contains the final course model for the Netherlands with the
hydrogen extension. Hydrogen is represented as a fixed industrial demand of
1.3 Mt per year, served by grey hydrogen, blue hydrogen, and grid electrolysis.
The 2020 reformers are represented as existing capacity.

The scenarios limit electrolyser capacity to represent water availability:

| Scenario | Meaning |
|---|---|
| S1 Base | No electrolyser capacity limit |
| S2 Medium | Electrolyser capacity capped at 50% of the S1 reference |
| S3 Scarce | No new electrolyser capacity |

The model is based on the final course database, Dutch energy-system input data,
and the group's hydrogen assumptions. The input values and cited sources are
kept in `build_h2_database.py` and the model code.

## Implementation answers

### Topology changes

Yes. The hydrogen extension adds the `Hydrogen` bus, the fixed
`industrial_h2` demand, and the `SMR`, `SMR CCS`, `Electrolyser`, and
`SMR - existing` links. The model topology is defined when
`build_h2_database.py` creates `input_databases/h2_nl`; the optimisation
logic remains in `energy_model/model.py`.

### Data obtained and changed

`input_databases/default` is copied and extended to create
`input_databases/h2_nl`. The default course database remains untouched.
Hydrogen demand, Dutch technology costs, efficiencies, lifetimes, and
emissions are added by `build_h2_database.py`. This published copy is the
without-additions H2 model: it does not include dedicated pure-green or pink
hydrogen routes. Hydrogen storage is retained only where explicitly enabled by
the published scenario registry.

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
settings applied in memory through `make_scenario()` and `model.py`.

### Key model outputs and results

Saved networks in `results/runs/*.nc` are the primary results. The result and
plot modules derive hydrogen route balances, capacity, full-load hours, costs,
CO2, gas use, electricity mix, water use, storage, and policy indicators.

### Staged plan and preliminary tests

Rebuild the H2 database, verify the hydrogen topology, solve S1/S2/S3, and
check the S2 reference and S3 capacity limit before running sensitivities.
Then aggregate the saved networks with `figures/plots/h2_results.py` and
generate run-based figures. The known infeasible case `S2_mandate` should not
be treated as a missing database or modelling error.

## Quick start

Use the configured course environment with Gurobi:

```bash
python build_h2_database.py
python run_batch.py S1 S2 S3
```

`run_batch.py` always uses Gurobi. The S1 run is solved first when S2 needs its
electrolyser reference. Results are written to `results/runs/`, while each run
also gets a reproducible snapshot under `input_databases/scenarios/<name>/`.

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

## Green levers and storage

The optional experiments retained in this package are:

- `desal`: electrolysis using alternative water outside the capacity limit;
- `h2_production_subsidy`: an operating subsidy per kilogram of hydrogen;
- `infrastructure_subsidy`: a 20% or 40% capital subsidy for electrolyser infrastructure;
- `green_mandate`: a minimum electrolytic-hydrogen share;
- `h2_storage`: hydrogen storage in salt caverns;
- `h2_storage_cost_factor`: storage-cost sensitivity.

Storage is controlled by the `STORAGE` switch near the top of
`energy_model/model.py`. Individual runs can override it with
`h2_storage=True` or `h2_storage=False`. The selected runs are defined in
`run_batch.py`.

## Main files

- `energy_model/model.py`: course model and H₂ integration.
- `energy_model/model.py`: scenarios, green levers, storage, prices, and constraints.
- `figures/plots/h2_results.py`: result calculations.
- `build_h2_database.py`: builds `input_databases/h2_nl`.
- `figures/plots/`: analysis and plotting modules used by the interface.
- `results/plots/`: generated slide, report, and system plots.
- `run_batch.py`: Gurobi batch runner.
- `interface.ipynb`: interactive model interface.
- `results/solver_run.log`: example solver log.
