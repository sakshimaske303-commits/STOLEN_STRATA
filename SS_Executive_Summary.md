# STOLEN STRATA: A Landform Under Erasure
### Quantifying the Anthropogenic Erasure of Kashmir's Karewa Terraces

Executive Summary · DOI: 10.5281/zenodo.21766464 · Sakshi D. Maske

## Project Overview

The karewas of Kashmir are a distinctive landform: flat-topped surfaces cut into the infill of an ancient intermontane lake. Their loess cap is the only reason Geographical Indication-tagged saffron grows in the Pampore belt at all. This is why I wrote STOLEN STRATA as a single line, not as an individual map: from the geology of the ancient lake basin, to the terraces it formed, to the saffron economy those terraces make possible, to the mining now systematically erasing them.

The headline number is a net increase of 190.3 hectares of bare-earth-classified surface on the mapped terraces since 1994. But the shape of that change matters more than the total figure; it rises only modestly up to 2015, then more than triples in the decade since. Recent, not gradual.

I didn't want to limit my analysis to a hectare count, so I took the analysis a bit further. Does degradation track road and settlement access? It is associated with both, more strongly with settlements than with roads (an association, not proof of cause). So how much is the saffron-proximity risk worth in money? Converted into rupees using official state yield and price data, it comes out to an estimated Rs 17.8 crore in annual production value (a number that makes sense to a district agriculture office in a way a hectare figure doesn't).

What's also not discussed in most satellite studies of this sort: is there a law specifically protecting karewas? No. As of the most recent legislative reporting located (February 2025), no karewa-specific law safeguards karewa land from being excavated. A protection bill was pending in the J&K Legislative Assembly, and extraction permits continued to be issued under general rules. Combine the geomorphology, the economics, and the legal void, and this is no longer just a change-detection exercise: it is a landform loss that carries a price tag, and it hands policymakers a lever worth pulling.

## The Question

How much of Kashmir's karewa terraces (the physical basis of the region's saffron economy) has been lost to unregulated soil mining, and does that loss line up with accessibility, or is it random? Apart from the hectare count, what is that loss worth in rupees to the saffron economy it threatens, and what legislation, if any, currently governs the extraction driving it?

## The Method

Geomorphologic boundaries of 201 karewa terraces, calculated algorithmically from a Copernicus DEM using a Topographic Position Index and slope threshold (TPI > 3, slope < 8°). No manual digitization anywhere in that step.

I tracked the 'bare-earth land-cover fraction' (share of pixels with NDVI < 0.15) at four time slices from Landsat 5/8 and Sentinel-2 (1994, 2005 [a 2001–2009 composite], 2015 and 2025; the 1994 and 2025 endpoints are season-matched, 2005 and 2015 use a wider May–October window), to see when, not just whether, the fraction rose. Saffron-cultivating terraces came out of an inverted-phenology NDVI signature, which I then converted into an estimated rupee value-at-risk figure using official 2024-25 J&K state saffron yield and price data. A rupee figure moves a policy conversation in a way a hectare count doesn't.

Two Mann-Whitney U tests, one with the OpenStreetMap road network, and one with 3,266 OpenStreetMap building footprints, test if degraded terraces are statistically closer to infrastructure than intact ones. On top of that: a threshold-sensitivity sweep, a quantification of the Landsat/Sentinel-2 mismatching of resolution sizes, and rank-biserial coefficients and a Holm-Bonferroni correction across all four tests so that those numbers would last longer than one conveniently set threshold. A follow-up search of the development of the J&K legislation is conducted to determine whether there are any current legislations which guard against excavation of karewa lands.

## The Finding

Degradation has happened fairly recently, and it is moving at a fast pace, not a slow one, over multi-decades. Mean bare-earth fraction rose only modestly from 1994 to 2015 (1.84% → 2.62% → 2.63%), then more than tripled by 2025, to 8.43%. That's a net increase of 190.3 hectares of bare-earth-classified surface, 67% of it within 12.4% of the terraces (9.7% of the mapped terrace area).

The degraded terraces, compared to the intact ones, are found to be statistically significantly near to the foot of building (455.9 m vs. 999.7 m, p = 0.0001) and drivable roads (75.6 m vs. 133.1 m, p = 0.0116). Both infrastructure signals point the same direction. Settlement proximity is the strongest statistical effect in the entire study.

Forty-three percent (43%) of the terraces flagged as likely saffron-cultivating are located within 1 km of already degraded land (a proximity indicator, not a probability). If both the at-risk and the other sections of a saffron growing area follow the official state yield and price at which it is marketed, then the total production value for this detected area comes to an estimated ₹32.4 crore per year, 55% of which would be generated by the at-risk subset.

