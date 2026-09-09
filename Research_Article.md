# Stolen Strata: Quantifying the Anthropogenic Erasure of Kashmir's Karewa Terraces and Its Threat to the Saffron Economy

## Abstract

Karewa terraces are elevated, flat-topped deposits of intermontane lake-basin age (Pleistocene/Pliocene), and they underlie one of Kashmir's most economically significant agricultural systems: the saffron-growing belt at Pampore. People who follow agriculture in Kashmir already know these terraces are disappearing under unregulated soil mining and unchecked urban growth, and plenty has been written about it. But nobody had put a number on how much. That's what I set out to do here, using 3 decades of satellite data. From TPI and slope-threshold terrain analysis, I identify 201 karewa terraces (3,305.3 ha) across the central Kashmir Valley, and estimate the bare-ground fraction of each using seasonally-aligned Landsat and Sentinel-2 composites at 4 dates: 1994, 2005, 2015, and 2025. Over that period, mean bare-earth fraction (BEF) rose from 1.84% to 8.43%, and nearly all of that rise happened in the past 10 years. 190.3 hectares of terrace surface have converted to bare earth, and that loss runs hot in patches. 67% of it sits within just 12.4% of the terraces. A saffron-signature index, built on the crop's inverted phenology, flags 14 potential saffron-cultivating terraces; 43% of them sit within 1 km of an already-degraded terrace. None overlap directly; they're near degraded ground, not on it, at least as far as the data show. At official 2024-25 yield and price figures, that at-risk segment represents roughly Rs 17.8 crore in annual production value, about 55% of the total annual production value this study traces to the area. The pattern holds even more strongly for settlements than for roads: degraded terraces sit significantly closer to roads than intact terraces (U = 1611.0, p = 0.0116), and even closer to settlements (U = 1176.0, p = 0.0001, the strongest effect in this study). So this looks like an accessibility-driven mining pattern, not a random one. Then there's the legal question most satellite studies like this skip: is there anything to stop this excavation? No. As of the most recent legislative reporting available, no identified law specifically protects karewa land from excavation in Jammu & Kashmir; a private member's bill titled the 'Karewa Protection Authority' has been pending for a long time. I ran threshold-sensitivity sweeps, a resolution-matching robustness test against the Landsat/Sentinel-2 pixel-size mismatch, and effect-size and multiple-comparison corrections across all 4 statistical tests. None of it changes the basic picture, though a modest degree of resolution-dependence shows up in the size of the post-2015 acceleration. Combine the geomorphology, the economics, and the legal void, and this stops being a change-detection exercise. It becomes a landform loss with a price tag attached, and it hands policymakers a lever they can pull.

**Keywords:** karewa terraces; land degradation; remote sensing; saffron economy; Kashmir; geospatial analysis

---

## 1. Introduction

Karewa terraces are flat-topped, loess-capped, and geologically unique, and in the Kashmir Valley, it is this loess-cap that makes the soils perfectly suited to Geographical Indication (GI) registered saffron variety, Crocus sativus, which supports the lives of thousands of farming families in the Pampore belt. But these terraces have been reported in investigative and grey literature for the last decade or so, with little regulation, and are being mined as construction quality soil for the brick, housing and infrastructure sectors for years without rhyme or reason.

That is what the reporting says, but it stays a story without numbers behind it. Nobody had gone and measured how much land, over how many years, using data that doesn't just rely on someone's word for it. That's the gap this study tries to close. This study is a fully scripted geospatial pipeline. It defines the boundary of karewa terraces from terrain information, and examines land-cover condition across a 31-year satellite record, in addition to tracking the scale of the saffron economy that the terraces need to sustain (valued here in rupees, not just hectares of land), and the road and settlement infrastructure that makes this extraction economic in the first place — which today, believe it or not, is very little.

## 2. Literature Review

### 2.1 The Geomorphological Evolution of the Karewa Landscape

The well-established stratigraphy of De Terra and Paterson (1939) marks the beginning of systematic Quaternary geology of this region, with a lacustrine-to-fluvial infill sequence linked to the uplift of the Pir Panjal Range. The picture has since been refined: Dar and Zeeden (2020) review the loess/palaeosol sequences overlying the karewa surface and their potential as an archive of Quaternary palaeoclimate, and soft-sediment deformation structures in the karewa formations have been reported by Bhat et al. (2016) and read as evidence of palaeoseismicity. Together, this body of work convinced me that the karewa surface isn't just another type of upland being mined away — it's a geologically unique, scientifically instructive record, and its loss is a loss of agricultural land and geological archive at once.

### 2.2 A Landform Under Economic Pressure

