# Sakshi D. Maske

Independent Geospatial Researcher

## Abstract

Karewa terraces — elevated, flat-topped remnants of a Pliocene-Pleistocene intermontane lake basin — underlie one of Kashmir's most economically important agricultural systems, the saffron cultivation belt of Pampore. Their loss to unregulated soil mining and unplanned urban expansion is well documented anecdotally but has not previously been quantified through a systematic, multi-decadal, satellite-derived pipeline. This study delineates 201 karewa terraces (3,305.3 ha) across the central Kashmir Valley using a Topographic Position Index and slope-threshold terrain analysis, then tracks their bare-earth land-cover fraction across four time points (1994, 2005, 2015, 2025) using season-matched Landsat and Sentinel-2 composites. Mean bare-earth fraction rose from 1.84% to 8.43% over the study period, with the increase concentrated almost entirely in the final decade; in absolute terms, 190.3 hectares of terrace surface converted to bare earth, 67% of it within just 12.4% of terraces. A saffron-signature index, exploiting the crop's inverted phenology, identifies 14 likely saffron-cultivating terraces, 43% of which lie within 1 km of an already-degraded terrace despite no direct overlap — an encroachment-risk finding rather than a direct-loss one. A Mann-Whitney U test confirms degraded terraces sit significantly closer to road infrastructure than intact terraces (p = 0.0116), consistent with an accessibility-driven model of unregulated extraction. Together these results establish karewa degradation as a recent, accelerating, spatially concentrated, and infrastructure-linked phenomenon, with direct implications for how saffron-sector policy investment should be spatially targeted.

**Keywords**: karewa terraces, Kashmir, saffron, land degradation, remote sensing, multi-temporal change detection, unregulated mining, geomorphology

---

## 1. Introduction

The Kashmir Valley's karewa terraces are a geologically singular landform: flat-topped, loess-capped remnants of an ancient lake basin whose fertile, well-drained soils happen to be exceptionally well suited to *Crocus sativus* — saffron — a Geographical Indication-tagged crop that anchors the livelihoods of thousands of farming households in the Pampore belt. Investigative and grey-literature reporting has, over the past decade, documented a steady conversion of this landform into construction-grade soil, driven by unregulated mining for the brick and construction industries and by unplanned urban and infrastructure expansion. What this reporting has not done is quantify the phenomenon systematically, at scale, across time, using independent satellite evidence.

This study addresses that gap directly. Rather than relying on site-specific observation, it builds a fully scripted geospatial pipeline that delineates karewa terrace boundaries from terrain data alone, tracks their land-cover condition across a 31-year satellite record, and connects the resulting degradation pattern to two things that determine whether it matters: the saffron economy the terraces sustain, and the road infrastructure that makes their extraction economically viable in the first place.

## 2. Literature Review

### 2.1 The Geomorphological Origins of the Karewa Landscape

The Karewa Group sediments have been studied since the earliest systematic Quaternary geology of the region, beginning with De Terra and Paterson's (1939) foundational stratigraphic work identifying a lacustrine-to-fluvial infill sequence tied to the tectonic uplift of the Pir Panjal Range. More recent work has refined this picture considerably: Dar and Zeeden (2020) review the loess-palaeosol sequences capping the karewa surface and their value as a Quaternary palaeoclimate archive, while Bhat et al. (2016) document soft-sediment deformation structures within the Karewa formations as evidence of palaeo-seismicity. This body of work establishes the karewa surface not as generic upland terrain but as a geologically distinctive, scientifically valuable record — one whose loss to excavation is a loss of both agricultural capacity and geological archive simultaneously.

### 2.2 A Landform Under Economic Pressure

