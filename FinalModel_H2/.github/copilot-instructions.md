# Copilot context: green hydrogen and water scarcity (PyPSA, the Netherlands)

UvA course *Modelling for Transitions*, group policy scenario **"Green hydrogen production and water availability in the Netherlands"** by Māra Učelniece, Agaath de Vries and Josefina Rodríguez Zuloaga. The code is the **final course model** (PyPSA, the Netherlands, 2020–2050) extended with hydrogen. This file summarises the decisions taken so far (the meeting with Francesco, the group's choices, our working sessions) and how the code works, so suggestions stay consistent with them. The full notes are in `docs/model_notes.md`.

**This folder is the package without additions** (`ADDITIONS = False` in `energy_model/package.py`): 30 runs (31 defined; `S2_mandate` has no solution). Its numbers are the left column of the key results.

## The study in brief

- **Hydrogen is a fixed demand:**
  - load `industrial_h2` on bus `Hydrogen`: 1.3 Mt/yr = 43.3 TWh/yr (33.33 MWh/t), flat, in every period and scenario;
  - it is feedstock for refineries and ammonia (Elzenga et al., 2025).
- **Three supply routes**, links that feed the demand directly:
  - SMR (grey), plus `SMR - existing` for the 2020 stock;
  - SMR CCS (blue): 90% captured; CO₂ storage capped at 10 / 22 / 25 Mt/yr in 2030 / 2040 / 2050, shared with industry;
  - the grid `Electrolyser` (green).
- **Water itself is not modelled.** The scenarios limit the electrolyser capacity that may be built, per vintage:
  - S1 **Base**: no limit (cost-optimal). Without storage it builds exactly the flat hourly demand, 4,946 MW of H₂ output (7.1 GW_el), all in the 2050 vintage.
  - S2 **Medium**: ≤ 50% of what Base *without additions* builds, i.e. 2,473 MW of H₂ output (3.5 GW_el) for all electrolysers together.
  - S3 **Scarce**: no electrolysers.
  - The 50% and 0% come from the Dutch *verdringingsreeks* (report Figure 2), not from the model.
- **Main result:**
  - Water scarcity does not stop the hydrogen supply; blue hydrogen fills the gap.
  - Over 2020–2059 it costs €2.4–5.1 bn, 49–94 Mt CO₂ and 218–453 TWh of extra gas imports. These are the numbers without additions; with additions: €3.7–6.4 bn, 110–155 Mt and 433–668 TWh.
- **Policy result:**
  - Water from outside the verdringingsreeks (desalinated seawater, €0.03/kg) lifts the limit and pays.
  - A subsidy per kg under a water limit buys running hours, not CO₂.
  - A 60% mandate is infeasible under a water limit without that alternative water.

## Decisions in the code (keep them unless the group changes them)

| Decision | Where | Source |
|---|---|---|
| Hydrogen is a demand, not a secondary resource. SMR, SMR CCS and the electrolyser are links in the technology table | `build_h2_database.py` | Francesco, 14 Oct: "What you need is just a demand for hydrogen" |
| Water is a `max` row per electrolyser and vintage in the course's capacity constraints (`get_cap_constraints`) | `hydrogen.apply_scenario_inputs` | Francesco, 14 Oct: "Exogenously limit this capacity to mimic … less water" |
| Base = no water scarcity (100%): S1 Base, S2 Medium (50%), S3 Scarce (0%) | `hydrogen.SCENARIOS` | Group, 15 Oct. The report of 5 Oct still has S1 and S2 swapped (S1 = 50%); see `docs/report_tables_check.md` |
| H₂ storage, pure green and pink are options ("additions"), on in a second package | `energy_model/package.py` | Group, 15 Oct; two packages since 16 Oct |
| The limit is fixed **in MW** by Base *without additions* (`S1`, or `S1_noadd` with additions), for every run | `run_batch.ref()` | Taking "50% of Base with storage" would give Medium 3,969 MW instead of 2,473: more water, not a storage effect. *Open: group to confirm* |
| One joint limit for all electrolysers (`electrolyser_limit_scope='total'`) | `make_extra_functionality` | The same water, whatever the power source |
| The 1.3 Mt is feedstock, on top of the course demands (`h2_demand_use='feedstock'`). `'htp_fuel'` instead subtracts its heat from the industrial HTP demand | `apply_network_settings` | Francesco, 14 Oct: "Make sure you have an answer" to what it is used for. *Open: group to confirm* |
| Economic system cost = objective + subsidies added back (they are transfers) | `h2_results.economic_cost`, `presentation._econ_cost` | Subsidies are not a cost to society |
| Discounting as in the course: years at `RS` = 1%, investments as annuities at `RT` = 7% | `run_batch.py` | Course model |
| HiGHS, 15-hour steps, one thread per run | `run_batch.py` | No Gurobi licence needed; HiGHS reproduces the course objective exactly |
| Fuel and CO₂ prices of the *period*, not of the build year. ETS2 price for household gas boilers and petrol cars | `hydrogen.set_period_prices`, `ets2_price` | Otherwise a 2030 SMR would pay the 2030 CO₂ price until 2060 |
| Storage is cyclic within each period | `apply_network_settings` | PyPSA 1.3 defaults to one cycle over the whole horizon |
| All money in 2024 euros (HICP-converted) | `hydrogen.py`, `build_h2_database.py` | Research report (`docs/Dutch hydrogen model input data.md`) |

## Two packages, one flag

`energy_model/package.py` sets `ADDITIONS = False` (package **without additions**) or `True` (package **with additions**). Code, data and water limits are otherwise identical.
- **With additions**, every run has:
  - H₂ storage in salt caverns, ≤ 0.22 / 0.9 / 5 TWh;
  - the pure green route: dedicated wind + solar → electrolyser, no grid;
  - pink hydrogen: dedicated nuclear → electrolyser.

  Extra runs show what they do: `S*_noadd`, `S*_storage`, `S*_green`, `S*_pink`, `S1/S2_storage_x3`, `S1_green_only`.
- **Without additions**, those components are not in the database, and switching one on raises `ValueError`.
- Never flip the flag inside a package folder: its database (`input_databases/h2_nl`) and runs belong to that package. If you must, rebuild the database and rerun everything.
- Check: S1, S2 and S3 without additions have exactly the same objective as `S1_noadd`, `S2_noadd` and `S3_noadd` with additions.

## Code map

| File | Role |
|---|---|
| `energy_model/model.py` | The course `model_run()`. Every change is marked `# [H2]`; with `scenario=None` it is the course model. |
| `energy_model/hydrogen.py` | The scenario layer: technology names; presets (CO₂, gas, CAPEX, storage and build caps); `SCENARIOS`; `DEFAULTS` (every setting, commented); `make_scenario()`; `electrolyser_reference()`; `apply_scenario_inputs()` (input data, before the network is built); `apply_network_settings()` (the built network); `make_extra_functionality()` (extra constraints); `store_shadow_prices()`. |
| `energy_model/package.py` | The `ADDITIONS` flag and the package name. |
| `build_h2_database.py` | Copies `input_databases/default` (never edited) to `input_databases/h2_nl` and adds: the H₂ demand, the routes, the `Electrolyser - seawater` lever, the additions (with the flag) and the Dutch data. |
| `run_batch.py` | `RUNS = {name: (scenario, settings)}`, `INFEASIBLE`, `ref()`, `_reference()`, `run()`. |
| `energy_model/h2_results.py` | Reads a run: `h2_balance`, `summary`, `cumulative_co2`, `gas_use`, `water_use`, `economic_cost`, `policy_table`. |
| `energy_model/presentation.py` | All result figures P00–P16 in two styles (`FIGURES` registry; `results/figures/presentation` and `results/figures/apa`), plus `lever_table()`, `scarcity_numbers()` and `key_numbers()`. |
| `energy_model/results_summary.py` | Writes `docs/results_summary.md` from the runs of this package. |
| `energy_model/h2_plots.py`, `h2_sankey.py` | Hydrogen plots and Sankey diagrams. |
| `energy_model/system_plots.py` | System-wide plots (energy balances, electricity supply, capacity, CO₂ by sector, whole-system Sankey) and the course's quick plots, unchanged. |
| `energy_model/ensemble.py`, `ensemble_analysis.py` | Exploratory ensemble (EMA Workbench, XLRM). Updated to base = 100% but not rerun; a rerun takes 1–2 hours. |
| `energy_model/preprocessing.py` | Course preprocessing of the database (costs ×1e3: per kW → per MW). |
| `figures_document/*.py` | Report Figures 1–3, and the course overview slide redrawn with hydrogen. Plain matplotlib, APA by default; `--bw`, and `--slide` for Figures 1–2. They read the package flag as text. |
| `interface.ipynb` | The course notebook, extended. It only loads runs; `RUN_COURSE_CHECK`, `REBUILD` and `REDRAW` switch on the slow parts. |
| `docs/` | `model_notes.md` (full notes; 5.11 compares the packages; 6 suggests report text), `results_summary.md`, `report_tables_check.md`, `Dutch hydrogen model input data.md` (the research report). |

### What one run does (`python run_batch.py S2`)

1. `RUNS['S2'] = ('S2', ref())`, where `ref()` = `{'electrolyser_reference': 'from:S1'}` (`'from:S1_noadd'` with additions).
2. `_reference()` loads that run (solving it first if needed) and replaces the string by `electrolyser_reference(n)`. That is `{technology: {vintage: MW of H₂ output}}`, here `{'Electrolyser': {'2030': 0, '2040': 0, '2050': 4946}}`.
3. `make_scenario('S2', …)` = `DEFAULTS` + `SCENARIOS['S2']` (`electrolyser_cap_share=0.5`) + the run's settings. Unknown keys raise `KeyError`.
4. `model_run()` calls `hydrogen.apply_scenario_inputs()`, which:
   - disables the technologies of options that are off;
   - writes a `max` row per electrolyser and vintage, 0.5 × the reference: 0 / 0 / 2,473 MW for 2030 / 2040 / 2050. These are kept as `_electrolyser_caps_mw_h2` in `n.meta['scenario']`;
   - applies the costs: electrolyser CAPEX path and subsidy (2a); CO₂ price (2b); H₂ storage cost (2c); gas and CO₂-storage prices; batteries (3); and the desal cost and the per-kg subsidy as VOM.
5. The course code builds the network. The `[H2]` changes here: stores, own carriers, no copies before a technology's start year, battery lifetime and hours.
6. `apply_network_settings()` sets: prices per period (and ETS2), storage cyclic per period, the output share of the oversized plant, and the demand use.
7. `n.optimize(extra_functionality=make_extra_functionality(scen))` adds these constraints:
   - the CO₂-storage cap;
   - build limits per period, for 2030 / 2040 / 2050: electrolysers 3 / 20 / 40 GW_el, offshore wind 21 / 40 / 70 GW, nuclear 0.5 / 2.7 / 7 GW_e;
   - the H₂-storage cap;
   - the green mandate;
   - the joint water limit, when more than one electrolyser can be built;
   - the hourly water-output cap (`S2_oversized` with additions);
   - the battery power cap (3b).
8. `store_shadow_prices()` puts two values on `n.meta`: 1 kW more electrolyser (€/kW_H2, present value) and CO₂ storage. The network is saved to `results/runs/S2.nc`.

### Scenario settings used by the runs (all documented in `DEFAULTS`)

- **Water:**
  - `electrolyser_cap_share`, `electrolyser_reference`, `electrolyser_limit_scope`, `cap_from`;
  - `electrolyser_limit_on='output'` with `electrolyser_plant_reference`: the over-dimensioned plant (`S2_oversized`).
- **Additions:** `h2_storage`, `pure_green`, `pink`; `grid_electrolysis=False` (`S1_green_only`).
- **Variations:**
  - (2a) `electrolyser_subsidy` 0.2 / 0.4 (20% was Francesco's example); `electrolyser_capex='low'`;
  - (2b) `co2_price` low / central / high: 170 / 250 / 500 €/t in 2050;
  - (2c) `h2_storage_cost_factor=3`;
  - (3a, 3c) `battery_cost_factor=0.5`, `battery_max_hours=8`;
  - `S3_10pct`: `electrolyser_cap_share=0.1` (Francesco: "zero or ten percent");
  - `h2_demand_use='htp_fuel'`.
- **Green levers (16 Oct):**
  - `desal=True`: `desal_cost_eur_per_kg` 0.03, or ×10 = 0.30;
  - `h2_production_subsidy`: €1 or €2/kg;
  - `green_mandate={2040: 0.6, 2050: 0.6}` (RED III-type).

## Commands

```bash
pip install pypsa==1.3.0 highspy openpyxl matplotlib     # gurobipy if you use Gurobi
python build_h2_database.py                # only after editing the data
python run_batch.py S1 S2 S3               # named runs; no names = every run (30, or 45 with additions)
SOLVER=gurobi python run_batch.py S1       # the course solver
python -m energy_model.presentation        # all figures, slide + APA; add keys (e.g. levers) and/or --slide / --apa
python -m energy_model.results_summary     # docs/results_summary.md
```
- A run takes about 4–5 minutes (the logged runs took 0.5–16 minutes). Several can run side by side, one thread each.
- Runs already on disk are skipped: delete a `.nc` to solve it again.
- `S2_mandate` runs only when named, and it has no solution.

## Rules for changes

- **Model code:**
  - With `scenario=None`, `model_run()` must stay the course model: the course check (`RUN_COURSE_CHECK` in the notebook) must still give 2.1292789279e12.
  - Mark changes to course files `# [H2]`.
  - New options go into `DEFAULTS` with a comment, off by default.
  - New runs go into `RUNS`, with `ref()` wherever a Medium-type water limit applies.
  - Do not edit `input_databases/default`: change `build_h2_database.py` and rebuild `h2_nl`.
  - Do not model water explicitly, and do not change the 1.3 Mt in the scenarios. A different demand is a variation (`h2_demand_mt`).
- **Units:**
  - CAPEX and FOM are per kW of **output**, VOM per kWh of **input** (course convention). Inside `apply_scenario_inputs`, `techs_d` is already per MW and per MWh.
  - Water limits and electrolyser references are in **MW of H₂ output**. Reported capacities are in GW of **electricity input** (`GW_el`).
  - Water use is an output only: 22 / 10 / 28 L/kg for electrolysis / SMR / SMR CCS.
- **Figures:**
  - Two styles:
    - slide: the template's content box, 11.5 × 4.76 in;
    - APA: 6.5 in wide, all text ≥ 8 pt, no titles or notes in the image (they go in the report caption).
  - Colours:
    - scenarios: Base `#6250d6`, Medium `#eda100`, Scarce `#e34948`;
    - routes: green `#1baf7a`, pure green `#008300`, pink `#e87ba4`, blue `#2a78d6`, grey `#75746f`.
  - Text in figures, tables and slide notes is **computed from the runs**. Never hard-code a result: the two packages have different numbers.
- **Writing:**
  - Plain English, short sentences, numbers with units, APA citations.
  - In the group report, change groupmates' text only with tracked changes (or flag it). Keep the original key points and citations.
  - Names: Base / Medium / Scarce in figures and tables; S1 / S2 / S3 in the report.

## Key results (sums over 2020–2059 unless a year is given)

| | Without additions | With additions |
|---|---|---|
| Electrolysis share 2050, Base / Medium / Scarce | 54 / 25 / 0% | 84 / 25 / 0% |
| Base electrolysers 2050 | 7.1 GW_el | 11.3 GW_el + 0.93 TWh H₂ storage |
| System cost, Base / Medium / Scarce (bn €, discounted) | 1,059.3 / 1,061.7 / 1,064.4 | 1,058.0 / 1,061.7 / 1,064.4 |
| Water scarcity, Medium / Scarce: extra cost | +2.4 / +5.1 bn € | +3.7 / +6.4 bn € |
| … extra CO₂ | +49 / +94 Mt | +110 / +155 Mt |
| … extra gas imports | +218 / +453 TWh | +433 / +668 TWh |
| … per kg of green H₂ not made | €0.92 / €1.04 | €0.69 / €0.83 |
| Value of 1 kW more electrolyser in Medium | €1,031/kW_H2 | €1,031/kW_H2 |
| Desalinated water, Medium / Scarce | −2.3 / −5.0 bn €; 53% electrolysis | −3.6 / −6.2 bn €; 84% electrolysis |
| Subsidy €1–2/kg, Medium | 41–48% electrolysis, CO₂ ≈ 0 | The same |
| 60% mandate | Base +10.7 bn €, −32.5 Mt; Medium infeasible | Base +4.0 bn €, −47 Mt; Medium infeasible |
| Over-dimensioned plant (Base plant, Medium water) | +2.9 bn € | +6.4 bn € |
| Water scarcity at the high CO₂ price, Medium / Scarce | +11.1 / +22.6 bn € | +21.4 / +32.9 bn € |

- **Up to 2040 the scenarios are the same.** In 2030 the existing reformers make all the hydrogen (grey); in 2040 blue takes over. The difference is in 2050.
- **Limiting electrolysis does not save water.** Blue hydrogen uses more water per kg, mostly for cooling. Water for H₂ in 2050 rises from 32 Mm³ in Base to 36 Mm³ in Scarce (with additions: from 30 to 36).
- **The CO₂ price moves green hydrogen; cheaper electrolysers hardly do.** Base electrolysis at the low / central / high CO₂ price is 31 / 54 / 73% (with additions 31 / 84 / 100%).
- **Medium and Scarce are identical in both packages.** Under the water limit, storage is not built and pure green and pink are never chosen. Only Base differs: storage lets its electrolysers exceed the flat hourly demand.
- **Checks:** the merged code on the course database gives the course objective exactly (2.1292789279e12, HiGHS), and `S2_mandate` has no solution, as expected.

## History of the work (summary of our chats)

- **5 Oct:** report draft, with the old scenario numbering (S1 = 50%).
- **7 Oct:** guest lecture by van der Zwaan with the Broadleaf colour scheme. It is the source of "pink"; in that scheme our grid electrolysis is "yellow".
- **12 Oct:** Francesco's annotations.
- **14 Oct:** meeting with Francesco on the set-up above: H₂ as a demand, three links, the capacity limit, variations within the scenarios, the outputs to show, the over-dimensioned plant, and what the hydrogen is used for.
- **15 Oct:** group decisions: base = 100%, with S1 and S2 renumbered; storage, pure green and pink as options.
- **16 Oct:**
  - figures in colour (slide + APA);
  - green levers;
  - two packages;
  - two decks.
- **17 Oct:**
  - a run-through doc for the group (talking through the code);
  - the remaining slides (context, difficulties, results, policy, limitations, improvements, follow-up work, credit statement);
  - cover images;
  - this file.

## Status (17 Oct) and open decisions

- **Done:**
  - both packages (runs, figures, notebook, notes);
  - two decks, `Presentation_without_additions` and `Presentation_with_additions` (all main slides, back-up slides, speaker notes, cover);
  - report Figures 1–3 in colour.
- **Open decisions for the group** (`docs/model_notes.md`, "Decisions for the group"):
  1. renumbering S1/S2 in the report text and tables (`docs/report_tables_check.md`);
  2. what the 1.3 Mt is used for: feedstock (now) or fuel for heat;
  3. Scarce at 0% or 10%;
  4. which package to present;
  5. the water limit with the additions: the same MW as now, or 50% of Base with additions;
  6. whether the green levers go in the report or only in the back-up slides.
- **Deadline:** the presentation PDF goes on Canvas before **Monday 19 October 2026, 10:59**.
  - The talk is 10 minutes, then 10 minutes of Q&A. Agaath does the implementation part.
  - Credit statement items: model development, analysis, visualization, presentation design, reviewing & editing, presenting.
- **The decks and cover art were built outside this repository** (python-pptx on the group template `Presentation2.pptx`, with numbers taken from each package's runs). Edit the decks in PowerPoint, not through this code.