There's a lot of mass sentiment and some news reporting fueling the perception that the land in Karewa is being lost faster than it's being saved, and the perception matches the facts. As reported by Rafi and Syed (2023) in Mongabay India, karewa conversion, brick-kiln expansion in Budgam, and ongoing projects such as the Semi Ring Road further underscore the pressure: 90% of the construction material for the Qazigund-Baramulla project was sourced from karewa excavation, backed by direct quotes from local farmers linking the project to the loss of their ability to grow saffron. According to the documentation done by the Food and Agriculture Organization's Globally Important Agricultural Heritage Systems programme (FAO GIAHS, 2012), above 3,200 ha of land is under saffron cultivation at Pampore, supporting more than 17,000 farming families. Kashmir's saffron cultivation, on the other hand, has been reported to be producing at its highest level in the past few seasons with 25-year production records (Deccan Herald, 2022), and more recent government figures put cumulative five-year production above 90 metric tonnes (Kashmir Reader, 2026). I kept that last number in mind throughout this study, as it can help remind you that degradation and short-term output gains do not necessarily contradict each other when reading either one or the other would be wrong.

The use of remote sensing approaches for detecting land degradation has grown substantially.

My terrain-based landform classification is based on the TPI of Weiss (2001), which classifies terrain by comparing the elevation of each cell to its local neighbourhood elevation mean, and not to a reference elevation; this approach is commonly used to identify aspects of the terrain, such as ridges, valleys and here, flat raised terrace surfaces. Directly concerned with the change in land cover is Madasa, Orimoloye, and Ololade (2021), who find that geospatial vegetation indices are able to distinguish mining-disturbed ground from vegetated cover using a multi-temporal satellite record. That's substantial in my mind as to why I believed in a bare-earth-fraction approach for the methodology of this study.

There exists a large and expanding body of literature that relates the economic aspects of unregulated resource extraction to road infrastructure. The latest and most helpful for my purposes is Engert et al. (2025), who find that road expansion is a primary driver of future deforestation "hotspots" in the tropics, a universal rule being that extractive land-use pressure focuses where it's easiest to extract material at minimal expense. I take karewa mining as a case here, because there's a clear logic to test it against. The PM Saffron Mission has recently been valued at Rs 400 crore, with a goal of rejuvenating 2,598 hectares (Press Post, 2026). That's the message for me: there's already policy investment going into this. It doesn't tell me whether that funding targets the land where degradation risk is most concentrated — that's the question Section 3.8 comes back to.

## 3. Data and Methodology

### 3.1 Study Design

This study focuses on Pampore, Pulwama and Budgam districts and karewa exposures in the central Kashmir Valley (Zewan section) near Srinagar. This area was chosen for 2 reasons: 1st, it holds the highest concentration of saffron-bearing karewas within the valley, and 2nd, the secondary literature repeatedly flags this area as a hotspot for unregulated soil mining. No boundary or layer in this section was hand-drawn: terrace boundaries come from an algorithm, and every analytical layer derived from them — degradation status, saffron signature, road proximity, and so on — is based on that same algorithmically-defined boundary.

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

The rule I used to extract karewa terrace boundaries from the DEM is: Topographic Position Index greater than 3, and slope less than a threshold angle of 8°. This separates locally raised, flat-topped surfaces from their surroundings — the topographic signature that defines a karewa tread's scarp boundary. I vectorized the candidate pixels, then narrowed the search to polygons of at least 0.05 km² within the 1550-2000 m elevation band where karewa exposures are thought to occur. This left 201 terrace polygons accounting for 3,305.3 ha.

### 3.4 Multi-Temporal Degradation Detection

To measure land-cover condition within each terrace, I used a metric I call bare-earth fraction: the percentage of pixels within a given polygon that fell below an NDVI threshold I took to represent bare ground. It was calculated from each seasonally-aligned composite in the years 1994 (June-September, based on Landsat 5 data), 2005 (May-October, based on Landsat 5 data), 2015 (May-October, based on Landsat 8 data), and 2025 (June-September, based on Sentinel-2 data). Terraces that degraded by 15% or more of bare earth between 1994 and 2025 were likely degraded, and received this label. This classifier flags any pixel that falls below the NDVI threshold, whatever the cause; on its own it cannot tell mining apart from construction, tillage, or natural erosion. The mining/anthropogenic reading in this study comes from combining that bare-earth trend with the infrastructure-proximity results in Section 4.5 and the mining activity already documented in the grey literature covered in Section 2, not from the classifier by itself.

### 3.5 Saffron Signature Identification and Economic Valuation

Saffron is dormant and bare in summer, and reaches peak leaf canopy in March following its autumn flowering — exactly the phenological contrast my Saffron Index looks for. For each terrace, I calculated the difference between NDVI in the canopy window and NDVI in the summer dormant window, and marked any portion clearing a 0.15 difference as likely-saffron. From there, I looked at the distance from each flagged saffron polygon to the closest degraded terrace (between 500 m and 2500 m).

A line in a budget cannot be shifted by a hectare count. A rupee figure is likely to. The official reply from MLA Hasnain Masoodi to the state Legislative Assembly's Agriculture Production Department (February 2026) puts J&K's statewide saffron acreage at 3,715 ha, statewide production at 19.58 MT, and the statewide sale value at Rs 534.53 crore for 2024-25 (Kashmir Life, 2026; Greater Kashmir, 2026). That Rs 534.53 crore figure is the state's own total, not this study's number, since it covers all saffron cultivation across J&K, most of which sits outside the 201 terraces mapped here. What this study actually draws from those same official figures is a rate, not a total: a yield of 5.27 kg/ha and a price of almost Rs. 2.73 lakh/kg. I applied that rate to the saffron area this study itself detects (Section 4.4), and separately to the at-risk subset of it. So the rupee figure this study reports, Rs 32.4 crore, is a number for the 225.4 ha this detection pipeline finds, not the state's total production value, and not a number for what any one terrace grows. I have no way to measure that last part directly.

