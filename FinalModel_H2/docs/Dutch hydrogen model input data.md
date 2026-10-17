# Evidence recalibrates the Dutch hydrogen model

The Dutch PyPSA hydrogen model can be built on verified data for 2020-2030 and on clearly sourced ranges for 2040-2050: EU ETS1 carbon prices rise from €24.6/t in 2020 and about €74/t in 2025 to a central **€110/t in 2030** (inside PBL's official KEV 2025 band of €75-138), about €180/t in 2040 and €250/t in 2050; TTF gas falls back to roughly **€24-26/MWh** once the 2026 Hormuz price spike passes; installed electrolysers cost **€1,800-3,400/kW today and about €1,650/kW in 2030**; CO2 transport and storage costs **€47-72/t**, with no Dutch storage capacity before 2027; salt-cavern hydrogen storage arrives around 2031; and domestic hydrogen demand stays at **about 1.1-1.3 Mt to 2030** before rising to 2.3-5.3 Mt by 2050. Checked against this evidence, three settings in the current model distort results more than the S1-S3 scenario parameter does: the course VOMs are read as €/kWh and are therefore **about 100 times too high** (a CCGT pays €200/MWh against a realistic €2-6), a cumulative 1,000 TWh gas "reserve" adds a scarcity cost to gas that is in reality imported at the TTF price, and prices locked to each plant's build year let a reformer built in 2030 pay the 2030 carbon price in 2050, making its hydrogen about €1.3/kg too cheap. The water evidence does not support S1 (50%) and S3 (0%) as outcomes of water scarcity: making all 1.3 Mt by electrolysis needs only 13-27 Mm³ of feed water a year, coastal sites have ample sea and brackish water, desalination adds €0.01-0.03/kg, and even the record 2026 drought restricted only category-4 users, the lowest priority in the national water ranking, so S1 and S3 are better presented as policy or social-licence stress tests, or redefined as the share of electrolysis allowed to use fresh water. Because most post-2030 values are syntheses rather than official forecasts, they belong in an exploratory ensemble of roughly 500-1,000 Latin-hypercube futures crossed with the S1-S3 and subsidy levers, screened with Morris or extra-trees, mined with PRIM for the conditions under which each option fails, and judged with regret and satisficing metrics. The energy-system literature suggests that the discount rate, demand, import availability and build limits will drive outcomes more than electrolyser CAPEX does.

## Carbon prices roughly double by 2040 while gas drifts back to the mid-twenties

The base year can be calibrated on verified price series. German EUA auction averages track EU-wide clearing prices to within cents. They were **€24.61/t in 2020**, €52.50 in 2021, €80.32 in 2022, €83.66 in 2023 and €65.00 in 2024 ([Umweltbundesamt, 2021](https://www.umweltbundesamt.de/themen/jahresbericht-zu-deutschen-versteigerungen-im-eu); [Solarserver, 2023](https://www.solarserver.de/2023/01/04/umweltbundesamt-meldet-rekordeinnahmen-aus-dem-emissionshandel/); [Umweltbundesamt, 2025](https://www.umweltbundesamt.de/presse/pressemitteilungen/einnahmen-aus-dem-emissionshandel-erneut-auf)). ICAP gives **€73.43 (auctions) and €74.35 (secondary market) for 2025** ([ICAP, 2026](https://icapcarbonaction.com/en/ets/eu-emissions-trading-system-eu-ets)).

TTF annual averages, computed from ACER's quarterly figures, were €14.6/MWh in 2019, **€9.7 in 2020**, €47.4 in 2021, €133 in 2022, €41.2 in 2023 and €34.5 in 2024 ([ACER, n.d.-a](https://aegis.acer.europa.eu/chest/dataitems/744/view)). The Commission's quarterly gas report gives matching values of €132, €41 and €35 for 2022-2024 ([European Commission, 2025](https://energy.ec.europa.eu/document/download/4aebee79-01e9-4a06-927e-8dd42fc4f9a8_en?filename=New+Quarterly+Report+on+European+gas+markets+Q4+2024.pdf&prefLang=de)). The IEA reports a rise of about 9% in 2025 ([IEA, 2026](https://www.iea.org/reports/electricity-2026/prices)), which implies roughly €37.5-38/MWh. That 2025 value is derived; no primary annual figure was found.

A 2020 calibration should therefore use about €25/t and about €10/MWh_HHV (about €10.7/MWh_LHV). The model's €20/MWh_th for 2020 is closer to a 2019-type year than to the COVID-depressed 2020 average, and that choice should be stated explicitly.

| Year | EUA, €/t nominal | TTF, €/MWh_HHV nominal | Status |
|---|---|---|---|
| 2019 | n/a | 14.6 | verified (ACER quarterly data, averaged) |
| 2020 | 24.6 | 9.7 | verified |
| 2021 | 52.5 | 47.4 | verified |
| 2022 | 80.3 | 132-133 | verified |
| 2023 | 83.7 | 41.2 | verified |
| 2024 | 65.0 | 34.5-35 | verified |
| 2025 | 73.4 (auction) / 74.4 (secondary) | ≈37.5-38 | EUA verified; TTF derived from IEA +9% |
| 2026 to date | Dec-26 future €83.87 on 6 Oct | €73-76 spot in Sept-Oct | single-day market quotes only |

The firmest forward anchor is PBL's KEV 2025 (2024 prices). It assumes **ETS1 at €111/t in 2030 (band €75-138)**, gas at 23 ct/m³ (band 15-46, ≈€23.5/MWh with a band of €15-47) and wholesale electricity at **€73/MWh (band €48-105)** ([PBL, 2025a](https://www.pbl.nl/system/files/document/2025-09/pbl-2025-klimaat-en-energieverkenning-2025-5692.pdf)). That electricity band is a direct sanity check on the model's own power prices.

No official Dutch ETS forecast exists beyond 2030. The WLO 2025 "efficient" CO2 prices of **€149-432/t in 2040 and €186-540/t in 2050 (2021 prices)** are target-consistent shadow prices, and CPB and PBL state explicitly that they are not ETS forecasts ([CPB & PBL, 2025a](https://www.wlo2025.nl/system/files/document/2025-07/cpb-pbl-2025-toekomstverkenning-wlo-efficiente-co2-prijzen-5916.pdf)). A December 2025 update revised them only slightly, to €142-415/t in 2040 and €187-547/t in 2050 ([CPB & PBL, 2025b](https://www.wlo2025.nl/system/files/document/2025-12/cpb-pbl-publicatie-wlo2025-update-efficiente-co2-prijzen-per-2026.pdf)). Market-oriented anchors sit lower. TYNDP 2024 uses €113, €147 and €168/t for 2030, 2040 and 2050 ([ENTSO-E & ENTSOG, 2025](https://2024.entsos-tyndp-scenarios.eu/wp-content/uploads/2025/01/TYNDP_2024_Scenarios_Methodology_Report_Final_Version_250128.pdf)). Enerdata's November 2025 path under the current ETS design was €75/t in 2030 and €130/t in 2040 (€2024), rising to €400-630/t by 2050 ([Enerdata, 2025](https://www.enerdata.net/publications/executive-briefing/carbon-price-projections-eu-ets.html)).

The policy regime changed in July 2026, when the Commission's ETS review proposal cut the linear reduction factor to **3.7% for 2031-2035 and 1.7% from 2036**, moved the zero-cap endpoint to about **2048** and admitted carbon removals and international credits ([ClearBlue Markets, 2026](https://www.clearbluemarkets.com/knowledge-base/the-eu-ets-review-proposal-july-2026-relief-for-industry-stability-for-the-market)). Enerdata now projects about **€100/t in 2030 and €180/t in 2040**, which is 15-30% below current law ([Enerdata, 2026](https://www.enerdata.net/publications/executive-briefing/eu-ets-reform-carbon-market-industrial-competitiveness.html)). A Nordic bank sees €180-270/t by 2040 ([Carbon Pulse, 2026a](https://carbon-pulse.com/548718/)), and Poland's KOBiZE models marginal costs of €470/t ([Carbon Pulse, 2026b](https://carbon-pulse.com/556730/)).

The defensible band is therefore **75/110/140 €/t in 2030, 130/180/270 in 2040 and 170/250/500 in 2050** (low/central/high, €2024), with stress values of 450 (2040) and 630 (2050). The low tail is real. Current prices rest on credible policy and farsighted market actors, and they "could plummet" if that credibility breaks ([Sitarz et al., 2024](https://doi.org/10.1038/s41560-024-01505-x)). Long-run uncertainty also widens as the cap approaches zero ([Pahle et al., 2025](https://doi.org/10.2139/ssrn.4373443)).

ETS2 and the Dutch industrial levy belong in the model only where they apply. ETS2 starts with surrender obligations for 2028. Its price-stability trigger of €45/t in 2020 prices equals about **€57/t in 2025 prices**. PBL's May 2026 study uses **€57/86/135 per tonne for 2030 (2025 prices)**; the middle and high paths grow 10% a year afterwards, while the low path stays at the trigger level ([PBL, 2026c](https://www.pbl.nl/downloads/pbl-2026-ets2-en-de-gevolgen-voor-huishoudens-5921pdf)). KEV 2025 itself uses the trigger, €57 (band 57-114), as its central value ([PBL, 2025a](https://www.pbl.nl/system/files/document/2025-09/pbl-2025-klimaat-en-energieverkenning-2025-5692.pdf)).

This matters for the current model. It contains residential gas boilers and petrol cars, and its `co2_price_scope='all'` puts the ETS1 price on household and transport emissions even before 2028. A separate ETS2 price, applied from 2028, is more faithful. Existing Dutch energy taxes already imply about €338/t on natural gas for households ([PBL, 2026c](https://www.pbl.nl/downloads/pbl-2026-ets2-en-de-gevolgen-voor-huishoudens-5921pdf)).

The CO2-heffing industrie (Dutch industrial CO2 levy) sets a statutory tariff of €30.48/t in 2021, rising linearly to **€125/t in 2030** plus indexation, minus the ETS price. In effect it is a minimum carbon price ([PBL, 2025c](https://acc.pbl.nl/downloads/pbl-2025-notitie-co2-heffing-industrie-toelichting-ten-behoeve-van-de-overlegtafel-co2-heffing-industrie-5955pdf)). On 22 July 2025 the cabinet announced it intends to suspend the levy through 2030 ([Taxlive, 2025](https://www.taxlive.nl/nl/documenten/vn-vandaag/kabinet-wil-co2-heffing-tijdelijk-opschorten/)). The central case should therefore add nothing on top of the ETS, with a single sensitivity at max(ETS, €125/t) in 2030.

Gas projections converge on the mid-twenties, but supply shocks are now part of the evidence. WLO 2025 puts wholesale gas at €8.2-8.7/GJ (≈€30-31/MWh, 2022 prices) for 2040-2050 ([PBL, 2025d](https://www.wlo2025.nl/system/files/document/2025-07/pbl-2025-toekomstverkenning-wlo-cahier-klimaat-en-energie-5455.pdf)). TYNDP 2024 uses €6.3, €5.7 and €5.0 per GJ, about €23, €21 and €18 per MWh ([ENTSO-E & ENTSOG, 2025](https://2024.entsos-tyndp-scenarios.eu/wp-content/uploads/2025/01/TYNDP_2024_Scenarios_Methodology_Report_Final_Version_250128.pdf)). The IEA's long-run European price is about USD 7/MBtu in its Announced Pledges Scenario and USD 4.5/MBtu in its Net Zero Emissions Scenario ([IEA, 2023](https://iea.blob.core.windows.net/assets/3e076ae9-9055-4af4-bba9-15ddaedcb703/Outlooksforgasmarketsandinvestment.pdf)), and Goldman Sachs takes a "normalised" view of about €19/MWh for 2030-2035 ([Business Today, 2026](https://www.businesstoday.in/amp/world/story/european-gas-prices-may-stay-elevated-this-winter-as-lng-disruptions-persist-goldman-sachs-557961-2026-09-26)). Against that, the closure of the Strait of Hormuz from March 2026 ([Trading Economics, 2026a](https://tradingeconomics.com/commodity/eu-natural-gas/news/529286)) pushed TTF to **€76.45/MWh on 7 October 2026, up 135% year on year** ([Trading Economics, 2026b](https://tradingeconomics.com/commodity/eu-natural-gas)). EUAs meanwhile stayed in the €80s ([Prestige Business Solutions, 2026](https://www.prestigebusiness.energy/marketreports/energy-market-update06-oct2026)). The two prices can clearly decouple, and Europe's gas risk takes the form of sharp, asymmetric price spikes rather than physical shortage ([Chyong et al., 2026](https://doi.org/10.1016/j.isci.2026.115866)).

The recommended TTF inputs are **15/24/47 (2030), 14/26/40 (2040) and 13/25/38 (2050) €/MWh_HHV** in 2024 euros, multiplied by about 1.11 for an LHV basis, with a 2030 shock value of €70-75. TTF excludes carbon. At about 0.20 tCO2/MWh_LHV, each €100/t adds about €20/MWh. That emission factor is a general-knowledge value in the notes and was not re-verified.

The notes carry many price bases: KEV in €2024, WLO in €2021 and €2022, REF2020 in €2015, PBL ETS2 in €2025, PyPSA technology-data in EUR2025, TNO in €2023 and IEAGHG in €2014. The cleanest convention is to run the whole model in **€2024 real**. The deflators in the notes are approximate and internally inconsistent: €2020→€2024 is given as both 1.13 and 1.17, while €2021→€2024 is also 1.17, which cannot both hold. Take the factors from Eurostat HICP (`prc_hicp_aind`) before converting anything.

## Installed electrolysers cost four to six times the old equipment targets

Electrolyser costs moved the wrong way during the 2020s. The IEA puts the cost of making and installing an electrolyser outside China in 2024 at **USD 2,000-2,600/kW**, and more than half of that is engineering, procurement, construction and contingency ([IEA, 2025](https://iea.blob.core.windows.net/assets/12d92ecc-e960-40f3-aff5-b2de6690ab6b/GlobalHydrogenReview2025.pdf)). ACER's EUR2024 compilation of the IEA series shows observed 2024 costs of €1,819/kW (alkaline) and €2,365/kW (PEM). It also shows forecasts drifting upwards: the 2030 alkaline projection rose from €508/kW in the 2022 review to **€1,274/kW in the 2025 review**, with PEM at €1,647/kW ([ACER, n.d.-b](https://aegis.acer.europa.eu/chest/dataitems/967/view)).

The European Hydrogen Observatory reports €2,310/kW (alkaline) and €2,503/kW (PEM) for 2024, with O&M of about 2% of CAPEX ([European Hydrogen Observatory, 2025](https://observatory.clean-hydrogen.europa.eu/sites/default/files/2025-11/The%20European%20hydrogen%20market%20landscape_November%202025.pdf)). The JRC finds **€2,630 to over €3,050/kW** for 100-200 MW projects ([JRC, 2025](https://www.enagas.es/content/dam/enagas/en/files/transicion-energetica/red-hidrogeno/observatorio-tecnologico-hidrogeno/jrc-water-electrolysis-hydrogen.pdf)). These figures sit far above the Clean Hydrogen JU equipment targets of €400-700/kW ([Clean Hydrogen Partnership, n.d.](https://www.clean-hydrogen.europa.eu/knowledge-management/strategy-map-and-key-performance-indicators/clean-hydrogen-ju-sria-key-performance-indicators-kpis_en)).

Dutch figures are the highest. TNO's evaluation of 14 datasets from 11 developers gives **€3,050/kW at 2023 prices**, O&M of 3.8% of direct costs, 56 kWh/kg at plant level, stack replacement after 55,556 hours and unsubsidised LCOH of €13-14/kg at 4,800 full-load hours ([TNO, 2024](https://zoek.officielebekendmakingen.nl/blg-1145411.pdf)). Shell's Holland Hydrogen 1 reports €684.2 m for 200 MW, about **€3,420/kW** including some grid assets ([RVO, n.d.](https://projecten.rvo.nl/projecten/54075)), and Air Liquide's ELYgator more than €500 m for 200 MW ([Air Liquide, 2025](https://www.airliquide.com/group/press-releases-news/2025-07-23/air-liquide-takes-final-investment-decision-build-elygator-large-scale-electrolyzer-netherlands)).

The Danish Energy Agency's 2024 update raised investment costs by about 60% (alkaline) and 25% (PEM) and cut 2025 efficiencies by about 10% ([Danish Energy Agency, 2024](https://ens.dk/media/4254/download)). The resulting PyPSA defaults are €1,793, €1,435 and €1,196 per kW_e, with 62.2%, 65.3% and 69.9% LHV efficiency, for 2030, 2040 and 2050 ([van Greevenbroek et al., 2025](https://arxiv.org/pdf/2412.07464)); their currency year is unconfirmed. These are close to the €1,886, €1,509 and €1,257 per kW_e already in the current model.

Learning evidence is mixed. European project data give learning rates of 22.9-32.1%, yet large projects show "no clear cost reductions" so far ([Galletti et al., 2025](https://doi.org/10.1016/j.ijhydene.2025.06.002)). The recommended CAPEX path is **€1,800/2,200/3,100 (2025), €1,250/1,650/2,500 (2030), €800/1,250/1,800 (2040) and €500/1,000/1,400 per kW_e (2050)**. It comes with 2-4% FOM, a plant life of 25-30 years and stack replacement at about 20-30% of CAPEX. On this evidence, the current electrolyser inputs sit at the central-to-high end and are defensible.

Grey and blue reformers are better characterised, but on older price bases. IEAGHG's 300 MW_H2 merchant SMR (Q4-2014 prices) implies about **€740/kW_H2**, about **76% LHV** efficiency and **9.0 kg CO2 per kg H2** of direct emissions, and capture options of 56-90% add 18-79% to CAPEX and avoid CO2 at €47-70/t ([IEAGHG, 2017](https://ieaghg.org/publications/techno-economic-evaluation-of-smr-based-standalone-merchant-hydrogen-plant-with-ccs/)). The TNO-affiliated COMPETES table uses €744, €881 and **€1,330/kW** for plain SMR, SMR with 54% capture and SMR with 89% capture, at 76%, 74% and 69% efficiency ([Morales-España et al., 2023](https://doi.org/10.1016/j.ijepes.2023.109686)). UK BEIS assumes 90% capture at 74% HHV efficiency for SMR with carbon capture, and 95% capture at 84% HHV for autothermal reforming (ATR) with carbon capture ([BEIS, 2021](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/1011506/Hydrogen_Production_Costs_2021.pdf)).

The capture configuration matters more than the "blue" label. Process (syngas) capture removes only about 55-60% of site CO2, which is how Air Liquide's Rotterdam retrofit "halves" its site emissions ([Air Liquide, n.d.](https://www.airliquide.com/stories/sustainability/capturing-co2-decarbonize-rotterdams-industrial-basin)). Full flue-gas capture or ATR reaches 90-95%. Life-cycle intensities range from 3.9 kgCO2e/kg for ATR with CCS to 8.2 for SMR with 52% capture ([Oni et al., 2022](https://doi.org/10.1016/j.enconman.2022.115245)). The current model's blue SMR (€1,108/kW_H2, 69% efficiency, 90% capture) sits at the low end of a €1,150-1,600 band. Its grey SMR (€867/kW_H2, 76%) is consistent with the evidence. Escalating 2014-2020 costs by 25-35% to reach 2024 money is an assumption in the notes, not a sourced figure.

Captured CO2 has a disposal cost, and Dutch storage is both expensive and scarce before 2030. **Porthos** charges at most **€47.10/t**; its investment rose from €664 m to €1,213 m (2023 prices), it stores 37.6 Mt at about 2.45 Mt/yr ([Algemene Rekenkamer, 2024](https://english.rekenkamer.nl/binaries/rekenkamer-english/documenten/reports/2024/03/28/carbon-storage-under-the-north-sea/PAC21+ENGELS+rapport+Porthos.pdf)), and first injection has slipped to **2027** ([S&P Global, 2026b](https://www.spglobal.com/energy/en/news-research/latest-news/energy-transition/061726-dutch-porthos-ccs-project-marks-construction-progress-despite-delays)). **Aramis** has an expected tariff of **€67-72/t at 7.5 Mt/yr** in 2022 real terms ([Xodus Group, n.d.](https://www.eerstekamer.nl/9370000/1/j4nvgs5kjg27kof_j9vvkfvj6b325az/vlutrvd2g2y4)); Gasunie and EBN now lead its 22 Mt/yr pipeline ([Gasunie, 2025](https://www.gasunie.nl/en/news/aramis-takes-next-step-towards-investment-decision)) and aim for an investment decision in 2027 and operation in 2030 ([ChemXplore, 2026](https://chemxplore.com/news/aramis-ccs-final-investment-decision)). Meanwhile €8.2 bn of SDE++ awards for CCS were withdrawn by April 2026, after costs and permitting bottlenecks escalated across the chain ([Solar Magazine, 2026a](https://solarmagazine.nl/nieuws-zonne-energie/i43609/sde-8-2-miljard-euro-aan-co2-opslagprojecten-ingetrokken)).

At about 8 kg of CO2 captured per kg of H2, these tariffs add **€0.38-0.56/kg** to blue hydrogen (derived). The model needs a T&S price of 45/55/75 €/t around 2030 and an annual capacity cap: zero before 2027, 2.5 Mt/yr from 2027, and Aramis volumes added from 2030. The decline to €25-65/t by 2050 in the notes is a learning assumption without a source.

Underground hydrogen storage arrives late, but it costs less per kWh than the model assumes. HyStock's first Zuidwending cavern holds 216 GWh (about 6.5 kt). It is now expected around **2031**, three years later than first planned, with four caverns in total (about 20 kt, roughly 0.67 TWh) following later ([Gasunie, n.d.](https://www.gasunie.nl/en/projects/hystock-hydrogen-storage); [HyStock, 2023](https://www.hystock.nl/en/news/successful-open-season-ample-interest-in-hydrogen-storage-first-salt-cavern-hystock)). The state committed €450 m to the project in July 2026 ([Energy News, 2026](https://energynews.biz/the-netherlands-commits-e450-million-to-hydrogen-storage-as-it-tackles-a-critical-gap-in-green-hydrogen-infrastructure/?amp=1)).

How much storage is needed by 2050 is uncertain. The government's storage agenda assumes about 250 GWh per cavern and a **2050 need of 20-40 caverns**, about 5-10 TWh ([Ministerie van KGG, 2025](https://www.eerstekamer.nl/behandeling/20250704/brief_regering_nationale_agenda/document3/f=/vmp2jywo3tzl.pdf)). TNO's 2020 estimate was much lower, at 1.5-2.9 TWh against an onshore salt potential of 43.3 TWh ([TNO, 2020](https://projecten.topsectorenergie.nl/storage/app/uploads/public/618/269/e7b/618269e7bb312950892810.pdf)), while one recent study finds salt capacity in the northern Netherlands inadequate in its medium- and high-demand scenarios ([de Vries et al., 2026](https://doi.org/10.1016/j.ijhydene.2025.152686)). On cost, the Clean Hydrogen JU cavern target of €35/kg (2020) falling to €30/kg (2030) ([Clean Hydrogen Partnership, n.d.](https://www.clean-hydrogen.europa.eu/knowledge-management/strategy-map-and-key-performance-indicators/clean-hydrogen-ju-sria-key-performance-indicators-kpis_en)) converts to **€0.9-1.05/kWh**. That is consistent with a levelised cost of about USD 0.8/kg for large European caverns ([Talukdar et al., 2023](https://doi.org/10.1016/j.isci.2023.108771)). The model's €2.67/kWh for 2030, with a 100-year lifetime and no compressor or withdrawal equipment, is two to three times that target. The notes could not confirm whether the target includes surface facilities.

The national hydrogen network and imports both fall outside the current single-node model, but the evidence prices both. The cost estimate for the ~1,200 km network rose from **€1.5 bn to €3.8 bn**, with start-up losses of €2.5 bn against a €750 m subsidy ([Algemene Rekenkamer, 2025](https://english.rekenkamer.nl/latest/news/2025/12/10/construction-of-sustainable-hydrogen-network-uncertain)), and completion has slipped to **2033 at the latest** ([Gasunie, 2024](https://www.gasunie.nl/en/news/national-hydrogen-network-roll-out-plan-updated-2)). The 2026 tariff is **€48.71/kW/yr on an HHV basis for entry plus exit**, indexed to inflation ([Hynetwork, n.d.](https://www.hynetwork.nl/en/business/become-a-customer/transport-tariff)), which works out to about €0.22/kg at baseload and €0.48/kg at 4,000 full-load hours (derived). ACM expects only 1-1.5 GW of network use in 2030 instead of 4 GW and warns that tariffs "can increase considerably" ([ACM, 2025](https://www.acm.nl/nl/node/27759)). For imports, PBL cites ship-borne hydrogen at €6-7.5/kg in 2030 (€13-14 in pessimistic cases) and pipeline hydrogen at €3.5-5/kg from Spain and €4-6/kg from Tunisia ([Elzenga et al., 2025](https://pbl.nl/downloads/pbl-2025-groene-waterstof-de-praktische-uitdagingen-tussen-droom-en-werkelijkheid-5608pdf)), and the grid operators expect **10-30 TWh of imports in 2030 and 150-300 TWh in 2050** ([Netbeheer Nederland, 2025a](https://www.netbeheernederland.nl/sites/default/files/2025-05/netbeheer_nederland_scenarios_editie_2025_-_def_12-05.pdf)). These figures give the model a natural fallback: when electrolysis is restricted, hydrogen does not have to come from reformers alone.

LCOH benchmarks are validation targets for model outputs, not inputs. EU-average 2024 costs were €3.3/kg for grey hydrogen, €4.1/kg for blue, €7.4/kg for grid-powered electrolysis and €6.7/kg for renewable-PPA electrolysis ([European Hydrogen Observatory, 2025](https://observatory.clean-hydrogen.europa.eu/sites/default/files/2025-11/The%20European%20hydrogen%20market%20landscape_November%202025.pdf)). ACER puts January-October 2025 at **€2.00/kg** for SMR, €2.80/kg for SMR with CCS excluding transport and storage, and **€7-10/kg** for RFNBO-compliant hydrogen ([pv magazine, 2025](https://www.pv-magazine.com/2025/12/03/price-gap-between-conventional-renewable-hydrogen-widens-in-europe/)). Dutch electrolytic hydrogen costs €13-14/kg according to TNO, and PBL expects €12-16/kg over the next 15 years, five to six times grey and blue ([Elzenga et al., 2025](https://pbl.nl/downloads/pbl-2025-groene-waterstof-de-praktische-uitdagingen-tussen-droom-en-werkelijkheid-5608pdf)). A 2025-2030 model run that produces green hydrogen far below €7/kg is running on optimistic inputs. Modelled long-run costs of €1.3-3/kg ([Zeyen et al., 2023](https://doi.org/10.1038/s41467-023-39397-2)) depend on cost declines that have not yet been observed.

## Dutch hydrogen demand holds near 1.1 Mt to 2030, then multiplies

The model's 1.3 Mt baseline is sound as a 2020 gross figure. PBL puts 2020 use at about 1.3 Mt (150 PJ):

| Use | Amount |
|---|---|
| Ammonia | ~0.5 Mt |
| Refineries | >0.5 Mt |
| Other industry | 0.15 Mt |
| Methanol (since discontinued) | 0.1 Mt |
| Residual gases burnt for energy | ~0.25 Mt |

Production of this hydrogen emits about 12 Mt CO2 a year at about 9 kg CO2/kg ([Elzenga et al., 2025](https://pbl.nl/downloads/pbl-2025-groene-waterstof-de-praktische-uitdagingen-tussen-droom-en-werkelijkheid-5608pdf)).

Market counts are lower. In 2024 the Netherlands consumed **1.054 Mt** and produced 1.02 Mt, from 1.50 Mt/yr of capacity: 1.26 Mt/yr of reforming, 0.20 Mt/yr of by-product hydrogen and only 0.04 Mt/yr (34.2 MW) of electrolysis ([European Hydrogen Observatory, 2025](https://observatory.clean-hydrogen.europa.eu/sites/default/files/2025-11/The%20European%20hydrogen%20market%20landscape_November%202025.pdf)). The base relevant to the RED III obligations is only 70 PJ, about 0.84 Mt ([Kamerstukken II 36936-3, 2026](https://zoek.officielebekendmakingen.nl/kst-36936-3.odt)).

Two consequences follow for the model. By-product and residual hydrogen (about 0.2-0.25 Mt) is must-run supply and should not count towards the S1-S3 share. And the existing reforming fleet still operates.

Demand stays essentially flat to 2030 and grows only afterwards. In the grid operators' policy-baseline scenario, Koersvaste Middenweg (KM), total demand is **37 TWh (2030), 104 TWh (2035), 201 TWh (2040) and 288 TWh (2050)**. In the carrier-import variant (KM_IW) it is 26, 64, 113 and 143 TWh ([Netbeheer Nederland, 2026](https://www.netbeheernederland.nl/sites/default/files/2026-04/verkenningen_netbeheer_nederland_scenarios_editie_2025_0.pdf)). These totals include export and transit, which reach 128 TWh in KM in 2050.

Domestic 2050 use is therefore about 160 TWh (≈4.8 Mt) in KM and about 78 TWh (≈2.3 Mt) in KM_IW. That brackets PBL's 450-630 PJ (≈3.8-5.3 Mt) ([Elzenga et al., 2025](https://pbl.nl/downloads/pbl-2025-groene-waterstof-de-praktische-uitdagingen-tussen-droom-en-werkelijkheid-5608pdf)). Keeping demand fixed at 1.3 Mt in all periods, as the current model does, understates 2050 domestic demand by a factor of about **2-4**. This is the input most likely to change the S1-S3 ranking.

Electrolysis ambitions have collapsed, and that sets a deployment ceiling well below any water limit in 2030:

| When announced | Target |
|---|---|
| Klimaatakkoord era ([Jetten, 2022a](https://eerstekamer.nl/9370000/1/j4nvi0xeni9vr2l_j9vvkfvj6b325az/vlqxmvtu9xdh/f=/vlqxmwoxau8x.pdf)) | 500 MW in 2025; 3-4 GW in 2030 |
| December 2022 ([Jetten, 2022b](https://app.1848.nl/static/pdf/bd/32/bd323e63705182110cc51091685a12c2c4ae1bad.pdf)) | doubled to 6-8 GW in 2030 |
| April 2026 ([RVO, 2026a](https://www.rvo.nl/sites/default/files/2026-04/Waterstof%20infographic.pdf)) | **1.2 GW (≈12 PJ) in 2030; 3-4 GW in 2035** |

Only 34.2 MW was operating in 2024. Shell's 200 MW Holland Hydrogen 1 was due to start "later in 2026" ([S&P Global, 2026a](https://www.spglobal.com/energy/en/news-research/latest-news/refined-products/042826-shell-readies-europes-largest-refinery-for-green-hydrogen)), and Air Liquide's 200 MW ELYgator follows in 2027. The 1.2 GW of funded or subsidised capacity yields about 12 PJ, roughly **8-9% of 2030 demand** (derived). So even S1's 50% cap would not bind in 2030 unless the model is free to build several gigawatts the evidence says will not exist.

The grid operators' range is 1-3 GW in 2030 and 14-35 GW in 2050 ([Netbeheer Nederland, 2025a](https://www.netbeheernederland.nl/sites/default/files/2025-05/netbeheer_nederland_scenarios_editie_2025_-_def_12-05.pdf)). The National Energy System Plan (NPE) target is 40 GW in 2050 ([Elzenga et al., 2025](https://pbl.nl/downloads/pbl-2025-groene-waterstof-de-praktische-uitdagingen-tussen-droom-en-werkelijkheid-5608pdf)). Official documents use about 10 PJ of hydrogen per GW of electrolysis per year, roughly 4,500 full-load hours, which is a useful calibration for the model's electrolyser utilisation.

Policy instruments explain why green hydrogen remains marginal before 2030. The Dutch RFNBO obligation for industry is set at only **4% in 2030** (1.6% for ammonia producers) and 9.9% in 2035. Full RED III compliance would need 29 PJ (≈245 kt) in 2030 and 42 PJ in 2035. The government itself expects its instrument mix to deliver "less than half" of the EU requirement ([Kamerstukken II 36936-3, 2026](https://zoek.officielebekendmakingen.nl/kst-36936-3.odt); [Ministerie van KGG, 2026](https://berthub.eu/tkconv/getraw/2026D20450)). The Raad van State (Council of State) warned of a significant risk of non-compliance ([Kamerstukken II 36936-4, 2026](https://zoek.officielebekendmakingen.nl/kst-36936-4.pdf)).

Subsidy intensity is high. Round 1 of the OWE scheme (the Dutch electrolyser subsidy) paid €250 m for 101 MW, about €2.5 m/MW ([Rijksoverheid, 2024](https://www.rijksoverheid.nl/actueel/nieuws/2024/04/29/zeven-projecten-krijgen-subsidie-voor-de-productie-van-volledig-hernieuwbare-waterstof)). Round 2 paid more than €700 m for 602 MW ([Solar Magazine, 2025d](https://solarmagazine.nl/nieuws-zonne-energie/i41282/kabinet-investeert-700-miljoen-euro-in-elektrolysers-voor-productie-groene-waterstof)). Dutch bids in European Hydrogen Bank auctions were about twice the winners' ([Elzenga et al., 2025](https://pbl.nl/downloads/pbl-2025-groene-waterstof-de-praktische-uitdagingen-tussen-droom-en-werkelijkheid-5608pdf)), whose premiums were €0.2-0.6/kg ([Hydrogen Europe, 2025](https://hydrogeneurope.eu/boosting-renewable-hydrogen-the-commission-selects-15-projects-to-receive-nearly-e1-billion/)). The government's own assumption is an extra cost of €8/kg in 2030.

Two of these settings are natural model levers rather than uncertainties: the RFNBO share, at 4% (Dutch bill) or 42% (RED III), and a capital subsidy of 0-80%, which the current model already supports.

Offshore electrolysis is in a demonstration phase: Demo 1 is at least 20 MW from 2031, with €225-260 m of subsidy ([Ministerie van KGG, 2024](https://internetconsultatie.nl/demonstratieproject/document/13363)). Import volumes before about 2032-2033 are limited to ship-borne carriers such as the NEOM ammonia contract (about 0.2 Mt H2-equivalent). PBL expects imports to cover 40-60% of green-hydrogen demand in 2035 and 40-70% in 2040 ([Elzenga et al., 2025](https://pbl.nl/downloads/pbl-2025-groene-waterstof-de-praktische-uitdagingen-tussen-droom-en-werkelijkheid-5608pdf)).

## The power system: slipping targets, costlier offshore wind and near-zero VOM

At the end of 2025 the Dutch power system had about **29.4 GWp of solar PV** (26 GW AC) ([Solar Magazine, 2026c](https://solarmagazine.nl/nieuws-zonne-energie/i44006/cbs-nederland-installeerde-vorig-jaar-1-447-megawattpiek-zonnepanelen)), **7.0 GW of onshore and 4.7 GW of offshore wind** ([CBS, 2026b](https://www.cbs.nl/en-gb/news/2026/11/production-and-export-of-electricity-at-record-levels)), about 17.4 GW of gas-fired capacity and 3.4 GW of coal ([CBS, 2026a](https://www.cbs.nl/en-gb/figures/detail/86266ENG)), and Borssele at **485 MW net** ([NEI Magazine, 2026](https://www.neimagazine.com/?p=107843)). A second extraction of the StatLine table gave no fuel split, so the gas and coal figures need verifying. The wind series is solid. Onshore capacity grew from 4,188 MW in 2020 to 6,965 MW in 2024, and offshore from 2,460 MW to 4,748 MW ([CBS, 2025](https://www.cbs.nl/nl-nl/longread/rapportages/2025/hernieuwbare-energie-in-nederland-2024/4-windenergie)). Generation was flat at 117-120 TWh in 2020-2024 and jumped to a record **132 TWh in 2025**. That year gas supplied 48 TWh, coal 12 TWh (up 25%), and the country was a net exporter of 14 TWh ([CBS, 2026b](https://www.cbs.nl/en-gb/news/2026/11/production-and-export-of-electricity-at-record-levels)). Power-sector CO2 was 26.4 Mt in 2025 (provisional) ([PBL, 2026d](https://www.pbl.nl/system/files/document/2026-09/pbl-2026-klimaat-en-energieverkenning-2026-6050.pdf)).

Every capacity target has slipped. In July 2025 the government cut the 2040 offshore wind target from 50 GW to **30-40 GW**, calling 50 GW "unrealistic and unnecessary" ([offshoreWIND.biz, 2025a](https://www.offshorewind.biz/2025/07/17/dutch-govt-lowers-2040-offshore-wind-target-50-gw-unrealistic-and-unnecessary)). The 2032 target remains 21 GW, up to about 23 GW with over-programming ([Hermans, 2025](https://www.eerstekamer.nl/behandeling/20250916/brief_regering_actieplan/document3/f=/vmqvpympliy3.pdf)), but the 1 GW Nederwiek I-A tender drew **zero bids** in October 2025 ([offshoreWIND.biz, 2025b](https://www.offshorewind.biz/2025/10/31/zero-bids-in-1-gw-dutch-offshore-wind-tender/)) and subsidies are back, with a ceiling of €104/MWh for IJmuiden Ver Gamma ([RVO, 2026b](https://www.rvo.nl/onderwerpen/windenergie-op-zee/plannen-windenergie-op-zee)). KEV 2026 therefore expects only **about 9.5 GW of offshore wind in 2030 and 21 GW in 2040** without extra policy, and 30-36 GW with it ([PBL, 2026d](https://www.pbl.nl/system/files/document/2026-09/pbl-2026-klimaat-en-energieverkenning-2026-6050.pdf)). Onshore wind and solar are the exception: the 35 TWh RES target for 2030 will probably be met, with 42 TWh (38-46) expected ([PBL, 2025b](https://www.pbl.nl/downloads/pbl-2025-monitor-res-2025-5967pdf)). Borssele's 2033 closure date was removed, so it could run to 2054, but the first new reactor is now expected in the late 2030s at the earliest, against an ambition of about 7 GWe by 2050 ([NEI Magazine, 2026](https://www.neimagazine.com/?p=107843); [World Nuclear Association, n.d.](https://world-nuclear.org/our-association/publications/world-nuclear-outlook-report/netherlands---world-nuclear-outlook-report)). Coal is banned from 2030, so plants must close by the end of 2029 ([Enerdata, 2018](https://www.enerdata.net/publications/daily-energy-news/netherlands-confirms-phasing-out-coal-fired-power-plants-2030.html)). TenneT projects a loss-of-load expectation of 12.6 h in 2033 and 9.2 h in 2035 against a 4 h norm, with about 1.7 GW of gas capacity at risk of closing ([Solar Magazine, 2025b](https://solarmagazine.nl/nieuws-zonne-energie/i40567/tennet-wijst-opnieuw-op-risico-stroomtekort-na-2030)). These are hard per-period bounds, and the current model lacks them for 2030 and later.

Electricity demand projections diverge more than supply projections. KEV 2024 gives **130 TWh of net end-use demand in 2030** ([Solar Magazine, 2024](https://solarmagazine.nl/nieuws-zonne-energie/i38866/nederland-telt-33-6-gigawatt-zonnepanelen-in-2030-groei-hernieuwbare-energie-blijft-achter)). The grid operators' scenarios reach **290-440 TWh in 2050** ([Netbeheer Nederland, 2025b](https://www.netbeheernederland.nl/artikelen/nieuws/netbeheer-nederland-scenarios-editie-2025)), and KM runs 169, 227, 286 and 344 TWh for 2030, 2035, 2040 and 2050 ([Netbeheer Nederland, 2026](https://www.netbeheernederland.nl/sites/default/files/2026-04/verkenningen_netbeheer_nederland_scenarios_editie_2025_0.pdf)). Those totals include electrolysis and data centres, so endogenous electrolysis must be subtracted to avoid double counting.

The KEV 2026 coverage also says the Netherlands will even need to import electricity in 2030 ([Solar Magazine, 2026d](https://solarmagazine.nl/nieuws-zonne-energie/i44765/nederland-mist-europees-doel-voor-duurzame-energie-en-moet-in-2030-zelfs-stroom-importeren)), a reversal of the 14 TWh net export in 2025. An isolated single-node model cannot reproduce either situation, and that affects curtailment and electrolyser full-load hours.

Technology costs from DEA via PyPSA technology-data (EUR2025) are a reasonable central set ([PyPSA technology-data contributors, 2026](https://github.com/PyPSA/technology-data)). Utility PV falls from €595/kW (2025) to €368/kW (2050). Onshore wind falls from €1,439 to €1,286/kW. Offshore turbines, excluding the grid connection, fall from €2,224 to €1,916/kW, with FOM of €42-53/kW/yr. A CCGT costs €1,142-1,069/kW at 57-60% efficiency.

Dutch-specific offshore costs are higher. PBL's 2026 tender advice gives **€2,566-2,603/kW excluding the TenneT grid**, FOM of €46-47/kW/yr, 3,703-3,756 net full-load hours and a 35-year life ([PBL, 2026a](https://www.pbl.nl/en/downloads/pbl-2026-advice-offshore-wind-tender-2026-5971pdf)). For new nuclear, PyPSA's €10,806/kW (Lazard) and EIA's AP1000 figure of $7,861/kW ([EIA, 2024](https://www.eia.gov/analysis/studies/powerplants/capitalcost/pdf/capital_cost_AEO2025.pdf)) bracket a synthesised range of €6,500/9,000/12,000 per kW. The current model's €6,000-4,800/kW is below even the low end.

Variable O&M is where the evidence most clearly departs from the course database ([PyPSA technology-data contributors, 2026](https://github.com/PyPSA/technology-data); [EIA, 2024](https://www.eia.gov/analysis/studies/powerplants/capitalcost/pdf/capital_cost_AEO2025.pdf)):

| Technology | Realistic VOM, €/MWh | Source |
|---|---|---|
| CCGT | 5.3-5.7 (DEA); about 3 (EIA, $3.3-3.4) | PyPSA technology-data; EIA |
| Onshore wind | 1.6-1.9 | DEA |
| Offshore wind and PV | about 0 (PyPSA tie-breakers of 0.013-0.027) | PyPSA technology-data |
| Nuclear | 2.5-4.5 | EIA; PyPSA technology-data |

PBL's €9.9/MWh for PV is imbalance and transaction cost, not O&M, and should not enter a cost-minimising model as VOM ([Lensink et al., 2025](https://zoek.officielebekendmakingen.nl/blg-1231279.pdf)).

Batteries have become much cheaper than the DEA-based defaults. BNEF's 2025 survey shows turnkey systems at **$117/kWh globally and $177/kWh in Europe**, and Ember gives $125/kWh all-in outside China and the US ([Energy-Storage.news, 2025](https://www.energy-storage.news/?p=92133)). NREL's 2025 update projects a 4-hour system at $207/279/354 per kWh in 2030 and $108/178/307 in 2050 (2024 USD), with 85% round-trip efficiency and a 15-year life ([NREL, 2025](https://docs.nrel.gov/docs/fy25osti/93281.pdf)). The DEA-based 2025 value (about €322/kWh for 4 hours) is therefore two to three times too high. A synthesised path of **150/200/280 (2025), 100/150/240 (2030) and 50/90/120 €/kWh (2050)** is defensible, and cost reviews find that projections have consistently been too pessimistic ([Haas et al., 2025](https://doi.org/10.1016/j.apenergy.2025.125856)).

Installed Dutch storage was 350 MW / 620 MWh at the end of 2024 ([Solar Magazine, 2025c](https://solarmagazine.nl/nieuws-zonne-energie/i41154/de-harde-cijfers-84-grote-batterijen-in-nederland-met-620-megawattuur-opslagcapaciteit)), with about 2.1 GWh expected by the end of 2025 ([Solar Magazine, 2025e](https://solarmagazine.nl/nieuws-zonne-energie/i41847/nederland-installeert-dit-jaar-2-1-gigawattuur-grote-batterijen)). Scenarios put 7-10 GW in 2030 and 27-56 GW in 2050 ([Solar Magazine, 2025a](https://solarmagazine.nl/nieuws-zonne-energie/i40555/vraag-naar-duurzame-energie-groeit-sneller-dan-aanbod-tot-3-5-keer-meer-stroom-nodig)). The model's default one-hour battery is shorter than the 2-4 hour systems now being built.

Three observed quantities make good calibration checks. Full-load hours in 2024-2025 were about 3,290-3,440 for offshore wind, 2,350-2,580 for onshore wind and 830-890 kWh/kWp DC for solar (derived from CBS output and capacity). Market-based curtailment exceeded **1 TWh in 2025**, about 1-2% of wind and solar output ([Solar Magazine, 2026b](https://solarmagazine.nl/nieuws-zonne-energie/i43654/tennet-kosten-congestiemanagement-stijgen-fors-meer-dan-1-terawattuur-curtailment)), and there were **584 hours of negative day-ahead prices** ([pv magazine, 2026](https://www.pv-magazine.com/2026/02/03/germany-france-netherlands-curtail-3-9-twh-of-renewables-in-2025/)).

## Water steers where electrolysers go, not whether the country can run them

The volumes are small at national scale. Electrolysis needs about 9 L of water per kg H2 stoichiometrically. The ministries' study puts feed water at **0.9-1.9 Mm³/yr per GW at 5,000 hours**, about 10-21 L/kg including demineralisation reject; closed cooling multiplies that by about 5 and once-through cooling by about 100, although almost all once-through water is returned ([Folmer et al., 2024](https://eerstekamer.nl/overig/20241025/onderzoeksrapport_water_voor/document)). KWR found about 17 L of drinking water per kg ([Oesterholt et al., 2017](https://api.kwrwater.nl//uploads/2018/11/BTO-2016.086-De-vraag-naar-water-in-een-waterstofeconomie.Kansen-en-gevolgen-voor-de-drinkwatersector.pdf)). Including cooling, IRENA puts consumption at 17.5 L/kg for PEM and 22.3 L/kg for alkaline ([SPICe, 2024](https://www.parliament.scot/-/media/files/committees/citizen-participation-and-public-petitions-committee/correspondence/2024/pe2159/spice-briefing-for-petition-pe2159.pdf)), and the US DOE gives about 9 L/kg with dry cooling to 30 L/kg with a cooling tower for PEM ([Melaina et al., 2026](https://www.energy.gov/documents/record-25003-water-use-hydrogen-production)). Making all 1.3 Mt by electrolysis would therefore need **13-27 Mm³/yr of feed water**, 1-2% of drinking-water abstraction and 0.2-0.4% of fresh-water abstraction, which CBS puts at about 1,259 and 7,368 Mm³ in 2023 ([CBS, 2026c](https://www.cbs.nl/nl-nl/cijfers/detail/82883NED)). Even with closed evaporative cooling (about 76-161 Mm³) the share stays small, and as a flow it is 0.4-0.85 m³/s against a record-low Rhine flow of 655 m³/s (derived). The binding issues are local: the water source, the cooling method, discharge-temperature limits and priority during drought.

Those local constraints are real but narrow. Water shortages were declared nationally in 2003, 2006, 2011, 2018, 2022 and 2026. In 2026 the Rhine at Lobith fell to **655 m³/s on 6 August**, the lowest for that time of year since records began in 1901 ([KNMI, 2026](https://www.knmi.nl/over-het-knmi/nieuws/zeer-lage-rijnafvoer-door-aanhoudende-droogte-in-stroomgebied)). Yet the ministry reported that effects "fall under Category 4", with categories 1-3 facing no major issues ([Ministerie van IenW, 2026](https://zoek.officielebekendmakingen.nl/kst-1264000.pdf)).

The verdringingsreeks (the legal priority order for water during shortages) ranks the categories as follows ([IPLO, n.d.](https://iplo.nl/thema/water/beheer-watersysteem/verdringingsreeks/)):

| Category | Users |
|---|---|
| 2 | drinking water and energy supply |
| 3 | industrial process water |
| 4 | other industry |

No official source places electrolysis in this order. Feed water most plausibly counts as category 3 and cooling water as category 4, so in practice it is inland cooling and fresh-water intakes that are exposed. Heat waves are a second channel: in 2018 Nouryon cut output by 25% when cooling-water temperature limits were exceeded ([van Hussen et al., 2019](https://www.ecorys.com/sites/default/files/2019-10/20190221%20Rapport%20Economische%20schade%20door%20droogte%20in%202018.pdf)).

Climate trends tighten the margin. KNMI'23 projects that the 1-in-10-year precipitation deficit rises by 9-30% by 2050 ([Klimaatadaptatie Nederland, n.d.](https://klimaatadaptatienederland.nl/kennisdossiers/droogte/hoeveel-droger)), and summer Rhine and Meuse discharge falls by 10-30% by 2100 ([Rijkswaterstaat, 2023](https://www.rijkswaterstaat.nl/nieuws/archief/2023/12/toekomstige-rivierafvoeren-rijn-en-maas-lager-in-de-zomer-en-hoger-in-de-winter)). Neither trend moves coastal sites.

National policy has already chosen how to deal with this. The minister's October 2024 letter states that coastal electrolysis has "no water shortage" and that sea or brackish water, desalinated if needed, is "a structural solution" ([Hermans, 2024](https://eerstekamer.nl/9370000/1/j4nvi0xeni9vr2l_j9vvkfvj6b325az/vmie42e6ffwd/f=/vmhv413eyuv6.pdf)). The drinking-water companies' association, Vewin, rejects using drinking water ([KWR, 2026](https://www.kwrwater.nl/en/projecten/water-voor-waterstofproductie-w4h2/)). Desalination is cheap per kilogram. Treatment costs €0.5-2.2/m³ ([Folmer et al., 2024](https://eerstekamer.nl/overig/20241025/onderzoeksrapport_water_voor/document)), the US DOE estimates USD 0.01-0.04 per kg H2 ([U.S. Department of Energy, 2024](https://www.energy.gov/eere/fuelcells/can-water-usage-electrolysis-pose-problems-parts-united-states-currently-facing)), RMI no more than USD 0.10/kg ([Ramirez et al., 2023](https://rmi.org/resources/hydrogen-reality-check-distilling-green-hydrogens-water-consumption/)), and water stays under 2.4% of LCOH even at €10/m³ ([Vinardell et al., 2025](https://doi.org/10.1016/j.nexus.2025.100457)). Seawater reverse osmosis uses 3.7-8 kWh/m³ ([Walter et al., 2023](https://iewt2023.eeg.tuwien.ac.at/download/contribution/fullpaper/8/8_fullpaper_20230210_174238.pdf)), well under 0.5% of electrolysis electricity. The best European model of water-constrained electrolysis adds freshwater caps and a priced seawater option, and finds that about **10% of electrolysis capacity relocates**; none is eliminated ([Walter et al., 2025](https://doi.org/10.1016/j.adapen.2025.100208)).

The current model's framing is S1 = 50% (medium scarcity, category 3) and S3 = 0% (high scarcity, category 4). The evidence does not support it as hydrology. A physically grounded mapping gives 100% availability for S2, with a desalination adder of €0.01-0.03/kg; 95-98% of potential electrolytic output under medium scarcity (100% at the coast, 85-95% inland); and 75-90% under high scarcity for fresh-water-dependent inland capacity, while coastal or desalinated plants stay near 100%. Even 50% would require about half of capacity to sit inland on fresh water and be shut for about six months a year, which no drought from 2018 to 2026 came close to.

S3 is also internally inconsistent. IRENA reports **32.2 L/kg for SMR with carbon capture and 24.2 L/kg for ATR with carbon capture**, as much as or more than electrolysis ([SPICe, 2024](https://www.parliament.scot/-/media/files/committees/citizen-participation-and-public-petitions-committee/correspondence/2024/pe2159/spice-briefing-for-petition-pe2159.pdf)). Arup disagrees, so this point is contested, but a water-motivated shift to blue hydrogen does not obviously save water.

There are two defensible reframings. The first keeps 0/50/100% but labels S1 and S3 explicitly as policy or social-licence stress tests. The second redefines the parameter as the maximum share of electrolysis that may use fresh water, so that all remaining capacity carries the sea, brackish or effluent water cost and energy adders.

## Where the evidence overturns the current model

Comparing the model files (`build_h2_database.py`, `energy_model/hydrogen.py`, `input_databases/h2/*.xlsx`) with the evidence shows several settings that matter more than the scenario parameter. The model's own notebook concedes the same: "a few settings in the course database largely decide the outcome, more than the scenario parameter itself." The table ranks the findings by likely impact.

| Model element | Current model | What the evidence supports | Consequence and fix |
|---|---|---|---|
| VOM convention | Course VOMs in €/kWh, multiplied by 1,000: CCGT and biomass €200/MWh of fuel, wind €100/MWh, PV €50/MWh, nuclear €500/MWh of fuel | CCGT €2-6/MWh_e, onshore €1.6-1.9, offshore and PV about 0, nuclear €2.5-4.5 ([PyPSA technology-data contributors, 2026](https://github.com/PyPSA/technology-data); [EIA, 2024](https://www.eia.gov/analysis/studies/powerplants/capitalcost/pdf/capital_cost_AEO2025.pdf)) | **About 100× too high**, consistent with ct/kWh entered as €/kWh. Electricity averages €130-330/MWh in the model against the KEV 2030 €73 (48-105) ([PBL, 2025a](https://www.pbl.nl/system/files/document/2025-09/pbl-2025-klimaat-en-energieverkenning-2025-5692.pdf)). A wind VOM of €100/MWh alone adds about €5.4/kg to green H2 at 54 kWh/kg (derived). Make `vom_scale=0.01` the default, not a sensitivity. |
| Natural gas supply | Cumulative "reserve" of 1,000 TWh shared by all periods and fully used by 2050; price €20/MWh in 2020 rising to €50 in 2050 | Gas is imported at the TTF price. Central €24-26/MWh_HHV (≈€27-29 LHV) for 2030-2050, high €38-47. The risk is price spikes, not physical shortage ([Chyong et al., 2026](https://doi.org/10.1016/j.isci.2026.115866)) | The reserve creates a scarcity rent that real markets do not have, and SMR's 57 TWh/yr deepens it. The 2040-2050 prices sit above the evidence's high bound. Remove the stock (or make it non-binding), use the TTF path, and model shocks as a €70-75 price stress. |
| Prices locked per vintage | Each link pays the fuel and CO2 price of its build period for its whole life | Central CO2 rises from €110 (2030) to €250/t (2050) | An SMR built in 2030 underpays about €1.3/kg H2 in 2050 (derived: €140/t × 9 kg/kg). Use per-period (time-varying) marginal costs. |
| CO2 price | €0 in the database; preset paths of 40, 80 and 150-250 €/t are placeholders | 75/110/140 (2030), 130/180/270 (2040), 170/250/500 (2050), €2024 | Replace the presets. Separate ETS2 from ETS1 for households and cars from 2028. |
| CO2 transport and storage | €0/t and unlimited | Porthos €47.10/t, Aramis €67-72/t; no capacity before 2027, 2.5 Mt/yr from 2027, Aramis from 2030 | Add the price and an annual capacity cap. Otherwise blue hydrogen is favoured by about €0.4-0.6/kg plus unlimited volume. |
| Hydrogen demand | 1.3 Mt fixed in every period | 0.8-1.3 Mt in 2030; 2.3-5.3 Mt domestic in 2050 | Treat demand as a key uncertainty. Keep about 0.2-0.25 Mt of by-product and residual hydrogen as must-run supply outside the S1-S3 share. |
| Existing stock | "Existing" SMR and CCGT get lifetime 4 and vanish after 2020 | 1.26 Mt/yr of reforming capacity in 2024, with retrofits feeding Porthos from 2026-2027; about 17.4 GW of gas plant in 2025 | 2030 is forced to rebuild sunk assets, which inflates S3 cost. Give existing assets realistic residual lives and add a CCS retrofit option (an extra €130-590/kW_H2, derived from IEAGHG). |
| Hydrogen imports | Absent | 10-30 TWh in 2030 and 150-300 TWh in 2050, at €3.5-7.5/kg (2030) | Add an import generator with a price and an annual cap of zero until about 2032-2033. Without it S3 has no realistic fallback. |
| Hydrogen storage | €4.01/2.67/2.01/1.60 per kWh, 100-year life, no compressor, no cap, available from 2030 | €0.5-1.2/kWh, 40-50 year life; first cavern about 2031; 0.67-0.9 TWh by the mid-2030s; 1.5-10 TWh in 2050 | Lower the cost, add an energy cap per period and add compressor/withdrawal links. |
| Hydrogen network | Absent | 2026 tariff €48.71/kW_HHV/yr, about €0.22-0.48/kg; complete only by 2033 | Add a delivered-hydrogen adder of €0.15-1.20/kg. |
| Water and S1-S3 | S1 50% and S3 0% justified by verdringingsreeks categories 3 and 4 | Small volumes; 2026 restrictions reached only category 4; physically 75-100% availability | Relabel S1 and S3 as policy stress tests, or redefine them as a fresh-water share. Count blue hydrogen's water use in S3. |
| Capacity bounds after 2020 | No minimums or maximums from 2030 | Offshore wind 9.5-21 GW (2030); coal 0 from 2030; no new nuclear before the late 2030s; electrolysis 0.5-3 GW (2030) | Add per-period bounds. Deployment, not water, limits green hydrogen in 2030. |
| Nuclear and offshore wind costs | Nuclear €6,000→4,800/kW; offshore wind €1,300/kW and FOM €65/kW/yr in 2050 | Nuclear €6,500/9,000/12,000; offshore wind €1,900-2,300/kW and FOM €41-53/kW/yr | Nuclear is too cheap; offshore 2050 CAPEX is too low while its FOM is too high. |
| Batteries | Default 1-hour duration | 2-4 hour systems; Europe $177/kWh (2025) | Split energy and power costs. |
| 2020 calibration capacities | Wind and nuclear bounds equal 0.7 × CBS values (onshore 2,931.6 = 0.7 × 4,188 MW; offshore 1,722 = 0.7 × 2,460 MW; nuclear 358.4 = 0.7 × 512 MW) | CBS end-2020 actual values | Looks like a course calibration factor. Document it and do not carry it into later periods. |

Correcting values is not enough on its own; the model also needs several features it lacks. Fuel and CO2 costs must apply to every asset in every period, attached to buses or entered as time-varying marginal costs. Natural gas should be bought at the TTF price path, with any security-of-supply question expressed as a price stress or an annual import cap rather than a depleting stock. The hydrogen bus needs the full chain the evidence describes: existing reformers with realistic residual lives and a CCS-retrofit option, must-run by-product hydrogen, an import generator that stays at zero until the network and terminals exist, a network adder, salt-cavern stores with separate compressor links and per-period energy caps, and a CO2 transport-and-storage sink with both a price and an annual capacity.

Per-period capacity bounds should encode what is decided or physically impossible: coal at zero from 2030, the offshore-wind roadmap, no nuclear new-build before the late 2030s and electrolysis of about 0.5-3 GW in 2030, with the RFNBO obligation optionally acting as a minimum green share. My own inference is that a bounded electricity import/export option with a price profile is the minimum needed to avoid misstating curtailment and electrolyser utilisation, and that ETS2 needs its own price from 2028 if households and cars stay in the model. An optional water bus, mirroring Walter et al. (2025), would give each region a fresh-water supply with an annual cap and a summer availability profile that drops to 0-50% in drought weather years, a desalination link using 3.7-7.4 kWh/m³ at €0.5-2.5/m³, and electrolysis as a multi-input link consuming 0.18-0.38 m³ per MWh of electricity. Finally, every run should log system cost and the hydrogen marginal price, LCOH by route, electrolyser GW and full-load hours, import share and storage TWh, CO2 emitted and stored, water withdrawn and consumed, subsidy outlay, the shadow price of the electrolysis limit and an infeasibility flag, because these are the metrics the ensemble analysis needs.

## Consolidated input parameters for 2020-2050

The table keeps each source's own price basis in the unit column; convert everything to €2024 before use (see the deflator caveat above). Cells give low / central / high values. Each row carries a status tag:

| Tag | Meaning |
|---|---|
| **[V]** | read in a primary or official source |
| **[S]** | secondary report, headline or abstract only |
| **[D]** | derived or synthesised by the researchers from several sources |
| **[U]** | flagged as unverified in the notes (prior knowledge, extraction conflict or unclear scope) |

The research was compiled on 6-7 October 2026.

| Parameter | Unit | 2020 / 2025 | 2030 (L / C / H) | 2040 (L / C / H) | 2050 (L / C / H) | Source (APA short) | Notes on model use |
|---|---|---|---|---|---|---|---|
| EU ETS1 CO2 price | €/tCO2; history nominal, projections €2024 | 24.6 / 74 | 75 / 110 / 140 | 130 / 180 / 270 (stress 450) | 170 / 250 / 500 (stress 630) | [Umweltbundesamt (2021)](https://www.umweltbundesamt.de/themen/jahresbericht-zu-deutschen-versteigerungen-im-eu); [ICAP (2026)](https://icapcarbonaction.com/en/ets/eu-emissions-trading-system-eu-ets); [PBL (2025a)](https://www.pbl.nl/system/files/document/2025-09/pbl-2025-klimaat-en-energieverkenning-2025-5692.pdf); [Enerdata (2025](https://www.enerdata.net/publications/executive-briefing/carbon-price-projections-eu-ets.html), [2026)](https://www.enerdata.net/publications/executive-briefing/eu-ets-reform-carbon-market-industrial-competitiveness.html); [ENTSO-E & ENTSOG (2025)](https://2024.entsos-tyndp-scenarios.eu/wp-content/uploads/2025/01/TYNDP_2024_Scenarios_Methodology_Report_Final_Version_250128.pdf) | History and KEV 2030 band [V]; 2040-2050 [D]. Price per period on all ETS1 emissions. Under a net-zero cap, report the shadow price against WLO efficient prices (€149-547/t, €2021). |
| ETS2 price (buildings, road fuels) | €2025/tCO2 | n/a (starts 2028) | 57 / 86 / 135 | 57 / 223 / 350 | converge with ETS1 | [PBL (2026c)](https://www.pbl.nl/downloads/pbl-2026-ets2-en-de-gevolgen-voor-huishoudens-5921pdf); [PBL (2025a)](https://www.pbl.nl/system/files/document/2025-09/pbl-2025-klimaat-en-energieverkenning-2025-5692.pdf) | 2030 [V]; 2040 is PBL's mechanical +10%/yr for the middle and high paths [D]. *Corrected 13 October:* PBL keeps the low path flat at the price-stability trigger ("loopt niet op in de tijd", p. 17), so low 2040 is 57, not 148. KEV 2025 uses 57 (band 57-114). Needed because the model includes household gas and cars. |
| Dutch industrial CO2 levy (extra on top of ETS) | €/tCO2 | tariff €30.48 (2021), rising linearly to €125 (2030), minus ETS | 0 (suspended) / 0 / max(ETS, 125) | unknown | unknown | [PBL (2025c)](https://acc.pbl.nl/downloads/pbl-2025-notitie-co2-heffing-industrie-toelichting-ten-behoeve-van-de-overlegtafel-co2-heffing-industrie-5955pdf); [Taxlive (2025)](https://www.taxlive.nl/nl/documenten/vn-vandaag/kabinet-wil-co2-heffing-tijdelijk-opschorten/) | Tariff [V]; suspension status [S]. Sensitivity only. |
| TTF natural gas | €/MWh_HHV; history nominal, projections €2024; ×1.11 for LHV | 9.7 / ≈37.5 | 15 / 24 / 47 (shock 70-75) | 14 / 26 / 40 | 13 / 25 / 38 | [ACER (n.d.-a)](https://aegis.acer.europa.eu/chest/dataitems/744/view); [European Commission (2025)](https://energy.ec.europa.eu/document/download/4aebee79-01e9-4a06-927e-8dd42fc4f9a8_en?filename=New+Quarterly+Report+on+European+gas+markets+Q4+2024.pdf&prefLang=de); [PBL (2025a](https://www.pbl.nl/system/files/document/2025-09/pbl-2025-klimaat-en-energieverkenning-2025-5692.pdf), [2025d)](https://www.wlo2025.nl/system/files/document/2025-07/pbl-2025-toekomstverkenning-wlo-cahier-klimaat-en-energie-5455.pdf); [IEA (2023)](https://iea.blob.core.windows.net/assets/3e076ae9-9055-4af4-bba9-15ddaedcb703/Outlooksforgasmarketsandinvestment.pdf) | 2019-2024 and KEV band [V]; 2025 and 2040-2050 [D]. Excludes CO2. Replaces the cumulative gas reserve. |
| CO2 intensity of natural gas | tCO2/MWh_LHV | 0.20 | 0.20 | 0.20 | 0.20 | Notes (IPCC default, about 56 kg/GJ; not retrieved) | [U]. Matches the current model. |
| Discount rate (WACC) | % | PBL tender: 4.5% debt, 10% equity, 70/30 | 3 / 6 / 10 | same | same | [PBL (2026a)](https://www.pbl.nl/en/downloads/pbl-2026-advice-offshore-wind-tender-2026-5971pdf); [Moret et al. (2017)](https://doi.org/10.1016/j.apenergy.2017.05.106) | Financing terms [V]; range [D]. One of the dominant uncertainties in GSA studies. |
| Electrolyser CAPEX (installed system, excluding grid) | €2024/kW_e | 2025: 1,800 / 2,200 / 3,100 (Dutch FOAK 2,500-3,420) | 1,250 / 1,650 / 2,500 | 800 / 1,250 / 1,800 | 500 / 1,000 / 1,400 | [IEA (2025)](https://iea.blob.core.windows.net/assets/12d92ecc-e960-40f3-aff5-b2de6690ab6b/GlobalHydrogenReview2025.pdf); [ACER (n.d.-b)](https://aegis.acer.europa.eu/chest/dataitems/967/view); [European Hydrogen Observatory (2025)](https://observatory.clean-hydrogen.europa.eu/sites/default/files/2025-11/The%20European%20hydrogen%20market%20landscape_November%202025.pdf); [TNO (2024)](https://zoek.officielebekendmakingen.nl/blg-1145411.pdf) | 2030 central is the IEA 2025 review figure (alkaline 1,274 / PEM 1,647) [V]; ranges [D]. Current model (2,515 / 1,886 / 1,509 / 1,257) lies inside the band. |
| Electrolyser efficiency | % LHV (kWh/kg) | 2025: 57-60 (56-58) | ≈62 (54) | ≈65 (51) | ≈70 (48) | [TNO (2024)](https://zoek.officielebekendmakingen.nl/blg-1145411.pdf); [van Greevenbroek et al. (2025)](https://arxiv.org/pdf/2412.07464) | TNO plant-level 56 kWh/kg [V]; path [D]. Consistent with the model. |
| Electrolyser FOM, life and stack | % CAPEX/yr; years; hours | 2 / 3 / 4%; 25-30 years; stack 55,000-60,000 h | same | same | stack 80,000-100,000 h | [European Hydrogen Observatory (2025)](https://observatory.clean-hydrogen.europa.eu/sites/default/files/2025-11/The%20European%20hydrogen%20market%20landscape_November%202025.pdf); [TNO (2024)](https://zoek.officielebekendmakingen.nl/blg-1145411.pdf) | [V] / [D]. Stack replacement costs 20-30% of CAPEX. Alkaline minimum load 10-40%. |
| Grey SMR | €/kW_H2 (2014-2020 basis) | 600 / 750 / 1,000 | same | same | same | [IEAGHG (2017)](https://ieaghg.org/publications/techno-economic-evaluation-of-smr-based-standalone-merchant-hydrogen-plant-with-ccs/); [Morales-España et al. (2023)](https://doi.org/10.1016/j.ijepes.2023.109686) | [V]. Efficiency 74-76% LHV; FOM 3.6-5%; 9 kgCO2/kg. Escalating to €2024 (+25-35%) is [U]. Model value 867 is consistent. |
| Blue SMR, full capture (89-90%) | €/kW_H2 (2014-2020 basis) | Dutch retrofits from 2026-2027 (process capture, about 50%) | 1,150 / 1,330 / 1,600 | same | same | [IEAGHG (2017)](https://ieaghg.org/publications/techno-economic-evaluation-of-smr-based-standalone-merchant-hydrogen-plant-with-ccs/); [BEIS (2021)](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/1011506/Hydrogen_Production_Costs_2021.pdf); [Air Liquide (n.d.)](https://www.airliquide.com/stories/sustainability/capturing-co2-decarbonize-rotterdams-industrial-basin) | [V] / [D]. Efficiency 69% LHV; residual about 1 kg/kg. Process-only capture: about 880, 74% efficiency, 55-60% capture. ATR: 95% capture, about 79% LHV excluding power; its CAPEX is not verified. |
| CO2 transport and storage tariff | €/tCO2 (about 2022-2024) | Porthos maximum 47.10 | 45 / 55 / 75 | 30 / 45 / 70 | 25 / 40 / 65 | [Algemene Rekenkamer (2024)](https://english.rekenkamer.nl/binaries/rekenkamer-english/documenten/reports/2024/03/28/carbon-storage-under-the-north-sea/PAC21+ENGELS+rapport+Porthos.pdf); [Xodus Group (n.d.)](https://www.eerstekamer.nl/9370000/1/j4nvgs5kjg27kof_j9vvkfvj6b325az/vlutrvd2g2y4) | 2030 anchors [V]; 2040-2050 [U] (learning not sourced). Adds €0.38-0.56/kg H2 at full capture. Model value 0. |
| CO2 storage capacity | MtCO2/yr | 0 before 2027 | 2.5 (Porthos) + 5-7.5 (Aramis launch) | up to 22 (Aramis pipeline) | 22-25 | [Algemene Rekenkamer (2024)](https://english.rekenkamer.nl/binaries/rekenkamer-english/documenten/reports/2024/03/28/carbon-storage-under-the-north-sea/PAC21+ENGELS+rapport+Porthos.pdf); [Gasunie (2025)](https://www.gasunie.nl/en/news/aramis-takes-next-step-towards-investment-decision); [ChemXplore (2026)](https://chemxplore.com/news/aramis-ccs-final-investment-decision); [S&P Global (2026b)](https://www.spglobal.com/energy/en/news-research/latest-news/energy-transition/061726-dutch-porthos-ccs-project-marks-construction-progress-despite-delays) | [V] / [S]. Annual cap on the CO2 storage bus. The Dutch share of Aramis is not fixed. |
| Salt-cavern H2 storage (energy) | €/kWh_H2,LHV | n/a | 0.5 / 0.9 / 1.2 | ≈0.45 / 0.85 / 1.15 (interpolated) | 0.4 / 0.8 / 1.1 | [Clean Hydrogen Partnership (n.d.)](https://www.clean-hydrogen.europa.eu/knowledge-management/strategy-map-and-key-performance-indicators/clean-hydrogen-ju-sria-key-performance-indicators-kpis_en); [Talukdar et al. (2023)](https://doi.org/10.1016/j.isci.2023.108771) | [D]; KPI scope [U]. FOM about 2%; life 40-50 years. Add a compressor link (no verified €/kW). Model value 2.67 for 2030. |
| Salt-cavern capacity available | TWh_H2 | 0 | 0 (first cavern, 0.22 TWh, about 2031) | ≥0.67-0.9 (HyStock, 4 caverns) | 1.5 / 5 / 10 | [Gasunie (n.d.)](https://www.gasunie.nl/en/projects/hystock-hydrogen-storage); [Ministerie van KGG (2025)](https://www.eerstekamer.nl/behandeling/20250704/brief_regering_nationale_agenda/document3/f=/vmp2jywo3tzl.pdf); [TNO (2020)](https://projecten.topsectorenergie.nl/storage/app/uploads/public/618/269/e7b/618269e7bb312950892810.pdf) | [V]; 2040 [D]. Use as `e_nom_max` per period. |
| H2 transport network | €/kg H2 delivered | 2026 tariff €48.71/kW_HHV/yr | 0.20 / 0.40 / 1.20 | 0.15 / 0.30 / 0.60 | 0.15 / 0.30 / 0.60 | [Hynetwork (n.d.)](https://www.hynetwork.nl/en/business/become-a-customer/transport-tariff); [ACM (2025)](https://www.acm.nl/nl/node/27759); [Algemene Rekenkamer (2025)](https://english.rekenkamer.nl/latest/news/2025/12/10/construction-of-sustainable-hydrogen-network-uncertain) | Tariff [V]; adder [D]. The high value is the cost-reflective tariff at 1-1.5 GW of use. Network complete by 2033 at the latest. |
| H2 imports | €/kg; TWh/yr | NEOM ammonia ≈0.2 Mt H2-eq from 2026 | price: pipeline 3.5-6, ship 6-7.5 (pessimistic 13-14); volume 10-30 TWh | volume: 40-70% of green demand (PBL, 2035-2040) | volume 65 / 132 / 300 TWh | [Elzenga et al. (2025)](https://pbl.nl/downloads/pbl-2025-groene-waterstof-de-praktische-uitdagingen-tussen-droom-en-werkelijkheid-5608pdf); [Netbeheer Nederland (2025a](https://www.netbeheernederland.nl/sites/default/files/2025-05/netbeheer_nederland_scenarios_editie_2025_-_def_12-05.pdf), [2026)](https://www.netbeheernederland.nl/sites/default/files/2026-04/verkenningen_netbeheer_nederland_scenarios_editie_2025_0.pdf) | [V]. No import prices for after 2030 were retrieved. Pipeline imports only after about 2032-2033. |
| Dutch H2 demand | Mt H2/yr (TWh_LHV) | 1.3 gross (2020) / 1.05 consumed (2024) | 0.8 / 1.1 / 1.3 (26 / 37 / 43) | total incl. transit 3.4-6.0 (113-201) | domestic 2.3 / 4.8 / 5.3 (78 / 160 / 177) | [Elzenga et al. (2025)](https://pbl.nl/downloads/pbl-2025-groene-waterstof-de-praktische-uitdagingen-tussen-droom-en-werkelijkheid-5608pdf); [European Hydrogen Observatory (2025)](https://observatory.clean-hydrogen.europa.eu/sites/default/files/2025-11/The%20European%20hydrogen%20market%20landscape_November%202025.pdf); [Netbeheer Nederland (2026)](https://www.netbeheernederland.nl/sites/default/files/2026-04/verkenningen_netbeheer_nederland_scenarios_editie_2025_0.pdf) | [V]; Mt conversions [D]. Domestic 2040 split not retrieved. RED III base is 70 PJ (0.84 Mt). |
| Electrolysis capacity (policy and plans) | GW | 0.034 (2024) / HH1 0.2 starting | 0.5 / 1.2 / 3 | 2035: 3-4; NPE 2040: 15-20 | 14 / 35 / 40 | [RVO (2026a)](https://www.rvo.nl/sites/default/files/2026-04/Waterstof%20infographic.pdf); [Netbeheer Nederland (2025a)](https://www.netbeheernederland.nl/sites/default/files/2025-05/netbeheer_nederland_scenarios_editie_2025_-_def_12-05.pdf); [Elzenga et al. (2025)](https://pbl.nl/downloads/pbl-2025-groene-waterstof-de-praktische-uitdagingen-tussen-droom-en-werkelijkheid-5608pdf) | [V]; 2030 low [D]. Use as per-period build caps. About 10 PJ per GW-year. |
| RFNBO obligation (industry) | % of industrial H2 | n/a | 4% (ammonia 1.6%) vs RED III 42% (29 PJ) | 2035: 9.9% vs 60% (42 PJ) | n/a | [Kamerstukken II 36936-3 (2026)](https://zoek.officielebekendmakingen.nl/kst-36936-3.odt); [Ministerie van KGG (2026)](https://berthub.eu/tkconv/getraw/2026D20450) | [V]. Lever: minimum green share. |
| Offshore wind installed | GW | 2.46 / 4.7 | 9.5 / 10.2 / 21 | 21 / 33 / 40 | 40 / 55 / 70 | [CBS (2025)](https://www.cbs.nl/nl-nl/longread/rapportages/2025/hernieuwbare-energie-in-nederland-2024/4-windenergie); [PBL (2026d)](https://www.pbl.nl/system/files/document/2026-09/pbl-2026-klimaat-en-energieverkenning-2026-6050.pdf); [Hermans (2025)](https://www.eerstekamer.nl/behandeling/20250916/brief_regering_actieplan/document3/f=/vmqvpympliy3.pdf); [Netbeheer Nederland (2026)](https://www.netbeheernederland.nl/sites/default/files/2026-04/verkenningen_netbeheer_nederland_scenarios_editie_2025_0.pdf) | Anchors [V]; centrals [D]. The 2030 central counts operating plus under-construction capacity. KM 2050 is 66.6 GW. The 70 GW ambition was not reconfirmed after July 2025. |
| Onshore wind and solar PV | GW | onshore 4.19 / 7.0; PV about 11-13 / 29.4 GWp DC (26 AC) | RES: 42 TWh (38-46) expected; PV 33.6 GW (KEV 2024) | n/a | onshore 13.0 (KM); PV 77-174 GWp (KM 80.4) | [CBS (2025)](https://www.cbs.nl/nl-nl/longread/rapportages/2025/hernieuwbare-energie-in-nederland-2024/4-windenergie); [PBL (2025b)](https://www.pbl.nl/downloads/pbl-2025-monitor-res-2025-5967pdf); [Solar Magazine (2024](https://solarmagazine.nl/nieuws-zonne-energie/i38866/nederland-telt-33-6-gigawatt-zonnepanelen-in-2030-groei-hernieuwbare-energie-blijft-achter), [2025a](https://solarmagazine.nl/nieuws-zonne-energie/i40555/vraag-naar-duurzame-energie-groeit-sneller-dan-aanbod-tot-3-5-keer-meer-stroom-nodig), [2026c)](https://solarmagazine.nl/nieuws-zonne-energie/i44006/cbs-nederland-installeerde-vorig-jaar-1-447-megawattpiek-zonnepanelen) | [V]; PV 2020 [D]. Use AC capacity in PyPSA (DC/AC ≈1.13). |
| Nuclear | GW_e net | 0.485 / 0.485 | 0.485 | 0.485 + 0-2.2 new | 0.485 + 3.7 (KM) to 7 (ambition) | [NEI Magazine (2026)](https://www.neimagazine.com/?p=107843); [World Nuclear Association (n.d.)](https://world-nuclear.org/our-association/publications/world-nuclear-outlook-report/netherlands---world-nuclear-outlook-report) | [V] / [D]. Borssele may run to 2054. |
| Coal | GW | about 4-4.6 [U] / 3.43 | 0 | 0 | 0 | [CBS (2026a)](https://www.cbs.nl/en-gb/figures/detail/86266ENG); [Enerdata (2018)](https://www.enerdata.net/publications/daily-energy-news/netherlands-confirms-phasing-out-coal-fired-power-plants-2030.html) | Legal ban [V]. Hard upper bound of zero. |
| Gas-fired capacity | GW | 17.5 (2024) / 17.4 [U] | about 17 minus 1.7 at risk | n/a | about 2.2 (KM) | [CBS (2026a)](https://www.cbs.nl/en-gb/figures/detail/86266ENG); [Solar Magazine (2025b)](https://solarmagazine.nl/nieuws-zonne-energie/i40567/tennet-wijst-opnieuw-op-risico-stroomtekort-na-2030) | StatLine split [U]. Keep an adequacy check (LOLE 4 h norm). |
| Exogenous electricity demand | TWh/yr | ≈120 / ≈118 | 125 / 130 / 169 | 200 / 250 / 286 | 290 / 344 / 440 | [CBS (2026b)](https://www.cbs.nl/en-gb/news/2026/11/production-and-export-of-electricity-at-record-levels); [Solar Magazine (2024)](https://solarmagazine.nl/nieuws-zonne-energie/i38866/nederland-telt-33-6-gigawatt-zonnepanelen-in-2030-groei-hernieuwbare-energie-blijft-achter); [Netbeheer Nederland (2025b](https://www.netbeheernederland.nl/artikelen/nieuws/netbeheer-nederland-scenarios-editie-2025), [2026)](https://www.netbeheernederland.nl/sites/default/files/2026-04/verkenningen_netbeheer_nederland_scenarios_editie_2025_0.pdf) | [V] / [D]. Subtract endogenous electrolysis from the grid-operator totals. |
| Utility PV | €2025/kW_AC | 595 (2025) | 482 | 403 | 368 | [PyPSA technology-data contributors (2026)](https://github.com/PyPSA/technology-data); [Lensink et al. (2025)](https://zoek.officielebekendmakingen.nl/blg-1231279.pdf) | [V]. FOM 2.2-2.5%/yr. PBL's 517 €/kWp DC is consistent. Ensemble range ±20-30%. |
| Onshore wind | €2025/kW | 1,439 | 1,383 | 1,306 | 1,286 | [PyPSA technology-data contributors (2026)](https://github.com/PyPSA/technology-data) | [V]. FOM €17.8→15.1/kW/yr; VOM €1.6-1.9/MWh. |
| Offshore wind (excluding TenneT grid) | €2025/kW | 2,224 (DEA) to 2,603 (PBL tender) | 2,100 / 2,400 / 2,600 | 1,950 / 2,150 / 2,400 | 1,900 / 2,100 / 2,300 | [PBL (2026a)](https://www.pbl.nl/en/downloads/pbl-2026-advice-offshore-wind-tender-2026-5971pdf); [PyPSA technology-data contributors (2026)](https://github.com/PyPSA/technology-data) | Anchors [V]; ranges [D]. FOM €41-53/kW/yr; life 30-35 years; new-site FLH 3,700-3,760. |
| CCGT / OCGT | €2025/kW; efficiency (LHV) | CCGT 800-1,142, eff. 0.57; OCGT 594, eff. 0.405 | CCGT eff. 0.58; OCGT 581 | 0.59; 566 | 0.60; 550 | [PyPSA technology-data contributors (2026)](https://github.com/PyPSA/technology-data); [EIA (2024)](https://www.eia.gov/analysis/studies/powerplants/capitalcost/pdf/capital_cost_AEO2025.pdf) | [V]. DEA central-high, EIA low. CCGT FOM €12-38/kW/yr. |
| Nuclear new build | €2025/kW_e | n/a | 6,500 / 9,000 / 12,000 | same | same | [EIA (2024)](https://www.eia.gov/analysis/studies/powerplants/capitalcost/pdf/capital_cost_AEO2025.pdf); [PyPSA technology-data contributors (2026)](https://github.com/PyPSA/technology-data) | [D]. FOM €120-160/kW/yr; fuel €7.45/MWh_th. |
| VOM (dispatch) | €/MWh_e | wind 0-2; offshore and PV about 0 (0.01-0.03); CCGT 2-6; OCGT 1-6; nuclear 2.5-4.5; coal about 4 | constant | constant | constant | [PyPSA technology-data contributors (2026)](https://github.com/PyPSA/technology-data); [EIA (2024)](https://www.eia.gov/analysis/studies/powerplants/capitalcost/pdf/capital_cost_AEO2025.pdf) | [V]. Course database is about 100× higher. PV imbalance cost is not VOM. |
| Battery (4 h, all-in) | €2025/kWh | 2025: 150 / 200 / 280 | 100 / 150 / 240 | ≈75 / 120 / 180 (interpolated) | 50 / 90 / 120 | [Energy-Storage.news (2025)](https://www.energy-storage.news/?p=92133); [NREL (2025)](https://docs.nrel.gov/docs/fy25osti/93281.pdf) | [S] / [D]. Round-trip efficiency 85-92%; life 15-20 years; 15-25% of cost is power-related. NL had 0.35 GW / 0.62 GWh (2024). |
| Full-load hours (profile check) | h/yr | offshore 3,290-3,440 existing, 3,700-3,760 new sites; onshore 2,350-2,600; PV 830-890 kWh/kWp DC | n/a | n/a | n/a | [CBS (2025)](https://www.cbs.nl/nl-nl/longread/rapportages/2025/hernieuwbare-energie-in-nederland-2024/4-windenergie); [PBL (2026a](https://www.pbl.nl/en/downloads/pbl-2026-advice-offshore-wind-tender-2026-5971pdf), [2026b)](https://www.pbl.nl/downloads/pbl-2026-eindadvies-sde-plus-plus-2026-5698-1pdf) | Derived from CBS [D]; PBL [V]. Validate weather profiles against these. |
| Electrolysis water intensity | L/kg H2 (m³/MWh_H2) | feed 10-21 (0.30-0.63); with evaporative cooling 17-40; closed-cooling withdrawal about 50-125 | same | same | same | [Folmer et al. (2024)](https://eerstekamer.nl/overig/20241025/onderzoeksrapport_water_voor/document); [Oesterholt et al. (2017)](https://api.kwrwater.nl//uploads/2018/11/BTO-2016.086-De-vraag-naar-water-in-een-waterstofeconomie.Kansen-en-gevolgen-voor-de-drinkwatersector.pdf); [Melaina et al. (2026)](https://www.energy.gov/documents/record-25003-water-use-hydrogen-production) | Per-GW factor via summary [S]; conversions [D]. SMR about 8-12.5 L/kg; blue 24-32 L/kg. |
| Water treatment and desalination | €/kg H2; kWh/m³; €/m³ | 0.01-0.03 €/kg (≤0.10); 3.7-7.4 kWh/m³; €0.5-2.2/m³; brine about 2 m³ per m³ | same | same | same | [Folmer et al. (2024)](https://eerstekamer.nl/overig/20241025/onderzoeksrapport_water_voor/document); [U.S. Department of Energy (2024)](https://www.energy.gov/eere/fuelcells/can-water-usage-electrolysis-pose-problems-parts-united-states-currently-facing); [Vinardell et al. (2025)](https://doi.org/10.1016/j.nexus.2025.100457); [Walter et al. (2023)](https://iewt2023.eeg.tuwien.ac.at/download/contribution/fullpaper/8/8_fullpaper_20230210_174238.pdf) | [V] / [S] / [D]. Desalination link on the water bus. |
| Water-driven availability of electrolysis | % of potential output | coastal 100; inland ≈95-100 (current climate) | medium scarcity 95-98 (inland 85-95) | high scarcity: inland 75-90, coastal about 100 | as 2040, with drier KNMI'23 summers | [Folmer et al. (2024)](https://eerstekamer.nl/overig/20241025/onderzoeksrapport_water_voor/document); [Hermans (2024)](https://eerstekamer.nl/9370000/1/j4nvi0xeni9vr2l_j9vvkfvj6b325az/vmie42e6ffwd/f=/vmhv413eyuv6.pdf); [Ministerie van IenW (2026)](https://zoek.officielebekendmakingen.nl/kst-1264000.pdf) | [D] synthesis, not an official figure. This is the physical counterpart to S1-S3. |

## Designing an ensemble that maps failure rather than forecasting the future

### XLRM turns S1-S3 into levers rather than futures

Exploratory modelling treats each model run as a computational experiment. It analyses thousands of such runs to find where options succeed or fail, rather than relying on a single best-estimate forecast ([Kwakkel, 2017](https://doi.org/10.1016/j.envsoft.2017.06.054); [Marchau et al., 2019](https://doi.org/10.1007/978-3-030-05252-2)). The standard frame is XLRM:

| Element | Meaning | In this model |
|---|---|---|
| X | external uncertainties | the price, cost, demand, availability and water inputs in the range table below |
| L | policy levers | the electrolysis share, framed as S1-S3 or as the fresh-water share; capital subsidy 0, 40 or 80% of CAPEX; RFNBO minimum 4% or 42%; optionally, desalination investment |
| R | the model's relationships | the PyPSA network build plus `n.optimize()` |
| M | metrics | system cost, hydrogen marginal price and LCOH by route, electrolyser GW and full-load hours, import share, storage TWh, CO2 emitted and stored, water use, subsidy outlay, and the shadow price of the electrolysis limit |

The fixes in the previous section, such as the VOM convention, no gas reserve and per-period prices, are corrections, not uncertainties. They must be applied before any sampling.

### Ranges should be wide, per parameter and sampled as paths

The standard choice under deep uncertainty is independent uniform sampling over deliberately wide ranges, using Latin hypercube or low-discrepancy sequences ([Neumann & Brown, 2023](https://doi.org/10.1016/j.isci.2023.106702); [EMA Workbench developers, n.d.](https://emaworkbench.readthedocs.io/en/latest/indepth_tutorial/open-exploration.html)). The fraction of runs in which an outcome occurs is not a probability. Changing the assumed input distribution changes both the robustness scores and the vulnerabilities that scenario discovery finds ([Reis & Shortridge, 2020](https://doi.org/10.1111/risa.13405)). Ranges must be set per parameter: a blanket ±X% gives "a fundamentally different parameter ranking" ([Moret et al., 2017](https://doi.org/10.1016/j.apenergy.2017.05.106)).

Sampling each trajectory as one index that interpolates between its low path and its high path is my recommendation. It keeps the dimension near 15 and avoids implausible zig-zag paths. The evidence shows CO2 and gas can decouple, so sample them independently, then add explicit stress corners: high CO2 with cheap gas, low CO2 with expensive gas, and a 2030 gas shock. Gas and CO2 correlation is not otherwise handled in the DMDU literature retrieved.

| Uncertain input | Unit | Low | High | Rationale |
|---|---|---|---|---|
| ETS1 CO2 path (index for 2030 / 2040 / 2050) | €2024/t | 75 / 130 / 170 | 140 / 270 / 500 | KEV 2025 band; Enerdata and TYNDP lows; current-law and analyst highs; stress corners 450 (2040) and 630 (2050) ([PBL, 2025a](https://www.pbl.nl/system/files/document/2025-09/pbl-2025-klimaat-en-energieverkenning-2025-5692.pdf); [Enerdata, 2026](https://www.enerdata.net/publications/executive-briefing/eu-ets-reform-carbon-market-industrial-competitiveness.html)) |
| TTF gas path (2030 / 2040 / 2050) | €2024/MWh_HHV | 15 / 14 / 13 | 47 / 40 / 38 | KEV band; IEA NZE and TYNDP lows; REF2020 and WLO highs; 2030 shock corner at €70-75 ([Trading Economics, 2026b](https://tradingeconomics.com/commodity/eu-natural-gas)) |
| Electrolyser CAPEX path (2030 / 2040 / 2050) | €2024/kW_e | 1,250 / 800 / 500 | 2,500 / 1,800 / 1,400 | IEA 2025 forecast and learning lows; Dutch first-of-a-kind highs; IEA 2030 forecasts more than doubled since 2022 ([ACER, n.d.-b](https://aegis.acer.europa.eu/chest/dataitems/967/view)) |
| Electrolyser efficiency in 2050 | % LHV | 64 | 74 | TNO's 56 kWh/kg today; the 48 kWh/kg KPI; my synthesis |
| Electrolyser FOM | % CAPEX/yr | 2 | 4 | EHO 2.0%, TNO 3.8%, DEA 4% |
| Blue route (categorical) | capture configuration | process capture 55-60% (≈€880/kW_H2) | full 90% (€1,150-1,600) or ATR 95% | Residual CO2 about 4 vs about 1 kg/kg ([IEAGHG, 2017](https://ieaghg.org/publications/techno-economic-evaluation-of-smr-based-standalone-merchant-hydrogen-plant-with-ccs/)) |
| CO2 transport and storage tariff | €/t | 25 | 75 | Porthos €47.10, Aramis €67-72; the low end is an unsourced learning assumption |
| CO2 storage capacity (2030 / 2050) | Mt/yr | 2.5 / 10 | 10 / 25 | Porthos only vs Porthos plus a full Aramis ramp-up |
| Salt-cavern storage cost | €/kWh | 0.4 | 2.7 | Clean Hydrogen KPI vs current PyPSA technology-data value |
| Salt-cavern capacity in 2050; availability in the 2030 period | TWh | 1.5; 0 | 10; 0.22 | TNO 2020 vs 40 caverns; first cavern about 2031 |
| H2 network adder | €/kg | 0.15 | 1.20 | Tariff at baseload vs cost-reflective tariff at 1-1.5 GW of use ([ACM, 2025](https://www.acm.nl/nl/node/27759)) |
| H2 import price | €/kg | 3.5 | 7.5 (stress 14) | Pipeline (Spain, Tunisia) vs ship ([Elzenga et al., 2025](https://pbl.nl/downloads/pbl-2025-groene-waterstof-de-praktische-uitdagingen-tussen-droom-en-werkelijkheid-5608pdf)) |
| H2 import availability (2030 / 2050) | TWh/yr | 0 / 65 | 30 / 300 | No pipeline before 2032-2033; KM_IW vs grid-operator maximum |
| Domestic H2 demand (2030 / 2050) | Mt/yr | 0.8 / 2.3 | 1.3 / 5.3 | KM_IW vs PBL's 630 PJ ([Netbeheer Nederland, 2026](https://www.netbeheernederland.nl/sites/default/files/2026-04/verkenningen_netbeheer_nederland_scenarios_editie_2025_0.pdf)) |
| Exogenous electricity demand in 2050 | TWh/yr | 290 | 440 | II3050 range, net of endogenous electrolysis |
| Offshore wind buildable (2030 / 2040 / 2050) | GW | 9.5 / 21 / 40 | 21 / 40 / 70 | KEV 2026 baseline vs legacy targets ([PBL, 2026d](https://www.pbl.nl/system/files/document/2026-09/pbl-2026-klimaat-en-energieverkenning-2026-6050.pdf)) |
| Offshore wind CAPEX in 2030 | €2025/kW | 2,100 | 2,600 | DEA vs PBL 2026 tender advice |
| PV and onshore wind CAPEX | multiplier on central value | 0.7 | 1.25 | DEA optimistic and pessimistic ranges; past projections were too pessimistic ([Haas et al., 2025](https://doi.org/10.1016/j.apenergy.2025.125856)) |
| Battery 4 h cost (2030 / 2050) | €2025/kWh | 100 / 50 | 240 / 120 | BNEF and Ember vs DEA |
| New nuclear in 2050 | GW_e | 0 | 7 | Programme failure vs government ambition |
| WACC | % real | 3 | 10 | Economic parameters dominate GSA results ([Moret et al., 2017](https://doi.org/10.1016/j.apenergy.2017.05.106)); 52% of LCOH variance in one study ([Coppitters et al., 2019](https://doi.org/10.1016/j.apenergy.2019.04.101)) |
| Weather year (categorical) | year | n/a | n/a | At least three years, including a low-wind winter and a hot, dry summer like 2018 or 2022 |
| Inland, fresh-water-dependent share of electrolysis | % | 0 | 30 | Coastal sites have sea or brackish water ([Folmer et al., 2024](https://eerstekamer.nl/overig/20241025/onderzoeksrapport_water_voor/document)) |
| Summer restriction on fresh-water intake | months/yr | 0 | 3 | About 1 declaration in 4 years; KNMI'23 projects drier summers |
| Water intensity including cooling | L/kg | 10 | 120 | Feed only vs closed-cooling withdrawal |
| Treatment or desalination cost | €/m³ | 0.5 | 2.5 | [Folmer et al. (2024)](https://eerstekamer.nl/overig/20241025/onderzoeksrapport_water_voor/document); [Vinardell et al. (2025)](https://doi.org/10.1016/j.nexus.2025.100457) |

The last four rows are active only in a water-bus variant of the model. Without that bus, S1-S3 remain the water lever.

### A phased run budget fits a 1-5 minute model

The SALib run-count formulas are as follows ([SALib developers, n.d.](https://salib.readthedocs.io/en/main/api/SALib.sample.html)):

| Design | Runs |
|---|---|
| Sobol, without second-order indices | N(D+2) |
| Sobol, with second-order indices | N(2D+2) |
| Morris | r(D+1) |

PyPSA's own GSA example re-optimises a copied network for each sample and recommends 64 or more Sobol samples for real analysis ([PyPSA developers, n.d.](https://docs.pypsa.org/stable/examples/gsa/)). Benchmarks on a 13-parameter model found that Morris screening identified the important parameters in about 280 runs, tree- and regression-based screening needed about 400-600 runs, and Sobol needed at least 1,050 ([Gan et al., 2014](https://doi.org/10.1016/j.envsoft.2013.09.031)). Convergence is case-dependent, so check it by bootstrapping rather than assuming it ([Sarrazin et al., 2016](https://doi.org/10.1016/j.envsoft.2016.02.005)). A polynomial-chaos surrogate of a PyPSA-Eur model with five inputs reached acceptable accuracy with 50-200 samples ([Neumann & Brown, 2023](https://doi.org/10.1016/j.isci.2023.106702)).

| Phase | Design | Runs (D about 12-15) | Purpose | Tool |
|---|---|---|---|---|
| 0. Pilot | 50 Latin-hypercube runs | 50 | Debug infeasibilities, runtime and output logging | EMA Workbench |
| 1. Screen | Morris, r = 10-20, judged on the median of elementary effects | 130-320 | Drop non-influential inputs | SALib |
| 2. Ensemble | 500-1,000 Latin-hypercube runs under the reference policy | 500-1,000 | Feature scoring, scatter plots, PRIM | EMA Workbench |
| 3. Policy comparison | Same futures × 9 policies (S1-S3 × 0/40/80% subsidy) | 4,500-9,000 | Regret, satisficing, parallel coordinates | EMA Workbench |
| 4. Quantify | Sobol on the top 4-5 inputs (D = 5, N = 128 gives 896 runs), or a surrogate trained on phase-2 runs | 0-900 | Variance shares, interactions | SALib, chaospy |
| 5. Stress and adapt | Corner cases, fix-and-dispatch runs, 2-D sweeps | 100-300 | Adaptation tipping points, robustness of committed plans | PyPSA |

At 3 minutes per solve with 8 single-threaded workers, about 160 runs an hour, the 4,500-run policy comparison takes about 28 hours (derived). The Morris statistic should be the median, because the mean "can be unstable" at small samples ([Menberg et al., 2016](https://doi.org/10.1016/j.enbuild.2016.10.005)).

Every run should return NaN and an infeasibility flag rather than crash the batch. Solver threads should be fixed at 1 so that parallel PyPSA solves do not compete for cores and memory.

### Sensitivity analysis must cope with regime switches

PyPSA outputs switch between regimes, for example electrolysers versus imports, or storage built versus not built, which makes them skewed or multi-modal, so each method has a distinct role. Extra-trees feature scoring works on the same Latin-hypercube sample, approximates Sobol total-effect rankings better than Morris and handles categorical inputs such as the weather year ([Jaxa-Rozen & Kwakkel, 2018](https://doi.org/10.1016/j.envsoft.2018.06.011)). PAWN, a moment-independent method suited to skewed outputs, also works from a generic sample ([Pianosi & Wagener, 2018](https://doi.org/10.1016/j.envsoft.2018.07.019)), but it is sensitive to its tuning parameters ([Puy et al., 2020](https://doi.org/10.1016/j.envsoft.2020.104679)), so include a dummy input as a screening threshold. Sobol indices should be computed only on the few dominant inputs, or on a surrogate.

The visual layer is simple but essential: pairs scatter plots of the outcomes coloured by policy, scatter plots of each key outcome (LCOH, electrolyser GW, import share) against its top two drivers, and regional-sensitivity CDF plots that split runs at a policy-relevant threshold, all of which are built into the EMA Workbench ([EMA Workbench developers, n.d.](https://emaworkbench.readthedocs.io/en/latest/indepth_tutorial/open-exploration.html)).

The literature gives a hypothesis to test rather than assume. The discount rate, demand, import price or availability, the carbon budget and expansion limits tend to dominate system-level outcomes, while technology CAPEX matters less ([Moret et al., 2017](https://doi.org/10.1016/j.apenergy.2017.05.106); [Grimm et al., 2026](https://doi.org/10.1016/j.enpol.2025.115044)). In hydrogen-specific studies, the annualised costs of electrolysers, storage and pipelines, together with domestic hydrogen demand, rank highest ([Rubino et al., 2026](https://doi.org/10.1016/j.ijhydene.2026.153822)).

### Scenario discovery names the conditions under which each option fails

Scenario discovery uses data mining to find "easy-to-interpret combinations of uncertain model input parameters" that predict policy-relevant outcomes ([Bryant & Lempert, 2010](https://doi.org/10.1016/j.techfore.2009.08.002)). Candidate failure definitions for this study are green LCOH above €8/kg (the government's assumed premium) in 2030 or 2040, domestic electrolysis below 3 GW in 2035, cost regret above 5% relative to the best option in the same future, a binding CO2-storage cap, and fresh-water use above a regional cap.

PRIM finds boxes in input space that trade coverage (the share of failures captured) against density (the share of cases in the box that are failures). Its trade-off curve should be inspected rather than taking a single box. CART is the tree-based alternative, and both "often imperfectly" capture the cases ([Lempert et al., 2008](https://consensus.app/papers/details/eda07246690751e48102fd3a104d522e/)). Several refinements help: bagging random boxes guards against PRIM's hill-climbing defects ([Kwakkel & Cunningham, 2016](https://consensus.app/papers/details/311cee2281b15f8899ca976dc11f3bcf/)), a Gini objective handles outcomes with more than two classes, such as the dominant supply route ([Kwakkel & Jaxa-Rozen, 2016](https://doi.org/10.1016/j.envsoft.2015.11.020)), and dimensional stacking gives a quick first visual pass.

Expected boxes include "high CO2 and low gas and imports available", which should favour imports over domestic electrolysis, and "CO2 storage capped at Porthos and low CO2 price", which should keep grey hydrogen in the mix.

### Trade-offs, robustness and vulnerability

Multi-objective trade-offs are best shown with parallel-coordinates plots. Each axis is one outcome: system cost, CO2, water use, subsidy outlay, import dependence and the hydrogen price. One line is drawn per run, or per policy's robustness score. Interactive trade-off visualisation of this kind is central to many-objective robust decision making ([Kasprzyk et al., 2013](https://doi.org/10.1016/j.envsoft.2012.12.007)).

Robustness metrics differ in whether they use absolute performance or regret, in their level of risk aversion, and in whether they reward high performance or low spread ([McPhail et al., 2018](https://doi.org/10.1002/2017EF000649)), and different metrics can rank the same options differently ([Giuliani & Castelletti, 2016](https://doi.org/10.1007/s10584-015-1586-9)). Report several side by side: the mean, the 90th-percentile cost, the maximum and 90th-percentile regret (the cost of a policy in a future minus the cheapest policy's cost in that same future), and a satisficing share, the fraction of futures in which LCOH, emissions, water and subsidy budgets all meet their targets. Regret needs a full factorial design, with every policy run on the same futures.

Two robustness tests answer different questions. Re-optimising every future measures how sensitive the optimal system is. Fixing the capacities from a reference run and re-dispatching across futures measures how robust a committed plan is. A Dutch-relevant hub study took the second route and found that more electrolysis raised costs but reduced sensitivity to disruptions, while relying early on a European hydrogen network was cheaper but less resilient ([Jodry et al., 2026](https://doi.org/10.1016/j.enpol.2026.115258)).

The PRIM boxes in which a policy fails are its vulnerabilities, and they double as candidate signposts to monitor. Behaviour can be highly sensitive without being structurally vulnerable ([Tangi et al., 2026](https://doi.org/10.1016/j.rset.2026.100139)), so separate the inputs that move costs from those that change the chosen technologies.

### Adaptive pathways and clustering

Dynamic Adaptive Policy Pathways (DAPP) commit to short-term actions, find the adaptation tipping point at which each action stops meeting its objectives, map alternative sequences of actions as a "metro map", and define signposts and triggers early enough to act in time ([Haasnoot et al., 2013](https://doi.org/10.1016/j.gloenvcha.2012.12.006)). Scenario discovery supplies multi-dimensional tipping points that can become technical signposts ([Ramm et al., 2018](https://doi.org/10.1016/j.envsci.2018.06.001)). Signposts should be measurable, timely and institutionally connected ([Haasnoot et al., 2018](https://doi.org/10.1016/j.gloenvcha.2018.08.003)).

Two pathways suit this model. For water, compare fresh water only, water-efficient cooling, brackish treatment and seawater desalination, and find each option's tipping point in drought frequency × hydrogen demand; the signpost is observed drought declarations or permit-curtailment days, and the trigger must leave enough lead time to permit and build desalination. For electrolysis, commit to the funded 1.2 GW now and scale towards 3-4 GW in 2035 only if signposts show the network on its 2033 path, CO2 prices above a threshold and import prices above domestic cost. A myopic sequence of 2030, 2040 and 2050 runs that fixes earlier capacities captures the path dependency that one-shot optimisation hides.

Clustering the standardised outcome vectors with k-means, agglomerative or spectral methods reveals system archetypes, for example import-heavy, domestic-electrolysis and blue-heavy systems. Running PRIM on each cluster then describes the conditions that produce it ([Steinmann et al., 2020](https://doi.org/10.1016/j.techfore.2020.120052); [Jaxa-Rozen et al., 2021](https://doi.org/10.1007/s11367-021-01921-1)).

Cost-optimal results also hide near-optimal alternatives. One study found many very different system configurations within a few percent of the optimal cost ([Neumann & Brown, 2023](https://doi.org/10.1016/j.isci.2023.106702)). A light near-optimal check, finding the minimum and maximum electrolyser capacity within 5% cost slack in a handful of representative futures, shows whether electrolyser conclusions survive near-optimality ([Pickering et al., 2022](https://doi.org/10.1016/j.joule.2022.05.009)).

## Conclusion

The evidence shifts the question the model should answer. Nearly every Dutch hydrogen milestone has slipped in four years: electrolysis for 2030 fell from 4 GW (with 6-8 GW once proposed) to 1.2 GW, the national network moved from 2030 to 2033, Porthos from 2026 to 2027, the first HyStock cavern from 2028 to 2031, the 2040 offshore wind target from 50 GW to 30-40 GW after a 1 GW tender drew zero bids, and the first new reactor from 2035 to the late 2030s. Timing and availability are therefore more decision-relevant uncertainties than any single cost. In 2030, deployment rather than water caps green hydrogen at about 8-9% of demand, so S1, S2 and S3 should barely differ in that year; their real divergence lies in 2040-2050, exactly where demand, imports and CO2-storage capacity are most uncertain. The ensemble should therefore sample availability dates and build caps as well as prices, and scenario discovery should look specifically for "delay" boxes.

Reframing the water parameter makes the study sharper, not weaker. As a policy or social-licence stress test, S1 and S3 measure what a restriction on electrolysis costs the system, and the shadow price of the electrolysis limit becomes the headline output. Once the VOM, gas and carbon artefacts are fixed, that shadow price can be compared directly with three yardsticks: the €0.01-0.03/kg cost of desalinated feed water, the €8/kg green premium the government assumes, and the €1.2-2.5 m/MW that OWE rounds have paid. If restricting electrolysis consistently costs more than coastal siting with desalination, the ensemble has a robust, monitorable finding; if it costs more only where the inland fresh-water share and summer restrictions are high, the finding is a siting rule rather than a national limit on electrolysis.

## References

Entries marked * have author lists abbreviated in the research notes (first author only from Consensus metadata). Complete them from the DOI before publication. Volume and page numbers were not verified for most peer-reviewed items.

Air Liquide. (n.d.). *Capturing CO2 to decarbonize Rotterdam's industrial basin*. https://www.airliquide.com/stories/sustainability/capturing-co2-decarbonize-rotterdams-industrial-basin

Air Liquide. (2025, July 23). *Air Liquide takes final investment decision to build ELYgator, a large-scale electrolyzer in the Netherlands* [Press release]. https://www.airliquide.com/group/press-releases-news/2025-07-23/air-liquide-takes-final-investment-decision-build-elygator-large-scale-electrolyzer-netherlands

Algemene Rekenkamer. (2024). *Carbon storage under the North Sea: On profits under water*. https://english.rekenkamer.nl/binaries/rekenkamer-english/documenten/reports/2024/03/28/carbon-storage-under-the-north-sea/PAC21+ENGELS+rapport+Porthos.pdf

Algemene Rekenkamer. (2025, December 10). *Construction of sustainable hydrogen network uncertain*. https://english.rekenkamer.nl/latest/news/2025/12/10/construction-of-sustainable-hydrogen-network-uncertain

Autoriteit Consument & Markt [ACM]. (2025, May 1). *Marktrapportage waterstof: Tarieven waterstoftransportnet*. https://www.acm.nl/nl/node/27759

Bryant, B. P., & Lempert, R. J. (2010). Thinking inside the box: A participatory, computer-assisted approach to scenario discovery. *Technological Forecasting and Social Change, 77*(1), 34-49. https://doi.org/10.1016/j.techfore.2009.08.002

Business Today. (2026, September 26). *European gas prices may stay elevated this winter as LNG disruptions persist: Goldman Sachs*. https://www.businesstoday.in/amp/world/story/european-gas-prices-may-stay-elevated-this-winter-as-lng-disruptions-persist-goldman-sachs-557961-2026-09-26

Carbon Pulse. (2026a, September 9). *Bank sees EUAs at €180-270 by 2040 under Commission ETS reform proposal*. https://carbon-pulse.com/548718/

Carbon Pulse. (2026b, October 2). *Marginal carbon costs to hit €470/t by 2040 under EU ETS package, modelling suggests*. https://carbon-pulse.com/556730/

Centraal Bureau voor de Statistiek [CBS]. (2025). *Hernieuwbare energie in Nederland 2024: 4. Windenergie*. https://www.cbs.nl/nl-nl/longread/rapportages/2025/hernieuwbare-energie-in-nederland-2024/4-windenergie

Centraal Bureau voor de Statistiek [CBS]. (2026a). *Electricity and heat; production, input, and capacity by energy commodity* [StatLine table 86266ENG]. https://www.cbs.nl/en-gb/figures/detail/86266ENG

Centraal Bureau voor de Statistiek [CBS]. (2026b, March 9). *Production and export of electricity at record levels*. https://www.cbs.nl/en-gb/news/2026/11/production-and-export-of-electricity-at-record-levels

Centraal Bureau voor de Statistiek [CBS]. (2026c). *Watergebruik binnen de Nederlandse economie; Milieurekeningen* [StatLine table 82883NED]. https://www.cbs.nl/nl-nl/cijfers/detail/82883NED

ChemXplore. (2026, September 3). *Gasunie & EBN ready Aramis for FID and execution leadership*. https://chemxplore.com/news/aramis-ccs-final-investment-decision

*Chyong, C. K., et al. (2026). Stress-testing the EU energy system: Modeling resilience without Russian gas. *iScience*, 115866. https://doi.org/10.1016/j.isci.2026.115866

Clean Hydrogen Partnership. (n.d.). *Clean Hydrogen JU SRIA key performance indicators (KPIs)*. https://www.clean-hydrogen.europa.eu/knowledge-management/strategy-map-and-key-performance-indicators/clean-hydrogen-ju-sria-key-performance-indicators-kpis_en

ClearBlue Markets. (2026, July 23). *The EU ETS review proposal July 2026: Relief for industry, stability for the market*. https://www.clearbluemarkets.com/knowledge-base/the-eu-ets-review-proposal-july-2026-relief-for-industry-stability-for-the-market

Coppitters, D., De Paepe, W., & Contino, F. (2019). Surrogate-assisted robust design optimization and global sensitivity analysis of a directly coupled photovoltaic-electrolyzer system under techno-economic uncertainty. *Applied Energy, 248*, 310-320. https://doi.org/10.1016/j.apenergy.2019.04.101

CPB Netherlands Bureau for Economic Policy Analysis & PBL Netherlands Environmental Assessment Agency. (2025a). *Toekomstverkenning WLO 2025: Efficiënte CO2-prijzen* (PBL publicatienummer 5916). https://www.wlo2025.nl/system/files/document/2025-07/cpb-pbl-2025-toekomstverkenning-wlo-efficiente-co2-prijzen-5916.pdf

CPB Netherlands Bureau for Economic Policy Analysis & PBL Netherlands Environmental Assessment Agency. (2025b). *WLO 2025: Update efficiënte CO2-prijzen per 2026*. https://www.wlo2025.nl/system/files/document/2025-12/cpb-pbl-publicatie-wlo2025-update-efficiente-co2-prijzen-per-2026.pdf

Danish Energy Agency. (2024). *Technology brief: Hydrogen production via electrolysis*. https://ens.dk/media/4254/download

*de Vries, J., et al. (2026). Structuring hydrogen storage networks: Matching geological capacity with future demand in the Northern Netherlands. *International Journal of Hydrogen Energy*, 152686. https://doi.org/10.1016/j.ijhydene.2025.152686

Department for Business, Energy & Industrial Strategy [BEIS]. (2021). *Hydrogen production costs 2021*. https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/1011506/Hydrogen_Production_Costs_2021.pdf

Elzenga, H., Eggink, E., & de Joode, J. (2025). *Groene waterstof: De praktische uitdagingen tussen droom en werkelijkheid*. PBL Planbureau voor de Leefomgeving. https://pbl.nl/downloads/pbl-2025-groene-waterstof-de-praktische-uitdagingen-tussen-droom-en-werkelijkheid-5608pdf

EMA Workbench developers. (n.d.). *Open exploration* [Tutorial]. EMA Workbench documentation. Retrieved October 7, 2026, from https://emaworkbench.readthedocs.io/en/latest/indepth_tutorial/open-exploration.html

Enerdata. (2018, May 21). *Netherlands confirms phasing out coal-fired power plants by 2030*. https://www.enerdata.net/publications/daily-energy-news/netherlands-confirms-phasing-out-coal-fired-power-plants-2030.html

Enerdata. (2025, November 27). *Carbon price forecast 2030-2050: Assessing market stability & future challenges* [Executive briefing]. https://www.enerdata.net/publications/executive-briefing/carbon-price-projections-eu-ets.html

Enerdata. (2026, August 6). *EU ETS reform 2026: Carbon market and industry impacts* [Executive briefing]. https://www.enerdata.net/publications/executive-briefing/eu-ets-reform-carbon-market-industrial-competitiveness.html

Energy News. (2026, July 21). *The Netherlands commits €450 million to hydrogen storage*. https://energynews.biz/the-netherlands-commits-e450-million-to-hydrogen-storage-as-it-tackles-a-critical-gap-in-green-hydrogen-infrastructure/?amp=1

Energy-Storage.news. (2025, December 16). *Battery storage system prices continue to fall sharply, BNEF and Ember reports find*. https://www.energy-storage.news/?p=92133

ENTSO-E & ENTSOG. (2025). *TYNDP 2024 scenarios methodology report* (Final version, January 2025). https://2024.entsos-tyndp-scenarios.eu/wp-content/uploads/2025/01/TYNDP_2024_Scenarios_Methodology_Report_Final_Version_250128.pdf

European Commission, Directorate-General for Energy. (2025). *Quarterly report on European gas markets, Q4 2024* (Market Observatory for Energy, Vol. 17). https://energy.ec.europa.eu/document/download/4aebee79-01e9-4a06-927e-8dd42fc4f9a8_en?filename=New+Quarterly+Report+on+European+gas+markets+Q4+2024.pdf&prefLang=de

European Hydrogen Observatory. (2025, November). *The European hydrogen market landscape: November 2025*. Clean Hydrogen Partnership. https://observatory.clean-hydrogen.europa.eu/sites/default/files/2025-11/The%20European%20hydrogen%20market%20landscape_November%202025.pdf

European Union Agency for the Cooperation of Energy Regulators [ACER]. (n.d.-a). *Average prices of key international gas benchmarks, 2019-2024 (EUR/MWh)* [Data item 744]. AEGIS CHEST. Retrieved October 7, 2026, from https://aegis.acer.europa.eu/chest/dataitems/744/view

European Union Agency for the Cooperation of Energy Regulators [ACER]. (n.d.-b). *Investment costs for electrolysers (IEA Global Hydrogen Review 2022-2025 compilation)* [Data item 967]. AEGIS CHEST. https://aegis.acer.europa.eu/chest/dataitems/967/view

Folmer, I., Rastegarian, H., Boons, B., Busking, T., Lenzen, K., Kuin, P., & Leeuwis, J. (2024). *Water voor waterstof* [Report, Royal HaskoningDHV, July 9, 2024; sent to Parliament October 25, 2024]. https://eerstekamer.nl/overig/20241025/onderzoeksrapport_water_voor/document

*Galletti, A., et al. (2025). Learning in green hydrogen production: Insights from a novel European dataset. *International Journal of Hydrogen Energy*. https://doi.org/10.1016/j.ijhydene.2025.06.002

Gan, Y., Duan, Q., Gong, W., Tong, C., Sun, Y., Chu, W., Ye, A., Miao, C., & Di, Z. (2014). A comprehensive evaluation of various sensitivity analysis methods: A case study with a hydrological model. *Environmental Modelling & Software, 51*, 269-285. https://doi.org/10.1016/j.envsoft.2013.09.031

Gasunie. (n.d.). *HyStock hydrogen storage*. https://www.gasunie.nl/en/projects/hystock-hydrogen-storage

Gasunie. (2024, December 16). *National hydrogen network roll-out plan updated*. https://www.gasunie.nl/en/news/national-hydrogen-network-roll-out-plan-updated-2

Gasunie. (2025). *Aramis takes next step towards investment decision*. https://www.gasunie.nl/en/news/aramis-takes-next-step-towards-investment-decision

Giuliani, M., & Castelletti, A. (2016). Is robustness really robust? How different definitions of robustness impact decision-making under climate change. *Climatic Change, 135*, 409-424. https://doi.org/10.1007/s10584-015-1586-9

*Grimm, G., et al. (2026). Uncertainties in the German energy transition: Detecting robust solutions under shock events in long-term transformation pathways. *Energy Policy*, 115044. https://doi.org/10.1016/j.enpol.2025.115044

*Haas, J., et al. (2025). Are we too pessimistic? Cost projections for solar photovoltaics, wind power, and batteries are over-estimating actual costs globally. *Applied Energy*. https://doi.org/10.1016/j.apenergy.2025.125856

Haasnoot, M., Kwakkel, J. H., Walker, W. E., & ter Maat, J. (2013). Dynamic adaptive policy pathways: A method for crafting robust decisions for a deeply uncertain world. *Global Environmental Change, 23*(2), 485-498. https://doi.org/10.1016/j.gloenvcha.2012.12.006

Haasnoot, M., van 't Klooster, S., & van Alphen, J. (2018). Designing a monitoring system to detect signals to adapt to uncertain climate change. *Global Environmental Change, 52*, 273-285. https://doi.org/10.1016/j.gloenvcha.2018.08.003

Hermans, S. T. M. (2024, October 25). *Kamerbrief over hernieuwbare waterstof en waterbeschikbaarheid*. Ministerie van Klimaat en Groene Groei. https://eerstekamer.nl/9370000/1/j4nvi0xeni9vr2l_j9vvkfvj6b325az/vmie42e6ffwd/f=/vmhv413eyuv6.pdf

Hermans, S. T. M. (2025, September 16). *Actieplan windenergie op zee* [Letter to Parliament]. Ministerie van Klimaat en Groene Groei. https://www.eerstekamer.nl/behandeling/20250916/brief_regering_actieplan/document3/f=/vmqvpympliy3.pdf

Hydrogen Europe. (2025). *Boosting renewable hydrogen: The Commission selects 15 projects to receive nearly €1 billion*. https://hydrogeneurope.eu/boosting-renewable-hydrogen-the-commission-selects-15-projects-to-receive-nearly-e1-billion/

Hynetwork. (n.d.). *Transport tariff for the national hydrogen network*. Retrieved October 2026, from https://www.hynetwork.nl/en/business/become-a-customer/transport-tariff

HyStock. (2023, July 24). *Successful open season: Ample interest in hydrogen storage first salt cavern HyStock*. https://www.hystock.nl/en/news/successful-open-season-ample-interest-in-hydrogen-storage-first-salt-cavern-hystock

IEAGHG. (2017). *Techno-economic evaluation of SMR based standalone (merchant) hydrogen plant with CCS* (Technical Report 2017/02). https://ieaghg.org/publications/techno-economic-evaluation-of-smr-based-standalone-merchant-hydrogen-plant-with-ccs/

Informatiepunt Leefomgeving [IPLO]. (n.d.). *Verdringingsreeks: Rangorde bij waterschaarste*. Retrieved October 7, 2026, from https://iplo.nl/thema/water/beheer-watersysteem/verdringingsreeks/

International Carbon Action Partnership [ICAP]. (2026). *EU Emissions Trading System (EU ETS)* [ETS detailed information]. Retrieved October 7, 2026, from https://icapcarbonaction.com/en/ets/eu-emissions-trading-system-eu-ets

International Energy Agency [IEA]. (2023). *Outlooks for gas markets and investment: A report for the G7*. https://iea.blob.core.windows.net/assets/3e076ae9-9055-4af4-bba9-15ddaedcb703/Outlooksforgasmarketsandinvestment.pdf

International Energy Agency [IEA]. (2025). *Global hydrogen review 2025*. https://iea.blob.core.windows.net/assets/12d92ecc-e960-40f3-aff5-b2de6690ab6b/GlobalHydrogenReview2025.pdf

International Energy Agency [IEA]. (2026). *Electricity 2026: Prices*. https://www.iea.org/reports/electricity-2026/prices

Jaxa-Rozen, M., & Kwakkel, J. (2018). Tree-based ensemble methods for sensitivity analysis of environmental models: A performance comparison with Sobol and Morris techniques. *Environmental Modelling & Software, 107*, 245-266. https://doi.org/10.1016/j.envsoft.2018.06.011

Jaxa-Rozen, M., Pratiwi, A. S., & Trutnevyte, E. (2021). Variance-based global sensitivity analysis and beyond in life cycle assessment: An application to geothermal heating networks. *The International Journal of Life Cycle Assessment, 26*, 1008-1026. https://doi.org/10.1007/s11367-021-01921-1

Jetten, R. A. A. (2022a, March 2). *Kamerbrief over Fit-for-55 waterstofpakket en Nationaal Waterstof Programma*. Ministerie van Economische Zaken en Klimaat. https://eerstekamer.nl/9370000/1/j4nvi0xeni9vr2l_j9vvkfvj6b325az/vlqxmvtu9xdh/f=/vlqxmwoxau8x.pdf

Jetten, R. A. A. (2022b, December 2). *Kamerbrief voortgang waterstofbeleid*. Ministerie van Economische Zaken en Klimaat. https://app.1848.nl/static/pdf/bd/32/bd323e63705182110cc51091685a12c2c4ae1bad.pdf

*Jodry, A., et al. (2026). Resilience analysis for energy foresight scenarios: Addressing the deep uncertainties of hydrogen deployment in industrial hubs. *Energy Policy*, 115258. https://doi.org/10.1016/j.enpol.2026.115258

Joint Research Centre [JRC]. (2025). *Clean Energy Technology Observatory: Water electrolysis and hydrogen in the European Union. Status report 2025*. https://www.enagas.es/content/dam/enagas/en/files/transicion-energetica/red-hidrogeno/observatorio-tecnologico-hidrogeno/jrc-water-electrolysis-hydrogen.pdf

Kamerstukken II 2025/26, 36936, nr. 3. (2026). *Memorie van toelichting: Wet jaarverplichting hernieuwbare brandstoffen van niet-biologische oorsprong in de industrie*. https://zoek.officielebekendmakingen.nl/kst-36936-3.odt

Kamerstukken II 2025/26, 36936, nr. 4. (2026). *Advies Afdeling advisering Raad van State (10 december 2025) en nader rapport (23 april 2026)*. https://zoek.officielebekendmakingen.nl/kst-36936-4.pdf

Kasprzyk, J. R., Nataraj, S., Reed, P. M., & Lempert, R. J. (2013). Many objective robust decision making for complex environmental systems undergoing change. *Environmental Modelling & Software, 42*, 55-71. https://doi.org/10.1016/j.envsoft.2012.12.007

Klimaatadaptatie Nederland. (n.d.). *Hoeveel droger wordt het?* Retrieved October 7, 2026, from https://klimaatadaptatienederland.nl/kennisdossiers/droogte/hoeveel-droger

KNMI. (2026, August 7). *Zeer lage Rijnafvoer door aanhoudende droogte in stroomgebied*. https://www.knmi.nl/over-het-knmi/nieuws/zeer-lage-rijnafvoer-door-aanhoudende-droogte-in-stroomgebied

Kwakkel, J. H. (2017). The Exploratory Modeling Workbench: An open source toolkit for exploratory modeling, scenario discovery, and (multi-objective) robust decision making. *Environmental Modelling & Software, 96*, 239-250. https://doi.org/10.1016/j.envsoft.2017.06.054

Kwakkel, J. H., & Cunningham, S. C. (2016). Improving scenario discovery by bagging random boxes. *Technological Forecasting and Social Change, 111*, 124-134. https://consensus.app/papers/details/311cee2281b15f8899ca976dc11f3bcf/

Kwakkel, J. H., & Jaxa-Rozen, M. (2016). Improving scenario discovery for handling heterogeneous uncertainties and multinomial classified outcomes. *Environmental Modelling & Software, 79*, 311-321. https://doi.org/10.1016/j.envsoft.2015.11.020

KWR Water Research Institute. (2026). *Water voor waterstofproductie (W4H2)* [Project page]. https://www.kwrwater.nl/en/projecten/water-voor-waterstofproductie-w4h2/

Lempert, R. J., Bryant, B. P., & Bankes, S. C. (2008). *Comparing algorithms for scenario discovery* (WR-557-NSF). RAND. https://consensus.app/papers/details/eda07246690751e48102fd3a104d522e/

Lensink, S., Henriquez, C., van der Welle, A., & Beurskens, L. (2025, December 9). *Advies Subsidieregeling Coöperatieve Energieopwekking 2026*. PBL & TNO. https://zoek.officielebekendmakingen.nl/blg-1231279.pdf

Marchau, V. A. W. J., Walker, W. E., Bloemen, P. J. T. M., & Popper, S. W. (Eds.). (2019). *Decision making under deep uncertainty: From theory to practice*. Springer. https://doi.org/10.1007/978-3-030-05252-2

McPhail, C., Maier, H. R., Kwakkel, J. H., Giuliani, M., Castelletti, A., & Westra, S. (2018). Robustness metrics: How are they calculated, when should they be used and why do they give different results? *Earth's Future, 6*(2), 169-191. https://doi.org/10.1002/2017EF000649

Melaina, M., Penev, M., Zavell, B., Khanal, A., & Koleva, M. (2026, May 14). *Water use for hydrogen production* (Program Record #25003). U.S. Department of Energy. https://www.energy.gov/documents/record-25003-water-use-hydrogen-production

Menberg, K., Heo, Y., & Choudhary, R. (2016). Sensitivity analysis methods for building energy models: Comparing computational costs and extractable information. *Energy and Buildings, 133*, 433-445. https://doi.org/10.1016/j.enbuild.2016.10.005

Ministerie van Infrastructuur en Waterstaat [IenW]. (2026, July 16). *Kamerbrief over droogte en opschaling naar feitelijk watertekort* (kst-1264000). https://zoek.officielebekendmakingen.nl/kst-1264000.pdf

Ministerie van Klimaat en Groene Groei [KGG]. (2024, November 29). *Oproep tot voorstellen demonstratieproject 1 waterstofproductie op zee* [Internetconsultatie]. https://internetconsultatie.nl/demonstratieproject/document/13363

Ministerie van Klimaat en Groene Groei [KGG]. (2025). *Nationale agenda ondergrondse waterstofopslag* [Letter to Parliament]. https://www.eerstekamer.nl/behandeling/20250704/brief_regering_nationale_agenda/document3/f=/vmp2jywo3tzl.pdf

Ministerie van Klimaat en Groene Groei [KGG]. (2026, March 9). *Aanbieding nader rapport wetsvoorstel jaarverplichting RFNBO's industrie* (2026D20450). https://berthub.eu/tkconv/getraw/2026D20450

*Morales-España, G., et al. (2023). Impact of large-scale hydrogen electrification and retrofitting of natural gas infrastructure on the European power system. *International Journal of Electrical Power & Energy Systems*. https://doi.org/10.1016/j.ijepes.2023.109686

Moret, S., Codina Gironès, V., Bierlaire, M., & Maréchal, F. (2017). Characterization of input uncertainties in strategic energy planning models. *Applied Energy, 202*, 597-617. https://doi.org/10.1016/j.apenergy.2017.05.106

National Renewable Energy Laboratory [NREL]. (2025). *Cost projections for utility-scale battery storage: 2025 update*. https://docs.nrel.gov/docs/fy25osti/93281.pdf

NEI Magazine. (2026, October 1). [Dutch new nuclear programme update]. https://www.neimagazine.com/?p=107843

Netbeheer Nederland. (2025a, May). *Netbeheer Nederland scenario's editie 2025*. https://www.netbeheernederland.nl/sites/default/files/2025-05/netbeheer_nederland_scenarios_editie_2025_-_def_12-05.pdf

Netbeheer Nederland. (2025b). *Netbeheer Nederland scenario's editie 2025* [News release]. https://www.netbeheernederland.nl/artikelen/nieuws/netbeheer-nederland-scenarios-editie-2025

Netbeheer Nederland. (2026, April). *Verkenningen Netbeheer Nederland scenario's editie 2025* (concept 12-12-2025 / 17-04-2026). https://www.netbeheernederland.nl/sites/default/files/2026-04/verkenningen_netbeheer_nederland_scenarios_editie_2025_0.pdf

Neumann, F., & Brown, T. (2023). Broad ranges of investment configurations for renewable power systems, robust to cost uncertainty and near-optimality. *iScience, 26*(5), 106702. https://doi.org/10.1016/j.isci.2023.106702

Oesterholt, F. I. H. M., van Alphen, H. J., & Koeman-Stein, N. (2017). *De vraag naar water in een waterstofeconomie: Kansen en gevolgen voor de drinkwatersector* (BTO 2016.086). KWR. https://api.kwrwater.nl//uploads/2018/11/BTO-2016.086-De-vraag-naar-water-in-een-waterstofeconomie.Kansen-en-gevolgen-voor-de-drinkwatersector.pdf

offshoreWIND.biz. (2025a, July 17). *Dutch govt lowers 2040 offshore wind target, 50 GW "unrealistic and unnecessary"*. https://www.offshorewind.biz/2025/07/17/dutch-govt-lowers-2040-offshore-wind-target-50-gw-unrealistic-and-unnecessary

offshoreWIND.biz. (2025b, October 31). *Zero bids in 1 GW Dutch offshore wind tender*. https://www.offshorewind.biz/2025/10/31/zero-bids-in-1-gw-dutch-offshore-wind-tender/

*Oni, A. O., et al. (2022). Comparative assessment of blue hydrogen from steam methane reforming, autothermal reforming, and natural gas decomposition technologies for natural gas-producing regions. *Energy Conversion and Management*, 115245. https://doi.org/10.1016/j.enconman.2022.115245

*Pahle, M., et al. (2025). *The emerging endgame: The EU ETS on the road towards climate neutrality* [Working paper]. SSRN. https://doi.org/10.2139/ssrn.4373443

PBL Planbureau voor de Leefomgeving. (2025a). *Klimaat- en Energieverkenning 2025* (Publicatienummer 5692). https://www.pbl.nl/system/files/document/2025-09/pbl-2025-klimaat-en-energieverkenning-2025-5692.pdf

PBL Planbureau voor de Leefomgeving. (2025b). *Monitor RES 2025*. https://www.pbl.nl/downloads/pbl-2025-monitor-res-2025-5967pdf

PBL Planbureau voor de Leefomgeving. (2025c). *Notitie CO2-heffing industrie: Toelichting ten behoeve van de overlegtafel CO2-heffing industrie* (Publicatienummer 5955). https://acc.pbl.nl/downloads/pbl-2025-notitie-co2-heffing-industrie-toelichting-ten-behoeve-van-de-overlegtafel-co2-heffing-industrie-5955pdf

PBL Planbureau voor de Leefomgeving. (2025d). *Toekomstverkenning WLO 2025: Cahier Klimaat en Energie* (Publicatienummer 5455). https://www.wlo2025.nl/system/files/document/2025-07/pbl-2025-toekomstverkenning-wlo-cahier-klimaat-en-energie-5455.pdf

PBL Planbureau voor de Leefomgeving. (2026a, January 16). *Advice offshore wind tender 2026*. https://www.pbl.nl/en/downloads/pbl-2026-advice-offshore-wind-tender-2026-5971pdf

PBL Planbureau voor de Leefomgeving. (2026b, February 13). *Advies basisbedragen SDE++ 2026*. https://www.pbl.nl/downloads/pbl-2026-eindadvies-sde-plus-plus-2026-5698-1pdf

PBL Planbureau voor de Leefomgeving. (2026c). *Het ETS2 en de gevolgen voor Nederlandse huishoudens* (Publicatienummer 5921). https://www.pbl.nl/downloads/pbl-2026-ets2-en-de-gevolgen-voor-huishoudens-5921pdf

PBL Planbureau voor de Leefomgeving. (2026d). *Klimaat- en Energieverkenning 2026* (Publicatienummer 6050). https://www.pbl.nl/system/files/document/2026-09/pbl-2026-klimaat-en-energieverkenning-2026-6050.pdf

Pianosi, F., & Wagener, T. (2018). Distribution-based sensitivity analysis from a generic input-output sample. *Environmental Modelling & Software, 108*, 197-207. https://doi.org/10.1016/j.envsoft.2018.07.019

Pickering, B., Lombardi, F., & Pfenninger, S. (2022). Diversity of options to eliminate fossil fuels and reach carbon neutrality across the entire European energy system. *Joule, 6*(6), 1253-1276. https://doi.org/10.1016/j.joule.2022.05.009

Prestige Business Solutions. (2026, October 6). *Energy market report: 06 October 2026*. https://www.prestigebusiness.energy/marketreports/energy-market-update06-oct2026

Puy, A., Lo Piano, S., & Saltelli, A. (2020). A sensitivity analysis of the PAWN sensitivity index. *Environmental Modelling & Software, 127*, 104679. https://doi.org/10.1016/j.envsoft.2020.104679

pv magazine. (2025, December 3). *Price gap between conventional, renewable hydrogen widens in Europe*. https://www.pv-magazine.com/2025/12/03/price-gap-between-conventional-renewable-hydrogen-widens-in-europe/

pv magazine. (2026, February 3). *Germany, France, Netherlands curtail 3.9 TWh of renewables in 2025*. https://www.pv-magazine.com/2026/02/03/germany-france-netherlands-curtail-3-9-twh-of-renewables-in-2025/

PyPSA developers. (n.d.). *Global sensitivity analysis* [Example notebook]. PyPSA documentation. Retrieved October 7, 2026, from https://docs.pypsa.org/stable/examples/gsa/

PyPSA technology-data contributors. (2026). *technology-data* (master branch, outputs/costs_2025-2050.csv; eur_year 2025) [Data set]. GitHub. https://github.com/PyPSA/technology-data

Ramirez, K., Weiss, T., Kirk, T., & Gamage, C. (2023, August 2). *Hydrogen reality check: Distilling green hydrogen's water consumption*. RMI. https://rmi.org/resources/hydrogen-reality-check-distilling-green-hydrogens-water-consumption/

Ramm, T. D., Watson, C. S., & White, C. J. (2018). Strategic adaptation pathway planning to manage sea-level rise and changing coastal flood risk. *Environmental Science & Policy, 87*, 92-101. https://doi.org/10.1016/j.envsci.2018.06.001

Reis, J., & Shortridge, J. (2020). Impact of uncertainty parameter distribution on robust decision making outcomes for climate change adaptation under deep uncertainty. *Risk Analysis, 40*(3), 494-511. https://doi.org/10.1111/risa.13405

Rijksdienst voor Ondernemend Nederland [RVO]. (n.d.). *Holland Hydrogen 1* [Project 54075]. https://projecten.rvo.nl/projecten/54075

Rijksdienst voor Ondernemend Nederland [RVO]. (2026a, April). *Waterstof infographic*. https://www.rvo.nl/sites/default/files/2026-04/Waterstof%20infographic.pdf

Rijksdienst voor Ondernemend Nederland [RVO]. (2026b, August 13). *Plannen windenergie op zee*. https://www.rvo.nl/onderwerpen/windenergie-op-zee/plannen-windenergie-op-zee

Rijksoverheid. (2024, April 29). *Zeven projecten krijgen subsidie voor de productie van volledig hernieuwbare waterstof*. https://www.rijksoverheid.nl/actueel/nieuws/2024/04/29/zeven-projecten-krijgen-subsidie-voor-de-productie-van-volledig-hernieuwbare-waterstof

Rijkswaterstaat. (2023, December 13). *Toekomstige rivierafvoeren Rijn en Maas lager in de zomer en hoger in de winter*. https://www.rijkswaterstaat.nl/nieuws/archief/2023/12/toekomstige-rivierafvoeren-rijn-en-maas-lager-in-de-zomer-en-hoger-in-de-winter

*Rubino, G., et al. (2026). Key uncertainties for hydrogen in Switzerland: Insights from global sensitivity analysis and Plackett-Burman design. *International Journal of Hydrogen Energy*, 153822. https://doi.org/10.1016/j.ijhydene.2026.153822

S&P Global Commodity Insights. (2026a, April 28). *Shell readies Europe's largest refinery for green hydrogen*. https://www.spglobal.com/energy/en/news-research/latest-news/refined-products/042826-shell-readies-europes-largest-refinery-for-green-hydrogen

S&P Global Commodity Insights. (2026b, June 17). *Dutch Porthos CCS project marks construction progress despite delays*. https://www.spglobal.com/energy/en/news-research/latest-news/energy-transition/061726-dutch-porthos-ccs-project-marks-construction-progress-despite-delays

SALib developers. (n.d.). *SALib.sample package* [API documentation]. Retrieved October 7, 2026, from https://salib.readthedocs.io/en/main/api/SALib.sample.html

Sarrazin, F., Pianosi, F., & Wagener, T. (2016). Global sensitivity analysis of environmental models: Convergence and validation. *Environmental Modelling & Software, 79*, 135-152. https://doi.org/10.1016/j.envsoft.2016.02.005

Scottish Parliament Information Centre [SPICe]. (2024). *SPICe briefing for petition PE2159* [Citing IRENA & Bluerisk (2023), *Water for hydrogen production*]. https://www.parliament.scot/-/media/files/committees/citizen-participation-and-public-petitions-committee/correspondence/2024/pe2159/spice-briefing-for-petition-pe2159.pdf

*Sitarz, J., et al. (2024). EU carbon prices signal high policy credibility and farsighted actors. *Nature Energy*. https://doi.org/10.1038/s41560-024-01505-x

Solar Magazine. (2024, October 24). *Nederland telt 33,6 gigawatt zonnepanelen in 2030, groei hernieuwbare energie blijft achter*. https://solarmagazine.nl/nieuws-zonne-energie/i38866/nederland-telt-33-6-gigawatt-zonnepanelen-in-2030-groei-hernieuwbare-energie-blijft-achter

Solar Magazine. (2025a, May 15). *Vraag naar duurzame energie groeit sneller dan aanbod: Tot 3,5 keer meer stroom nodig*. https://solarmagazine.nl/nieuws-zonne-energie/i40555/vraag-naar-duurzame-energie-groeit-sneller-dan-aanbod-tot-3-5-keer-meer-stroom-nodig

Solar Magazine. (2025b, May 16). *TenneT wijst opnieuw op risico stroomtekort na 2030*. https://solarmagazine.nl/nieuws-zonne-energie/i40567/tennet-wijst-opnieuw-op-risico-stroomtekort-na-2030

Solar Magazine. (2025c, July 19). *De harde cijfers: 84 grote batterijen in Nederland met 620 megawattuur opslagcapaciteit*. https://solarmagazine.nl/nieuws-zonne-energie/i41154/de-harde-cijfers-84-grote-batterijen-in-nederland-met-620-megawattuur-opslagcapaciteit

Solar Magazine. (2025d, August 11). *Kabinet investeert 700 miljoen euro in elektrolysers voor productie groene waterstof*. https://solarmagazine.nl/nieuws-zonne-energie/i41282/kabinet-investeert-700-miljoen-euro-in-elektrolysers-voor-productie-groene-waterstof

Solar Magazine. (2025e, October 9). *Nederland installeert dit jaar 2,1 gigawattuur grote batterijen*. https://solarmagazine.nl/nieuws-zonne-energie/i41847/nederland-installeert-dit-jaar-2-1-gigawattuur-grote-batterijen

Solar Magazine. (2026a, April 29). *SDE++: 8,2 miljard euro aan CO2-opslagprojecten ingetrokken*. https://solarmagazine.nl/nieuws-zonne-energie/i43609/sde-8-2-miljard-euro-aan-co2-opslagprojecten-ingetrokken

Solar Magazine. (2026b, May 4). *TenneT: Kosten congestiemanagement stijgen fors, meer dan 1 terawattuur curtailment*. https://solarmagazine.nl/nieuws-zonne-energie/i43654/tennet-kosten-congestiemanagement-stijgen-fors-meer-dan-1-terawattuur-curtailment

Solar Magazine. (2026c, June 13). *CBS: Nederland installeerde vorig jaar 1.447 megawattpiek zonnepanelen*. https://solarmagazine.nl/nieuws-zonne-energie/i44006/cbs-nederland-installeerde-vorig-jaar-1-447-megawattpiek-zonnepanelen

Solar Magazine. (2026d, September 14). *Nederland mist Europees doel voor duurzame energie en moet in 2030 zelfs stroom importeren*. https://solarmagazine.nl/nieuws-zonne-energie/i44765/nederland-mist-europees-doel-voor-duurzame-energie-en-moet-in-2030-zelfs-stroom-importeren

Solarserver. (2023, January 4). *Umweltbundesamt meldet Rekordeinnahmen aus dem Emissionshandel*. https://www.solarserver.de/2023/01/04/umweltbundesamt-meldet-rekordeinnahmen-aus-dem-emissionshandel/

Steinmann, P., Auping, W. L., & Kwakkel, J. H. (2020). Behavior-based scenario discovery using time series clustering. *Technological Forecasting and Social Change, 156*, 120052. https://doi.org/10.1016/j.techfore.2020.120052

*Talukdar, M., et al. (2023). Techno-economic analysis of underground hydrogen storage in Europe. *iScience*. https://doi.org/10.1016/j.isci.2023.108771

*Tangi, M., et al. (2026). Global sensitivity analysis and scenario discovery reveal resilient water-energy system configurations on small islands under deep uncertainty. *Renewable and Sustainable Energy Transition*, 100139. https://doi.org/10.1016/j.rset.2026.100139

Taxlive. (2025, July 22). *Kabinet wil CO2-heffing tijdelijk opschorten*. VN Vandaag. https://www.taxlive.nl/nl/documenten/vn-vandaag/kabinet-wil-co2-heffing-tijdelijk-opschorten/

TNO (Groenenberg, R.). (2020). *Large-scale energy storage in salt caverns and depleted fields* (TNO 2020 R12186). https://projecten.topsectorenergie.nl/storage/app/uploads/public/618/269/e7b/618269e7bb312950892810.pdf

TNO. (2024). *Evaluation of the levelised cost of hydrogen based on proposed electrolyser projects in the Netherlands* (TNO 2024 R10766). https://zoek.officielebekendmakingen.nl/blg-1145411.pdf

Trading Economics. (2026a, March). *TTF gas prices surge on Middle East supply fears*. https://tradingeconomics.com/commodity/eu-natural-gas/news/529286

Trading Economics. (2026b). *EU natural gas TTF* [Market data]. Retrieved October 7, 2026, from https://tradingeconomics.com/commodity/eu-natural-gas

U.S. Department of Energy, Hydrogen and Fuel Cell Technologies Office. (2024, updated 2026). *Can water usage for electrolysis pose problems for parts of the United States currently facing water shortages?* https://www.energy.gov/eere/fuelcells/can-water-usage-electrolysis-pose-problems-parts-united-states-currently-facing

U.S. Energy Information Administration [EIA]. (2024, January). *Capital cost and performance characteristics for utility-scale electric power generating technologies* [Report prepared by Sargent & Lundy]. https://www.eia.gov/analysis/studies/powerplants/capitalcost/pdf/capital_cost_AEO2025.pdf

Umweltbundesamt. (2021). *Jahresbericht zu deutschen Versteigerungen im EU-Emissionshandel 2020*. https://www.umweltbundesamt.de/themen/jahresbericht-zu-deutschen-versteigerungen-im-eu

Umweltbundesamt. (2025, January 7). *Einnahmen aus dem Emissionshandel erneut auf Rekordniveau* [Press release]. https://www.umweltbundesamt.de/presse/pressemitteilungen/einnahmen-aus-dem-emissionshandel-erneut-auf

van Greevenbroek, K., Schmidt, J., Zeyringer, M., & Horsch, A. (2025). *Little to lose: The case for a robust European green hydrogen strategy* [Preprint]. arXiv. https://arxiv.org/pdf/2412.07464

van Hussen, K., van de Velde, I., Läkamp, R., & van der Kooij, S. (2019, February 21). *Economische schade door droogte in 2018*. Ecorys. https://www.ecorys.com/sites/default/files/2019-10/20190221%20Rapport%20Economische%20schade%20door%20droogte%20in%202018.pdf

*Vinardell, S., et al. (2025). Powering renewable hydrogen production with alternative water sources: Is it economically feasible? *Energy Nexus*. https://doi.org/10.1016/j.nexus.2025.100457

Walter, J., Löhr, L., Venghaus, S., & Moser, A. (2023). *Analysis of water resources for green hydrogen production in Europe* [Conference paper]. IEWT 2023, TU Wien. https://iewt2023.eeg.tuwien.ac.at/download/contribution/fullpaper/8/8_fullpaper_20230210_174238.pdf

Walter, J. D., Fischer, L. S., Venghaus, S., & Moser, A. (2025). Integrating water availability for electrolysis into energy system modeling. *Advances in Applied Energy*, 100208. https://doi.org/10.1016/j.adapen.2025.100208

World Nuclear Association. (n.d.). *Netherlands: World nuclear outlook report*. https://world-nuclear.org/our-association/publications/world-nuclear-outlook-report/netherlands---world-nuclear-outlook-report

Xodus Group. (n.d.). *Aramis tariff study* (L-400699-S00-Y-REPT-001). Eerste Kamer. https://www.eerstekamer.nl/9370000/1/j4nvgs5kjg27kof_j9vvkfvj6b325az/vlutrvd2g2y4

Zeyen, E., Victoria, M., & Brown, T. (2023). Endogenous learning for green hydrogen in a sector-coupled energy model for Europe. *Nature Communications, 14*. https://doi.org/10.1038/s41467-023-39397-2
