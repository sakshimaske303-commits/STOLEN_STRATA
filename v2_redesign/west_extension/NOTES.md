# Extended box (74.55–75.15 E, 33.80–34.15 N) — first pass, 2 Oct 2026

Same rules as the original box, nothing re-tuned. `01_flat_top_delineation_wide.py` → 274 flat tops; scarp share ≥ 0.25 and
clipped to the box → **180 terraces, 173.3 km²** (93.5 km² in the old box, 79.8 km² in the extension).
Terrace IDs here are new: the kiln terrace that was "5" in the original box is "9" here (the wider DEM splits it differently).

## Vegetated 2013–15 → persistently bare 2023–25 (Landsat 8/9 only)
| Part | Terraces | Other flat land | Rest |
|---|---|---|---|
| Whole box | 107.0 ha (0.62%) | 11.4 ha (0.07%) | 329 ha (0.18%) |
| Old box | 89.8 ha (0.96%) | 0.07% | 0.25% |
| Extension | 17.2 ha (0.22%) | 0.07% | 0.09% |

Sentinel-2 calls 97.4% of the converted terrace pixels bare in 2023–25. Landsat 7 vs Landsat 8 to 2019–21: 70.8 vs 68.6 ha.
8 of 180 terraces have ≥ 1 ha converted. Terraces 9 + 3 (Rangeen Kultreh) = 87.8 ha = 82% of all terrace conversion.
Second site: terrace 10 (34.02 N, 74.67 E), 9.6 ha; imagery shows brick kilns there too. Not yet checked against documents.
Cluster at 34.142 N, 74.712 E (8.9 ha) is the Jhelum river, not land.

## Landsat 5/7 era (1993/94/98 → 2005/06/07)
Terraces 30 ha (0.18%), other flat 0.10%, rest 0.11%. No terrace-specific signal in that period at this strictness,
and only three usable early years, so this is weak either way.

## Missing
`StolenStrata_v2w_LS_p90_2008_2025.tif` had not arrived when this was run; nothing above depends on it.
The geology map tile from Phase 1 starts at about 74.66 E, so the western strip has no geology check yet.

## CORRECTION (same day): the strict test undercounts kiln land — see 03_drop_test_wide.py
Imagery of the second site (34.02 N, 74.67 E) shows it is not a small patch but a kiln landscape several km across
(Bandagam, Chand Pora, Hardu Bata Pora, Nijlu, Bonahama). The strict test found only ~10 ha of new conversion there.
Reason: at 30 m kiln land is mixed pixels at p90 NDVI 0.25–0.45, rarely below 0.25. In a 20.6 km² window over that
belt, Landsat 8/9 pixels below 0.35 rise from 11.6% (2013) to 18.1% (2025); below 0.25 only from 3.5% to 8.7%.

Drop test (median p90 2013–15 ≥ 0.45, late median < 0.40, fall ≥ 0.20), Landsat 8/9, 2013–15 → 2023–25:
| Part | Terraces: drop / reverse / net | Other flat: net | Rest: net |
|---|---|---|---|
| Old box | 162.8 / 11.3 / **151.5 ha** (1.74%) | 30.9 ha (0.70% gross) | 1,048 ha (1.31% gross) |
| Extension | 165.8 / 31.4 / **134.4 ha** (2.08%) | 9.6 ha (0.45% gross) | 454 ha (0.86% gross) |

27 of 180 terraces lose ≥ 1 ha, 13 lose ≥ 5 ha; a whole group of them lies at 34.00–34.03 N, 74.62–74.70 E.
Landsat 7 agrees on 86% of the Landsat 8 drop pixels (to 2019–21). Sentinel-2 late median on dropped pixels: 0.17.
In the extension most of the drop comes after 2019–21 (48.8 ha by 2019–21, 165.8 ha by 2023–25).

So there are two defensible numbers, not one: strict = 107 ha (a floor, almost all Rangeen Kultreh);
drop-based = 329 ha gross, about 286 ha net of reverse change, spread over two kiln belts.
The drop test is noisier (the "rest" stratum shows large reverse change), so it needs a visual accuracy check
on a sample before either number goes in the paper. The statement in the first section that the extension
"adds little" holds only for the strict test.

## Accuracy check (04_accuracy_sample.py, 05_accuracy_result.py) — 120 points on terraces, labelled blind by the author
Present-day Google imagery (2026). Two passes: 7 classes; then, for the 68 points first called bare_other or road, one question:
inside a brick-kiln field or not. A first-pass-only version could not separate kiln ground from other bare ground.

| Stratum (terraces) | n | area | kiln | built / road | other bare | still vegetated | unclear |
|---|---|---|---|---|---|---|---|
| A strict test | 25 | 107 ha | 19 (76%) | 2 | 4 | 0 | 0 |
| B drop test only | 60 | 224 ha | 16 (27%) | 17 | 16 | 9 (15%) | 2 |
| C not flagged | 35 | 17,000 ha | 1 (3%) | 4 | 8 | 22 (63%) | 0 |

- Both tests are right that the vegetation is gone: 100% (CI 87–100%) for strict, 82% (70–89%) for drop-only (49 of 60; two more points are unclear and are not counted as bare).
- What it went to differs. Strict: about three quarters kiln ground. Drop-only: about a quarter kiln, a quarter buildings and
  roads, a quarter other bare ground, 15% false alarms.
- **Kiln ground among flagged terrace land: about 141 ha (95% CI roughly 110–172 ha)** = 81 ha from the strict test + 60 ha from the drop-only part.
- 37% of unflagged terrace points also look non-vegetated today, so "bare in the 2026 image" alone means little; the tests rest on
  the change, which the imagery cannot verify.