### 3.6 Infrastructure Proximity Testing

Within the study area, I extracted the drivable road network using the OpenStreetMap package 'osmnx' (Boeing, 2017), 44,622 segments in total, pulling in the full road network instead of reducing it to centroid points. I computed the minimum distance from each terrace polygon to the nearest road line; where a road crosses into or touches the polygon boundary, that counts as a valid 0 m distance. I also ran the same polygon-distance procedure on OpenStreetMap building footprints (3,266 features), which provides a second and independent accessibility indicator besides the road network. Roads relate to this, but not in a one-to-one way: a terrace next to a village access track might sit well outside what OpenStreetMap classifies as the drivable road network, and vice versa. To compare distances between degraded and intact terraces for each infrastructure layer, I opted for a one-sided Mann-Whitney U test (Mann & Whitney, 1947), since this statistic isn't sensitive to normality or to zero-inflation in the terrace-to-infrastructure distances.

### 3.7 Geomorphometric Comparison

Do degraded terraces differ in shape, not just in land cover? To check, I calculated two geomorphic variables per terrace: a compactness index (4π·Area/Perimeter², with 1.0 being a perfect circle and values close to 0 being very elongated, dissected shapes), and the mean terrace internal slope angle, taken directly from the terrace-delineation DEM. Degraded and intact terraces were compared on both using a Mann-Whitney U test.

### 3.8 Governance Context

I wanted to explore a 4th issue: does current agricultural policy favor investment in land that is technically good and fit for agriculture but disturbed by degradation, over intact karewa? I couldn't answer that, at least not in a form that's both spatially resolved and publicly accessible — country-level programs like the PM Saffron Mission don't have that kind of land-lease and enforcement data available. So instead I address it narratively in the Discussion, presenting this study's degradation pattern as the evidentiary basis for a future policy-alignment overlay. A related but more answerable question was: are there any legal safeguards whatsoever on karewa land, irrespective of which scheme funds it? That one I could pursue, through J&K legislative reporting, because protection status is a regulatory binary fact, not something I need to overlay on a map.

### 3.9 Threshold Sensitivity and Robustness Checks

The three numbers this whole study rests on — the TPI/slope pair used to delineate terraces, the 15-percentage-point bare-earth degradation threshold, and the 0.15 saffron-signature threshold — were determined by visual inspection of known morphology and location on maps. I didn't have a preset validated landscape on which to calibrate, so I wanted to see how important that was. I traversed different possible values of thresholds over a neighbourhood and recalculated the number of terraces, their areas and the risk percentage for each.

2 more checks. 1st, I wanted to reconcile the 10 m resolution Sentinel-2 data (2025) with the 30 m resolution Landsat data (1994-2015), so I resampled the 2025 Sentinel-2 data to 30 m and reran the same bare-earth-fraction pipeline at that resolution, to see how much of the apparent post-2015 acceleration is explained by the resolution difference rather than genuine change. Ignoring it would be the worst thing to do here. 2nd, I calculated 4 rank-biserial effect sizes and applied a Holm-Bonferroni correction across the 4 Mann-Whitney tests this study reports, since without correction, four significance tests would inflate the family-wise false-positive rate.

## 4. Results

Each static map below (Figures 1, 2, 3, 4, 9, 11, 14 and 15) is accompanied by an interactive counterpart that is pannable and zoomable and can be accessed from the Interactive Maps page of the dashboard, or directly from the information in the README.

### 4.1 Terrace Delineation and Plausibility Check

The delineation pipeline produced a total of 201 candidate polygons covering the Pampore-Pulwama-Budgam-Srinagar karewa belt. Overlaid on the satellite basemap, they trace visible upland landforms sitting above the forested valley floor, as expected, and they also line up with the "Saffron Fields, Lethpora" location labeled on the map. The TPI/slope thresholds themselves were set from the shape of the candidate polygons, not from this location (Section 3.3): an earlier, stricter threshold pair produced thin, sliver-shaped candidates, and the looser pair used here produced compact, blob-shaped ones instead. The Lethpora line-up came afterward, as a plausibility check on the resulting boundaries against a named cultivation site, not as an independent validation and not as the basis on which the thresholds were chosen.

**Figure 1.** Study area overview showing the Kashmir Valley karewa belt, the analytical bounding box, and key settlement reference points. *Map disclaimer: the designations employed and the presentation of the material on this and all subsequent map figures in this article do not imply the expression of any opinion concerning the legal status of any country, territory, city, or area, or of its authorities, or concerning the delimitation of its frontiers or boundaries.*

**Figure 2.** The 201 karewa terrace polygons delineated algorithmically from Topographic Position Index and slope-threshold terrain analysis.

