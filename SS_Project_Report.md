# STOLEN STRATA: A Landform Under Erasure

## Project Report

## Project Overview

Kashmir's karewas are elevated, flat-topped terraces formed by the infilling of an ancient intermontane lake basin — a geomorphological accident of the Pir Panjal's uplift that, millennia later, produced the loess-capped soils supporting *Crocus sativus* (saffron), one of the world's most valuable agricultural commodities and the economic backbone of thousands of farming households in the Pampore belt. STOLEN STRATA is a satellite-based geospatial framework built to quantify how much of this landform has been lost to unregulated soil mining and unplanned urban expansion, and to test whether that loss is spatially and economically consequential rather than diffuse background change.

Beyond physical loss, the project extends into an infrastructure and governance dimension: testing whether degradation is systematically linked to road access — consistent with an economically-driven extraction model — and whether existing agricultural policy investment is targeting the land that remains geomorphologically and agronomically intact, rather than land already under active erosion pressure. The study area spans the karewa belts of Pampore, Pulwama, and Budgam districts together with the type-locality exposures near Srinagar (Zewan section), the highest-concentration saffron-bearing karewa zone in the Kashmir Valley.

## Problem Statement

Karewa loss to unregulated soil mining is well documented in journalistic and grey-literature sources, but almost entirely through site-specific or anecdotal observation rather than a systematic, multi-decadal, satellite-derived quantification. A second, related gap is economic rather than geomorphological: no existing work spatially overlays mapped terrace loss against saffron cultivation extent to establish how much of the loss is occurring near, or within, agriculturally productive land, as opposed to marginal terrain. A third gap is one of governance — formal policy instruments such as the National Saffron Mission are rarely tested against evidence of where degradation pressure actually is.

## Aim

To build a reproducible, script-first geospatial pipeline that algorithmically delineates karewa terrace boundaries from terrain data, quantifies their multi-temporal loss to bare-earth land cover, overlays that loss against mapped saffron cultivation and road infrastructure, and evaluates whether the resulting risk pattern is one that current governance instruments appear to be responding to.

## Research Questions

**RQ1**: What is the net areal change in karewa terrace extent across the Kashmir Valley study area between the earliest usable Landsat archive and the present day?

**RQ2**: Where is this loss concentrated, and does it correlate spatially with proximity to road infrastructure?

**RQ3**: What proportion of the lost or at-risk terrace area overlaps or lies near active saffron cultivation, and what does this imply for the long-term viability of the saffron economy?

**RQ4**: Are current agricultural policy investments spatially aligned with the karewa land that remains geomorphologically and agronomically intact?

## Hypotheses

**H1 (Degradation Pathway)**: Karewa terrace surfaces will show a measurable increase in bare-earth land cover between 1994 and 2025, with the majority of this loss concentrated within the most recent decade rather than distributed evenly across the full study period.

**H2 (Saffron Proximity Pathway)**: Saffron-cultivating terraces will show measurable spatial proximity to already-degraded terraces, representing a leading-indicator encroachment risk to the saffron economy even in the absence of direct terrace-level overlap.

**H3 (Infrastructure-Access Pathway)**: Degraded terraces will lie significantly closer to drivable road infrastructure than intact terraces, consistent with an accessibility-driven model of unregulated soil mining.

## Data Sources

The project integrates datasets acquired via reproducible, script-based pipelines rather than manual digitization, consistent with its emphasis on transparency and reproducibility: the Copernicus GLO-30 DEM (terrain analysis and terrace delineation); a season-matched Landsat 5/7/8/9 archive spanning four time points — 1994, 2005, 2015 — and a 2025 Sentinel-2 composite (multi-temporal bare-earth and saffron-signature detection); the OpenStreetMap drivable road network, extracted via `osmnx` (infrastructure-proximity analysis); and the FAO GIAHS "Saffron Heritage Site of Kashmir" documentation (an independent baseline for validating detected saffron extent). Study-area boundary and settlement-reference layers were generated programmatically rather than hand-digitized, preserving a fully scripted pipeline end to end.

## Methodology

### Phase 1 — Automated Terrace Delineation