- Limits: one labeller; imagery is a single date; the reference shows the present state, not that the land was vegetated in 2013–15;
  n is small, especially for the strict stratum; the unflagged stratum is far too thinly sampled to estimate missed kiln land
  (1 of 35 points, 86–2,470 ha). A second opinion was taken on about eight points while labelling (first pass 1–6,
  second pass 81 and 112); the rest were labelled alone.

## Robustness and the long view (06, 07, 08)
**Terrace cut-offs (06).** Slope 3/4/5° × height above drainage 10/15/20 m. Terrace area swings from 106 to 258 km², but the
strict conversion stays at 95–120 ha and the drop test at 221–422 ha; terraces convert 5–13 times (strict) and 2.4–3.7 times
(drop) faster than other flat land in every one of the nine versions. Height above drainage hardly matters; slope does.

**Drop-test cut-offs (07).** 27 combinations (early ≥ 0.40/0.45/0.50, late < 0.35/0.40/0.45, fall ≥ 0.15/0.20/0.25):
net of reverse change 234–374 ha on terraces; ratio to other flat land 1.9–5.7; Rangeen Kultreh 30–44% of it.
The accuracy labels apply only to the setting actually sampled (0.45 / 0.40 / 0.20).

**Long series (08), Landsat 5/7/8/9 as one family, 1993–2025.** Terrace land with a 3-year median yearly-peak NDVI below 0.35:
| | 1993–98 | 2003–07 | 2008–12 | 2013–15 | 2018–20 | 2023–25 |
|---|---|---|---|---|---|---|
| Bandagam–Batapora terraces | 102 ha (3.7%) | 162 | 304 (10.9%) | 268 | 287 | 378 ha (13.6%) |
| Rangeen Kultreh terraces | 1 ha | 0 | 0 | 6 | 103 | 122 ha (25.0%) |
| All other terraces | 417 ha (3.0%) | 459 | 654 | 254 | 273 | 273 ha (1.9%) |
Drop test 1993–98 → 2023–25, net of reverse: Rangeen Kultreh +92 ha, Bandagam–Batapora +243 ha, all other terraces −336 ha.
So the two kiln belts lost roughly 335 ha of vegetated terrace land over three decades while the rest of the terraces, if
anything, got greener. Bandagam–Batapora grew in two steps (to 2008–12, and again after 2018–20); Rangeen Kultreh is entirely after 2015.
Caution: yearly-peak NDVI is higher from 2013 on everywhere (terrace median 0.57 → 0.67), partly because Landsat 8 added
observations. That pushes the long comparison toward "greener", so the two belts' losses are if anything understated and the
greening elsewhere overstated. 1999–2002 is noisy (few scenes) and is not used for conclusions.

**Documents for the Bandagam–Batapora belt.** None found that name those villages. District level only: the J&K Pollution Control
Committee reported 213 brick kilns in Budgam (19 April 2023), 96 notices for lapsed consent, 46 closure orders; a status
report by the Committee in NGT OA 594/2022 (Syed Riyaz v. UT of J&K), dated 4 October 2023, lists 226 kilns in Budgam: 100 consented,
11 under process, 43 with closure orders, 72 with legal notices. Read in full. Rows by village name: Chandpora 22, 51, 56, 63, 71, 129, 135, 141, 142, 151, 158, 172 (Batapora Chandpora);
Bonhama/Bunhama Beerwah 38, 72, 153, 189, 215, 224; Batpora 41, 98, 107, 110 (Batpora Wudar); Harda Batapora 219; Bandgam Magam 148;
Nigloo Beerwah 208. Kultreh: 199 Koka K11 (without consent, closure order), 202 Modern 17T (consented), 203 Brick No. 37 D (closure
order); Kultruch 221-223 with consent to establish, not yet built. No coordinates and, for most rows, no date of establishment. An additional report of 1 January 2024 says kilns within 8 km of the Srinagar Airport runway may
not operate from 1 November to 31 March. Which kilns stand on mapped terraces is still identified from imagery only.

**Not done.** Geology check for the strip west of 74.66 E (needs the map figure captured again; the in-app browser was not usable).
**Still open.** A second labeller for the 120 points.

## Before check (10_before_check_result.py): the 85 flagged points in imagery of 2013-2014

Each flagged sample point (strata A and B) was looked up in Google Earth Pro historical imagery, from `accuracy_sample_points.kml`,
and labelled vegetated / not_vegetated / unclear at the point. Record: `accuracy_before_pass.csv` (label, image date, what is seen).
September 2014 imagery for 77 points, a clear image between June 2013 and July 2014 for the other eight. Not blind: only flagged
points were looked at. Labels were drafted from screen captures and each was confirmed on screen by the author.

| Stratum | n | vegetated | not vegetated | unclear | vegetated then and kiln field now |
|---|---|---|---|---|---|
| A_strict | 25 | 25 | 0 | 0 | 19 (81 ha) |
| B_drop_only | 60 | 47 | 12 | 1 | 14 (52 ha) |
| together | 85 | 72 (85%, 76-91%) | 12 | 1 | 33 (134 ha, about 103-164) |

The twelve: already kiln benches or drying rows (27, 30, 32); buildings or hard ground (79, 87, 114); bare ground and tracks beside
sheds and structures (8, 39, 69); bare soil plots (20, 78, 106). Unclear: 90. All thirteen are drop-only points whose Landsat median
yearly peak in 2013-2015 was 0.45 or more, so picture and record disagree there: mixed 30 m pixels, or one image date against a
yearly peak. Kiln estimate restricted to points vegetated in the older image: 134 ha, against 141 ha from the satellite test alone.
`accuracy_before_pass.html` was the labelling page prepared for this pass; the record that counts is the csv.
