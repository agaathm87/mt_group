# Results of the package without additions

*Written by `python -m energy_model.results_summary` from the 30 runs in `results/runs/` (16 October 2026). Package: without additions: SMR, SMR + CCS and the grid electrolyser. System costs are discounted over 2020-2059 (the model objective, with subsidies added back because they are transfers); CO₂ and gas are summed over 2020-2059; "vs central" = against the central run of the same scenario.*

## The three scenarios

|  | Base | Medium | Scarce |
|---|---|---|---|
| System cost 2020-2059 (bn €, discounted) | 1,059.3 | 1,061.7 | 1,064.4 |
| Electrolysis share 2050 (%) | 53.6 | 25.0 | 0.0 |
| Electrolysers 2050 (GW_el) | 7.1 | 3.5 | 0.0 |
| Full-load hours 2050 | 4,691.6 | 4,383.2 | 0.0 |
| H2 storage 2050 (TWh) | 0.0 | 0.0 | 0.0 |
| Gas for H2 2050 (TWh) | 29.2 | 47.1 | 62.8 |
| Gas imports 2020-2059 (TWh) | 11,047.2 | 11,265.5 | 11,500.3 |
| CO2 2020-2059 (Mt) | 1,778.1 | 1,826.6 | 1,872.3 |
| CO2 2050 (Mt/yr) | 4.7 | 9.0 | 13.2 |
| Water for H2 2050 (Mm3) | 32.2 | 34.4 | 36.4 |
| Value of 1 kW more electrolyser (€/kW_H2) | – | 1,031.2 | – |

## What water scarcity costs (against Base)

|  | Medium | Scarce |
|---|---|---|
| Extra system cost (bn €) | 2.41 | 5.12 |
| Extra CO2 (Mt) | 48.52 | 94.21 |
| Extra gas imports (TWh) | 218.27 | 453.09 |
| Cost per kg of green H2 lost (€/kg) | 0.92 | 1.04 |

## Variations within the scenarios

| variation | scenario | Electrolysis share 2050 (%) | Electrolysers 2050 (GW_el) | System cost vs central (bn €) | CO2 vs central (Mt) |
|---|---|---|---|---|---|
| central | Base | 53.6 | 7.1 | 0.0 | 0.0 |
| central | Medium | 25.0 | 3.5 | 0.0 | 0.0 |
| central | Scarce | 0.0 | 0.0 | 0.0 | 0.0 |
| subsidy 20% | Base | 53.6 | 7.1 | 0.0 | 0.0 |
| subsidy 20% | Medium | 25.0 | 3.5 | 0.0 | 0.0 |
| subsidy 40% | Base | 53.6 | 7.1 | 0.0 | 0.0 |
| subsidy 40% | Medium | 25.0 | 3.5 | 0.0 | 0.0 |
| low electrolyser CAPEX | Base | 53.6 | 7.1 | -2.9 | 0.0 |
| low electrolyser CAPEX | Medium | 25.0 | 3.5 | -1.5 | 0.0 |
| CO₂ price low | Base | 30.6 | 5.1 | -45.3 | 399.2 |
| CO₂ price low | Medium | 20.4 | 3.5 | -47.7 | 368.6 |
| CO₂ price low | Scarce | 0.0 | 0.0 | -50.1 | 363.2 |
| CO₂ price high | Base | 73.1 | 7.1 | 37.9 | -223.6 |
| CO₂ price high | Medium | 34.3 | 3.5 | 46.6 | -214.4 |
| CO₂ price high | Scarce | 0.0 | 0.0 | 55.4 | -199.5 |
| batteries half price | Medium | 26.5 | 3.5 | -4.8 | -68.0 |
| batteries 8 h | Medium | 25.0 | 3.5 | 0.0 | 0.0 |
| oversized plant | Medium | 25.0 | 7.1 | 2.9 | 0.0 |
| Scarce at 10% | Scarce | 4.6 | 0.7 | -0.6 | -10.4 |
| H₂ as high-temp. fuel | Base | 52.1 | 7.1 | -69.3 | -332.3 |

## Green levers within the water scenarios

| scenario | lever | Electrolysis share 2050 (%) | Electrolysers 2050 (GW_el) | of which on desalinated water (GW_el) | Full-load hours 2050 | System cost vs central (bn €) | CO2 vs central (Mt) | Gas imports vs central (TWh) | Production subsidy paid (bn €, present value) | Fresh water for H2 2050 (Mm3) |
|---|---|---|---|---|---|---|---|---|---|---|
| Base | none (central) | 53.6 | 7.1 | 0.0 | 4,691.6 | 0.0 | 0.0 | 0.0 | 0.0 | 32.2 |
| Base | production subsidy €1/kg | 84.6 | 7.1 | 0.0 | 7,409.9 | 1.7 | 2.9 | -12.5 | 7.8 | 29.8 |
| Base | production subsidy €2/kg | 95.8 | 7.6 | 0.0 | 8,395.7 | 17.6 | -10.9 | -529.0 | 35.4 | 28.0 |
| Base | mandate: 60% electrolysis from 2040 | 63.7 | 7.4 | 0.0 | 5,576.4 | 10.7 | -32.5 | -347.9 | 0.0 | 28.4 |
| Medium | none (central) | 25.0 | 3.5 | 0.0 | 4,383.2 | 0.0 | 0.0 | 0.0 | 0.0 | 34.4 |
| Medium | desalinated water (+€0.03/kg) | 53.4 | 7.1 | 3.5 | 4,675.7 | -2.3 | -47.3 | -216.1 | 0.0 | 25.4 |
| Medium | production subsidy €1/kg | 40.8 | 3.5 | 0.0 | 7,147.0 | 0.8 | -0.4 | -4.3 | 3.8 | 33.2 |
| Medium | production subsidy €2/kg | 47.6 | 3.5 | 0.0 | 8,335.0 | 1.5 | -0.3 | -3.3 | 8.8 | 32.7 |
| Medium | mandate + desalinated water | 63.5 | 7.4 | 5.2 | 5,564.7 | 8.5 | -80.1 | -567.0 | 0.0 | 18.4 |
| Scarce | none (central) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 36.4 |
| Scarce | desalinated water (+€0.03/kg) | 53.4 | 7.1 | 7.1 | 4,675.7 | -5.0 | -92.7 | -450.8 | 0.0 | 17.0 |
| Scarce | desalinated water at 10x (+€0.30/kg) | 52.3 | 7.1 | 7.1 | 4,582.9 | -3.7 | -86.9 | -438.2 | 0.0 | 17.4 |
| Scarce | mandate + desalinated water | 63.2 | 7.4 | 7.4 | 5,533.6 | 5.9 | -125.2 | -799.5 | 0.0 | 10.4 |

The 60% mandate alone is infeasible in Medium (water allows electrolysis for at most 50% of the hydrogen) and in Scarce (no electrolysers).

