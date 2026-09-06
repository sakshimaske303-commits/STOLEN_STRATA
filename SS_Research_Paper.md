# Stolen Strata: Quantifying the Anthropogenic Erasure of Kashmir's Karewa Terraces and Its Threat to the Saffron Economy

Sakshi D. Maske

*Independent Geospatial Researcher*

## Abstract

Karewa terraces are elevated, flat-topped deposits of intermontane lake-basin age (Pleistocene/Pliocene), and they underlie one of Kashmir's most economically significant agricultural systems — the saffron-growing belt at Pampore. Everyone who follows agriculture in Kashmir already knows these terraces are vanishing under unregulated soil mining and uncontrolled urban expansion; there's ample reporting on it. What was missing was a number. So I built a systematic, multi-decadal pipeline from satellite observations to get one. From TPI and slope-threshold terrain analysis, I identify 201 karewa terraces (3,305.3 ha) across the central Kashmir Valley, and estimate the bare-ground fraction of each using season-matched Landsat and Sentinel-2 composites at four dates — 1994, 2005, 2015, and 2025. Over that period, mean bare-earth fraction (BEF) rose from 1.84% to 8.43%, and nearly all of that rise happened in the past ten years. This isn't slow, steady erosion — it's hot-spotted: 190.3 hectares of terrace surface have converted to bare earth, and 67% of that loss sits within just 12.4% of the terraces. A saffron-signature index, built on the crop's inverted phenology, flags 14 potential saffron-cultivating terraces; 43% of them sit within 1 km of an already-degraded terrace — none overlap directly, they're near degraded ground rather than on it, at least as far as the data show. At official 2024-25 yield and price figures, that at-risk segment represents roughly Rs 17.8 crore in annual production value — about 55% of the total annual production value this study traces to the area. The pattern holds even more strongly for settlements than for roads: degraded terraces sit significantly closer to roads than intact terraces (U = 1611.0, p = 0.0116), and even closer to settlements (U = 1176.0, p = 0.0001 — the strongest effect in this study). So this looks like an accessibility-driven mining pattern, not a random one. Then there's the legal question most satellite studies like this skip: is there anything to stop this excavation? No. There is presently no law protecting karewa land in Jammu & Kashmir; a private member's bill titled the 'Karewa Protection Authority' has been pending for a long time. I ran threshold-sensitivity sweeps, a resolution-matching robustness test against the Landsat/Sentinel-2 pixel-size mismatch, and effect-size and multiple-comparison corrections across all four statistical tests — none of it changes the basic picture, though a modest degree of resolution-dependence shows up in the size of the post-2015 acceleration. Combine the geomorphology, the economics, and the legal void, and this stops being a change-detection exercise. It becomes a landform loss with a price tag and a policy lever attached.

---

## 1. Introduction

Karewa terraces are flat-topped, loess-capped, and geologically unique — and, in the Kashmir Valley, it is this loess-cap that makes the soils perfectly suited to Geographical Indication (GI) registered saffron variety, Crocus sativus, which supports the lives of thousands of farming families in Pampore belt. But these terraces have been reported in investigative and grey literature for the last decade or so, with little regulation, and are being mined as construction quality soil for the brick, housing and infrastructure sectors for years without rhyme or reason.

It is what that reporting says – and it's a qualitative story. No one had systematically measured it across scale, through time and with independent, satellite evidence — so I did. This study is a complete scripted process geospatial pipeline. It defines boundary of karewa terraces using the terrain information and examines land-cover condition over the period of satellite observations for 31 years, in addition to tracking the dimension of the saffron economy that the terraces need to sustain – here valued in rupees, not just hectares of land – and the road and settlement infrastructure that makes this extraction economic in the first place – which is today, believe it or not, very little.

## 2. Literature Review

The Geomorphological Evolution of the Karewa Landscape

The well-established stratigraphy of De Terra and Paterson (1939) marks the beginning of systematic Quaternary geology of this region with a lacustrine to fluvial infill sequence that is related to the uplift of Pir Panjal Range. The image has since undergone many modifications. Dar and Zeeden (2020) provide a review of the loess/palaeosol sequences overlying the surface of the karewa and its potential as a archive of Quaternary palaeoclimate. soft-sediment deformation structures in the Karewa formations have been reported by Bhat et al. (2016), and are also considered as evidence of palaeo – seismicity. Together this body of work gave me the conviction that is the nature of the karewa surface not a type of upland surface which is being mined away in general. This is a geologically unique, scientifically instructive record that also represents a loss of agriculture and geological archive together.

### 2.2 A Landform Under Economic Pressure