**Figure 3.** Close-range plausibility check of the delineation pipeline against the labelled Saffron Fields, Lethpora location, showing mapped terrace boundaries lining up with a known cultivation site.

### 4.2 Multi-Temporal Degradation: A Recent, Accelerating Trend

1.84% in 1994. 2.62% in 2005 (a 2001-2009 composite centred on that year, not a single-year image, per Section 6). 2.63% in 2015. Essentially flat for 2 decades. Then 8.43% by 2025, more than triple. That's the mean bare-earth fraction across all 201 terraces, and the shape of that curve is the whole point of this section: 2 flat decades, then a sharp jump. 25 of the 201 terraces (12.4%) crossed the threshold for likely degradation over the full study period.

**Figure 4.** Terrace-level degradation status, 1994–2025, showing the spatial distribution of likely-degraded terraces (25 of 201) relative to stable terraces.

**Figure 5.** Mean bare-earth fraction across all 201 terraces at 4 time points, showing 2 decades of relative stability followed by a sharp post-2015 acceleration.

### 4.3 Absolute Area Lost and Its Concentration

Converted into absolute area, the numbers get more concrete: total bare-earth cover across all 201 terraces went from 32.2 hectares in 1994 to 222.6 hectares in 2025, a net conversion of 190.3 hectares, 5.8% of the total mapped terrace area. But look at where that loss sits. Of the 190.3 hectares, 128.2 (67%) happened inside the 25 terraces already flagged as likely-degraded, and those 25 terraces account for only 9.7% of the total mapped area, a small corner of the study area carrying most of the loss.

**Figure 6.** Total bare-earth area across all mapped terraces, 1994 versus 2025.

**Figure 7.** Share of total net bare-earth loss occurring within the 25 terraces flagged as likely-degraded, relative to their share of total mapped terrace area.

**Figure 8.** Classification split of all 201 delineated terraces into likely-degraded (25) and stable (176) categories.

### 4.4 Saffron Vulnerability and Proximity Risk

14 of 201 terraces got flagged as likely saffron-cultivating by the Saffron Index, 225.4 hectares total, well short of the FAO's 3,200-hectare Pampore baseline. I don't read that gap as true crop-area loss; it's a compounding detection-recall issue across 2 conservative filtering stages (terrace delineation, then the saffron signature itself), and that reading is reinforced by independently reported saffron production highs over the same period.

None of the 14 saffron terraces directly overlap a degraded one, though the nearest sits just 80 m from an active degradation zone. 6 of them (43%) fall within 1 km of one. A sensitivity check across the 500 m to 2,500 m threshold range shows a smooth, monotonic climb in affected share: 21% at 500 m, rising through 29%, 43%, 71%, 86%, up to 93% at 2,500 m. If this were just an accident of where I drew the cutoff, I'd expect a jump at one particular distance. Instead, the climb is steady all the way across, which tells me this pattern isn't just a coincidence.

**Figure 9.** Detected saffron-cultivating terraces overlaid against proximity to the nearest degraded terrace.

**Figure 10.** Share of saffron-cultivating terraces classified "at risk" across a range of proximity thresholds to the nearest degraded terrace, from 500 m to 2,500 m.

At official 2024-25 yield and value figures (5.27 kg/ha, an implied Rs 2.73 lakh/kg), the 225.4 ha this study detects as saffron-cultivating comes out to roughly Rs 32.4 crore in annual production value. The 6 terraces sitting inside the 1 km at-risk radius account for 123.6 ha of that, 54.8% of the detected saffron area, worth an estimated Rs 17.8 crore annually. This number is easy to misread, so here's what it says: it's how much production value sits close to active degradation right now, not how much has already been lost. Figure 15 shows why: no saffron terrace overlaps mapped loss yet.

### 4.5 Infrastructure Association: Degradation Sits Closer to Roads and Settlements

Roads first. Degraded terraces sat a mean 75.6 m from the nearest road, median 0.0 m, meaning more than half of them are directly adjacent to or intersecting a road already. Intact terraces sat further out: mean 133.1 m, median 38.5 m. A one-sided Mann-Whitney U test confirms the difference (p = 0.0116).

Now settlements, and the pattern gets sharper. Degraded terraces sat a mean 455.9 m from the nearest of 3,266 OpenStreetMap building footprints, median 202.0 m, against 999.7 m mean (816.6 m median) for intact terraces. p = 0.0001. Rank-biserial r = 0.465, the strongest effect anywhere in this study (Section 4.9). Roads and settlements aren't the same infrastructure layer, they're correlated but distinct, so having both agree is convergent evidence from two distinct infrastructure layers for the same accessibility-driven pattern, not just the same result twice over.

**Figure 11.** Degraded and intact terraces overlaid against the OpenStreetMap drivable road network, illustrating the closer road proximity of degraded terraces.

**Figure 12.** Distribution of terrace-to-nearest-road distance, compared between degraded and intact terraces (Mann-Whitney U, p = 0.0116).

**Figure 13.** Distribution of terrace-to-nearest-building distance, compared between degraded and intact terraces (Mann-Whitney U, p = 0.0001).

**Figure 14.** Terrace degradation status overlaid against 3,266 OpenStreetMap building footprints, the spatial counterpart to Figure 13's distance distribution.

