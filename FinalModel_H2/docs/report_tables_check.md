# Report tables: what the 15 October set-up changes

This checks Tables 1–3 of the report (version of 5 October, the annotated PDF) against the model as it runs now. The proposed text is for the group to paste in with tracked changes. The original key points and citations are kept.

## 1. The scenario numbers swap (affects all three tables and the text)

With the base at 100% (group, 15 October), the numbering is now:

| Now | Water | Electrolyser capacity | Was |
|---|---|---|---|
| **S1 Base** | no water scarcity: desalinated seawater, outside the verdringingsreeks | the cost-optimal capacity (no limit) | S2 |
| **S2 Medium** | medium: electrolysis is process water (category 3), partly curtailed | at most 50% of S1 | S1 (base) |
| **S3 Scarce** | high: electrolysis is ordinary industry (category 4), curtailed first | none | S3 |

Every "S1" in the old text means today's S2, and every "S2" means today's S1. These are the places in the tables:

- **Table 1**, row "H₂ resource limit": "100% (S2), 50% (S1, base) … in S1, electrolysis is treated as process water".
- **Table 2**, row 1: "50% (S1, base…); 100% (S2…)"; "compared with S2?"; "The limit binds in S1…".
- **Table 3**, every cell under "Link to the scenarios": the S1 and S2 narratives swap. Political, Economic, Social, Technological, Legal and Environmental all name S1 and S2.
- **Table 3**, Environmental, "Treatment in the model": "50% (S1, base), 100% (S2), 0% (S3)".

The same swap applies to the notes under Figures 1–3 and to the text. Examples are "Post-processing compares S1 and S3 with S2" (now "S2 and S3 with S1") and the order and headings of the scenario narratives (the base narrative is now no water scarcity).

## 2. Table 1: Model Additions Needed to Run the Scenarios

| Model component | Proposed implementation text | Used for |
|---|---|---|
| H₂ production routes | Three end-use technologies feed the hydrogen demand directly. Green: electrolysis from grid electricity; this is a simplification, because grid electricity is not fully renewable. Grey: steam methane reforming from natural gas (~9 kg CO₂/kg H₂; Elzenga et al., 2025), including the reformers that exist in 2020. Blue: steam methane reforming with carbon capture and storage; the captured CO₂ uses the capped CO₂ storage (10 / 22 / 25 Mt/yr in 2030 / 2040 / 2050). Options, off by default: pure green (dedicated offshore wind and solar → electrolysis, no grid) and pink (dedicated nuclear → electrolysis; colour scheme of Broadleaf, shown by van der Zwaan, 2026). | All scenarios (options as variations) |
| H₂ demand | Exogenous: dedicated industrial H₂ demand for refineries and ammonia (1.3 Mt/yr ≈ 43 TWh; Elzenga et al., 2025), the same in every period and scenario and flat over the hours; it comes on top of the course demands (feedstock). Variation: the hydrogen is used as fuel for high-temperature heat instead and replaces part of that demand. | Fixed input (all scenarios) |
| Water limit (scenario parameter) | Limit on electrolyser capacity, written in the capacity constraints of the course model per period: a share of the cost-optimal capacity of S1. Shares: 100% (S1, base), 50% (S2) and 0% (S3). Grey or blue hydrogen meets the rest. It represents competition for water through the verdringingsreeks: in S2, electrolysis is treated as process water (category 3) and partly curtailed; in S3, as ordinary industry (category 4) and curtailed first. Water itself is not modelled. | Scenario parameter (1) |
| Sensitivity parameters | Electrolyser investment cost: a subsidy of 20% or 40% (up to 80% under OWE; RVO, n.d.) and the low CAPEX path (2a). CO₂ price paths low / central / high: 170 / 250 / 500 €/t in 2050 (2b). Hydrogen storage in salt caverns (option) and three times its cost (2c). Batteries at half the cost and with 8 instead of 4 hours (3a–c). | Within each scenario |
| *Optional:* Green levers | Three policy levers, off by default. An electrolyser on desalinated seawater, outside the water limit, at €0.01–0.03 per kg extra (€0.03 used; ten times that as a check). A production subsidy of €1 or €2 per kg of electrolytic hydrogen, a transfer that is left out of the system cost. A minimum share of 60% electrolytic hydrogen from 2040, after the RED III target for industry in 2035. | Within S2 and S3 (subsidy and mandate also in S1) |

**What changed and why:**