There's a lot of mass sentiment and some news reporting fueling the perception that the land in Karewa is being lost faster than it's being saved — and the perception matches the facts. As reported by Mongabay India by Rafi and Syed (2023), the conversion of karewa, the use of brick-kiln expansion in Budgam, and the many ongoing projects such as the Semi Ring Road, further underscore only 90% of the construction material for the Qazigund-Baramulla project was sourced from karewa excavation, using direct quotes from local farmers linking the project with the loss of their ability to grow saffrons. According to the documentation done by the Globally Important Agriculture Heritage Systems by food and agriculture organization (FAO GIAHS, 2012) above 3200 ha. of land is under saffron cultivation at Pampore contributing to more than 17 thousand farming families. Kashmir's saffron cultivation, on the other hand, has been reported to be producing at its highest level in the past few seasons with 25-year production records (Deccan Herald, 2022). I kept that last number in mind throughout this study, as it can help remind you that degradation and short-term output gains do not necessarily contradict each other when actually reading either one or the other would be wrong.

The use of remote sensing approaches for detecting land degradation has grown substantially.

My terrain-based landform classification is based on the TPI of Weiss (2001), which classifies terrain by comparing the elevation of each cell to its local neighbourhood elevation mean, rather than to a reference elevation; this approach is commonly used to identify aspects of the terrain, such as ridges, valleys and here, flat raised terrace surfaces. Directly concerned with the change in land cover is Madasa, Orimoloye, and Ololade (2021) who find that geospatial vegetation indices are able to distinguish between mining disturbed ground and vegetated cover using a multi-temporal satellite record. That's substantial in my mind as to why I believed in a bare-earth-fraction approach for the methodology of this study.

There exists a large and expanding body of literature that relates the economic aspects of unregulated resource extraction to road infrastructure. The latest and most helpful for my purposes is Engert et al. 2025: road expansion is a primary driver of future deforestation "hotspots" in the tropics, a universal rule being that extractive land-use pressure focuses where it's easiest to extract material at minimal expense. I just take karewa mining because there is a logic to it, and I test it against that. The governance market value of PM Saffron Mission is recently fetched at Rs 400 crore while its goal is to rejuvenate 2,598 hectares (Press Post, 2026). That's the message for me — there's already policy investment going in here, so to speak. Doesn't tell me if that is actually capital lands with concentrated degradation risk (back to the question of Section 3.8).

## 3. Data and Methodology

### 3.1 Study Design

This study will focus on Pampore, Pulwama and Budgam districts and karewa exposures in the central Kashmir Valley (Zewan section) near Srinagar. This area was chosen for two reasons: firstly because there is the highest concentration of saffron-bearing karewas within the valley and secondly, based on the secondary literature, there is continuous talk about this area as a hotspot for unregulated soil mining. There are no hand-entered entries in this section. Terrace boundaries are formed from an algorithm and all the analytical layers derived above, the degradation status, the saffron signature, road proximity etc. are based on the same algorithm that was used to create the boundary itself.

### 3.2 Data Sources

