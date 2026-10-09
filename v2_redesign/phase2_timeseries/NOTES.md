> **Read this first.** First pass on the original box, 2 October 2026. The figures here (88.9 ha, terrace 5, 0.98%) are from the
> 57-terrace original-box layer and were superseded by the wide-box run in `west_extension/`. Final figures: `SS_Research_Paper.md`.

# v2 Phase 2 — single-sensor time series (status: first full pass done, 2 Oct 2026)

Scripts: `gee_01_annual_composites.js`, `gee_02_summer_counts.js` (Earth Engine) → six GeoTIFFs in `data/raw/`;
`02_persistent_bare_analysis.py` (local) → the CSVs, `converted_patches_2013_2025.gpkg`, `phase2_summary.png`.

## What the data say (57 v2 terraces, 91.0 km²)
1. **The v1 headline does not survive a single sensor family.** v1 rule (June–Sep NDVI < 0.15) with Landsat throughout,
   on the v1 polygons: 1994 1.15%, 2015 1.11%, 2025 0.09% (v1 reported 8.43% for 2025 from Sentinel-2).
2. **The summer-median measure is not usable for trend.** It swings 0.3% → 16% → 1% between 1997 and 2006 and has
   almost no data in 1991, 1992, 1995. Median clear summer observations per pixel were 0–8 before 2009.
3. **Levels depend on the sensor.** Yearly p90 NDVI < 0.25 in 2025: Landsat harmonised 1.6%, Landsat 8/9 raw 2.3%,
   Sentinel-2 4.7%. Only change measured inside one sensor is defensible.
4. **There is a real, localised conversion after 2016.** Pixels vegetated (p90 ≥ 0.35) in all of 2013–15 and bare
   (p90 < 0.25) in all of 2023–25, Landsat 8/9 only: **88.9 ha on terraces (0.98%)** vs 6.0 ha (0.07%) on other flat
   elevated land and 263 ha (0.25%) in the rest of the box. Reverse change on terraces: 0.8 ha.
   Landsat 7 alone gives 64.4 ha by 2019–21 (Landsat 8: 62.2 ha, 89% pixel agreement). Sentinel-2 calls 97.8% of the
   converted pixels bare in 2023–25. Onset years: 2017–2018 (45 ha), then 2019–2023.
5. **It is one place.** 76.1 ha of the 88.9 ha are on terrace 5 (6.76 km², 11.2% of it), 10.9 ha on the neighbouring
   terrace 3. 52 of 57 terraces show none. Satellite imagery at 33.944 N, 74.848 E shows a dense brick-kiln field
   (Auwan Pora / Tumchi Nowpora, Budgam side). Not yet field- or document-verified.

## Not usable years (median clear observations < 10)
1990, 1991, 1992, 1995, 1996, 1997. 2001 passes the count rule but is an outlier (15%) and needs a look.

## Open
- Brick-kiln identification rests on one look at Google imagery: needs dates, kiln counts, and a source.
- Conversion is "vegetated → persistently low NDVI"; it does not separate excavation from buildings or roads (Phase 3).
- Thresholds 0.25 / 0.35 are choices; sensitivity not yet run.
- Before 2013 the Landsat record is too thin here for the same 3-year persistence test to be trusted.

## Whole-box check (04_conversion_whole_box.py)
Total converted in the box: 358 ha. By geology (valley part, below 2000 m), as a share of what was vegetated in 2013–15:
Karewa formation inside v2 terraces 1.36% (84 ha); Karewa formation outside v2 terraces 0.19% (37 ha); alluvium 0.19% (62 ha);
reworked karewa 0.14% (7 ha); unmapped 0.51% (74 ha). So Karewa ground that the scarp rule left out converts at the same
rate as ordinary valley floor: no second hot spot was missed inside this box.
Largest clusters: 1 = kiln block (85 ha); 2 = AIIMS Awantipora campus (37 ha, hillside, seen on imagery);
3, 4, 5, 8, 10, 14 = inside Dal Lake (58 ha together; lake vegetation to open water, not land);
6, 7, 13 = next to the kiln block (25 ha). Thin lines are road works and river-channel shifts.
The test therefore also flags construction and water changes: "converted" is not the same as "mined".
