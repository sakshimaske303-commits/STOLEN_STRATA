# STOLEN STRATA: Brick Kilns and the Loss of Karewa Tableland
### Budgam, Kashmir, 1993–2025, with a correction to my earlier estimate

Executive Summary · Revised 7 October 2026 · Sakshi D. Maske

*The earlier summary and preprint (DOI: 10.5281/zenodo.21766464, 4 September 2026) reported a rise in bare-earth share from 1.84% to 8.43% and a net increase of 190.3 ha. Those numbers are withdrawn. This summary replaces them.*

## What changed, in one paragraph

My first version said bare ground on Kashmir's karewa terraces had more than quadrupled since 1994, almost all of it after 2015. That jump sat exactly where the analysis switched from Landsat to Sentinel-2. When I ran the same polygons, the same rule and the same statistic on Landsat alone, the 2025 figure came out at 0.07%, not 8.43%. The rise came from mixing two differently built satellite products, not from the ground. So I rebuilt the study: a new terrace map checked against a published geological map, a time series that never compares one sensor with another, and an accuracy sample I labelled by hand. What survives is smaller, and I can defend all of it.

## What the study now shows

| | |
|---|---|
| Study box | About 2,160 km² across Budgam, Pulwama and Srinagar districts |
| Terraces mapped | 180 scarp-bounded karewa tablelands, 173.3 km² |
| Earlier headline | 1.84% → 8.43%, +190.3 ha: **artefact of mixing two satellite products, withdrawn** |
| Same rule and statistic, Landsat only | 2.02% (1994), 2.16% (2015), 0.07% (2025) |
| Vegetated in 2013–15, gone by 2023–25, on terraces | 107 ha by a strict test, 329 ha by a looser one |
| Of that, inside brick-kiln fields | **about 141 ha (roughly 110–172 ha)** |
| Of that, recognisable as kiln ground at close zoom | about 40 ha |
| Flagged sample points that show vegetation in 2013–14 imagery | 72 of 85 (all 25 strict, 47 of 60 looser) |
| Kiln-field land where the older image also shows vegetation | about 134 ha (roughly 103–164 ha) |
| Net loss in the two kiln belts since the mid-1990s | roughly 335 ha, indicative only: the record before 2013 is thin |
| Loss on the other 140 km² of terraces | None that this method can see |

## Where and when

**Rangeen Kultreh (Chadoora tehsil).** Green in every usable year from 1993 to 2016 (one anomalous year, 2001, aside). Then a kiln field opens: 21 ha bare in 2017, 66 ha in 2018, and today about a quarter of that terrace. Three satellites agree. A Pollution Control Committee report to the National Green Tribunal says one of the kilns there was commissioned in 2017 without consent and ordered closed in 2018, with 20 kilns within a kilometre. I got the 2017 date from the satellite record before I found that document.

**Bandagam–Batapora tablelands.** Older and slower. Land that never greens up was about 100 ha in the mid-1990s, about 300 ha by 2008–2012 and 378 ha now. The rise is not steady, and the early part rests on few images. The Pollution Control Committee's list of October 2023 has registered kilns under most of the village names in this belt, without locations.

**Everywhere else.** Of 180 terraces, 27 lost a hectare or more after 2013 by the looser test and only 8 by the strict one. Terraces convert several times faster than other flat, raised land in every version of the analysis I tried.

## How I checked it

- **One sensor family at a time.** Landsat 8/9 for the main test, Landsat 7 on its own as a second opinion (it confirms 86% of the pixels), Sentinel-2 as a third.
- **Terrace map against geology.** 80% of the mapped terrace area lies on Karewa formations on a published map.
- **My own choices.** Nine versions of the terrace rule and 51 versions of the change thresholds. The hectares move; the contrast and the locations do not.
- **By eye.** 120 random points, labelled without knowing which group each came from. The vegetation is gone at 100% of strict detections and 82% of looser ones (two of the 60 looser points could not be told). Three quarters of strict detections lie inside a kiln field; about one quarter of the looser ones do, the rest being houses, roads and other bare ground. Most of these points were first labelled plain bare ground and counted as kiln only on a second look, one zoom level out. Counting only points labelled kiln ground at close zoom gives about 40 ha instead of 141.
- **Back in time, point by point.** I looked up the 85 flagged points in Google Earth imagery of 2013–2014. Vegetation is visible at 72 of them: all 25 strict points and 47 of the 60 looser ones. Twelve looser points were not green in that image (three were already kiln ground, three were buildings or hard ground, three were bare ground beside sheds, three were bare soil plots) and one could not be told. Two of the twelve are points I count as kiln field today, so the kiln figure restricted to land the older image shows as vegetated is about 134 ha instead of 141.

## What I could not show

- **How deep the ground was dug.** Every free elevation model is older than the Rangeen Kultreh kiln field, and the space laser data has only nine shots on it.
- **A saffron link.** The saffron tablelands at Pampore are about 7 km or more from the main kiln field and show no conversion of this kind in 2013–2025. The saffron value-at-risk figure in the earlier version is withdrawn.
- **The whole karewa.** I map scarp-bounded tablelands, about a quarter of the Karewa formation area on the geological map. The terrace map itself has no accuracy figure yet.
- **A blind check of the past.** The older-imagery check looked only at points already flagged, mostly on one image of September 2014, and "vegetated" there includes rough grass and scattered trees. One image shows one day; the test uses the peak of the year.
- **Roads, settlements and the 25 "degraded terraces".** Those analyses depended on the withdrawn layer and are dropped.

## Why it matters

Protection of the karewas has a short, specific list of places where it matters most, and one of them was farmland ten years ago. And a satellite claim like my first one should be tested on a single sensor before it is published. Mine was not, and this revision is the result of doing that test late.

## Where things are

Paper: `SS_Research_Paper.md`. Scripts, tables, terrace layers and the labelled sample: `v2_redesign/`. Day-by-day record, including the mistakes: `SS_Development_Log.md`.
