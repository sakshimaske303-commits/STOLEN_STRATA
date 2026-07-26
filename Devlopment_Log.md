# STOLEN STRATA
### Quantifying the Anthropogenic Erasure of Kashmir's Karewa Terraces and Its Threat to the Saffron Economy

**Author:** Sakshi D. Maske
**Region of Study:** Kashmir Valley, Jammu & Kashmir, India
**Discipline:** Geomorphology · Remote Sensing & GIS · Environmental Policy

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

# Multi-Temporal NDVI Change Detection Within Karewa Terraces

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

Bohot achha robustness result — **smooth, gradual pattern hai** (21% → 29% → 43% → 71% → 86% → 93%), koi sudden ajeeb jump nahi. Ye confirm karta hai ki tera 43% number kisi ek arbitrary cutoff ka fluke nahi hai — ye ek genuine, consistent spatial signal hai ki saffron fields degradation zones ke kaafi kareeb hain.

**Saffron Signature Detection and Proximity-Risk Analysis**

*Objective:* Identify saffron-cultivating karewa terraces via their distinctive inverse phenology (dormant in summer, leafing out post-flowering), and quantify their spatial proximity to already-degraded terraces.

*Problem encountered:* The first saffron-index attempt (autumn NDVI minus summer NDVI, using an October–November "green" window) produced entirely negative values across all 201 polygons — the opposite of the expected signature. This was traced to saffron phenology: October–November is primarily the flowering period with sparse canopy, while the true leaf-canopy peak occurs later, after flowering, through the winter. Fixed by shifting the "green" comparison window to March, capturing post-flowering vegetative growth after snowmelt.

*Result:* With the corrected window, 14 of 201 terraces were classified as likely saffron-cultivating. None directly overlapped with the 25 already-degraded terraces, but proximity analysis showed the nearest saffron terrace lies just 80 metres from an active degradation zone, and 6 of 14 (43%) fall within 1 km of one. A sensitivity check across distance thresholds (500 m–2.5 km) showed a smooth, monotonic increase in the affected share, confirming this is a genuine spatial pattern rather than an artefact of the chosen cutoff.

*Outcome:* The project's core empirical and policy-relevant finding is established: saffron cultivation in the study area is not yet being directly consumed by mapped degradation, but a substantial share of it sits in close proximity to expanding bare-earth zones — an encroachment-risk finding rather than a direct-loss finding, and a more defensible claim than a blunt overlap statistic would have been.

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