Journalistic and policy-adjacent sources converge on the same underlying story: karewa land is being consumed faster than it is being protected. Rafi and Syed (2023), reporting for Mongabay India, document that the Qazigund-Baramulla railway project alone drew roughly 90% of its construction material from karewa excavation, alongside brick-kiln expansion in Budgam and continuing projects such as the Semi Ring Road, and quote local farmers directly linking this conversion to declining saffron-growing capacity. Against this backdrop of reported loss, the FAO's Globally Important Agricultural Heritage Systems documentation (FAO GIAHS, 2012) records over 3,200 hectares under saffron cultivation at Pampore, supporting more than 17,000 farming families — while separately, Kashmir's saffron sector has also been reported reaching a 25-year production high in recent seasons (Deccan Herald, 2022), a reminder that degradation and short-term output gains are not mutually exclusive signals and that neither should be read in isolation.

### 2.3 Remote Sensing Approaches to Land Degradation Detection

Terrain-based landform classification in this study follows Weiss's (2001) Topographic Position Index framework, which classifies terrain by comparing each cell's elevation to its local neighborhood mean rather than relying on absolute elevation — a method widely adopted for isolating terrain forms such as ridges, valleys, and, as applied here, flat elevated terrace surfaces. For the land-cover change component, this study draws on an established literature applying vegetation-index-based change detection to mining-driven land degradation specifically; Madasa, Orimoloye, and Ololade (2021) demonstrate that geospatial vegetation indices reliably discriminate mining-disturbed land from surrounding cover in a multi-temporal satellite record, a validation of the bare-earth-fraction approach adopted in this study's own methodology.

### 2.4 Infrastructure, Accessibility, and the Economics of Unregulated Extraction

A substantial and growing literature connects road infrastructure to the economics of unregulated resource extraction. Most recently, Engert et al. (2025) show that road expansion is a leading predictor of future tropical deforestation hotspots, reflecting a general principle that extractive land-use pressure concentrates where the marginal cost of transporting material to market is lowest. This study treats karewa mining as governed by the same logic, testing whether degraded terraces are systematically closer to drivable roads than intact ones. On the governance side, recent reporting on the Rs 400 crore PM Saffron Mission and its stated goal of bringing 2,598 hectares under rejuvenation (Press Post, 2026) establishes that meaningful policy capital is already being directed at this landscape — raising, but not yet answering, the question of whether that capital is spatially aligned with where degradation risk is actually concentrated.

## 3. Data and Methodology

### 3.1 Study Design

This study covers the central Kashmir Valley karewa belt spanning Pampore, Pulwama, and Budgam districts together with the type-locality exposures near Srinagar (Zewan section), selected for containing the highest concentration of saffron-bearing karewas in the valley and for being repeatedly identified in secondary literature as a hotspot of unregulated soil mining. Terrace boundaries are delineated algorithmically rather than manually digitized, and every subsequent analytical layer — degradation status, saffron signature, road proximity — is built on top of that same scripted delineation.

### 3.2 Data Sources

| Variable | Source | Temporal Coverage |
|---|---|---|
| Elevation / terrain | Copernicus DEM GLO-30 | Current |
| Land cover (bare-earth fraction) | Landsat 5/7/8/9; Sentinel-2 | 1994, 2005, 2015, 2025 |
| Saffron signature | Sentinel-2 (NDVI, phenology-based) | 2025 |
| Road network | OpenStreetMap (via `osmnx`) | Current |
| Saffron cultivation baseline | FAO GIAHS documentation | 2012 (reference) |

### 3.3 Terrace Delineation

Karewa terrace boundaries were delineated from the DEM using a Topographic Position Index (TPI > 3) combined with a slope threshold (< 8°), isolating terrain that is simultaneously flat-topped and locally elevated relative to its surroundings — the defining terrain signature of a karewa tread versus its bounding scarp. Candidate pixels were vectorized and filtered to polygons ≥ 0.05 km² in area and within the 1,550–2,000 m elevation band known to host karewa exposures, yielding 201 terrace polygons totalling 3,305.3 hectares.

### 3.4 Multi-Temporal Degradation Detection