- The endogenous hydrogen technology for high-temperature heat ("an H₂-based technology for high-temperature industrial heat that competes with existing options") is no longer in the model. Hydrogen is only the fixed feedstock demand, as agreed on 14 October. The high-temperature use is a single variation.
- "Subtracted from existing industrial demand" no longer holds. In the default the demand comes on top of the course demands; only the high-temperature variation replaces part of a demand.
- "Annual limit on hydrogen from electrolysis as a share of hydrogen demand (practicals P05–P06)" is replaced by the limit on electrolyser capacity, as agreed with Francesco.
- "Infrastructure cost; storage, if time allows" is replaced by the values that were actually run.

## 3. Table 2: Parameters, Values, Outputs and Plots per Parameter Group

Only the cells that change are shown. The hypotheses (column "Expected signal") can stay as written, apart from the scenario numbers.

| No. | Cell | Proposed text |
|---|---|---|
| 1 | Model representation | Limit on electrolyser capacity per period (capacity constraints) as a share of the cost-optimal capacity of S1; competition for water enters through the verdringingsreeks; water itself and water use by other technologies are not modelled |
| 1 | Values explored | 100% (S1, base: desalination, outside the verdringingsreeks); 50% (S2: category 3, partly curtailed); 0% (S3: category 4, curtailed first) |
| 1 | Key outputs | H₂ production by route, electrolyser capacity and run hours, shadow price of the capacity limit, system cost, gas use, CO₂ |
| 1 | Question tested | How much green hydrogen is lost when water limits electrolysis, and what does that cost compared with S1? |
| 1 | Expected signal | The limit binds in S2 wherever S1 builds electrolysers; grey or blue hydrogen fills the gap, all of it in S3; highest system cost and CO₂ emissions in S3 |
| 2a | Values explored | None, 20% and 40% subsidy on the investment (up to 80% under OWE; RVO, n.d.), and the low CAPEX path (500 €/kW in 2050 instead of 1,000) |
| 2b | Values explored | Low, central and high: 75 / 110 / 140 €/t in 2030 and 170 / 250 / 500 €/t in 2050 (EU ETS1) |
| 2c | Model representation | Hydrogen storage in salt caverns (option): capital cost of the storage, up to 0.22 / 0.9 / 5 TWh in 2030 / 2040 / 2050; the network is not modelled |
| 2c | Values explored | With and without storage; base cost and three times the cost |
| 3a | Parameter, values | "(optional)" and "if time allows" can go. Values: base cost and half the cost (in S2) |
| 3b | Model representation / values | The battery capacity is built by the model; more capacity comes from the lower cost of 3a. Key outputs and plot unchanged |
| 3c | Values explored | 4 hours (base) and 8 hours (in S2) |
| new | Options | H₂ storage, pure green route (dedicated wind and solar) and pink hydrogen (dedicated nuclear), off by default, each run in all three scenarios. Key outputs: route mix and system cost. Plot: heat table of options × scenarios |
| new, optional | Green levers | Desalinated water (outside the water limit), production subsidy (€1–2/kg), mandate (60% from 2040). Question tested: which green policy still works when water limits electrolysis? Key outputs: electrolysis share, full-load hours, system cost, CO₂, subsidy paid, feasibility. Plot: heat table of levers × scenarios (P16) and cost against CO₂ (P16b) |

**Plots that exist now** (results/figures/presentation; the code is in energy_model/presentation.py):

| Row | Plot |
|---|---|
| 1 | P01 (stacked bars), P02 (Sankeys), P03 (cost of the limit). The shadow price is in the notes: 1,031 €/kW of H₂ output in 2050 (present value) for S2. |
| 2a | P05 |
| 2b | P06 |
| 2c | P08 |
| 3a–c | P09 and P09b |
| Options | P07 |
| Green levers | P16, P16b |

Every plot also exists in APA style for the report (results/figures/apa: 6.5 inches wide, text 8 pt or more, in colour).

## 4. Other points found while checking

- **Inconsistent numbering in the text.** The text under Table 1 says "costs (3a–c) and storage (4a–c) are sensitivities". Table 2 numbers them 2a–c (costs) and 3a–c (batteries).
- **"Export variants with local ones (Figure 2)".** The text mentions post-processing of export variants. These are not in the model; drop them or say they are narrative only.
- **"Interpretation" paragraph.** It lists "demand segments (industry, high-temperature heat)". The high-temperature segment is now only a variation (see Table 1).