Terrace boundaries were delineated algorithmically from the DEM rather than manually traced, using a Topographic Position Index (Weiss, 2001) combined with a slope threshold to isolate terrain that is simultaneously flat-topped and locally elevated — the defining signature of a karewa tread. An initial, stricter threshold produced only thin, sliver-shaped candidates inconsistent with real terrace morphology; loosening the threshold recovered proper blob-shaped polygons. After an area and elevation filter, 201 candidate terraces remained. These aligned, on visual inspection, with the labelled "Saffron Fields, Lethpora" location — an independent ground-truth confirmation of the delineation method.

### Phase 2 — Multi-Temporal Degradation Detection

Land-cover change within each of the 201 terraces was tracked using a bare-earth-fraction metric — the share of pixels per polygon falling below an NDVI threshold indicative of bare ground — computed from season-matched composites at four time points (1994, 2005, 2015, 2025) rather than a single before/after comparison. Mean bare-earth fraction across all terraces rose from 1.84% (1994) to 2.62% (2005) to 2.63% (2015) to 8.43% (2025): essentially stable through 2005–2015, followed by more than a tripling within the final decade alone. Of the 201 terraces, 25 (12.4%) crossed a threshold for likely degradation.

### Phase 3 — Spatial Validation and the Headline Loss Figure

The 25 flagged terraces were checked visually against satellite basemap imagery in QGIS to confirm the classification corresponded to real, identifiable land-cover change rather than algorithmic noise. Degraded polygons formed a spatially coherent cluster near Pari Gam Khalsa / Newa Pulwama, directly over a visibly bare patch consistent with active quarrying, with a smaller cluster adjacent to the Lethpora saffron fields. Converting the bare-earth fractions into absolute area, total bare-earth cover across all 201 terraces rose from 32.2 ha (1994) to 222.6 ha (2025) — a net conversion of 190.3 hectares, 5.8% of total mapped terrace area. Of this, 128.2 hectares (67%) occurred within the 25 flagged terraces alone, which together account for only 9.7% of total mapped area: loss is concentrated, not diffuse.

### Phase 4 — Saffron Vulnerability and Proximity Risk

Saffron-cultivating terraces were identified using a Saffron Index exploiting the crop's inverted phenology — dormant through summer, at peak leaf canopy in March rather than during the October–November flowering window — yielding 14 likely saffron-cultivating terraces among the 201. None directly overlapped the 25 degraded terraces, but the nearest sat 80 m from an active degradation zone, and 6 of 14 (43%) fell within 1 km of one, a pattern confirmed smooth and monotonic across a 500 m–2.5 km sensitivity range. Detected saffron area (225.4 ha) was benchmarked against the FAO GIAHS baseline of 3,200 hectares under cultivation at Pampore; the resulting shortfall was attributed to a compounding detection-recall limitation across the terrace-delineation and saffron-signature filters rather than real-world crop loss, given independent reporting of saffron production at a 25-year high over the same period.

### Phase 5 — Infrastructure and Governance

Distance from each terrace polygon (full boundary, not a reduced centroid point) to the nearest road (OpenStreetMap network, 44,622 segments) was compared between degraded and intact terraces using a one-sided Mann-Whitney U test, appropriate given the non-normal, zero-inflated distribution of distances. Degraded terraces sat a mean 75.6 m from the nearest road (median 0.0 m) against 133.1 m (median 38.5 m) for intact terraces, a difference significant at p = 0.0116. Formal testing of policy alignment (RQ4) — whether National Saffron Mission investment targets intact rather than degrading land — was constrained by the limited availability of spatially resolved, publicly accessible land-lease and enforcement data, and is reported as an open question rather than a tested result.

### Phase 6 — Geomorphometric Cross-Check

As a supplementary, shape-based check independent of the NDVI-derived bare-earth signal, a compactness index (4π·Area/Perimeter²) and mean internal slope were computed per terrace from the same DEM and compared between degraded and intact terraces. Degraded terraces are significantly less compact — more irregular and dissected in outline — than intact ones (0.138 vs. 0.191, Mann-Whitney p = 0.0044), consistent with mining excavation cutting irregular scars rather than removing terrace surface uniformly. Mean internal slope does not differ significantly by status (p = 0.1711). This geometric result was independently recomputed from the raw DEM during the project's Deep Verify pass and confirmed exact.