Land-cover condition within each terrace was tracked using a bare-earth fraction metric — the share of pixels per polygon falling below an NDVI threshold indicative of bare ground — computed from season-matched (June–September) composites at four time points: 1994 (Landsat 5), 2005 (Landsat 5), 2015 (Landsat 8), and 2025 (Sentinel-2). A terrace was classified likely-degraded where its bare-earth fraction increased by ≥ 15 percentage points between 1994 and 2025.

### 3.5 Saffron Signature Detection

Saffron-cultivating terraces were identified using a Saffron Index exploiting the crop's inverted phenology: dormant and bare through summer, at peak leaf canopy in March following autumn flowering. The NDVI difference between the March leaf-canopy window and the summer dormant window was computed per terrace and thresholded at 0.15 to flag likely-saffron polygons. Distance from each flagged saffron polygon to the nearest degraded terrace was then computed, with a sensitivity analysis run across a 500 m–2,500 m threshold range.

### 3.6 Infrastructure Proximity Testing

The OpenStreetMap drivable road network within the study area (44,622 segments, extracted via `osmnx`; Boeing, 2017) was used to compute straight-line distance from each terrace centroid to the nearest road edge. Distances were compared between degraded and intact terraces using a one-sided Mann-Whitney U test (Mann & Whitney, 1947), selected over a t-test given the non-normal, zero-inflated distribution of terrace-to-road distances.

### 3.7 Governance Context

A fourth research question — whether current agricultural policy investment is spatially targeted toward intact rather than degrading karewa land — could not be tested statistically within this study, since spatially resolved, publicly accessible land-lease and scheme-level enforcement data for programs such as the PM Saffron Mission are not currently available. This question is instead addressed narratively in the Discussion, using the mapped degradation pattern established here as the evidentiary basis a future policy-alignment overlay could build on.

## 4. Results

### 4.1 Terrace Delineation and Validation

The terrace-delineation pipeline produced 201 candidate polygons spanning the Pampore-Pulwama-Budgam-Srinagar karewa belt. Overlaying these polygons on satellite basemap imagery showed them tracing visible upland terrain distinct from the forested valley floor and, critically, aligning with the independently labelled "Saffron Fields, Lethpora" location — a concrete ground-truth match rather than a coincidence of thresholding.

![Study Area Overview](outputs/maps/01_study_area_overview.png)

**Figure 1.** Study area overview showing the Kashmir Valley karewa belt, the analytical bounding box, and key settlement reference points.

![Delineated Terrace Boundaries](outputs/maps/03_terrace_boundaries.png)

**Figure 2.** The 201 karewa terrace polygons delineated algorithmically from Topographic Position Index and slope-threshold terrain analysis.

![Validation at Saffron Fields, Lethpora](outputs/maps/04_validation_lethpora.png)

**Figure 3.** Close-range validation of the delineation pipeline against the labelled Saffron Fields, Lethpora location, confirming mapped terrace boundaries correspond to a real, known cultivation site.

### 4.2 Multi-Temporal Degradation: A Recent, Accelerating Trend

Mean bare-earth fraction across all 201 terraces was essentially flat between 1994 and 2015 (1.84% → 2.62% → 2.63%), before more than tripling between 2015 and 2025 (2.63% → 8.43%). Of the 201 terraces, 25 (12.4%) crossed the threshold for likely degradation over the full study period.

![Terrace Degradation Status](outputs/maps/02_terrace_degradation_status.png)

**Figure 4.** Terrace-level degradation status, 1994–2025, showing the spatial distribution of likely-degraded terraces (25 of 201) relative to stable terraces.

![Four-Point Bare-Earth Trend, 1994–2025](outputs/figures/dashboard_charts/bare_earth_trend.png)

**Figure 5.** Mean bare-earth fraction across all 201 terraces at four time points, showing three decades of relative stability followed by a sharp post-2015 acceleration.

### 4.3 Absolute Area Lost and Its Concentration

