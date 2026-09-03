# STOLEN STRATA — A Landform Under Erasure
### Quantifying the Anthropogenic Erasure of Kashmir's Karewa Terraces

Executive Summary · DOI: 10.5281/zenodo.21766464 · Sakshi D. Maske

## Project Overview

I built STOLEN STRATA to trace a single continuous line: from an ancient lake basin's geology, to the terraces it left behind, to the saffron economy those terraces alone make possible, to the mining now quietly erasing them. Kashmir's karewas are a genuinely rare landform — flat-topped remnants of an intermontane lake infill found nowhere else on Earth at this scale — and their loess cap is the only reason Geographical Indication-tagged saffron grows in the Pampore belt at all, which is why I treat terrace loss as an economic story rather than a purely geomorphological one. The headline figure is 190.3 hectares of terrace surface converted to bare earth since 1994, and the pipeline shows that loss is recent rather than gradual: essentially flat through 2015, then more than tripling in the decade since. Rather than stop at a hectare count, I pushed the analysis in two further directions — testing whether degradation tracks road and settlement access (it does, more strongly for settlements than for roads) and converting the saffron-proximity risk into rupee terms using official state yield and price data, so that an abstract land-cover statistic becomes an estimated ₹17.8 crore in annual production value sitting within encroachment range. I also went looking for the governance side of the story that most satellite studies skip: whether any law actually protects karewa land from excavation, and found that none currently does, with a protective bill still pending while extraction permits continue to be issued. Together, the geomorphology, the economics, and the legal vacuum are what turn this from a change-detection exercise into something actionable — a landform loss with a price tag and an open policy lever attached to it.

## The Question

How much of Kashmir's karewa terraces — a geologically singular landform found nowhere else on Earth at this scale, and the physical base the region's GI-tagged saffron economy is grown on — has been lost to unregulated soil mining, and does that loss follow an accessibility-driven pattern rather than a random one? Beyond the hectare count, what is that loss actually worth in rupee terms to the saffron economy it threatens, and what legal framework, if any, currently governs the extraction driving it?

## The Method

201 karewa terrace boundaries are delineated algorithmically from a Copernicus DEM using a Topographic Position Index and slope threshold (TPI > 3, slope < 8°), with no manual digitization. Bare-earth land-cover fraction is tracked across four season-matched time points (1994, 2005, 2015, 2025; Landsat 5/7/8/9 and Sentinel-2), revealing when degradation actually accelerated. Saffron-cultivating terraces are identified via an inverted-phenology NDVI signature, then converted into an estimated ₹/year value-at-risk figure using official 2024-25 J&K state saffron yield and value data. Two independent Mann-Whitney U tests — against the OpenStreetMap road network and 3,266 OpenStreetMap building footprints — test whether degraded terraces sit statistically closer to infrastructure than intact ones. A threshold-sensitivity sweep, a Landsat/Sentinel-2 resolution-mismatch quantification, rank-biserial effect sizes, and a Holm-Bonferroni correction across all four tests validate the pipeline's robustness. A search of J&K legislative reporting investigates whether any statute currently protects karewa land from excavation.

## The Finding

Degradation is recent and accelerating, not a slow multi-decadal process: mean bare-earth fraction was essentially flat from 1994 to 2015 (1.84% → 2.62% → 2.63%), then more than tripled by 2025 (8.43%) — 190.3 hectares net converted, 67% of it concentrated within just 12.4% of terraces. Degraded terraces sit statistically significantly closer to both drivable roads (mean 75.6 m vs. 133.1 m, p = 0.0116) and building footprints (mean 455.9 m vs. 999.7 m, p = 0.0001) than intact terraces — two independent infrastructure signals pointing the same direction, with settlement proximity the strongest statistical effect in the entire study. Of 14 detected saffron-cultivating terraces, 43% sit within 1 km of already-degraded land; at official state yield and price figures, that at-risk subset represents an estimated ₹17.8 crore in annual production value, 55% of the ₹32.4 crore this study's detected saffron area is estimated to generate in total. No statute currently protects karewa land from excavation — a private member's bill proposing a dedicated Karewa Protection Authority remains pending while the Revenue and Geology & Mining Departments continue issuing the excavation permissions it would restrict.