**Figure 15.** The 6 saffron terraces within the 1 km degradation-proximity radius (Rs 17.8 crore/year) against the 8 beyond it, relative to the 25 degraded terraces.

### 4.6 Geomorphometric Comparison: Compactness and Slope

Obviously, shape plays a role too, not just land cover. The mean compactness value of degraded terraces is much lower than that of intact terraces (0.138 versus 0.191, p = 0.0044), indicating that boundaries are more irregular and fragmented, closer to ragged incisions being cut into the terrace edge than to the whole surface being planed down evenly. However, slope does tell a different story: the average internal slope angle is not significantly different between the 2 groups of slopes (2.89° among intact and 3.06° among degraded slopes, p = 0.1711) and so degradation does not appear to concentrate on more-steep slopes that are more likely to be subject to erosion. The compactness result is one more independent geometric signal, and it points to the same set of 25 terraces — exactly the shape-based check I wanted alongside the spectral bare-earth one.

### 4.7 Threshold Sensitivity

Sweeping the 15-percentage-point degradation threshold doesn't shift the classification by much. Across the 12-20 point range, the flagged count stays in a stable 23-31 terraces, with 25 of them at the 15-point threshold I used. Even at the extremes I tested, 5 points and 30 points, the count only moves to 49 and 14 respectively. That's a wide swing, but not a cliff edge sitting right at 15.

The share of saffron terraces classified as near-degradation stays between 39% and 44% across the saffron-signature threshold range of 0.05 to 0.175, close to the reported 43% share at the 0.15 threshold I used. Only starts to get noisy beyond 0.175, at which point the number of terraces detected is 4-6, and any percentage based on that few is unstable by construction. Running the same check on the TPI/slope delineation grid itself, with TPI in {2,3,4} and slope in {6°,8°,10°}, the (3,8) pair I used sits centrally within the tested range, well away from either extreme, and the resulting terrace count stays within roughly 144 to 279 candidate polygons after the elevation filter, with no sign that the central choice was a favourable outlier.

That doesn't constitute accuracy validation in the formal sense, since there is no separate (independently labelled) ground-truth set for this landscape, but it does rule out the reported numbers being a result of one fortuitous cut-off.

### 4.8 Resolution-Mismatch Robustness Check

Resample the 2025 Sentinel-2 composite to the same resolution as Landsat, 30 m, and the mean bare-earth fraction value drops from 8.43% to 7.48%, a decrease of 0.94 percentage points. Net 1994–2025 conversion falls from 190.3 ha to 165.2 ha, and the degraded-terrace count drops from 25 to 23. Resolution mismatch also inflates the apparent acceleration of the post-2015 net conversion by about 13% of the quantity. That is a solid, measurable impact, not one to be waved aside.

The acceleration, however, remains. Even resolution-matched at 30 m, 2025's 7.48% is still about 2.8 times the flat 2005/2015 baseline of ~2.6%. However, although the size of the degradation number in this paper does depend somewhat on sensor resolution, the central conclusion (that this is recent, rapid degradation and not something that built up steadily across the whole multi-decadal period) holds up regardless; the sensor switch isn't what's producing that pattern.

### 4.9 Effect Sizes and Multiple-Comparison Correction

Although I reported p-values, I also computed rank-biserial correlation, a nonparametric measure of effect size that naturally pairs with the Mann-Whitney U test, for all 4 comparisons: settlement proximity (r = 0.465), compactness (r = 0.352), road proximity (r = 0.268), slope (r = −0.170). Proximity to settlement is the most significant effect by standard measures, moderate to large. The size and compactness of roads are rated as small-to-moderate. Slope is negligible.

I applied a Holm-Bonferroni correction (family-wise α = 0.05) to 4 Mann-Whitney tests, so as to not illicitly inflate the number of false-positive results across the family. Settlement proximity (p = 0.0001, adjusted threshold 0.0125), compactness (p = 0.0044, adjusted threshold 0.0167), and road proximity (p = 0.0116, adjusted threshold 0.025) all survive it. The slope is already not significant before the correction (p = 0.1711).

## 5. Discussion

The central point here is timing and shape: this is recent, it's concentrated in space, and it keeps speeding up. That's a very different signature from slow degradation spread evenly over decades, matching directly to the pattern described in the grey, non-peer-reviewed literature reviewed in Section 2, which documents a contemporary, last-decade increase in mining pressure, not an old-standing trend. That reporting already said this was happening. This study just puts a figure next to it. The road result (p = 0.0116) and the settlement result (p = 0.0001, r = 0.465) both confirm that degraded terraces sit closer to both infrastructure types, consistent with the material's roadability, that is, how cheaply it moves to market where roads and labour are already present (Engert et al., 2025). But I don't want to read too much into the settlement result on its own. Yes, it's consistent with an accessibility-driven extraction model, but it's also consistent with something more fundamental: a general gradient of human activity with settlement distance that could show up just as easily through a transport-economics road-access mechanism. Both associations are correlational, and I don't have a dated road/settlement record that lets me establish which came first. That causal sequence is something for future work.