### Phase 7 — Threshold Sensitivity, Resolution Robustness, and Effect Sizes (External AI Review)

Four independent AI reviews of the project converged on the same core critique: the TPI/slope, degradation, and saffron thresholds were calibrated by visual inspection with no reported sensitivity check, the mixed Landsat/Sentinel-2 resolution was acknowledged only vaguely ("may modestly inflate"), and the three Mann-Whitney tests reported p-values with no effect size or correction for testing three hypotheses. All three were addressed directly rather than argued around. Sweeping the degradation threshold from 5 to 30 percentage points shows the reported 25-terrace count sits within a stable 23-31 range across the 12-20 point neighbourhood; sweeping the saffron threshold from 0.05 to 0.25 shows the 43% proximity-risk share stays within 39-44% across 0.05-0.175, only becoming noisy where the detected count drops below 6. Resampling the 2025 Sentinel-2 composite to 30 m (matching the Landsat pixel size used in earlier years) and rerunning the pipeline shows the resolution mismatch does inflate the post-2015 acceleration — mean bare-earth fraction falls from 8.43% to 7.48%, net conversion from 190.3 to 165.2 ha — by a real but modest ~13%, with the underlying acceleration surviving resolution-matching. Rank-biserial effect sizes (road proximity r=0.268, compactness r=0.352, slope r=−0.170) and a Holm-Bonferroni correction confirm road proximity and compactness remain significant as a 3-test family; slope was already non-significant.

## Final Findings

Karewa terrace surfaces show a genuine, quantifiable degradation signal, supporting Hypothesis H1: 190.3 hectares converted to bare-earth land cover since 1994, with the majority of that loss occurring only in the final decade of the study period — degradation here is recent and accelerating, not a steady multi-decadal process. The saffron-proximity pathway (H2) is also supported: while no saffron terrace directly overlaps mapped degradation yet, a substantial share sits within encroachment range, making this an early-warning finding rather than a direct-loss one. The infrastructure-access pathway (H3) is statistically confirmed — degradation is significantly associated with road proximity, consistent with an accessibility-driven, economically rational model of unregulated mining rather than a geographically random one. The governance-alignment question (RQ4) remains open, limited by data availability rather than by the underlying analytical framework.

## Deliverables

A fully reproducible, script-first geospatial pipeline spanning DEM-derived terrace delineation, four-point multi-temporal degradation detection, saffron-signature classification, and infrastructure-proximity testing; a validated dataset of 201 karewa terraces carrying bare-earth fraction, degradation status, and road-proximity attributes; an eight-page interactive Streamlit dashboard presenting all findings alongside static and interactive QGIS-based cartography; a public, version-controlled GitHub repository; and a set of publication-quality maps and figures for the research paper and portfolio.

## Limitations

Detected saffron cultivation area (225.4 ha) falls well below the FAO GIAHS-documented baseline (3,200 ha), a shortfall attributed to compounding recall limitations across two conservative filtering stages rather than genuine crop-area loss, and reported transparently as such rather than adjusted to fit expectation — the sensitivity sweep in Phase 7 shows the proximity-risk finding this feeds into is stable across a wide range of detection thresholds, so this is a bound on precision, not a threat to the finding itself. Governance-alignment testing (RQ4) could not be completed within this project: a targeted search for spatially resolved PM Saffron Mission site- or district-level data found only aggregate, valley-wide figures, with no dataset at a resolution this study's terrace-level map could be overlaid against, so RQ4 is deferred to future work rather than estimated without a verifiable source. The multi-temporal analysis is bounded at its early end by the operational start of a usable, season-matched Landsat record (1994), meaning pre-1994 baseline conditions are outside the scope of what satellite verification here can support; the 2005 point itself required widening the acquisition window to a nine-year span after the original single-year query returned zero images, so it is a multi-year composite rather than a single-year snapshot. Resampling the 2025 Sentinel-2 composite to match the earlier years' 30 m Landsat resolution shows the mixed-sensor record does modestly inflate the reported acceleration (Phase 7) — a real effect, quantified rather than hand-waved, though the acceleration itself survives it. All classifications rest on thresholds validated by sensitivity sweeps rather than a formal accuracy assessment against independently labelled ground-truth points; no such reference dataset exists for this landscape, and building one is the highest-priority item for future work.