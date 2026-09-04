# Raw Data Access

`data/raw/` is gitignored (see `.gitignore`) because the rasters are too large
to keep in the repo. This means cloning the repo alone is not enough to
re-run the `src/analysis/` pipeline from scratch — the six files below have
to be fetched and placed in `data/raw/` first. This file exists so that gap
doesn't stay implicit. It documents what each raw file is and roughly how it
was pulled, based on the actual acquisition steps recorded in
`SS_Development_Log.md` (Entries 2, 3, 5, 8) — it is not a re-run script, and
where the log doesn't pin down an exact parameter (precise cloud-cover cutoff,
compositing function for every single year), that's left unstated here rather
than guessed at.

| File expected in `data/raw/` | Used by | Source | Notes |
|---|---|---|---|
| `StolenStrata_DEM_GLO30.tif` | `01_extract_karewa_terraces.py` | Copernicus DEM GLO-30 (30m), via Google Earth Engine | AOI: 33.85–34.15°N, 74.75–75.15°E (Pampore / Pulwama / Budgam / Zewan, central Kashmir) |
| `StolenStrata_NDVI_1994_v2.tif` | `03_ndvi_change_detection.py` | Landsat 5, Google Earth Engine | Season-matched to the June–September window (originally pulled from a wider 1993–1996 stack, then narrowed to match the 2025 window — see Entry 3) |
| `StolenStrata_NDVI_2025.tif` | `03_ndvi_change_detection.py`, `12_robustness_and_effect_sizes.py` | Sentinel-2, Google Earth Engine | June–September window, ~10m native resolution |
| `StolenStrata_NDVI_2005.tif` | `08_multitemporal_trend.py` | Landsat 5, Google Earth Engine | **Not a single-year image** — the May–October / low-cloud query for 2005 alone returned nothing, so the window was widened to a 9-year span (2001–2009) centered on 2005, with no cloud filter and a median composite used to suppress cloud noise instead (see Entry 8, and the caveat already in `SS_Executive_Summary.md`) |
| `StolenStrata_NDVI_2015.tif` | `08_multitemporal_trend.py` | Landsat 8, Google Earth Engine | May–October window |
| `StolenStrata_SaffronIndex_2025_v2.tif` | `04_saffron_overlay.py` | Sentinel-2, Google Earth Engine (3-band index raster, band 1 = Saffron_Index) | March window — chosen because saffron's leaf canopy grows out post-flowering, after winter snowmelt, not during the October–November flowering period (see Entry 5) |

Everything else the pipeline needs is either downloaded live at run time
(the OSM road network and building footprints, via `osmnx`/Overpass in
`09_road_proximity.py`, `14a_download_settlement_footprints.py`, and the
`src/visualization/` export scripts — no manual download needed, just a live
internet connection) or already checked into `data/processed/`.

Shared parameters used throughout the pipeline (the AOI box, the projection,
and every calibrated threshold — TPI window/threshold, slope cutoff,
elevation range, bare-earth/degradation/saffron thresholds, the saffron
risk radius) now live in `config.py` at the repo root instead of being
retyped in each script — see that file for the values and where each one
was calibrated.