The compactness result in Section 4.6 is relevant in its own right: it is independent of the NDVI threshold used to define bare-earth fraction, yet it identifies the same 25 terraces. Arriving at those same 25 through shape alone, with no reference to the NDVI threshold at all, is a second, convergent line of evidence, independent of the spectral method: a sign that the classification is picking up a consistent geometric signature on the ground, not a formal ground-truth confirmation.

The saffron-proximity finding is useful mainly as an early warning, not as a lagging one, since the data behind it can't support a direct-loss number. This finding is not affected by the drop-off from the FAO baseline set out in Section 6. The 14 terraces I detected are the ones that my phenological signature was able to align to with the highest confidence, and also based on a sensitivity analysis conducted in Section 4.7, the proximity-risk share doesn't change very much for a wide spectrum of detection thresholds so it's not dependent on the precise 0.15 threshold. A higher recall detection method would likely also detect smaller, less spectrally distinct parcels of saffron, and, after all, smaller parcels are likely to be closer to the margins of the already mined land. This was deliberate: hectares are the units that resonate with a geospatial audience, while rupees are what moves a district agriculture office or a legislative budget line, and I wanted this study to speak to both. I think this degradation and proximity-risk map comes close to being the kind of policy-alignment check this study can't fully deliver on its own: whether the Rs 400 crore PM Saffron Mission and its target of rejuvenating 2,598 hectares lines up with where the risk is highest. I've said before, I can't make that comparison right now because they don't have scheme-level spatial data that's publicly available, but if they did exist the outputs would be poised to support that comparison.

Then there's the legal dimension, which is a more basic problem than the misaligned-targeting question raised under RQ4 above: there's no minimum legal standard here at all. As of the most recent legislative reporting available, no identified legislation safeguards karewa land in Jammu & Kashmir against excavation. A private member's bill, sponsored by Dr. Syed Bashir Veeri, who represents Bijbehara, would ban any excavation or extraction of clay, sand and gravel in ecologically sensitive karewa areas (Kashmir Observer, 2025; Greater Kashmir, 2025), while authorising extraction in already-degraded areas where the need cannot be ignored, and only upon receipt of the necessary guidelines from the J&K State Environmental Impact Assessment Authority. In case of violation, the bill prescribes a monetary fine ranging from Rs 2,500 to Rs 10 lakh, along with imprisonment of up to 5 years. Currently, as best I can tell from newspaper and legislative reporting, it remains pending, while the Department of Revenue and the Department of Geology & Mining continue to grant "excavation" permits for the same activity the bill would prohibit. This changes how to read the road and settlement proximity results. There's no rule yet to fail against, so this isn't about enforcement falling short. It's about extraction happening with no rules in place at all. As that is the policy shift from "enforce what's already there more consistently" to "put a protection regime in place at all," this study will deliver the shape of evidence that that policy shift requires: a terrace-level risk map.

## 6. Limitations

- The detected zone of saffron cultivation (225.4 ha) is very weak with respect to the baseline of FAO GIAHS (3,200 ha). Because I find the reduction not to be due to a loss of cropland, I think it's prudent to report these as methodological limitations. Denying their reality just because it doesn't match what I expected would be the wrong call. In this case, it is the combination of 2 conservative filtering processes: terrace delineation, then the subsequent saffron-signature thresholding.
- RQ4 (about governance-alignment) was not amenable to statistical testing. I searched for spatially resolved PM Saffron Mission allocation data, but could only locate data at the valley level, which did not match the level of detail in this study's map of the terrace. It is put in the too-hard basket, that is in future action, preferably undertaken in collaboration with the implementing agency of the scheme.
- The multi-temporal analysis can't extend before 1994, since the Landsat record before that year doesn't provide a usable seasonal-coverage time frame.
- The 2025 point uses 10 m Sentinel-2 while 1994–2015 use 30 m Landsat. Section 4.8 measures this resolution effect directly: it comes to about 13% of the net-conversion rate. The gap between 190.3 ha and 165.2 ha comes from resampling the same area, and even though that gap looks small, it sets a floor: the sensor-driven inflation in the bare-earth-fraction number has to be at least this size, even if it seems negligible.
- 2005 used a wider net than intended. Since the same query, targeted at June-Sept 2005 using Landsat 5, returned 0 images, I expanded the window to include the previous and next 2 years on the same query, spanning 2001-2009, with 2005 as the mid-point (as detailed in SS_Development_Log.md). That's a multi-year composite; it may smooth over short-term degradation within that window, but it does not bias the 1994 or 2015 endpoints that drive the shape of the trend.
- Since no detailed dataset exists at the terrace level (or even at the Pampore-belt level) for saffron yield and price, this study applies a single statewide yield and price (5.27 kg/ha and Rs 2.73 lakh/kg) to each identified saffron terrace. Output per terrace is likely tied to soil quality, rejuvenation status, and micro-climate, and the premium that GI-tagged Pampore saffron commands is likely to exceed the statewide average applied here. This is not a precise appraisal but rather an "order of magnitude" value-at-risk estimate.
- The legal-protection finding is based on legislative reporting current as of this study's research. A private member's bill is in flux when not continually covered, so the "no current statute" finding should be rechecked against the latest reporting before being taken as still accurate.
- Because there is no ground truth data for reference use for this landscape, there is no existing formal accuracy evaluation of this data set using independently labeled ground truth points yet, nor is there a confusion matrix with producers' and user's accuracy. Instead I have validated the thresholds behind each classification here by doing the sensitivity sweep in Section 4.7 and checking their results visually. I have already developed a ground-truth class of 150 samples to this end, but these have not yet been labelled manually.
- The 201 terrace polygons themselves come from the current Copernicus DEM, and that same fixed set of 201 is what the 1994-2025 NDVI history is then measured against. A terrace that had already been substantially excavated or erased before this DEM was captured simply wouldn't register as a terrace-shaped landform today, so it would never enter this 201-polygon set to begin with. That means the 190.3 ha figure is the bare-earth conversion measured within the terraces that a present-day, DEM-based algorithm can still recognize as terraces now, not a full historical accounting of every karewa surface that has ever existed across this belt.
- As a small, separate check alongside that still-unlabelled 150-point sample, I visited the Lethpora saffron belt in person on 3 September 2026 and took 4 GPS-tagged photographs across the same terraces used in the Section 4.1 plausibility check, clustered around 33.97°N, 74.95°E. Saffron flowers only in a short October–November window, so what these photos show is dormant, freshly-tilled soil, not visible crop. That's what an active, pre-flowering saffron plot is supposed to look like at this time of year, not evidence that nothing is planted there. This bare, tilled appearance is not the same signal as the persistent, multi-year bare-earth increase the degradation classifier looks for, so one seasonal photo like this can't confirm or rule out degradation on its own. It's a small field anchor, not a validation exercise. I'm planning a return visit in October 2026, during peak bloom, to get a proper before/after pair at the same coordinates.
- The low-vegetation areas (0-40%) pinpointed in this study have not yet been cross-checked against crop-stress or drought impacts reported at the ground level by the districts.

