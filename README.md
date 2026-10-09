# STOLEN STRATA

**Brick kilns and the loss of karewa tableland in Budgam, Kashmir, 1993–2025, with a correction to an earlier estimate.**

> **This repository was revised in October 2026.** The version of September 2026 reported that bare ground on Kashmir's karewa
> terraces rose from 1.84% to 8.43% between 1994 and 2025 (a net 190.3 ha), with 25 degraded terraces and a saffron value at
> risk of ₹17.8 crore. Those numbers came from comparing two differently built satellite products and are **withdrawn**, with
> everything built on them. Section 4.1 of the paper shows the check. The September preprint
> ([EarthArXiv](https://eartharxiv.org/repository/view/14805/), [Zenodo](https://doi.org/10.5281/zenodo.21766464)) is that earlier version and has not yet been replaced.

## Live dashboard

**[Open the dashboard →](https://stolenstrata-ekmgvmukfnfkpigxtgsak6.streamlit.app/)**

## Documents

| Document | What it is |
|---|---|
| [`SS_Executive_Summary.md`](./SS_Executive_Summary.md) | Two pages: what changed, what the study shows, what it cannot show. Start here. |
| [`SS_Research_Paper.md`](./SS_Research_Paper.md) | The full paper. |
| [`SS_Development_Log.md`](./SS_Development_Log.md) | Day-by-day record. Entries 1–15 describe the first version; Entries 16 onward the rebuild and the correction. |

## The questions

Karewas are the flat-topped, scarp-bounded tablelands left by the old lake and river deposits of the Kashmir Valley. Reporting
from Kashmir has said for years that they are being dug away for brick clay and fill. Using one family of satellite sensors at a time, this project asks:

1. How much karewa tableland that was vegetated in 2013–2015 was no longer vegetated in 2023–2025, and does it convert faster than comparable land?
2. What did that land become, and how much of it now lies inside brick-kiln fields?
3. Where and when did the change happen?

## What the study shows

| | |
|---|---|
| Study box | 74.55°–75.15° E, 33.80°–34.15° N, about 2,160 km² (Budgam, Pulwama, Srinagar) |
| Terraces mapped | 180 scarp-bounded tablelands, 173.3 km² |
| Vegetated in 2013–15, bare in 2023–25, on terraces | 107 ha by a strict test; 329 ha by a looser one (286 ha net of reverse change) |
| Of the flagged land, not vegetated today | about 299 ha of 331 (95% interval roughly 285–313 ha), from two hand-labelled samples, 240 points in all |
| Vegetated in 2013–15 imagery and not vegetated today | about 260 ha (roughly 241–279 ha) |
| Of the flagged land, inside brick-kiln fields today | about 188 ha (roughly 166–210 ha); 141 ha by the first sample and 232 ha by the second, depending on how the edges of kiln fields are counted |
| Flagged sample points that show vegetation in 2013–15 imagery | 158 of 180 (59 of 60 strict, 99 of 120 looser); kiln-field land restricted to those: about 179 ha |
| Where | Two belts in Budgam: Rangeen Kultreh (a kiln field that opens in 2017–2018) and Bandagam–Batapora (older, and the largest post-2013 loss by the looser test). Outside them, terraces convert at the same rate as comparable land. |
| Back to the mid-1990s | A net loss of roughly 335 ha in the two belts. Indicative only: the Landsat record before 2013 is thin, and this series is being recomputed after a correction to the Landsat 8/9 adjustment. |

## What it does not show

- **Depth or volume.** Every free elevation model predates the Rangeen Kultreh kiln field; the result is "vegetated to bare", not "excavated".
- **A saffron link.** No conversion of this kind is seen on the Pampore tablelands in 2013–2025.
- **The whole Karewa formation.** The terrace map covers scarp-bounded tablelands, about a quarter of the mapped formation in the original box, and has no accuracy figure of its own yet.
- **A firm kiln figure.** The two samples agree on the loss of vegetation but give 141 and 232 ha of kiln land, because they counted the edges of kiln fields differently. A kiln-field outline on dated imagery or a second labeller is needed.
- **A fully blind check of the earlier state.** The first sample's 85 flagged points were looked up in 2013–14 imagery knowing they were flagged; the second sample was labelled blind. Twenty-one of the 120 looser points were not clearly vegetated in the older image.

The paper's Section 6 lists every limitation.

## Repository layout

```text
STOLEN_STRATA/
├── SS_Research_Paper.md, SS_Executive_Summary.md, SS_Development_Log.md
├── v2_redesign/                  the revised analysis: scripts, result tables, layers, labelled sample
│   ├── phase1_delineation/       terrace rule and geology check, original box
│   ├── phase2_timeseries/        single-sensor series, the rerun of the earlier rule, strict test, original box
│   ├── phase4_elevation/         elevation test (failed)
│   ├── west_extension/           everything on the wide box: terraces, both tests, accuracy sample, sensitivity, long series
│   ├── paper_figures/            Figures 1–4; make_figures.py draws 2 and 4, make_maps.py draws 1 and 3
│   └── RESUME_HERE.md            what is done and what is still open
├── dashboard/                    Streamlit dashboard (app.py, views/, map_data/)
├── data/processed/               layers of the earlier version; the Section 4.1 check reads the old polygons from here
├── data/raw/                     rasters (not stored in the repository, see DATA_ACCESS.md)
├── archive_v1/                   the withdrawn first version, kept for the record
├── DATA_ACCESS.md, CITATION.cff, LICENSE, requirements.txt
```

## Rerunning

```bash
git clone https://github.com/sakshimaske303-commits/STOLEN_STRATA.git
cd STOLEN_STRATA
pip install -r requirements.txt

# dashboard only (needs no rasters)
pip install -r dashboard/requirements.txt
streamlit run dashboard/app.py
```

The analysis scripts run from the repository root and need the rasters listed in [`DATA_ACCESS.md`](./DATA_ACCESS.md) in `data/raw/`.
The Earth Engine scripts in `v2_redesign/` regenerate them. Order, for the wide box:

```bash
python v2_redesign/west_extension/01_flat_top_delineation_wide.py   # writes data/interim/, which 02 reads
python v2_redesign/west_extension/02_conversion_wide_box.py
python v2_redesign/west_extension/03_drop_test_wide.py
python v2_redesign/west_extension/05_accuracy_result.py
python v2_redesign/west_extension/09_accuracy_by_labelling_pass.py
python v2_redesign/west_extension/10_before_check_result.py
python v2_redesign/west_extension/15_pooled_accuracy.py      # pools the two accuracy samples
python v2_redesign/west_extension/11_removed_flat_tops_check.py
python v2_redesign/west_extension/06_delineation_sensitivity.py
python v2_redesign/west_extension/07_drop_test_sensitivity.py
python v2_redesign/west_extension/08_long_series_wide.py
python v2_redesign/west_extension/13_polygon_level_comparison.py
python v2_redesign/west_extension/14_omitted_karewa_both_tests.py
python v2_redesign/phase2_timeseries/05_v1_rule_matched_statistic.py   # Section 4.1; needs the earlier rasters
python v2_redesign/phase4_elevation/01_elevation_gate_test.py
python v2_redesign/paper_figures/make_figures.py
python v2_redesign/paper_figures/make_maps.py
python dashboard/build_data.py
```

The geology check (`v2_redesign/phase1_delineation/01_…` to `04_geology_check.py`) and the first strict-test pass (`v2_redesign/phase2_timeseries/`) run on the original box and need its rasters (see `DATA_ACCESS.md`).

## Data sources

| Data | Provider |
|---|---|
| Elevation | Copernicus DEM GLO-30; SRTM; ALOS World 3D; GEDI |
| Time series | Landsat 5, 7, 8, 9 Collection 2 Level 2; Sentinel-2 with Cloud Score+ |
| Geology | Dar and Zeeden (2020), Figure 2, after Bhatt (1982) |
| Reference labels | Google Maps and Google Earth Pro imagery, newest available when labelled (October 2026) and 2013–2014 historical imagery |

## Author

**Sakshi D. Maske**, Independent Geospatial Researcher

## License

CC BY 4.0. See [`LICENSE`](./LICENSE).
