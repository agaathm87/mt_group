# Final course model with hydrogen

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

## Quick start

Use the configured course environment with Gurobi:

```bash
python build_h2_database.py
python run_batch.py S1 S2 S3
```

`run_batch.py` always uses Gurobi. The S1 run is solved first when S2 needs its
electrolyser reference. Results are written to `results/runs/`.

## Green levers and storage

The optional experiments retained in this package are:

- `desal`: electrolysis using alternative water outside the capacity limit;
- `h2_production_subsidy`: an operating subsidy per kilogram of hydrogen;
- `infrastructure_subsidy`: a 20% or 40% capital subsidy for electrolyser infrastructure;
- `green_mandate`: a minimum electrolytic-hydrogen share;
- `h2_storage`: hydrogen storage in salt caverns;
- `h2_storage_cost_factor`: storage-cost sensitivity.

Storage is controlled by the `STORAGE` switch near the top of
`energy_model/hydrogen.py`. Individual runs can override it with
`h2_storage=True` or `h2_storage=False`. The selected runs are defined in
`run_batch.py`.

## Main files

- `energy_model/model.py`: course model and H₂ integration.
- `energy_model/hydrogen.py`: scenarios, green levers, storage, prices, and constraints.
- `energy_model/h2_results.py`: result calculations.
- `build_h2_database.py`: builds `input_databases/h2_nl`.
- `run_batch.py`: Gurobi batch runner.
- `interface.ipynb`: interactive model interface.
- `results/solver_run.log`: example solver log.