As of the February 2025 reporting located, no karewa-specific legislation safeguards karewa land from excavation. A dedicated Karewa Protection Authority, proposed by the J&K Karewa Protection Bill, 2025 (a private member's bill), was still pending, and excavation permissions continued to be issued by the Revenue and Geology & Mining Departments.

| Test | U statistic | P-value | Effect size (r) | Holm-Bonferroni |
|---|---|---|---|---|
| Settlement proximity | 1176.0 | 0.0001 | 0.465 | Significant |
| Compactness | 1425.0 | 0.0044 | 0.352 | Significant |
| Road proximity | 1611.0 | 0.0116 | 0.268 | Significant |
| Slope | 2573.0 | 0.1711 | -0.170 | Not significant |

Settlement proximity, compactness, and road proximity all survive Holm-Bonferroni correction across the four-test family (family-wise α = 0.05); slope was already non-significant before correction. These are terrace-level tests with no adjustment for spatial clustering, so the p-values may overstate the evidence.

## Robustness & Evidence Checklist

✓ Two distinct (but spatially correlated) infrastructure-proximity signals (road network and 3,266 OSM building footprints) agree in direction

✓ Threshold-sensitivity sweep over the three classification thresholds (TPI/slope, degradation, saffron signature); the reported counts sit in a stable neighbourhood, not an isolated spike

✓ Resolution-mismatch check: 2025 Sentinel-2 resampled to Landsat 30 m; net conversion falls about 13% and the 2015–2025 jump about 16%, without reversing the acceleration (other sensor differences not tested)

✓ Rank-biserial effect sizes and Holm-Bonferroni correction computed across the full four-test family

✓ Economic valuation cross-verified: yield independently recomputed from raw production/area figures (19.58 MT / 3,715 ha = 5.271 kg/ha) matches the officially reported 5.27 kg/ha

✓ Saffron detection benchmarked openly against an independent FAO baseline; the recall shortfall is reported plainly, with nothing smoothed over

! Stratified, structured ground-truth sample (n=150), collected for a planned formal accuracy assessment. Manual labelling has not happened yet, so this stays a step for later work, still open.

! The area of terraces flagged as likely saffron (225.4 ha) is far below the FAO baseline (3,200 ha). This is mainly a coverage limitation: the TPI/slope rule captures terrace rims and spurs rather than broad flat plateau interiors where much saffron grows.

! Spatially resolved allocation data was not available to conduct governance-alignment testing (RQ4), so that alignment check was put off instead of guessed at without a proper source.

## Limitations

All thresholds used in the various types of classifications of this study were assessed visually and using a sensitivity sweep, but not by a formal procedure of comparing with independent ground-truth points, which are labeled in advance. There is a 150 point stratified sample that exists for that purpose, but the manual labelling and confusion matrix are yet to be created.

This economic valuation is based on a statewide yield and price which is applied to all detected saffron terraces in the same manner. The value per terrace may be bounded by soil quality or the awareness premium that one is able to command from Pampore as compared with non-GI premium, so the figure at ₹17.8 crore should not be considered as an exact valuation. The legal protection finding cannot be more up-to-date than the most recent reporting made by legislators, so, in the case of this private member's bill, verification is necessary because the status can change frequently without the media attention afforded by the other sources studied in this report.

An additional point to note: that closeness to the settlement may also be due to the general human activity gradient and not just the economics of transportation. And do note that the 2005 time point is a nine-year Landsat composite (2001-2009), not a single-year snapshot. My original single-year query came back empty, so I widened the window. That blurs short-term change around 2005, but it does not affect the 1994 and 2025 endpoints or the 2015 point.

## Practical Relevance

Combined, two related infrastructure-accessibility signals and the absence of karewa-specific protection give officials a governance picture they can act on: degradation is associated with the most accessible terraces, and there's no dedicated protection legislation in place.

I framed the saffron-proximity risk in rupees and not an abstract hectare count, because there is a very good reason to do so: it makes the crux of the saffron-proximity issue, which is the threat to the physical erosion of the terraces, directly relate to the livelihoods of those growing this crop. It also ties the finding to the pending Karewa Protection Authority bill this study identifies as the one concrete policy lever currently on the table.

GitHub: github.com/sakshimaske303-commits/STOLEN_STRATA | Live Dashboard: stolenstrata-ekmgvmukfnfkpigxtgsak6.streamlit.app | Zenodo DOI: 10.5281/zenodo.21766464

Sakshi D. Maske, Independent Geospatial Researcher