| Variable | Source | Temporal Coverage |
|---|---|---|
| Elevation / terrain | Copernicus DEM GLO-30 | Current |
| Land cover (bare-earth fraction) | Landsat 5/7/8/9; Sentinel-2 | 1994, 2005, 2015, 2025 |
| Saffron signature | Sentinel-2 (NDVI, phenology-based) | 2025 |
| Road network | OpenStreetMap (via `osmnx`) | Current |
| Building footprints | OpenStreetMap (via `osmnx`) | Current |
| Saffron cultivation baseline | FAO GIAHS documentation | 2012 (reference) |
| Saffron yield, area, and production value | J&K Legislative Assembly, Agriculture Production Dept. | 2024-25 |
| Karewa legal-protection status | J&K legislative reporting (private member's bill) | 2025 |

### 3.3 Terrace Delineation

The rule I used to extract karewa terrace boundaries from the DEM is greater than TPI and less than a threshold angle of 8°. It separates locally raised flat-topped top surface from the surrounding, which is the correct topography element defining a scarp boundary of a karewa tread. I vectorized the candidate pixels, then reduced my search to only polygons with an area of at least 0.05 km2 and within the elevation band of 1550-2000 m, in which karewa exposures are thought to occur. This resulted in a remaining number of 201 terrace polygons accounting for 3,305.3 ha.

### 3.4 Multi-Temporal Degradation Detection

To measure the condition of the land covers within each terrace, I used a new metric I'm playing with that was bare-earth fraction, which was the percentage of the pixels within a given polygon that were below an NDVI threshold that I thought represented bare ground. It was calculated from each season-matched composite in the years 1994 (June-September, based on Landsat 5 data), 2005 (May-October, based on Landsat 5 data), 2015 (May-October, based on Landsat 8 data), and 2025 (June-September, based on Sentinel-2 data). Terraces that degraded by 15% or more of bare earth between 1994 and 2025 were likely degraded, and received this label.

### 3.5 Saffron Signature Identification and Economic Valuation

Saffron is dormant and barren this time of year, and has peak leaf canopy following autumn flowering in March, which is exactly what my Saffron Index is looking for. For each terrace, I calculated the difference between NDVI in the canopy window, and NDVI in the summer dormant window, and marked any portion that passed this threshold as likely-saffron at 0.15. From there, I looked at the distance from each flagged saffron polygon to the closest degraded terrace (between 500 m and 2500 m).

A line in a budget cannot be shifted by a hectare count. A rupee figure is likely to. Which's why, I have derived the annual estimate of the production in terms of estimated to be Rs 534.53 crore, using official figures of acreage of saffron grown is 3715 ha throughout J&K, and production figures come to 19.58 MT, statewide (reply from MLA Hasnain Masoodi to state Legislative Assembly Agriculture production Dept, Feb 2026). Overall they suggest a yield of 5.27 kg/ha and a price of almost Rs. 2.73 lakh/kg. I used this yield and price to all the saffron area and the subset of the area as well which are at risk. So what comes out of this is a number for a risk – a value at risk, not a claim of what any individual terrace produces – I have no means to measure direct.

### 3.6 Infrastructure Proximity Testing

Within the study area, I extracted the drivable road network using the OpenStreetMap package 'osmnx' (Boeing 2017) — 44,622 segments in total — pulling in the full road network rather than reducing it to centroid points. A minimum distance polygon to line; if a line crosses into the boundary, or it is in touch, this is treated as a valid 0 m line. I also did the same polygon-distance procedure on OpenStreetMap building footprints (3266 features), which provides a p1-second and independent accessibility indicator besides the road network. Roads relate, but not in a one-to-one way: A terrace next to a village access track might be well outside the extent of the roads classified as drivable roads and vice versa. Having to compare distances between degraded and intact terraces for each infrastructure layer, I opted for a one-sided Mann-Whitney U test, as this statistic was not sensitive to normality or zero-inflation of distance between terraces and infrastructure layers.

### 3.7 Geomorphometric Comparison

Are degraded terraces shape diverse, apart from the land cover? I checked, calculating two geomorphic variables per terrace: one compactness index (4π·Area/Perimeter2, with 1.0 being perfectly circle/Compact, (close to 0) being very elongated (dissected) shape), and another one being the mean terrace internal slope angle, obtained directly from the terrace delineation DEM. The degraded and intact terraces for both were compared using a Mann-Whitney U test.

### 3.8 Governance Context

I wanted to explore a fourth issue: Does current agricultural policy favor the investment of land which is technically good and fit for agriculture but is disturbed by degradation as compared to intact karewa? Well, I couldn't, I suppose, in an accessible form that is spatially resolved and accessible—country programs like the PM Saffron Mission don't have that kind of land-lease and enforcement data anyhow. So I approach it in a narrative manner instead in the discussion and present the pattern of degradation from this study as the evidentiary basis to support a future overlay that would be aligned with the policy. A different, more specific answer might have been possible: Is there any legal safeguards whatsoever on the karewa land, irrespective of which money funds the scheme? I could have looked into any of those other two, but one I could have done through legislative reporting in J&K, because protection status is a regulatory binary fact not something that I overlay on a map.

### 3.9 Threshold Sensitivity and Robustness Checks

The three numbers on which this whole study rests, the TPI/slope pair used to delineate terraces; the 15 percentage-point bare-earth degradation threshold; the 0.15 saffron-signature threshold, were determined by visual inspection of the known morphology and location of those points on maps. I didn't have a preset validated landscape on which to calibrate, so I wanted to see how important that was. I traversed different possible values of thresholds over a neighbourhood and recalculated the number of terraces, their areas and the risk percentage for each.

Two more checks. First, however, I wanted to coordinate the 10 m resolution Sentinel-2 data (2025) with the 30 m resolution Landsat data (30y), so I resampled the 10 m data into 30 m, and used the same bare-earth-fraction pipeline but with 30 m resolution, rerunning it with Sentinel-2 (2025) data, to explicitly show that the difference in resolution causes a post-2015 acceleration, rather than ignoring it, which is the worst place to do so. Second, to meet the requirements of this study, I calculated four rank bi-serial effect sizes, and applied a Holm-Bonferroni correction across the four Mann-Whitney tests that this study reports, as without correction 4 significance tests will overestimate the family-wise false-positive rate.

## 4. Results

Each static map below (Figures 1, 2, 3, 4, 9, 11, 14 and 15) is accompanied by an interactive counterpart that is pannable and zoomable and can be accessed from the Interactive Maps page of the dashboard, or directly from the information in the README.

### 4.1 Terrace Delineation and Validation

A total of 201 candidate polygons covering the Pampore-Pulwama-Budgam-Srinagar karewa belt. The result of the delineation pipeline was that. Overlaid on the satellite basemap images, they delineate visible landforms such as uplands and provide confirmation that they are in close proximity to the forested valley floor, which is where the forest community is expected, with the added advantage that they correspond to the "Saffron Fields, Lethpora" location shown on the map. Not just a coincidence that it's that same match that I set those thresholds on, it's a real match where it's done.

This section compares the macro-topography maps geomorphometrically.

![Study Area Overview](outputs/maps/01_study_area_overview.png)

**Figure 1.** Study area overview showing the Kashmir Valley karewa belt, the analytical bounding box, and key settlement reference points.

![Delineated Terrace Boundaries](outputs/maps/03_terrace_boundaries.png)

**Figure 2.** The 201 karewa terrace polygons delineated algorithmically from Topographic Position Index and slope-threshold terrain analysis.

![Validation at Saffron Fields, Lethpora](outputs/maps/04_validation_lethpora.png)

**Figure 3.** Close-range validation of the delineation pipeline against the labelled Saffron Fields, Lethpora location, confirming mapped terrace boundaries correspond to a real, known cultivation site.

### 4.2 Multi-Temporal Degradation: A Recent, Accelerating Trend

1.84% in 1994. 2.62% in 2005. 2.63% in 2015. Essentially flat for two decades. Then 8.43% by 2025 — more than triple. That's the mean bare-earth fraction across all 201 terraces, and the shape of that curve is the whole point of this section: this isn't a slow bleed, it's a recent acceleration. Twenty-five of the 201 terraces, 12.4%, crossed the threshold for likely degradation over the full study period.

![Terrace Degradation Status](outputs/maps/02_terrace_degradation_status.png)

**Figure 4.** Terrace-level degradation status, 1994–2025, showing the spatial distribution of likely-degraded terraces (25 of 201) relative to stable terraces.

![Four-Point Bare-Earth Trend, 1994–2025](outputs/figures/01_bare_earth_trend_1994_2025.png)

**Figure 5.** Mean bare-earth fraction across all 201 terraces at four time points, showing three decades of relative stability followed by a sharp post-2015 acceleration.

### 4.3 Absolute Area Lost and Its Concentration

Converted into absolute area, the numbers get more concrete: total bare-earth cover across all 201 terraces went from 32.2 hectares in 1994 to 222.6 hectares in 2025, a net conversion of 190.3 hectares — 5.8% of the total mapped terrace area. But look at where that loss actually sits. Of the 190.3 hectares, 128.2 (67%) happened inside the 25 terraces already flagged as likely-degraded, and those 25 terraces account for only 9.7% of the total mapped area. This loss isn't spread evenly across the landscape. It's piled up in a small fraction of it.

![Bare-Earth Area, 1994 vs. 2025](outputs/figures/02_bare_earth_area_comparison.png)

**Figure 6.** Total bare-earth area across all mapped terraces, 1994 versus 2025.

![Loss Concentration Among Flagged Terraces](outputs/figures/03_degradation_loss_concentration.png)

**Figure 7.** Share of total net bare-earth loss occurring within the 25 terraces flagged as likely-degraded, relative to their share of total mapped terrace area.

![Degraded vs. Stable Terrace Classification](outputs/figures/05_degraded_vs_stable_terraces.png)

**Figure 8.** Classification split of all 201 delineated terraces into likely-degraded (25) and stable (176) categories.

### 4.4 Saffron Vulnerability and Proximity Risk

Fourteen of 201 terraces got flagged as likely saffron-cultivating by the Saffron Index — 225.4 hectares total, well short of the FAO's 3,200-hectare Pampore baseline. I don't read that gap as genuine crop-area loss; it's a compounding detection-recall issue across two conservative filtering stages (terrace delineation, then the saffron signature itself), and that reading is reinforced by independently reported saffron production highs over the same period.

None of the 14 saffron terraces directly overlap a degraded one, though the nearest sits just 80 m from an active degradation zone. Six of them — 43% — fall within 1 km of one. A sensitivity check across the 500 m to 2,500 m threshold range shows a smooth, monotonic climb in affected share: 21% at 500 m, rising through 29%, 43%, 71%, 86%, up to 93% at 2,500 m. That smoothness is what tells me this is a genuine spatial pattern, not an artefact of wherever I happened to put the cutoff.

![Saffron Proximity-Risk](outputs/maps/05_saffron_proximity_risk.png)

**Figure 9.** Detected saffron-cultivating terraces overlaid against proximity to the nearest degraded terrace.

![Saffron Proximity-Risk Sensitivity](outputs/figures/04_saffron_proximity_sensitivity.png)

**Figure 10.** Share of saffron-cultivating terraces classified "at risk" across a range of proximity thresholds to the nearest degraded terrace, from 500 m to 2,500 m.

At official 2024-25 yield and value figures — 5.27 kg/ha, an implied Rs 2.73 lakh/kg — the 225.4 ha this study detects as saffron-cultivating comes out to roughly Rs 32.4 crore in annual production value. The six terraces sitting inside the 1 km at-risk radius account for 123.6 ha of that, 54.8% of the detected saffron area, worth an estimated Rs 17.8 crore annually. I'll be precise about what that means, because it's easy to overstate: it's a value-at-risk figure, not a loss figure. It's how much annual production value currently sits within proximity range of active degradation — nothing here says that production has already been lost, and Figure 15 shows exactly why: no saffron terrace overlaps mapped loss yet.

### 4.5 Infrastructure Association: Degradation Follows Roads and Settlements

Roads first. Degraded terraces sat a mean 75.6 m from the nearest road, median 0.0 m — meaning more than half of them are directly adjacent to or intersecting a road already. Intact terraces sat further out: mean 133.1 m, median 38.5 m. A one-sided Mann-Whitney U test confirms the difference (p = 0.0116).

Now settlements, and the pattern gets sharper. Degraded terraces sat a mean 455.9 m from the nearest of 3,266 OpenStreetMap building footprints, median 202.0 m, against 999.7 m mean (816.6 m median) for intact terraces. p = 0.0001. Rank-biserial r = 0.465 — the strongest effect anywhere in this study (Section 4.9). Roads and settlements aren't the same infrastructure layer, they're correlated but distinct, so having both agree is a second, independent confirmation of the same accessibility-driven pattern rather than the same result twice over.

![Road Network Proximity](outputs/maps/06_road_network_proximity.png)

**Figure 11.** Degraded and intact terraces overlaid against the OpenStreetMap drivable road network, illustrating the closer road proximity of degraded terraces.

![Distance to Nearest Road by Degradation Status](outputs/figures/04_road_distance_by_status.png)

**Figure 12.** Distribution of terrace-to-nearest-road distance, compared between degraded and intact terraces (Mann-Whitney U, p = 0.0116).

![Distance to Nearest Settlement by Degradation Status](outputs/figures/06_settlement_distance_by_status.png)

**Figure 13.** Distribution of terrace-to-nearest-building distance, compared between degraded and intact terraces (Mann-Whitney U, p = 0.0001).

![Degradation vs Settlement Proximity](outputs/maps/07_settlement_proximity.png)

**Figure 14.** Terrace degradation status overlaid against 3,266 OpenStreetMap building footprints, the spatial counterpart to Figure 13's distance distribution.

![Saffron Economic Value-at-Risk](outputs/maps/08_economic_value_at_risk.png)

**Figure 15.** The six saffron terraces within the 1 km degradation-proximity radius (Rs 17.8 crore/year) against the eight beyond it, relative to the 25 degraded terraces.

### 4.6 Geomorphometric Comparison: Compactness and Slope

Obviously, the shape also plays a role and not only land cover. The mean compactness value of degraded terraces is much lower than that of intact terraces (0.138 versus 0.191, p = 0.0044), indicating that boundaries are more irregular and fragmented. This is a picture of the 'cutting out ragged incision' into the once level terrace-bounding profile rather than a picture of levelling the surface of the terrace uniformly. However, slope does tell a different story – the average internal slope angle is not significantly different between the two groups of slopes (2.89° among intact and 3.06° among degraded slopes, p = 0.1711) and so degradation does not appear to concentrate on more-steep slopes that are more likely to be subject to erosion. Certainly, the compactness is one more independent geometric signal and together with it it points on the same set of 25 terraces, which is exactly what I wanted – a shape-based check on the same thing as the spectral bare-earth one.

### 4.7 Threshold Sensitivity

Sweeping the 15-percentage-point degradation threshold doesn't shift the classification by much. Across the 12-20 point range, the flagged count stays in a stable 23-31 terraces — 25 of them at the actual 15-point threshold I used. Even at the extremes I tested, 5 points and 30 points, the count only moves to 49 and 14 respectively. That's a wide swing, but not a cliff edge sitting right at 15.

The share of saffron terraces classified as near-degradation stays between 39% and 44% across the saffron-signature threshold range of 0.05 to 0.175 — close to the reported 43% share at the actual 0.15 threshold I used. Only starts to get noisy beyond 0.175, at which point the number of terraces detected is 4-6, and any percentage based on that few is unstable by construction. Running the same check on the TPI/slope delineation grid itself — TPI in {2,3,4} and slope in {6°,8°,10°} — the (3,8) pair I actually used sits centrally within the tested range rather than at an extreme, and the resulting terrace count stays within roughly 144 to 279 candidate polygons after the elevation filter, with no sign that the central choice was a favourable outlier.

That doesn't constitute accuracy validation in the formal sense, since there is no separate (independently labelled) ground-truth set for this landscape, but it does rule out the reported numbers being a result of one fortuitous cut-off.

### 4.8 Resolution-Mismatch Robustness Check

Resample the 2025 Sentinel-2 composite to the same resolution as Landsat, 30 m, and the mean bare-earth fraction value drops from 8.43% to 7.48% — a decrease of 0.94 percentage points. Net 1994–2025 conversion falls from 190.3 ha to 165.2 ha, and the degraded-terrace count drops from 25 to 23. Resolution mismatch also boosts up the apparent acceleration of the post-2015 net-conversion by about 13% of the quantity. That is a very real and measurable impact – and not one to be waved aside.

The accel however remains. Even resolution-matched at 30 m, 2025's 7.48% is still about 2.8 times the flat 2005/2015 baseline of ~2.6%. However, although the magnitude of the degradation of this paper is in part dependent on sensor resolution, the central conclusion of the paper – recent, rapid degradation, rather than a steady process over the multi-decadal time frame – does not seem to be an artefact of the sensor switchover.

### 4.9 Effect Sizes and Multiple-Comparison Correction

Although I reported some P-values, I have computed rank-biserial correlation, a nonparametric measure of effect-size that naturally pairs with the Mann-Whitney U test, for all four comparisons for which I have data and reported P values – settlement proximity (r = 0.465), compactness (r = 0.352), road proximity (r = 0.268), slope (r = −0.170). Proximity to settlement is the most significant effect by standard measures, moderate to large. The size and compactness of roads are rated as small-to-moderate. Slope is negligible.

I applied a Holm-Bonferroni correction (family-wise α = 0.05) to four Mann-Whitney tests, so as to not illicitly inflate the number of false-positive results across the family. Settlement proximity (p = 0.0001, adjusted threshold 0.0125), compactness (p = 0.0044, adjusted threshold 0.0167), and road proximity (p = 0.0116, adjusted threshold 0.025) all survive it. The slope is already not significant before the correction (p = 0.1711).

## 5. Discussion

The central point here: this isn't slow, uniform degradation. It's recent, concentrated in space, and accelerating — matching directly to the pattern described in the grey, non-peer-reviewed literature reviewed in Section 2, which documents a contemporary, last-decade increase in mining pressure rather than a historic trend. What I've added is a number that corresponds to what that reporting already describes qualitatively. The road result (p = 0.0116) and the settlement result (p = 0.0001, r = 0.465) both confirm that degraded terraces sit closer to both infrastructure types — consistent with the material's roadability, that is, how cheaply it moves to market where roads and labour are already present (Engert et al., 2025). But I want to be careful about over-reading the settlement result specifically. Yes, it's consistent with an accessibility-driven extraction model, but it's also consistent with something more fundamental: a general gradient of human activity with settlement distance that could show up just as easily through a transport-economics road-access mechanism. Both associations are correlational, and I don't have a dated road/settlement record that lets me establish which came first. That causal sequence is something for future work.

The compactness result in Section 4.6 is relevant in its own right, and is independent of the NDVI threshold for defining bare earth fraction; and it identified the same 25 terraces. That's a second, independent look and validation that the degradation classification is identifying something real, not some artifact of the spectral index.

I believe the result for the saffron-proximity finding is really useful—it's an early-warning rather than a lagging result in my opinion—because of the lack of any direct-loss statistic it supports from the data. This finding is not affected by the drop-off from the FAO baseline set out in Section 6. The 14 terraces I detected are the ones that my phenological signature was able to align to with the highest confidence, and also based on a sensitivity analysis conducted in Section 4.7, the proximity-risk share doesn't change very much for a wide spectrum of detection thresholds so it's not dependent on the precise 0.15 threshold. A higher recall detection method would likely likely also detect smaller, less spectrally distinct parcels of saffron – and, after all, smaller parcels are likely to be closer to the margins of the already mined land. This was done deliberately as I kept using hectares instead of rupees which are the units that would resonate with a geospatial audience, but is what moves a district agriculture office or a legislative budget line; I wanted this study to be resonating to both. Empirically verified, it seems like I think, that this degradation/proximity-risk map is near the surface of the empirical reality of such a realised assessment of policy alignment that the Rs 400 crore PM Saffron Mission and its target of 2,598-hectares rejuvenation is part of this substantiated evaluation. I've said before, I can't make that comparison right now because they don't have scheme-level spatial data that's publicly available, but if they did exist the outputs would be poised to support that comparison.

Then there is the legal crumb, which isn't even misaligned targeting (the RQ4 question above). Here we have no minimum standards whatsoever in the legal sense. Currently, there is no legislation to safeguard karewa land in Jammu & Kashmir against excavation. A private member's bill, sponsored by Dr. Syed Bashir Veeri, who represents Bijbehara, will ban any excavation or extraction of clay, sand and gravel in ecologically sensitive karewa areas, while authorising the extraction in already degraded areas where the need for the extraction cannot be ignored and only upon receipt of the necessary guidelines from the J&K State Environmental Impact Assessment Authority. In the case of violation the bill will prescribe a monetary fine ranging from Rs 2,500 to Rs 10 lakh and availability of imprisonment for five years. Currently (as best I can download from such resources as the newspaper), it remains pending but the department of Revenue, as well the departments of geology & mining, continue to grant “excavation” permits for the same purpose as the bill would prohibit. This changes how to read the road and settlement proximity results. They aren't evidence that enforcement is failing — there's no rule yet to fail against. What they show instead is extraction happening in a genuinely unregulated space. As that is the policy shift from "enforce what's already there more consistently" to "put a protection regime in place at all," this study will deliver the shape of evidence that that policy shift requires - a terrace-level risk map.

## 6. Limitations

- The detected zone of saffron cultivation (225.4 ha) is very weak with respect to the baseline of FAO GIAHS (3,200 ha). Because I find the reduction not to be due to an actual loss of cropland; I think it's prudent to report these as methodological limitations, rather than deroging their reality based on my expectation as to what should occur. In this case, it is the combination of two conservative filtering processes — terrace delineation, then the subsequent saffron-signature thresholding.
- RQ4 (about governance-alignment) was not amenable to statistical testing. I searched for spatially resolved PM Saffron Mission allocation data, but could only locate data at the valley level — which did not match the level of detail in this study's map of the terrace. It is put in the too-hard basket, that is in future action, preferably undertaken in collaboration with the implementing agency of the scheme.
- The multi-temporal analysis cannot be applied prior to 1994 as there is a gap in the landsat record before that year before it will operate in an usable time frame of seasonal coverage.
- The 2025 point uses 10 m Sentinel-2 while 1994–2015 use 30 m Landsat. What Section 4.8 quantifies, then, is that exact rate of real inflation, which here is about 13% of the rate of net conversion (190.3 - 165.2 ha is the result of resampling the same area, and even that is only modest because real inflation must be at least that rate from the actual rate of bare-earth fraction conversion, even if it seems negligible).
- 2005 used a wider net, than intended. Since the same query targeted to June-Sept 2005 using Landsat 5 returned 0 images, I expanded my window to include the previous and next two years on the same query, from 2001-2009, marked mid window with 2005 (as I detailed in SS_Development_Log.md). That's a multi-year composite; it may ameliorate short-term periods of degradation in that timeframe, but does not bias the 1994 or 2015 end points that drive the form of the trend.
- As there is no detailed dataset available at terrace level (or at Pampore-belt) and their saffron yield and price, one statewide yield and price (5.27kg/ha & Rs 2.73 lakh/kg) is used for each identified saffron terrace. The actual output per terrace is likely to be related to soil quality, rejuvenation status and micro-climate, and premium production prices of premium (GI-tagged) from Pampore are likely to exceed the statewide total applied here. This is not a precise appraisal but rather an "order of magnitude" VA estimate.
- Legal protection finding is the result of legislative reporting at the time of the study's research. A private member's bill is in flux when not continually covered, so it is advisable, after the events of this investigation, to recheck the status each time before assuming that "no current statute" is so.
- Because there is no ground truth data for reference use for this landscape, there is no existing formal accuracy evaluation of this data set using independently labeled ground truth points yet, nor is there a confusion matrix with producers' and user's accuracy. Instead I have validated the thresholds behind each classification here by doing the sensitivity sweep in Section 4.7 and checking their results visually. I have already developed a ground-truth class of 150 samples to this end, but these have not yet been labelled manually.
- The 201 terrace polygons themselves come from the current Copernicus DEM, and that same fixed set of 201 is what the 1994-2025 NDVI history is then measured against. A terrace that had already been substantially excavated or erased before this DEM was captured simply wouldn't register as a terrace-shaped landform today, so it would never enter this 201-polygon set to begin with. That means the 190.3 ha figure is the bare-earth conversion measured within the terraces that a present-day, DEM-based algorithm can still recognize as terraces now — not a full historical accounting of every karewa surface that has ever existed across this belt.
- As a small, separate check alongside that still-unlabelled 150-point sample, I visited the Lethpora saffron belt in person on 3 September 2026 and took four GPS-tagged photographs across the same terraces used in the Section 4.1 validation, clustered around 33.97°N, 74.95°E. Saffron flowers only in a short October–November window, so what these photos show is dormant, freshly-tilled soil rather than visible crop — that's what an active, pre-flowering saffron plot is supposed to look like at this time of year, not evidence that nothing is planted there. I want to be precise about what this does and doesn't prove: this bare, tilled appearance is not the same signal as the persistent, multi-year bare-earth increase the degradation classifier looks for, so one seasonal photo like this can't confirm or rule out degradation on its own. It's a small, honest field anchor, not a validation exercise. I'm planning a return visit in October 2026, during peak bloom, to get a proper before/after pair at the same coordinates.
- The areas with low level (0-40%) of vegetation that were pinpointed in this study have not yet been looked at for crop stress or impacts from drought as reported at the ground level by the districts.
- If referred to elsewhere in this project, the rainfall anomaly at the District level is derived from one region-wide climatological baseline instead of one per District.

## 7. Conclusion

Kashmir's karewa terraces are lost, it has been lost to the extent that it can be measured, and it has been lost at a fairly rapid pace – in fact, by the measure placed on the decade since 2015, almost all of it. It's not distributed randomly but rather follows the roadway as well as local human habitation. I don't think the saffron economy on these terraces is incapable of producing saffron now, at least not directly; what it has is perhaps Rs 17.8 crore in production value on these terraces, and that's the point that I think is near enough to be considered if ever production value is to be taken at all. The lack of any legal check on the excavation of karewas is a big reason why all of this is happening: Absent any legislation to govern today, the one bill that would regulates karewa excavation in Jammu & Kashmir is stuck. There are two implications from that, and I believe policy implications of both. Firstly, any funds that are assigned to rejuvenating the saffron sector would need to be matched with the money that is being spent where it is actually most at risk of degradation—don't assume that this is the same location. Second, the case for a provision for the protection of the karewa has now come equipped with scientific evidence – tangible, rapid, economic loss without any compulsion of law.

## References

De Terra, H., & Paterson, T. T. (1939). *Studies on the Ice Age in India and Associated Human Cultures.* Carnegie Institution of Washington. [Full text](https://archive.org/details/dli.pahar.2748)

Dar, R. A., & Zeeden, C. (2020). Loess-Palaeosol Sequences in the Kashmir Valley, NW Himalayas: A Review. *Frontiers in Earth Science*, 8, 113. [https://doi.org/10.3389/feart.2020.00113](https://doi.org/10.3389/feart.2020.00113)

Bhat, G. R., Bali, B. S., Balaji, S., Iqbal, V., & Balakrishna. (2016). Earthquake triggered soft sediment deformational structures (seismites) in the Karewa formations of Kashmir valley—An indicator for palaeo-seismicity. *Journal of the Geological Society of India*, 87(4), 439–452. [https://doi.org/10.1007/s12594-016-0412-y](https://doi.org/10.1007/s12594-016-0412-y)

Weiss, A. D. (2001). Topographic Position and Landforms Analysis. Poster presented at the ESRI International User Conference, San Diego, CA. [Poster PDF](https://www.jennessent.com/downloads/TPI-poster-TNC_18x22.pdf)

Boeing, G. (2017). OSMnx: New Methods for Acquiring, Constructing, Analyzing, and Visualizing Complex Street Networks. *Computers, Environment and Urban Systems*, 65, 126–139. [https://doi.org/10.1016/j.compenvurbsys.2017.05.004](https://doi.org/10.1016/j.compenvurbsys.2017.05.004)

Madasa, A., Orimoloye, I. R., & Ololade, O. O. (2021). Application of geospatial indices for mapping land cover/use change detection in a mining area. *Journal of African Earth Sciences*, 175, 104108. [https://doi.org/10.1016/j.jafrearsci.2021.104108](https://doi.org/10.1016/j.jafrearsci.2021.104108)

Mann, H. B., & Whitney, D. R. (1947). On a Test of Whether one of Two Random Variables is Stochastically Larger than the Other. *Annals of Mathematical Statistics*, 18(1), 50–60. [https://doi.org/10.1214/aoms/1177730491](https://doi.org/10.1214/aoms/1177730491)

Engert, J. E., Souza, C. M., Kleinschroth, F., Ishida, F. Y., Costa, S. P., Botelho, J., & Laurance, W. F. (2025). Road expansion risk predicts future hotspots of tropical deforestation. *Proceedings of the National Academy of Sciences*, 122(52). [https://doi.org/10.1073/pnas.2502426122](https://doi.org/10.1073/pnas.2502426122)

Rafi, A. B., & Syed, S. (2023, January 27). Nourishing soils of Kashmir's karewas crumble under infrastructure. *Mongabay India*. [Read](https://india.mongabay.com/2023/01/nourishing-soils-of-kashmirs-karewas-crumble-under-infrastructure/)

Deccan Herald. (2022, March 13). Saffron boom in Kashmir: Highest production in 25 years. [Read](https://www.deccanherald.com/india/saffron-boom-in-kashmir-highest-production-in-25-years-1090848.html)

FAO GIAHS. (2012). *Saffron Heritage Site of Kashmir in India* (Part 1). Globally Important Agricultural Heritage Systems Pilot Project, SKUAST-K. [Read](https://www.fao.org/3/bp791e/bp791e.pdf)

Press Post. (2026). Rs 400 cr PM Saffron Mission halts slide in Kashmir, 2,598 ha brought under rejuvenation. [Read](https://india.presspost.in/rs-400-cr-pm-saffron-mission-halts-slide-in-kashmir-2598-ha-brought-under-rejuvenation)

Greater Kashmir. (2026, February 18). J&K Saffron output drops to 19.58 MT in 2024-25: Govt. [Read](https://www.greaterkashmir.com/business/jk-saffron-output-drops-to-19-58-mt-in-2024-25-govt)

Kashmir Life. (2026, February 12). Kashmir's Saffron Sold for Rs 534.53 Cr in 2024-25, Govt Tells Assembly. [Read](https://kashmirlife.net/kashmirs-saffron-sold-for-rs-534-53-cr-in-2024-25-govt-tells-assembly-424949/)

Kashmir Reader. (2026, February 13). Over 90 metric tonnes of saffron produced in last five years in J&K: Govt. [Read](https://kashmirreader.com/2026/02/13/over-90-metric-tonnes-of-saffron-produced-in-last-five-years-in-jk-govt/)

Kashmir Observer. (2025, February 22). Will the Karewa Protection Bill Become a Law in J&K? [Read](https://kashmirobserver.net/2025/02/22/will-the-karewa-protection-bill-become-a-law-in-jk/)

Greater Kashmir. (2025, February 28). Why do Karewas need legal Protection in J&K? [Read](https://www.greaterkashmir.com/opinion/why-do-karewas-need-legal-protection-in-jk/)