## 7. Conclusion

Within the 201 karewa terraces this study can currently delineate from present-day DEM data, measurable bare-earth loss has happened at a fairly rapid pace. By the measure placed on the decade since 2015, most of that measured loss falls there. Degraded terraces sit closer to roads and to mapped buildings, the way Section 4.5's numbers already showed. The saffron economy on these terraces hasn't been directly hit yet — no saffron terrace overlaps mapped loss (Section 4.4) — but an estimated Rs 17.8 crore in production value sits close enough to active degradation that it's worth treating as at risk. The lack of any legal check on karewa excavation is a big part of why this is happening: the one bill that would regulate karewa excavation in Jammu & Kashmir remains stuck, absent any legislation governing it today. Two policy implications follow from that. 1st, any funds that are assigned to rejuvenating the saffron sector would need to be matched with the money that is being spent where it is most at risk of degradation. Don't assume that this is the same location. 2nd, the case for a provision for the protection of the karewa has now come equipped with scientific evidence: this loss can be measured, it's happening fast, and it comes with an economic cost, all without any compulsion of law.

## Declarations

**Ethics statement:** Not applicable. This study did not involve human participants, animals, or personal data of any kind.

**Competing interests:** I declare that I have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

**Funding:** This research received no external funding. All costs were covered by me.

**Data availability:** Processed data and analysis code for this study will be made available in a public repository upon publication. An interactive dashboard presenting the study's results will also be made available at that time. The raw satellite, terrain, and boundary datasets (Copernicus DEM, Landsat, Sentinel-2, OpenStreetMap) are publicly available from their original providers, cited in the References section below. The saffron cultivation baseline is drawn from FAO GIAHS documentation, also cited in the References section below.

**Acknowledgements:** None.

## Declaration of generative AI and AI-assisted technologies in the manuscript preparation process

During the preparation of this work, I used an AI assistant (Claude) to review the manuscript and project repository for internal inconsistencies, unverified or overstated claims, and wording issues, and to help revise affected passages accordingly. After using this tool, I reviewed, verified, and take full responsibility for all content in the published article.

## References