| Test | U statistic | P-value | Effect size (r) | Holm-Bonferroni |
|---|---|---|---|---|
| Settlement proximity | 1176.0 | 0.0001 | 0.465 | Significant |
| Compactness | 1425.0 | 0.0044 | 0.352 | Significant |
| Road proximity | 1611.0 | 0.0116 | 0.268 | Significant |
| Slope | 2573.0 | 0.1711 | -0.170 | Not significant |

Settlement proximity, compactness, and road proximity all survive Holm-Bonferroni correction across the four-test family (family-wise α = 0.05); slope was already non-significant before correction.

## Validation & Robustness Checklist

* Two independent infrastructure-proximity signals — road network and 3,266 OSM building footprints — agree in direction
* Threshold-sensitivity sweep across all three classification thresholds (TPI/slope, degradation, saffron signature); reported counts sit in a stable neighbourhood, not an isolated spike
* Resolution-mismatch check — 2025 Sentinel-2 resampled to match 30 m Landsat; a real but modest ~13% effect that does not reverse the acceleration
* Rank-biserial effect sizes and Holm-Bonferroni correction across the full four-test family
* Economic valuation cross-verified — yield independently recomputed from raw production/area figures (19.58 MT / 3,715 ha = 5.271 kg/ha) matches the officially reported 5.27 kg/ha
* Saffron detection benchmarked openly against an independent FAO baseline, reported as a recall shortfall rather than smoothed over
* 150-point stratified ground-truth sample generated for a forthcoming formal accuracy assessment
* Detected saffron area (225.4 ha) sits well below the FAO baseline (3,200 ha) — disclosed as a detection-recall limitation, not adjusted to fit expectation
* Governance-alignment testing (RQ4) could not be completed for lack of spatially resolved allocation data — deferred rather than estimated without a source

## Honest Limitation

All degradation, saffron, and delineation classifications rest on thresholds validated by visual inspection and a sensitivity sweep rather than a formal accuracy assessment against independently labelled ground-truth points; a 150-point stratified sample has been generated for this purpose but manual labelling and the resulting confusion matrix are not yet complete. The economic valuation applies a single statewide yield and price uniformly to every detected saffron terrace — actual per-terrace value plausibly varies with soil quality and the GI-tagged Pampore-origin premium, so the figure should be read as an order-of-magnitude value-at-risk estimate, not a precise appraisal. The legal-protection finding reflects the most recent legislative reporting located as of this study's research date and should be independently re-checked, since a private member's bill's status can change without the kind of ongoing coverage this study's other sources receive. Settlement proximity may partly reflect a general human-activity gradient rather than transport economics specifically, and the 2005 time point is a nine-year Landsat composite (2001-2009) rather than a single-year snapshot, smoothing over short-lived degradation episodes within that window without affecting the 1994 or 2015 endpoints that anchor the trend's overall shape.

## Real-World Relevance

The combination of two independent infrastructure-accessibility signals and a documented legal vacuum describes a specific, actionable governance picture: unregulated extraction concentrated where it is logistically easiest to conduct, in a landscape with no dedicated protective statute currently in force. Framing the saffron-proximity risk in rupee terms — rather than leaving it as an abstract hectare count — ties the karewa terraces' physical erosion directly to livelihoods dependent on the crop they support, and to the pending Karewa Protection Authority bill this study's legal-status finding documents as the one concrete policy lever currently on the table.

GitHub: github.com/sakshimaske303-commits/STOLEN_STRATA | Live Dashboard: stolenstrata-ekmgvmukfnfkpigxtgsak6.streamlit.app | Zenodo DOI: 10.5281/zenodo.21766464

Sakshi D. Maske — Independent Geospatial Researcher