Converting bare-earth fraction into absolute area, total bare-earth cover across all 201 terraces rose from 32.2 hectares in 1994 to 222.6 hectares in 2025 — a net conversion of 190.3 hectares, 5.8% of total mapped terrace area. Of this net loss, 128.2 hectares (67%) occurred within the 25 terraces already flagged as likely-degraded, even though those terraces account for only 9.7% of total mapped area: loss is heavily concentrated rather than diffuse.

![Bare-Earth Area, 1994 vs. 2025](outputs/figures/dashboard_charts/bare_earth_area_comparison.png)

**Figure 6.** Total bare-earth area across all mapped terraces, 1994 versus 2025.

![Loss Concentration Among Flagged Terraces](outputs/figures/dashboard_charts/loss_concentration_donut.png)

**Figure 7.** Share of total net bare-earth loss occurring within the 25 terraces flagged as likely-degraded, relative to their share of total mapped terrace area.

![Degraded vs. Stable Terrace Classification](outputs/figures/dashboard_charts/degraded_vs_stable_donut.png)

**Figure 8.** Classification split of all 201 delineated terraces into likely-degraded (25) and stable (176) categories.

### 4.4 Saffron Vulnerability and Proximity Risk

The Saffron Index flagged 14 of 201 terraces as likely saffron-cultivating, totalling 225.4 hectares — a smaller figure than the FAO's 3,200-hectare Pampore baseline, attributed to a compounding detection-recall limitation across the terrace-delineation and saffron-signature filtering stages rather than genuine crop-area loss, particularly given independently reported saffron production highs over the same period. No saffron terrace directly overlapped a degraded terrace, but the nearest sat just 80 m from an active degradation zone, and 6 of 14 (43%) fell within 1 km of one. A sensitivity check across the 500 m–2,500 m threshold range showed a smooth, monotonic increase in affected share (21% at 500 m, rising through 29%, 43%, 71%, and 86%, to 93% at 2,500 m), confirming this as a genuine spatial pattern rather than an artefact of the chosen cutoff.

![Saffron Proximity-Risk](outputs/maps/05_saffron_proximity_risk.png)

**Figure 9.** Detected saffron-cultivating terraces overlaid against proximity to the nearest degraded terrace.

![Saffron Proximity-Risk Sensitivity](outputs/figures/dashboard_charts/saffron_proximity_sensitivity.png)

**Figure 10.** Share of saffron-cultivating terraces classified "at risk" across a range of proximity thresholds to the nearest degraded terrace, from 500 m to 2,500 m.

### 4.5 Infrastructure Association: Degradation Follows Roads

Degraded terraces sat a mean 75.6 m from the nearest road (median 0.0 m — over half directly adjacent to or intersecting a road), compared to 133.1 m (median 38.5 m) for intact terraces. A one-sided Mann-Whitney U test confirmed this difference as statistically significant (p = 0.0116).

![Road Network Proximity](outputs/maps/06_road_network_proximity.png)

**Figure 11.** Degraded and intact terraces overlaid against the OpenStreetMap drivable road network, illustrating the closer road proximity of degraded terraces.

## 5. Discussion

The central finding of this study — that karewa degradation is recent, accelerating, and spatially concentrated rather than a slow, uniform, multi-decadal process — is directly consistent with the grey-literature accounts reviewed above, which describe intensifying mining pressure over roughly the same recent-decade window rather than a steady historical trend (Rafi & Syed, 2023). The strength of the road-proximity result (p = 0.0116) lends independent, quantitative support to what that reporting describes qualitatively as extraction driven by transport economics: material moves to market most cheaply where roads already exist, and this study's data confirm that degraded terraces are measurably, not just anecdotally, closer to road infrastructure than intact ones (Engert et al., 2025).