Bhat, G. R., Bali, B. S., Balaji, S., Iqbal, V., & Balakrishna. (2016). Earthquake triggered soft sediment deformational structures (seismites) in the Karewa formations of Kashmir valley—An indicator for palaeo-seismicity. *Journal of the Geological Society of India*, 87(4), 439–452. [https://doi.org/10.1007/s12594-016-0412-y](https://doi.org/10.1007/s12594-016-0412-y)

Boeing, G. (2017). OSMnx: New Methods for Acquiring, Constructing, Analyzing, and Visualizing Complex Street Networks. *Computers, Environment and Urban Systems*, 65, 126–139. [https://doi.org/10.1016/j.compenvurbsys.2017.05.004](https://doi.org/10.1016/j.compenvurbsys.2017.05.004)

Dar, R. A., & Zeeden, C. (2020). Loess-Palaeosol Sequences in the Kashmir Valley, NW Himalayas: A Review. *Frontiers in Earth Science*, 8, 113. [https://doi.org/10.3389/feart.2020.00113](https://doi.org/10.3389/feart.2020.00113)

Deccan Herald. (2022, March 13). Saffron boom in Kashmir: Highest production in 25 years. *Deccan Herald*. [https://www.deccanherald.com/india/saffron-boom-in-kashmir-highest-production-in-25-years-1090848.html](https://www.deccanherald.com/india/saffron-boom-in-kashmir-highest-production-in-25-years-1090848.html)

De Terra, H., & Paterson, T. T. (1939). *Studies on the Ice Age in India and Associated Human Cultures.* Carnegie Institution of Washington. [https://archive.org/details/dli.pahar.2748](https://archive.org/details/dli.pahar.2748)

Engert, J. E., Souza, C. M., Kleinschroth, F., Ishida, F. Y., Costa, S. P., Botelho, J., & Laurance, W. F. (2025). Road expansion risk predicts future hotspots of tropical deforestation. *Proceedings of the National Academy of Sciences*, 122(52). [https://doi.org/10.1073/pnas.2502426122](https://doi.org/10.1073/pnas.2502426122)

FAO GIAHS. (2012). *Saffron Heritage Site of Kashmir in India* (Part 1). Globally Important Agricultural Heritage Systems Pilot Project, SKUAST-K. [https://www.fao.org/3/bp791e/bp791e.pdf](https://www.fao.org/3/bp791e/bp791e.pdf)

Greater Kashmir. (2025, February 28). Why do Karewas need legal Protection in J&K? *Greater Kashmir*. [https://www.greaterkashmir.com/opinion/why-do-karewas-need-legal-protection-in-jk/](https://www.greaterkashmir.com/opinion/why-do-karewas-need-legal-protection-in-jk/)

Greater Kashmir. (2026, February 18). J&K Saffron output drops to 19.58 MT in 2024-25: Govt. *Greater Kashmir*. [https://www.greaterkashmir.com/business/jk-saffron-output-drops-to-19-58-mt-in-2024-25-govt](https://www.greaterkashmir.com/business/jk-saffron-output-drops-to-19-58-mt-in-2024-25-govt)

Kashmir Life. (2026, February 12). Kashmir's Saffron Sold for Rs 534.53 Cr in 2024-25, Govt Tells Assembly. *Kashmir Life*. [https://kashmirlife.net/kashmirs-saffron-sold-for-rs-534-53-cr-in-2024-25-govt-tells-assembly-424949/](https://kashmirlife.net/kashmirs-saffron-sold-for-rs-534-53-cr-in-2024-25-govt-tells-assembly-424949/)

Kashmir Observer. (2025, February 22). Will the Karewa Protection Bill Become a Law in J&K? *Kashmir Observer*. [https://kashmirobserver.net/2025/02/22/will-the-karewa-protection-bill-become-a-law-in-jk/](https://kashmirobserver.net/2025/02/22/will-the-karewa-protection-bill-become-a-law-in-jk/)

Kashmir Reader. (2026, February 13). Over 90 metric tonnes of saffron produced in last five years in J&K: Govt. *Kashmir Reader*. [https://kashmirreader.com/2026/02/13/over-90-metric-tonnes-of-saffron-produced-in-last-five-years-in-jk-govt/](https://kashmirreader.com/2026/02/13/over-90-metric-tonnes-of-saffron-produced-in-last-five-years-in-jk-govt/)

Madasa, A., Orimoloye, I. R., & Ololade, O. O. (2021). Application of geospatial indices for mapping land cover/use change detection in a mining area. *Journal of African Earth Sciences*, 175, 104108. [https://doi.org/10.1016/j.jafrearsci.2021.104108](https://doi.org/10.1016/j.jafrearsci.2021.104108)

Mann, H. B., & Whitney, D. R. (1947). On a Test of Whether one of Two Random Variables is Stochastically Larger than the Other. *Annals of Mathematical Statistics*, 18(1), 50–60. [https://doi.org/10.1214/aoms/1177730491](https://doi.org/10.1214/aoms/1177730491)

Press Post. (2026). Rs 400 cr PM Saffron Mission halts slide in Kashmir, 2,598 ha brought under rejuvenation. *Press Post*. [https://india.presspost.in/rs-400-cr-pm-saffron-mission-halts-slide-in-kashmir-2598-ha-brought-under-rejuvenation](https://india.presspost.in/rs-400-cr-pm-saffron-mission-halts-slide-in-kashmir-2598-ha-brought-under-rejuvenation)

Rafi, A. B., & Syed, S. (2023, January 27). Nourishing soils of Kashmir's karewas crumble under infrastructure. *Mongabay India*. [https://india.mongabay.com/2023/01/nourishing-soils-of-kashmirs-karewas-crumble-under-infrastructure/](https://india.mongabay.com/2023/01/nourishing-soils-of-kashmirs-karewas-crumble-under-infrastructure/)

Weiss, A. D. (2001). Topographic Position and Landforms Analysis. Poster presented at the ESRI International User Conference, San Diego, CA. [https://www.jennessent.com/downloads/TPI-poster-TNC_18x22.pdf](https://www.jennessent.com/downloads/TPI-poster-TNC_18x22.pdf)
