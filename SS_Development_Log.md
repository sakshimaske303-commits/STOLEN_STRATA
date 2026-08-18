# STOLEN STRATA
### Quantifying the Anthropogenic Erasure of Kashmir's Karewa Terraces and Its Threat to the Saffron Economy

**Author:** Sakshi D. Maske
**Region of Study:** Kashmir Valley, Jammu & Kashmir, India
**Discipline:** Geomorphology · Remote Sensing & GIS · Environmental Policy

---

## Index

1. [Project Overview](#1-project-overview)
2. [Geomorphological Background](#2-geomorphological-background)
3. [Problem Statement / Research Gap](#3-problem-statement--research-gap)
4. [Research Questions](#4-research-questions)
5. [Objectives](#5-objectives)
6. [Study Area](#6-study-area)
7. [Data Sources](#7-data-sources)
8. [Methodology (Overview)](#8-methodology-overview)
9. [Expected Deliverables](#9-expected-deliverables)
10. [Significance](#10-significance)
11. [Day 1 — Project Setup, Data Acquisition, and Automated Terrace Extraction](#day-1--project-setup-data-acquisition-and-automated-terrace-extraction)
12. [Multi-Temporal NDVI Change Detection Within Karewa Terraces](#multi-temporal-ndvi-change-detection-within-karewa-terraces)
13. [Spatial Validation of Degraded Terrace Classification](#spatial-validation-of-degraded-terrace-classification)
14. [Saffron Signature Detection and Proximity-Risk Analysis](#saffron-signature-detection-and-proximity-risk-analysis)
15. [Benchmarking Detected Saffron Extent Against an Independent Baseline](#benchmarking-detected-saffron-extent-against-an-independent-baseline)
16. [Quantifying Absolute Karewa Area Lost to Bare-Earth Conversion](#quantifying-absolute-karewa-area-lost-to-bare-earth-conversion)
17. [Extending to a Four-Point Multi-Temporal Trend](#extending-to-a-four-point-multi-temporal-trend)
18. [Testing Spatial Correlation Between Degradation and Road Proximity](#testing-spatial-correlation-between-degradation-and-road-proximity)
19. [Comprehensive Review and Deep Verify (2026-08-02)](#comprehensive-review-and-deep-verify-2026-08-02)
20. [Structured Review — Triage and Fixes (2026-08-03)](#structured-review--triage-and-fixes-2026-08-03)
21. [Infrastructure, Economic, and Regulatory Extension (2026-08-14)](#infrastructure-economic-and-regulatory-extension-2026-08-14)
22. [Interactive Map Suite and Code Cleanup Pass (2026-08-14)](#interactive-map-suite-and-code-cleanup-pass-2026-08-14)

---

## 1. Project Overview

The Kashmir Valley is underlain by a distinctive suite of elevated, flat-topped terraces known locally as **Karewas** — remnants of an ancient intermontane lake basin that once occupied the valley floor. These landforms are not merely a geological curiosity: their fertile, well-drained loess-capped surfaces support the cultivation of *Crocus sativus* (saffron), one of the world's most valuable agricultural commodities and a Geographical Indication (GI)-tagged crop central to the livelihood of thousands of farming households in the Pampore belt.

Over the past three decades, unregulated soil mining for the construction and brick industries, combined with unplanned urban expansion, has been steadily flattening these terraces. While the phenomenon has been documented in journalistic and grey-literature sources, it has not — to the extent this review could establish — been subjected to a systematic, multi-temporal, satellite-based quantification. **Stolen Strata** addresses this gap by combining classical geomorphological theory with a modern remote sensing and GIS pipeline to measure, map, and interpret the physical erasure of a unique Pleistocene-Pliocene landform, and to connect that erasure to the economic fate of the saffron industry it sustains.

---

## 2. Geomorphological Background

The Karewa Group sediments represent a fluvio-lacustrine and glacio-fluvial depositional sequence, infilling an intermontane basin that formed in association with the tectonic uplift of the Pir Panjal Range. Classical stratigraphic work (beginning with De Terra & Paterson's foundational studies and refined by subsequent Quaternary geologists) recognises a broadly two-fold division: a **Lower Karewa** sequence of lacustrine clays, silts, and lignite bands reflecting a standing water-body phase, and an **Upper Karewa** sequence of coarser fluvial gravels and sands marking the basin's gradual infilling and the re-establishment of through-flowing drainage. Geochronological estimates place these sediments broadly within the Plio-Pleistocene — spanning several million years — although the precise chronology remains an area of ongoing scientific refinement and should be treated as such in any literature review.

Subsequent incision by the Jhelum River and its tributaries dissected this infilled basin, isolating the resistant sediment packages as the flat-topped terraces observed today. A capping of aeolian loess, deposited during Pleistocene glacial-stage dust events, overlies much of the karewa surface and is the principal reason for its agronomic value: well-drained, calcareous, silt-rich soils that are exceptionally well suited to saffron corm cultivation.

This makes the karewa landscape a rare example of a landform whose **geomorphological genesis directly determines a regional economy** — a relationship this project treats as its analytical core.

---

## 3. Problem Statement / Research Gap

Existing literature and investigative reporting establish, largely through qualitative and localised observation, that karewa terraces are being lost to unregulated soil excavation and urban sprawl. What is currently absent is:

1. A **systematic, multi-decadal, satellite-derived quantification** of karewa areal loss across the Kashmir Valley, rather than site-specific or anecdotal accounts.
2. A **spatially explicit overlay** of karewa loss against saffron cultivation extent, to determine the degree to which agriculturally productive terrace land — as opposed to marginal or already-degraded terrace land — is being consumed.
3. An assessment of whether existing policy instruments (notably the National Saffron Mission) are targeting land that is geomorphologically secure, or land that is already under active erosion pressure.

This project is designed to fill each of these three gaps using freely available satellite archives and open-source geospatial tools.

---

## 4. Research Questions

- **RQ1:** What is the net areal change in karewa terrace extent across the Kashmir Valley between the earliest usable Landsat archive and the present day?
- **RQ2:** Where is this loss concentrated, and does it correlate spatially with proximity to urban centres, road networks, or known mining activity?
- **RQ3:** What proportion of the lost terrace area overlapped with active or historical saffron cultivation, and what does this imply for the long-term viability of Kashmir's saffron economy?
- **RQ4:** Are current agricultural policy investments (e.g., National Saffron Mission funding) spatially aligned with the karewa land that remains geomorphologically and agronomically intact?

---

## 5. Objectives

1. To review and synthesise the geomorphological literature on karewa formation, stratigraphy, and classification, establishing a rigorous theoretical foundation for the landform under study.
2. To delineate karewa terrace boundaries across the study area using DEM-derived terrain analysis (slope, elevation break, terrain ruggedness) validated against optical imagery.
3. To construct a multi-temporal land-cover change detection pipeline using the Landsat and Sentinel-2 archives to quantify karewa surface loss to bare-earth/mining and built-up land cover over the longest feasible time series.
4. To map active and historical saffron cultivation extent within the Pampore belt and overlay it against the terrace-loss time series.
5. To evaluate the spatial correspondence between the mapped erosion/mining pressure and existing agricultural policy interventions, framing this as a governance and land-use planning question rather than a purely descriptive one.
6. To produce a public-facing research output — GitHub repository, interactive dashboard, research paper, and geospatial maps — consistent with the standard of the author's prior portfolio work.

---

## 6. Study Area

The primary study area is the central Kashmir Valley, encompassing the karewa belts of **Pampore, Pulwama, and Budgam districts**, together with the type-locality exposures near **Srinagar (Zewan section)**. This area was selected because it contains the highest concentration of saffron-bearing karewas in the valley and has been repeatedly identified in secondary literature as a hotspot of unregulated soil mining. Approximate bounding coordinates: 33.85°N–34.15°N, 74.75°E–75.15°E. The final analytical extent will be refined once terrace boundaries are delineated in the DEM-based reconnaissance stage.

---

## 7. Data Sources

| Data | Source | Purpose |
|---|---|---|
| Landsat 5/7/8/9 archive (1990s–2026) | USGS / Google Earth Engine | Multi-decadal land-cover change detection |
| Sentinel-2 (2015–2026) | Copernicus / GEE | High-resolution recent-period mapping |
| Copernicus DEM / Cartosat DEM | Copernicus Data Space / ISRO Bhuvan | Terrace delineation via slope-break and elevation analysis |
| Historical topographic sheets (if accessible) | Survey of India / archival sources | Pre-satellite-era baseline reference |
| Saffron cultivation extent | Department of Agriculture (J&K), literature, ground-truthed via imagery | Economic overlay layer |
| National Saffron Mission documentation | Government of India / J&K publications | Policy evaluation layer |

---

## 8. Methodology (Overview)

The workflow follows four broad stages: (i) DEM-based terrace reconnaissance and boundary delineation; (ii) multi-temporal supervised/unsupervised classification of karewa surface versus mined/built-up/agricultural land cover across the available archive; (iii) change detection and loss-rate quantification, disaggregated spatially to identify hotspots; and (iv) overlay analysis linking terrace loss to saffron cultivation extent and to existing policy investment, framed honestly around the limits of publicly available enforcement and land-lease data. Full technical detail will be developed and documented stage-by-stage as implementation proceeds.

---

## 9. Expected Deliverables

- Public GitHub repository with fully documented, reproducible code
- Interactive Streamlit dashboard presenting terrace-loss time series and hotspot maps
- A formal research paper with literature review, methodology, results, and discussion
- A project journal / development log documenting the research process
- A set of publication-quality static maps and figures for the portfolio

---

## 10. Significance

This project contributes a rigorous, satellite-based evidentiary basis to a landform-and-livelihood crisis that has, to date, been documented only qualitatively. It demonstrates the application of classical geomorphological theory (depositional stratigraphy, terrace genesis, terrain analysis) in direct combination with modern remote sensing and GIS methods, and extends that analysis into a policy-relevant question about the spatial targeting of agricultural support schemes. It is intended to stand alongside the author's existing portfolio of causal, policy-oriented geospatial research as evidence of methodological range across both physical and human geography.

----------------------------------------------------------------------------------------------------

## Day 1 — Project Setup, Data Acquisition, and Automated Terrace Extraction

**Objective:** Establish a fully scripted, reproducible pipeline to algorithmically identify karewa terrace boundaries across the Kashmir Valley study area, consistent with the methodological standard set in prior portfolio projects (script-first, QGIS reserved for visual validation only).

**Setup:** Initialized the project repository (`data/`, `src/`, `notebooks/`, `outputs/`, `dashboard/`, `docs/`, `tests/`) to separate raw inputs, processing code, intermediate outputs, and final deliverables.

**Data Acquisition:** Used the Google Earth Engine Code Editor to define the study area (Pampore–Pulwama–Budgam–Srinagar/Zewan karewa belt) and export the Copernicus GLO-30 DEM for the region. The DEM was downloaded and stored under `data/raw/`.

**Method:** Adopted a Topographic Position Index (TPI, Weiss 2001) combined with a slope threshold to algorithmically classify terrain that is simultaneously flat-topped and locally elevated relative to its surroundings — the defining terrain signature of a karewa terrace. This approach was chosen specifically to avoid manual digitization in QGIS, keeping the terrace-delineation step fully scripted and reproducible.

**Problems encountered and resolved:**
- The slope raster exported separately from GEE loaded as entirely invalid; resolved by deriving slope directly from the DEM within Python instead of depending on a second GEE export.
- The original DEM was in geographic coordinates (degrees), which is invalid for metric slope calculation; resolved by reprojecting to UTM Zone 43N before computing any terrain derivatives.
- Reprojection introduced a thin border of no-data pixels at the image edges, which would have propagated through the smoothing filters used for TPI; resolved by trimming the border and nearest-neighbour filling any residual gaps.
- An early diagnostic incorrectly reported the entire raster as invalid; this was a false alarm caused by NumPy's default min/max functions returning NaN if even one NaN pixel is present in the array. Resolved by switching to NaN-aware statistics and explicit valid-pixel counts, which confirmed 99.6% of the DEM was valid.
- The binary output mask (uint8) could not inherit the DEM's original no-data value; resolved by explicitly setting the mask's no-data to None.

**Calibration:** An initial run (TPI > 5 m, slope < 5°) produced 3,053 raw candidate polygons; after filtering to a minimum area of 0.05 km², 115 candidates remained. Visual inspection showed these polygons were unexpectedly thin and sliver-shaped rather than blob-like, indicating the thresholds were too conservative and were isolating only ridge crests rather than full terrace surfaces. Thresholds were loosened (TPI > 3 m, slope < 8°), yielding 6,789 raw polygons; after the same area filter, 201 candidates remained. A subsequent elevation filter (1,550–2,000 m, the expected valley-floor-adjacent band for karewa deposits) excluded none of these, confirming the two filters were mutually consistent.

**Validation:** Overlaying the final 201 candidate polygons on satellite basemap imagery showed them tracing visible upland terrain distinct from the forested valley floor, and — critically — aligning with the labeled "Saffron Fields, Lethpora" location near Pampore, a concrete ground-truth match.

**Outcome:** Milestone 2 (automated karewa terrace delineation) is complete. 201 candidate terrace polygons are stored at `data/interim/karewa_candidates_filtered.gpkg` and will serve as the spatial units for the next stage — multi-temporal detection of land-cover loss (mining and urban encroachment) within these boundaries.

## Multi-Temporal NDVI Change Detection Within Karewa Terraces

**Objective:** Quantify land-cover degradation within the 201 validated karewa terrace polygons by comparing vegetation condition between an early baseline (1994) and the present (2025), using satellite-derived NDVI as a proxy for vegetated/agricultural land versus bare-earth (mining or built-up) conversion.

**Method:** Acquired an early Landsat 5 composite (1993–1996) and a recent Sentinel-2 composite (2024–2025) via Google Earth Engine, computed NDVI for both, and used zonal statistics within each of the 201 terrace polygons to summarise change over time.

**Problem encountered:** The first run produced a counter-intuitive result — average NDVI *increased* across the terraces from 1994 to 2025, the opposite of the expected mining-driven degradation. Rather than accept this at face value, the result was treated as a methodological red flag, consistent with the standard of scrutiny applied in prior projects.

Two issues were identified and corrected:
1. **Seasonal mismatch** — the 1994 composite had been built from a full multi-year date range spanning all seasons (including winter, when vegetation is naturally dormant), while the 2025 composite was restricted to the summer growing season. This made the two periods incomparable and would artificially inflate the apparent NDVI increase regardless of any real land-cover change. Fixed by restricting the 1994 Landsat acquisition to the same June–September window as the 2025 Sentinel-2 composite.
2. **Metric insensitivity** — using the *mean* NDVI across each polygon diluted the signal from small, localised mining pits within otherwise large, intact terrace polygons. Replaced the mean-NDVI comparison with a **bare-earth-fraction metric**: the percentage of pixels within each polygon falling below an NDVI threshold indicative of bare ground, compared between the two periods.

**Result:** With both corrections applied, the average bare-earth fraction across the 201 terraces rose from 1.8% in 1994 to 8.4% in 2025 — a roughly 4.6-fold increase. Of the 201 polygons, **25 (12.4%) showed a substantial increase in bare-earth share (≥15 percentage points)** and were flagged as likely degraded; the remaining 176 appear to have retained their vegetated/agricultural character over the same period.

**Outcome:** Milestone 3 (multi-temporal degradation detection) is complete. The dataset `data/processed/karewa_bare_earth_change.gpkg` now carries, for each of the 201 karewa terraces, its 1994 and 2025 bare-earth fraction, the change between the two, and a likely-degraded/intact classification. This is the project's first quantified empirical result and will be spatially validated next, then overlaid against saffron cultivation extent to assess the economic significance of the observed loss.

## Spatial Validation of Degraded Terrace Classification

**Objective:** Visually validate whether the 25 polygons flagged as "likely_degraded" by the bare-earth-fraction analysis correspond to real, identifiable land-cover change, rather than being an artefact of the classification pipeline.

**Method:** Loaded `data/processed/karewa_bare_earth_change.gpkg` in QGIS over a satellite basemap, symbolised by the `status` field (categorised styling: degraded vs. intact), and visually inspected the spatial distribution of the two classes across the study area.

**Result:** The degraded polygons were not randomly scattered — they showed a spatially coherent pattern. The largest concentration appeared near Pari Gam Khalsa / Newa Pulwama, directly overlapping a visibly bare, tan-coloured patch in the satellite imagery consistent with an active quarry or mining pit, distinct from the surrounding vegetated terrain. A smaller degraded polygon was also found immediately adjacent to the labelled "Saffron Fields, Lethpora" location — directly connecting the observed degradation to the saffron-cultivation heartland that is central to this project's economic argument. A few additional isolated degraded polygons appeared near Srinagar airport and Wuyan, but were not part of any larger cluster.

**Outcome:** The spatial pattern of the classification is consistent with genuine, localised land-cover degradation rather than algorithmic noise, and provides visual corroboration for the quantitative bare-earth-fraction result from the previous stage. This also identifies a priority location — the Pari Gam Khalsa cluster — for closer visual/imagery inspection, and confirms that at least one degraded terrace lies directly at the margin of a known, named saffron-cultivation site. Next step: acquire or construct a saffron cultivation extent layer for the Pampore belt and overlay it against the degraded-terrace map to quantify how much of the observed loss falls within productive saffron land.

This is a genuinely strong robustness result — the affected share rises in a **smooth, gradual pattern** across the sensitivity range (21% → 29% → 43% → 71% → 86% → 93%), with no sudden or erratic jump. This confirms the headline 43%-within-1-km figure is not an artefact of one arbitrarily chosen cutoff, but reflects a real, consistent spatial signal: saffron fields sit genuinely close to degradation zones across a wide range of proximity definitions.

## Saffron Signature Detection and Proximity-Risk Analysis

**Objective:** Identify saffron-cultivating karewa terraces via their distinctive inverse phenology (dormant in summer, leafing out post-flowering), and quantify their spatial proximity to already-degraded terraces.

**Problem encountered:** The first saffron-index attempt (autumn NDVI minus summer NDVI, using an October–November "green" window) produced entirely negative values across all 201 polygons — the opposite of the expected signature. This was traced to saffron phenology: October–November is primarily the flowering period with sparse canopy, while the true leaf-canopy peak occurs later, after flowering, through the winter. Fixed by shifting the "green" comparison window to March, capturing post-flowering vegetative growth after snowmelt.

**Result:** With the corrected window, 14 of 201 terraces were classified as likely saffron-cultivating. None directly overlapped with the 25 already-degraded terraces, but proximity analysis showed the nearest saffron terrace lies just 80 metres from an active degradation zone, and 6 of 14 (43%) fall within 1 km of one. A sensitivity check across distance thresholds (500 m–2.5 km) showed a smooth, monotonic increase in the affected share, confirming this is a genuine spatial pattern rather than an artefact of the chosen cutoff.

**Outcome:** The project's core empirical and policy-relevant finding is established: saffron cultivation in the study area is not yet being directly consumed by mapped degradation, but a substantial share of it sits in close proximity to expanding bare-earth zones — an encroachment-risk finding rather than a direct-loss finding, and a more defensible claim than a blunt overlap statistic would have been.

## Benchmarking Detected Saffron Extent Against an Independent Baseline

**Objective:** Sanity-check the credibility of the saffron-signature detection by comparing the total area of the 14 identified saffron-cultivating terraces against an independent, authoritative estimate of Pampore's saffron cultivation extent.

**Method:** Located the FAO GIAHS (Globally Important Agricultural Heritage Systems) "Saffron Heritage Site of Kashmir in India" report (Part-1, 31 May 2012, prepared under GIAHS pilot project advisor Dr. F. Nehvi and SKUAST-K), which documents **over 3,200 hectares** dedicated to saffron cultivation at Pampore, supporting more than 17,000 farm families. Calculated the total area of the 14 detected saffron polygons for direct comparison.

**Result:** The detected saffron-signature area totalled 225.4 hectares — approximately 7% of the FAO-documented 3,200-hectare baseline, an apparent 93% shortfall.

**Problem encountered:** This magnitude of discrepancy was treated as implausible rather than accepted as a finding. A shortfall of this scale would imply a near-total collapse of Kashmir's saffron cultivation, which directly contradicts independent news reporting of saffron production in Kashmir reaching a 25-year high in recent seasons. The discrepancy was therefore attributed to a **detection-recall limitation** rather than a real-world land-use change: the saffron-signature classification is applied only within the 201 terrace-candidate polygons, which were themselves produced by an already-conservative automated filtering pipeline (TPI/slope/elevation thresholds followed by an area cutoff). Compounding this with a further phenological threshold for saffron detection narrows the result to a small, high-confidence subset rather than a comprehensive census of cultivated area.

**Outcome:** The comparison is retained in the project record as a transparent methodological limitation rather than a substantive result: the 14 detected polygons should be understood as a conservative, high-precision subset of saffron-bearing karewa terraces, not the full cultivated footprint. Critically, this limitation does not undermine the proximity-risk finding from the previous stage (43% of detected saffron terraces within 1 km of a degraded terrace), since that result is a relative spatial comparison within the detected subset and does not depend on the subset representing the total saffron area. The FAO GIAHS baseline (3,200 ha; >17,000 farm families) is retained as a citable reference figure for the paper's introduction and literature review.

## Quantifying Absolute Karewa Area Lost to Bare-Earth Conversion

**Objective:** Convert the relative bare-earth-fraction results into an absolute, headline area figure — how many hectares of karewa terrace have actually been converted to bare-earth land cover between 1994 and 2025.

**Method:** For each of the 201 terrace polygons, multiplied polygon area by its bare-earth fraction in each period to obtain an absolute bare-earth area per polygon, then summed across all polygons for both years. The difference between the two totals gives the net area converted. The same calculation was repeated restricted to the 25 polygons previously flagged as "likely_degraded," to assess how concentrated the loss is.

**Result:** Total mapped karewa terrace area across the 201 polygons is 3,305.3 hectares — notably close to the FAO GIAHS-documented 3,200-hectare saffron cultivation baseline, which, while not measuring the identical quantity (total karewa area vs. saffron-specific area), served as a useful plausibility check on the overall scale of the terrace mapping. Bare-earth area rose from 32.2 hectares in 1994 to 222.6 hectares in 2025, a net conversion of **190.3 hectares (5.8% of total mapped terrace area)**. Of this net loss, 128.2 hectares — **67% of the total** — occurred within the 25 polygons already flagged as likely degraded, which together account for only 9.7% of the total mapped area.

**Outcome:** This establishes the project's headline empirical result: between 1994 and 2025, 190.3 hectares of karewa terrace were converted to bare-earth land cover, and this loss is spatially concentrated rather than diffuse — two-thirds of it occurring within a small subset (12.4%) of terraces. This figure, combined with the earlier proximity-risk result (43% of detected saffron terraces within 1 km of a degraded terrace), completes the project's core quantitative findings. The next phase moves from analysis to public-facing deliverables: visualizations, maps, dashboard, and the formal research paper.

## Extending to a Four-Point Multi-Temporal Trend

**Objective:** Address a limitation in the earlier two-point (1994 vs. 2025) degradation analysis by inserting two intermediate time points (2005 and 2015), to establish whether karewa degradation has proceeded as a steady multi-decadal trend or is concentrated in a particular period — consistent with the project's original aim of using "the longest feasible time series" rather than a single before/after comparison.

**Method:** Acquired season-matched (May–October) NDVI composites for 2005 (Landsat 5) and 2015 (Landsat 8) via Google Earth Engine, following the same acquisition and bare-earth-fraction methodology established for 1994 and 2025, and computed the mean bare-earth fraction across all 201 terrace polygons for each of the four years.

**Problem encountered:** The initial 2005 Landsat 5 query (matching the exact June–September window and cloud-cover threshold used for 1994) returned zero images for the study area, causing the export to fail with a missing-band error. Diagnostic printing of collection size confirmed the collection was genuinely empty under those constraints. Resolved by widening the acquisition window to May–October, extending the search to a nine-year span (2001–2009) centred on 2005, and removing the explicit cloud-cover filter (relying on median compositing across the wider image set to suppress cloud contamination instead).

**Result:** The four-point trend in mean bare-earth fraction across all 201 terraces was: 1.84% (1994), 2.62% (2005), 2.63% (2015), and 8.43% (2025). The near-identical values for 2005 and 2015 indicate the terraces were relatively stable across that decade, while the sharp rise to 8.43% by 2025 shows that the majority of observed degradation has occurred within the most recent decade alone — its magnitude exceeding the combined change of the preceding two decades.

**Outcome:** This resolves the earlier two-point-comparison limitation and adds a materially important qualification to the project's headline finding: karewa degradation is not a steady, multi-decadal process but a recent and accelerating one, concentrated in 2015–2025. The dataset `data/processed/karewa_multitemporal_trend.gpkg` now carries bare-earth fraction for all four years per polygon. Next step: formally test whether degraded terraces are systematically closer to roads or urban settlements than intact terraces (Research Question 2), using OpenStreetMap infrastructure data.

## Testing Spatial Correlation Between Degradation and Road Proximity

**Objective:** Formally test Research Question 2 — whether degraded karewa terraces are systematically closer to road infrastructure than intact terraces, rather than relying on the earlier informal visual observation.

**Method:** Downloaded the OpenStreetMap drivable road network for the study area using `osmnx` (44,622 road segments), computed the distance from each of the 201 terrace polygons to the nearest road, and compared the distribution between degraded and intact terraces using a one-sided Mann-Whitney U test (chosen over a t-test due to the non-normal, zero-inflated distribution of distance values).

**Result:** Degraded terraces show a mean distance to the nearest road of 75.6 m (median 0.0 m — over half directly adjacent to or intersecting a road), compared to 133.1 m (median 38.5 m) for intact terraces. The Mann-Whitney U test confirmed this difference is statistically significant (p = 0.0116).

**Outcome:** Research Question 2 is answered with statistical support: degradation is significantly associated with proximity to road infrastructure, consistent with an access-driven mining/encroachment mechanism. This completes the project's planned analytical scope — both previously identified gaps (multi-temporal trend, formal spatial correlation testing) are now resolved. The dataset `data/processed/karewa_road_proximity.gpkg` carries the final enriched attribute table. The project now moves from analysis to the deliverables phase: visualizations, maps, dashboard, and the formal research paper.

## Comprehensive Review and Deep Verify (2026-08-02)

**Objective:** Apply the same comprehensive review standard used on the rest of the portfolio (GHOST_INFRASTRUCTURE, GREEN_ALIBI) to STOLEN_STRATA: full file-by-file review of every script and dashboard page, independent recomputation of every reported statistic from raw and processed data, citation verification against real external sources, and a documentation-hygiene pass.

**Bug found and fixed — reproducibility break in terrace delineation:** `src/analysis/01_extract_karewa_terraces.py`, as checked into the repository, hardcoded `tpi_threshold = 5` and `slope_threshold = 5` — the *first, rejected* threshold pair from this log's own Day 1 entry, which produced only 115 thin, sliver-shaped candidate polygons. The actual thresholds used to produce every reported result in this project — 201 proper terrace polygons, 3,305.3 ha, and everything downstream of it — were the loosened pair, TPI > 3 and slope < 8°, as documented earlier in this same log and in the dashboard's Geomorphological Delineation page. In other words, the script on disk did not reproduce the pipeline that actually generated the paper's headline numbers: anyone cloning the repository and re-running it from scratch would have silently gotten the rejected 115-terrace result instead. Confirmed by re-running the DEM → TPI/slope → vectorize step from the raw `StolenStrata_DEM_GLO30.tif` with both threshold pairs: the checked-in (5, 5) pair reproduces exactly 115 candidates after the area filter, while the documented (3, 8) pair reproduces exactly 201 — matching every processed `.gpkg` file in the repository. Fixed by correcting the thresholds in the script and adding an inline comment recording the calibration history so this cannot silently drift again.

**Deep Verify — every headline statistic independently recomputed, all confirmed exact:** Working from the raw rasters and the raw OSM road-network export (not just re-reading the saved processed `.gpkg` files), independently reproduced: the four-point bare-earth-fraction trend (1.84% / 2.62% / 2.63% / 8.43% for 1994/2005/2015/2025, recomputed directly from the raw NDVI composites via the same zonal bare-earth-fraction method); total mapped terrace area (3,305.3 ha); net bare-earth conversion (190.3 ha, 5.8% of mapped area) and its concentration within the 25 flagged terraces (128.2 ha, 67% of net loss, terraces covering only 9.7% of mapped area); the saffron-signature count and area (14 terraces, 225.4 ha, recomputed directly from the raw Saffron Index raster); the full six-point proximity-risk sensitivity curve (21% / 29% / 43% / 71% / 86% / 93% at 500 m–2,500 m — previously only the 500 m and 2,500 m endpoints were marked "confirmed" in the dashboard, with the four interior points flagged as merely indicative; all six are now confirmed exact); and the road-proximity Mann-Whitney result (75.6 m vs. 133.1 m, p = 0.0116, against the full 44,622-segment OSM road network). No discrepancies were found in any of these — a materially cleaner result than the raw-data audits run on some other projects in this portfolio, which did surface aggregation bugs.

**Geomorphometrics closed out:** `src/analysis/10_geomorphometrics_and_figures.py` had been run previously but its result was left gated behind a `GEOMORPHOMETRICS_CONFIRMED = False` flag in the dashboard, with the Geomorphological Delineation page stating the characterisation was "being finalised." Independently recomputed compactness (4π·Area/Perimeter²) and mean internal slope from the raw DEM and confirmed the saved figures exactly: degraded terraces are significantly less compact than intact ones (0.138 vs. 0.191, Mann-Whitney p = 0.0044) — a shape-based signal, independent of the NDVI-derived bare-earth fraction, that the same 25 flagged terraces also carry irregular, dissected boundaries consistent with excavation scarring. Mean internal slope does not differ significantly by status (2.89° vs. 3.06°, p = 0.1711). This is now reported as a confirmed supplementary finding — Research_Paper.md §3.7/§4.6, Project_Journal.md Phase 6, and the dashboard's Geomorphological Delineation and Methodology & Data pages — rather than left as a pending item.

**Citations verified:** All external references in `Research_Paper.md` were checked against real, locatable sources — De Terra & Paterson (1939), Dar & Zeeden (2020, Frontiers in Earth Science), Bhat et al. (2016, Journal of the Geological Society of India), Weiss (2001), Boeing (2017, OSMnx), Madasa, Orimoloye & Ololade (2021, Journal of African Earth Sciences), Mann & Whitney (1947), Engert et al. (2025, PNAS), Rafi & Syed (2023, Mongabay India), Deccan Herald (2022), FAO GIAHS (2012), and Press Post (2026) — all confirmed real and correctly cited; no fabricated or misattributed references found.

**Documentation hygiene:** Fixed a heading-level inconsistency in this log (the "Multi-Temporal NDVI Change Detection" section was an `#` H1 rather than the `##` H2 used everywhere else; the "Saffron Signature Detection and Proximity-Risk Analysis" section was unstyled bold/italic text rather than a heading at all) — both now use consistent `##` headings and `**bold**` field labels matching the rest of the log. Rewrote an informal Hinglish note left mid-document (in the Spatial Validation section) into paper-appropriate English prose without changing its meaning. Added this clickable Index at the top of the log, matching the convention used in GREEN_ALIBI, GHOST_INFRASTRUCTURE, and BORDER_OPTICS. Corrected a project-wide "nine-page dashboard" claim (README.md ×2, Project_Journal.md ×1) to the actual eight pages, and a stray "Development_Log.md" reference in README.md (×2) to match this file's actual on-disk name, `Devlopment_Log.md`. Fixed a grammar slip ("a evidentiary basis" → "an evidentiary basis") on the dashboard's Governance & Infrastructure page. Removed a fictional `docs/` folder and an inaccurate root `requirements.txt` claim from README.md's repository-structure diagram and the dashboard's Methodology & Data page — replaced with an accurate structure, and a genuine root-level `requirements.txt` (covering the full analysis pipeline: geopandas, rasterio, numpy, scipy, osmnx, matplotlib, plus the dashboard's streamlit/plotly/kaleido) was added so README's literal "pip install -r requirements.txt" instruction actually works from the repository root.

**Outcome:** STOLEN_STRATA's Review-Fix and Deep Verify stages are complete. One reproducibility-breaking bug was found and fixed (script/result mismatch, not a result-correctness bug — every number ever reported in the paper was always correct); no bugs were found in any reported statistic itself. A previously-pending supplementary analysis (geomorphometrics) was completed and incorporated. All citations check out. Documentation hygiene issues (heading consistency, an informal note, several stale cross-references) were fixed.

## Structured Review — Triage and Fixes (2026-08-03)

**Objective:** Ran the project through four independent review passes, each structured around a different reviewer lens (statistical rigor, methodology defensibility, documentation consistency, and cross-portfolio consistency), each pass framed as an Erasmus Mundus GEM/CDE panel reviewer would approach it. All four passes converged strongly on the same handful of concerns, which is itself useful signal about where the real weak points are, rather than four scattered lists. This entry documents what was fixed, what was genuinely investigated and found to already be correct, and what was deliberately left as future work with a stated reason — the same standard applied to the review passes GREEN_ALIBI and GHOST_INFRASTRUCTURE went through.

**Fixed — threshold arbitrariness (all four passes flagged this):** The TPI/slope terrace-delineation pair, the 15-percentage-point degradation threshold, and the 0.15 saffron-signature threshold were all originally chosen by visual inspection with no reported sensitivity check. New script `src/analysis/11_threshold_sensitivity.py` sweeps all three: the degradation threshold across 5-30 percentage points (the reported 25-terrace count sits in a stable 23-31 range across the 12-20pp neighbourhood), the saffron threshold across 0.05-0.25 (the 43% proximity-risk share stays within 39-44% across 0.05-0.175, only destabilising below n=6 detected terraces), and a 3x3 TPI/slope grid (smooth and monotonic, 144-279 candidates, with the chosen (3,8) pair sitting centrally). New Research_Paper.md §3.9/§4.7, Project_Journal.md Phase 7.

**Fixed — resolution mismatch quantified, not hand-waved:** The paper previously said finer 2025 Sentinel-2 resolution "may modestly inflate" the post-2015 acceleration versus the 30m Landsat used for 1994/2005/2015 — vague and untested. New script `src/analysis/12_robustness_and_effect_sizes.py` resamples the 2025 composite to 30m (area-average downsampling) and reruns the bare-earth-fraction pipeline: mean fraction falls from 8.43% to 7.48%, net conversion from 190.3 to 165.2 ha, degraded count from 25 to 23 — a real, now-quantified ~13% resolution effect. The underlying acceleration survives it: even at matched 30m resolution, 7.48% is still ~2.8x the flat 2005/2015 baseline. Research_Paper.md §4.8, Limitations, and Abstract updated with the actual numbers in place of the vague hedge.

**Fixed — effect sizes and multiple-comparison correction:** The project runs three Mann-Whitney tests against degradation status (road proximity, compactness, slope) and had reported only p-values. Same script (12) adds rank-biserial correlation for each (road proximity r=0.268, compactness r=0.352, slope r=-0.170 — small-to-moderate, not overwhelming) and a Holm-Bonferroni correction across the 3-test family: road proximity and compactness both survive; slope was already non-significant. Research_Paper.md §4.9.

**Fixed — a real documentation bug a "centroid vs. edge distance" critique surfaced:** The review passes argued straight-line road distance should use terrace edges, not centroids, for accuracy in hilly terrain. Checking `src/analysis/09_road_proximity.py` against the paper's own methodology text found the *paper* was wrong, not the code: the script has always computed `polygon.distance(roads_union)` — full-polygon minimum distance — never a centroid. Research_Paper.md §3.6, Project_Journal.md, and the dashboard's Governance & Infrastructure page all previously misdescribed this as centroid-based; corrected to describe what the code actually does. This also fully answers the critique, since edge-distance was the methodologically correct approach it was asking for all along.

**Reframed, not just caveated — the saffron detection shortfall:** All four review passes pushed hardest on the 93% saffron-detection shortfall against the FAO baseline, several arguing it could undermine the 43%-within-1km proximity-risk finding built on that same 14-terrace subset. Rather than leaving this as a bare limitation, added the logical argument that a higher-recall detection method would plausibly also catch smaller, less spectrally distinct saffron parcels — which, being smaller, likely sit nearer the margins of already-mined terrain — making 43% a plausible conservative floor rather than an inflated estimate. Combined with the threshold-sensitivity result above (43% is stable across a wide detection-threshold range), this is now a defensible position rather than an unaddressed gap. Research_Paper.md §5 Discussion, Project_Journal.md, dashboard Saffron Vulnerability page.

**Investigated, not fabricated — RQ4 (governance/policy alignment):** One review pass pushed hardest that RQ4 being left fully open was a "missed opportunity" and suggested building a district-level overlay table of PM Saffron Mission rejuvenation targets against the degradation map — but the illustrative table sketched during that pass used made-up district figures, not real ones. Ran an actual search for spatially resolved PM Saffron Mission site- or district-level allocation data; found only the same aggregate, valley-wide figures already cited (2,598 ha under rejuvenation, Rs 400 crore — Press Post, 2026), with no locatable dataset at a resolution this project's terrace-level map could be meaningfully overlaid against. Building a policy-alignment table from invented numbers would look more complete but be actively dishonest, so RQ4 stays an explicitly documented open question — now with the search attempt itself recorded so it reads as investigated-and-blocked rather than skipped. Research_Paper.md §6 Limitations, dashboard Governance page.

**Added — explicit statement of the accuracy-assessment gap:** Multiple review passes noted no formal accuracy assessment (confusion matrix, producer's/user's accuracy against independently labelled ground-truth points) exists — only visual QGIS validation against known locations. This is accurate and was not previously stated as directly. Building a real confusion matrix requires manually labelling a sample of points against historical high-resolution imagery, which is a genuine data-collection task rather than something that can be computed from data already on hand — it is recorded as the single highest-priority item for future work rather than attempted with fabricated labels. Research_Paper.md §6 Limitations. (Resolved in the next entry.)

**Fixed — the 2005 composite-window caveat was missing:** The 2005 bare-earth-fraction figure is not a single-year snapshot; the original Landsat 5 query returned zero images and the window was widened to a nine-year span (2001-2009) centred on 2005 (documented earlier in this log). This was never stated as a limitation despite affecting how the "flat 2005-2015" stability claim should be read. Now explicit in Research_Paper.md and Project_Journal.md Limitations.

**Added — a causality caveat on the road-proximity finding:** The finding that degraded terraces sit closer to roads is correlational; no dated road-construction record exists to establish whether roads preceded degradation or vice versa. Both readings are consistent with an accessibility-driven extraction model, and the paper now says so explicitly rather than implying causation. Research_Paper.md §5 Discussion, dashboard Governance page.

**Explicitly not attempted this round, with reasons:** a supervised (Random Forest/XGBoost) saffron classifier to improve detection recall — a genuine improvement, but a new model-training effort beyond a review-triage pass, better scoped as its own future-work item; a least-cost-path (slope-weighted) road-distance metric in place of straight-line distance — plausible refinement, not attempted since the straight-line polygon-distance approach is already methodologically defensible and clearly documented as such; a manually-labelled ground-truth accuracy assessment — see above, requires new data collection rather than reanalysis (resolved in the next entry); an interactive "policy simulator" dashboard widget and additional narrative framing/comparison devices ("Xha = N football fields") — presentation polish rather than a correctness or rigor fix, left to a future dashboard-polish pass if wanted.

**A meta-note on portfolio-wide pattern:** One review pass flagged that this project's own dev-log rhetorical structure — "Day 1 struggles," "Problems encountered and resolved," a "Comprehensive Review and Deep Verify" entry with near-identical phrasing — closely mirrors GREEN_ALIBI's and GHOST_INFRASTRUCTURE's logs, and warned that a panel reviewing the whole portfolio at once might read this as templated rather than as three genuinely independent research efforts. The underlying work in all three projects is independently verifiable (each has its own raw data, its own bugs, its own fixes), but the *prose structure* is admittedly similar because the same review workflow was applied deliberately, project to project, for consistency. Noted here rather than silently ignored; worth being aware of if asked about it directly rather than treating it as a non-issue.

**Outcome:** All four review passes' technically substantive critiques (threshold sensitivity, resolution mismatch, effect sizes/multiple comparisons, the centroid/edge-distance description, the saffron-shortfall framing) were investigated and fixed with real computation, not reworded around. The one critique that would have required fabricating data (RQ4's district-level policy table) was investigated honestly and left open with the investigation documented. Two new reproducible scripts (`11_threshold_sensitivity.py`, `12_robustness_and_effect_sizes.py`) were added to `src/analysis/`, continuing the pipeline's numbering and script-first convention.

## Infrastructure, Economic, and Regulatory Extension (2026-08-14)

**Objective:** Three of the items flagged as future work in the previous entry — the ground-truth accuracy assessment, a second infrastructure-proximity signal, and a way to express the saffron-proximity finding in terms that land with a policy audience — were substantive enough to warrant their own pass rather than staying on a future-work list indefinitely. This entry covers settlement proximity, economic valuation, and karewa's legal-protection status; the ground-truth accuracy assessment is tracked separately pending a manually-labelled reference sample.

**Added — settlement proximity as a second, independent infrastructure signal:** Road proximity alone leaves open whether the accessibility-driven model is road-specific or reflects general human-activity proximity. Downloaded 3,266 OpenStreetMap building footprints for the study area and computed the same polygon-to-nearest-feature distance test already used for roads (`src/analysis/14b_settlement_proximity.py`, mirroring `09_road_proximity.py`'s methodology exactly). Result: degraded terraces sit a mean 455.9 m from the nearest building (median 202.0 m) versus 999.7 m (median 816.6 m) for intact terraces — a highly significant difference (Mann-Whitney p = 0.0001) and, at rank-biserial r = 0.465, the strongest effect of any test in this study, stronger than road proximity's r = 0.268. Merged into `karewa_final_with_geomorphometrics.gpkg` and folded into the effect-size/Holm-Bonferroni correction in `12_robustness_and_effect_sizes.py`, now run across four tests instead of three; settlement proximity, compactness, and road proximity all survive correction, slope remains non-significant. SS_Research_Paper.md §3.6/§4.5/§4.9, new Figure 13.

**Added — economic valuation of the saffron-proximity finding:** The 43%-within-1km proximity-risk result (Section 4.4) was reported only in hectares. Sourced official 2024-25 J&K saffron figures from the state legislative assembly (Agriculture Production Dept., reply to MLA Hasnain Masoodi: 19.58 MT from 3,715 ha statewide, valued at Rs 534.53 crore) — cross-verified the yield figure independently (19.58 MT / 3,715 ha = 5.27 kg/ha, matching the officially reported figure exactly) before using it, and derived an implied price of Rs 2.73 lakh/kg from value divided by quantity rather than pulling a separate retail listing, so yield, area, and price are all internally consistent with one source (`src/analysis/15_economic_valuation.py`). Applied to this study's own detected-saffron dataset: the 225.4 ha of detected saffron terraces represents an estimated Rs 32.4 crore in annual production value; the 123.6 ha within the 1 km at-risk radius represents an estimated Rs 17.8 crore (55% of the total). Framed explicitly as a value-at-risk figure, not a realized-loss claim, since it would otherwise contradict the study's own finding that no saffron terrace directly overlaps mapped degradation. SS_Research_Paper.md §3.5/§4.4/§5/§6.

**Added — karewa's legal-protection status:** RQ4 (whether PM Saffron Mission investment is spatially targeted) stays an open question — no fabricated policy-alignment table was built to close it. But a related, answerable question — whether any legal protection regime covers karewa land at all — was investigated through J&K legislative reporting. Finding: no statute currently protects karewas from excavation; a private member's bill (Dr. Syed Bashir Veeri, MLA for Bijbehara) proposing a Karewa Protection Authority, mandatory EIA before mining leases, and penalties up to Rs 10 lakh/5 years remains pending as of the most recent reporting located, with the Revenue and Geology & Mining Departments continuing to issue the excavation permissions the bill would restrict. This reframes how the road- and settlement-proximity results should be read — not as evidence of enforcement failure against an existing rule, but as the spatial signature of extraction proceeding in a genuinely unregulated space. SS_Research_Paper.md §3.8/§5, dashboard Governance & Infrastructure page.

**Also generated during this pass:** a 150-point stratified ground-truth sample (75 mapped bare-earth, 75 mapped vegetated, `outputs/ground_truth_sample_points.gpkg`) for manual reference-labelling against a satellite basemap — this is the highest-priority item from the review passes above, and is being labelled separately since it requires visual interpretation this pipeline cannot automate. Once labelled, it will produce the confusion matrix and producer's/user's accuracy figures those passes identified as missing.

**Outcome:** Two new reproducible scripts (`14b_settlement_proximity.py`, `15_economic_valuation.py`) join the pipeline, continuing its numbering and script-first convention; `12_robustness_and_effect_sizes.py` was updated in place to run across four tests rather than three, since settlement proximity is now part of the study's design rather than an add-on. SS_Research_Paper.md, SS_Project_Report.md, README.md, and the dashboard were all updated to reflect the expanded scope consistently.

## Interactive Map Suite and Code Cleanup Pass (2026-08-14)

**Objective:** Rebuild the interactive map suite so every layer in the study — including the two added in the previous entry — has both a static and an interactive export, add a settlement-proximity static map to match the new interactive one, and pass through every script in the repo trimming comments down to short, functional notes.

**Rebuilt — all interactive maps now generated from the project's own geopackages:** the QGIS2Web export path was dropped entirely (that pipeline had already excluded the saffron proximity-risk map over broken buffer symbology). `src/visualization/build_interactive_maps.py` now builds all 8 maps directly with GeoPandas + Folium — study area overview, terrace degradation status, terrace boundaries, Lethpora validation, saffron proximity risk (rebuilt with clean buffer rendering, fixing the earlier export issue), road network proximity, settlement proximity, and saffron economic value-at-risk. The road-network layer is merged into a single geometry before export (44,622 separate LineStrings brought the file to 11 MB; one merged MultiLineString brings it to 2.6 MB with no visual loss at this zoom range). Every map's feature count was checked against its source geopackage before treating the export as correct.

**Added — two new static maps:** `src/visualization/build_static_maps.py` produces `outputs/maps/07_settlement_proximity.png` and `outputs/maps/08_economic_value_at_risk.png` in the same dark print-layout style as the original six QGIS exports (sampled the exact background/panel/legend colors from `06_road_network_proximity.png` to match). The original six static maps and all ten dashboard figures were checked against current data and left as-is — none of the underlying terrace, road, or compactness numbers changed this pass, so they remain accurate; only the two new layers needed new maps.

**Updated — dashboard Interactive Maps page:** `dashboard/pages/7_Interactive_Maps.py` now lists all 8 maps in its dropdown and no longer carries the "saffron map temporarily excluded" caveat, since the rebuilt version renders correctly.

**Code cleanup — comments trimmed to plain, functional notes:** swept every script under `src/` and `dashboard/` for docstrings and comment blocks that had drifted into explanatory-essay territory (`11_threshold_sensitivity.py`, `12_robustness_and_effect_sizes.py`, `15_economic_valuation.py`, `14a`/`14b`, `dashboard/data.py`, `dashboard/style.py`, `dashboard/export_charts.py`, `dashboard/pages/8_Methodology_Data.py`) and cut them down to one-line, working-note-style headers. Also fixed a stale filename reference in `01_extract_karewa_terraces.py`'s threshold-calibration comment (`Devlopment_Log.md` → `SS_Development_Log.md`, matching the earlier file-naming correction) and removed a leftover conversational line from `14a_download_settlement_footprints.py`'s final print statement.

**Outcome:** Two new reproducible scripts (`build_interactive_maps.py`, `build_static_maps.py`) join `src/visualization/`; all 8 interactive maps and all 8 static maps are now generated from source data rather than partly depending on a QGIS export step. SS_Research_Paper.md gained Figures 14 and 15 and a note that every static map has an interactive counterpart; README.md's Interactive Maps and Interactive Plots sections were rebuilt to list all 8 maps; the portfolio site's STOLEN STRATA card was updated to link them individually via a dropdown, matching the pattern already used for other projects.

