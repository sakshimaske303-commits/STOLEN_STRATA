# Raster data

`data/raw/` and `data/interim/` are not stored in the repository because the rasters are too large. The dashboard does not
need them. The analysis scripts do. Every raster below is produced by an Earth Engine script that is in the repository:
run the script in the Earth Engine code editor, start the export tasks, and put the downloaded GeoTIFFs in `data/raw/`.

## Wide box (74.55°–75.15° E, 33.80°–34.15° N): the results reported in the paper

Script: `v2_redesign/west_extension/gee_04_extended_box.js`. All at 30 m, EPSG:32643, one band per year.

| File in `data/raw/` | Content |
|---|---|
| `StolenStrata_v2w_OLIonly_p90_2013_2025.tif` | Landsat 8/9, unadjusted: yearly 90th percentile of NDVI. The series both conversion tests use. |
| `StolenStrata_v2w_L7only_p90_2013_2021.tif` | Landsat 7 alone, same measure. |
| `StolenStrata_v2w_S2_p90_2019_2025.tif` | Sentinel-2 with Cloud Score+, same measure. |
| `StolenStrata_v2w_LS_p90_1990_2007.tif`, `StolenStrata_v2w_LS_p90_2008_2025.tif` | Landsat 5/7/8/9 together, with 8/9 adjusted to 7 (Roy et al., 2016). The long series. |
| `StolenStrata_v2w_LS_counts_1990_2025.tif` | Clear observations per pixel per year. |
| `StolenStrata_v2w_DEM_GLO30_buffered.tif` | Copernicus GLO-30 with a buffer of about 10 km. |

## Original box (74.75°–75.15° E, 33.85°–34.15° N): the first pass, the geology check and the rerun of the earlier rule

| File in `data/raw/` | Script | Content |
|---|---|---|
| `StolenStrata_v2_LS_p90_1990_2025.tif`, `StolenStrata_v2_L7only_p90_2013_2021.tif`, `StolenStrata_v2_OLIonly_p90_2013_2025.tif`, `StolenStrata_v2_S2_p90_2019_2025.tif` | `v2_redesign/phase2_timeseries/gee_01_annual_composites.js` | As above, for the original box. |
| `StolenStrata_v2_LS_summer_1990_2025.tif`, `StolenStrata_v2_LS_counts_1990_2025.tif` | `v2_redesign/phase2_timeseries/gee_02_summer_counts.js` | June–September median NDVI per year (the measure of the earlier version) and observation counts. |
| `StolenStrata_v2_DEM_SRTM_2000.tif`, `StolenStrata_v2_DEM_AW3D30_2006_2011.tif`, `StolenStrata_v2_GEDI_ground_2019_2025.tif` | `v2_redesign/phase4_elevation/gee_03_elevation_gate_test.js` | Elevation test. In the GEDI file a cell with no shot carries 0 in both the height and the count band; the script keeps only cells with a count above 0. |
| `StolenStrata_DEM_GLO30_buffered.tif` | exported as in `gee_04_extended_box.js`, for the original box | Copernicus GLO-30 with buffer. |

`data/interim/` is written by the two delineation scripts (`01_flat_top_delineation*.py`), which reproject the elevation model to UTM 43N.

## Files of the earlier version

`v2_redesign/phase2_timeseries/05_v1_rule_matched_statistic.py` (the check in Section 4.1 of the paper) reads the Sentinel-2 composite
of the earlier version, `data/raw/StolenStrata_NDVI_2025.tif`, and the earlier polygons in `data/processed/karewa_multitemporal_trend.gpkg`.
The other rasters of the earlier version (`StolenStrata_NDVI_1994_v2.tif`, `_2005`, `_2015`, `StolenStrata_DEM_GLO30.tif`,
`StolenStrata_SaffronIndex_2025_v2.tif`) are used only by the withdrawn scripts in `archive_v1/`. The Earth Engine script that exported the earlier Sentinel-2 composite (`StolenStrata_NDVI_2025.tif`) is not in the repository, so that file cannot be regenerated; its checksum is listed below.

## Checksums of the rasters used for the reported results

SHA-256 of the files in `data/raw/` that produced the numbers in the paper (computed 9 October 2026). Earth Engine collections are reprocessed from time to time, so a fresh export may not match byte for byte; if it does not, rerun the scripts and compare the tables.

| File | SHA-256 |
|---|---|
| `StolenStrata_v2w_DEM_GLO30_buffered.tif` | `f2cf755a98edd557adaa880a56f3796d69d03593c42d164506d33d7732a46816` |
| `StolenStrata_v2w_L7only_p90_2013_2021.tif` | `3fbad751bd41c23de73f1e8b488321a1e0289acf0bb4029b8c2e4ce9e573be29` |
| `StolenStrata_v2w_LS_counts_1990_2025.tif` | `fe859a7590ef0516c5768dd616679baa872f7b5646bbc3c830d58705f27c913f` |
| `StolenStrata_v2w_LS_p90_1990_2007.tif` | `a7903bb6d11f13086ba1a81486283d83ed619eb4e87af53137a91311a070b848` |
| `StolenStrata_v2w_LS_p90_2008_2025.tif` | `76d70965936cdcb084147a679bd183038f4dcf7a9810ecb8540132ce94ebbc03` |
| `StolenStrata_v2w_OLIonly_p90_2013_2025.tif` | `24a934c64bca49341f0c5f5cabb669874edb5a9b4ebb878a3ca5befbe77467a5` |
| `StolenStrata_v2w_S2_p90_2019_2025.tif` | `79339cd84ef4f50947249995bd587289a75f5918e29a642b8ba0f51aed40e97e` |
| `StolenStrata_v2_LS_summer_1990_2025.tif` | `bd7a8541fa335d7e0ac0a6bcaff41cdcb68d24c0f2638d7c3db2d828a06edd9e` |
| `StolenStrata_NDVI_2025.tif` | `04c2d3c79b2b6d3bd53bc8f001c341b12c8ce3176f03372da8b1e684e2e73de2` |
| `StolenStrata_v2_DEM_SRTM_2000.tif` | `ab354abf6f75f0552b1588be67976d8873b63829e797993c35d6263ab6cd3ebb` |
| `StolenStrata_v2_DEM_AW3D30_2006_2011.tif` | `85fa272c561c0f0a4af2c70bfaee9fa3a2b407a92e7459d65c1be6dc9024db65` |
| `StolenStrata_v2_GEDI_ground_2019_2025.tif` | `8fd1fa01874ff166b52888f8ec15f3f295d7a6f30ef0f136c4de19d723e7abef` |