The saffron-proximity finding reframes the crop's risk profile usefully: rather than reporting a direct-loss statistic that the data do not yet support, the 43%-within-1-km result establishes an early-warning pattern — proximity as a leading indicator, not a lagging one. Read alongside the reported Rs 400 crore PM Saffron Mission investment and its 2,598-hectare rejuvenation target (Press Post, 2026), this study's terrace-level degradation and proximity-risk maps constitute the kind of empirically verified risk surface that a genuine policy-alignment evaluation would need — a comparison this study is not yet able to make directly, given current constraints on publicly accessible, scheme-level spatial data, but one its outputs are positioned to support once such data becomes available.

## 6. Limitations

Detected saffron cultivation area (225.4 ha) falls well below the FAO GIAHS-documented baseline (3,200 ha), a shortfall attributed to compounding recall limitations across two conservative filtering stages — terrace delineation followed by saffron-signature thresholding — rather than to genuine crop-area loss, and reported transparently as a methodological constraint rather than adjusted to fit expectation. Governance-alignment testing (RQ4) could not be completed statistically within this study due to the limited public availability of spatially resolved, scheme-level land-lease and enforcement data, and is deferred to future work rather than estimated. The multi-temporal analysis is bounded at its early end by the operational start of a usable, season-matched Landsat record; conditions prior to 1994 fall outside what satellite verification here can support.

## 7. Conclusion

This study finds that Kashmir's karewa terraces are undergoing measurable, accelerating degradation concentrated in the decade since 2015, that this degradation is significantly associated with proximity to road infrastructure rather than randomly distributed, and that the saffron economy dependent on these terraces — while not yet directly overlapping mapped loss — sits close enough to active degradation fronts to warrant treating proximity itself as the operative vulnerability metric. The resulting implication for policy is direct: resources allocated to saffron-sector rejuvenation and karewa protection should be evaluated against where degradation risk is empirically concentrated, rather than assumed to already be aligned with it.

## References

De Terra, H., & Paterson, T. T. (1939). *Studies on the Ice Age in India and Associated Human Cultures.* Carnegie Institution of Washington.

Dar, R. A., & Zeeden, C. (2020). Loess-Palaeosol Sequences in the Kashmir Valley, NW Himalayas: A Review. *Frontiers in Earth Science*, 8, 113.

Bhat, G. R., Bali, B. S., Balaji, S., Iqbal, V., & Balakrishna. (2016). Earthquake triggered soft sediment deformational structures (seismites) in the Karewa formations of Kashmir valley—An indicator for palaeo-seismicity. *Journal of the Geological Society of India*, 87, 439–452.

Weiss, A. D. (2001). Topographic Position and Landforms Analysis. Poster presented at the ESRI International User Conference, San Diego, CA.

Boeing, G. (2017). OSMnx: New Methods for Acquiring, Constructing, Analyzing, and Visualizing Complex Street Networks. *Computers, Environment and Urban Systems*, 65, 126–139.

Madasa, A., Orimoloye, I. R., & Ololade, O. O. (2021). Application of geospatial indices for mapping land cover/use change detection in a mining area. *Journal of African Earth Sciences*, 175, 104108.

Mann, H. B., & Whitney, D. R. (1947). On a Test of Whether one of Two Random Variables is Stochastically Larger than the Other. *Annals of Mathematical Statistics*, 18(1), 50–60.

Engert, J. E., Souza, C. M., Kleinschroth, F., Ishida, F. Y., Costa, S. P., Botelho, J., & Laurance, W. F. (2025). Road expansion risk predicts future hotspots of tropical deforestation. *Proceedings of the National Academy of Sciences*, 122(52).

Rafi, A. B., & Syed, S. (2023, January 27). Nourishing soils of Kashmir's karewas crumble under infrastructure. *Mongabay India*.

Deccan Herald. (2022). Saffron boom in Kashmir: Highest production in 25 years.

FAO GIAHS. (2012). *Saffron Heritage Site of Kashmir in India* (Part 1). Globally Important Agricultural Heritage Systems Pilot Project, SKUAST-K.

Press Post. (2026). Rs 400 cr PM Saffron Mission halts slide in Kashmir, 2,598 ha brought under rejuvenation.

