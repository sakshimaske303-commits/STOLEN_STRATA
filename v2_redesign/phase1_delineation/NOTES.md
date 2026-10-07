# v2 Phase 1 — flat-top karewa delineation (status: 2 Oct 2026)

**Why:** the v1 rule (TPI > 3 m & slope < 8°) delineated terrace rims and spurs, not the flat karewa tops.

## Rule
1. slope < 4° on a lightly smoothed DEM
2. height above nearest drainage (HAND, streams ≥ 3 km²) > 15 m
3. elevation < 1950 m
4. scarp share ≥ 0.25: the share of the polygon's outer ring steeper than 6°. A karewa top ends in scarps; an alluvial fan fades into the plain.

Terrain is processed on the buffered DEM (`data/raw/StolenStrata_DEM_GLO30_buffered.tif`); polygons are clipped to the study box.

## Result
`karewa_terraces_v2.gpkg`: **57 polygons, 90.9 km²** inside the study box (46 with scarp share ≥ 0.45, 11 with 0.25–0.45). v1 was 201 polygons, 33.1 km².

Five small polygons that pass the rule were removed after review and are listed with reasons in `excluded_by_review.csv` (1.9 km² in total: hill-foot aprons and mountain valley floors).

## Independent check against a published Karewa Group map
Reference: Dar & Zeeden (2020), Fig. 2, after Bhatt (1982); see `geology/SOURCE.md`. Schematic map, ~100 m pixels, ~1 km positional error. Script: `04_geology_check.py`.

| Layer | on Karewa formations | on reworked karewa sediments | on recent alluvium |
|---|---|---|---|
| v2 terraces | 0.80 | 0.00 | 0.20 |
| prototype: scarp share ≥ 0.45 | 0.81 | 0.00 | 0.19 |
| prototype: 0.20–0.45 | 0.44 | 0.33 | 0.23 |
| prototype: < 0.20 (rejected) | 0.30 | 0.36 | 0.35 |
| whole study box below 2000 m | 0.39 | 0.07 | 0.54 |

- **User's accuracy 0.80** (0.67–0.89 if the map is shifted by up to 0.6 km in any direction).
- Scarp share and share on Karewa formations are correlated across the 44 polygons ≥ 0.5 km² (Spearman 0.58, p = 4 × 10⁻⁵).
- Scarp cut-off: at 0.25, 90% of the larger kept polygons sit on Karewa formations (94% at 0.30–0.45, 79% at 0.20). 0.25 was chosen from this table.
- The rejected polygons are mostly reworked karewa sediments and alluvium, which is what a fan should be.
- **Producer's accuracy is low: 0.24 of all mapped Karewa-formation area, 0.38 of the part that is flat (< 4°).** The v2 layer is the scarp-bounded tableland subset, not every karewa surface. Sloping karewa surfaces with no scarp (for example along the Tral valley side) and low-lying mapped karewa are left out.

## Not done
- Slope (4°) and HAND (15 m) cut-offs are not calibrated; the schematic map cannot do that.
- The GSI Bhukosh geology layer could not be downloaded (portal timing out).
- `reference_sample_points.csv` (460 blind stratified points) is drawn but not labelled. Human labelling would give an accuracy estimate that does not depend on a schematic map.
- First-pass review labels in `review_checklist.csv` were made from terrain, with satellite imagery for six polygons, and are not yet confirmed by me; 17 of 39 are low confidence. They are used only to remove the five polygons above.

## Early warning for Phase 2
On the first prototype plateaus, the share of pixels with summer NDVI < 0.15 was 0.14% (1994), 0.36% (2005), 0.39% (2015), 4.65% (2025 Sentinel-2 at 10 m), 3.98% (2025 at 30 m). A twelve-fold jump that coincides with the Landsat → Sentinel-2 switch cannot be trusted until it is reproduced with a single-sensor series.

## Files
`01_flat_top_delineation.py` → `karewa_flat_tops_prototype.gpkg` · `02_review_map.py` → `review_map.html`, `review_checklist.csv` · `03_finalize_and_sample.py` → `karewa_terraces_v2.gpkg`, `excluded_by_review.csv`, `reference_sample_*` · `04_geology_check.py` → `geology_*.csv`
