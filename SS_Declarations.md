# STOLEN STRATA: Declarations

**Stolen Strata: Brick Kilns and the Loss of Karewa Tableland in Budgam, Kashmir, 1993–2025, with a Correction to an Earlier Estimate**

Sakshi D. Maske · Independent Geospatial Researcher · ORCID [0009-0002-5683-5966](https://orcid.org/0009-0002-5683-5966)

Version 2.0.0  
Preprint: EarthArXiv, DOI [10.31223/X5HB8J](https://doi.org/10.31223/X5HB8J) (the earlier version, whose headline figures are withdrawn) · Code and data: [github.com/sakshimaske303-commits/STOLEN_STRATA](https://github.com/sakshimaske303-commits/STOLEN_STRATA)

## Highlights

- 180 scarp-bounded karewa tablelands (173.3 km²) mapped from the Copernicus elevation model in a 2,160 km² box across Budgam, Pulwama and Srinagar.
- Between 2013–2015 and 2023–2025, Landsat 8/9 alone flags 107 ha of vegetated tableland gone bare by a strict test and 329 ha by a looser one.
- Two stratified random samples (240 points) show about 262 ha of the flagged land was vegetated in 2013–2015 imagery and is not today; about 210 ha (roughly 189–231 ha) lies inside brick-kiln fields.
- The change sits in two kiln belts in Budgam; outside them, the tablelands convert at the same rate as comparable flat, raised land.
- The earlier estimate of a rise from 1.84% to 8.43% bare ground came from mixing two differently built satellite products and is withdrawn.

## Author contributions (CRediT)

Sakshi D. Maske: Conceptualization, Methodology, Software, Validation, Formal analysis, Investigation, Data curation, Writing – original draft, Writing – review and editing, Visualization. This is a single-author study.

## Funding

This research received no external funding. I covered all costs myself.

## Competing interests

I declare no competing interests.

## Ethics

Not applicable. This study did not involve human participants, animals, or personal data of any kind.

## Data availability

Landsat 5, 7, 8 and 9 Collection 2 Level-2 surface reflectance (U.S. Geological Survey), Sentinel-2 with Cloud Score+, the Copernicus DEM GLO-30, SRTM, ALOS World 3D-30m and GEDI are public and were accessed through Google Earth Engine. The geological reference is a published figure (Dar and Zeeden, 2020, after Bhatt, 1982). Reference labels were made on Google Maps and Google Earth Pro imagery. The result tables, terrace layers and the labelled samples are in the repository; `DATA_ACCESS.md` lists the input rasters with SHA-256 checksums.

## Code availability and reproducibility

All scripts are in the repository under `v2_redesign`, and the README gives the order in which to run them. The Earth Engine scripts regenerate every raster of the revised analysis. The dashboard runs without any rasters. The Sentinel-2 composite of the earlier version, used only to show where the withdrawn figure came from, has no export script in the repository and cannot be regenerated.

## Analysis transparency

The terrace rule and the thresholds of both change tests are choices; I report sensitivity runs over them, which bound their effect but do not remove it. Both accuracy samples rest on one labeller's judgement. The second sample was labelled blind to stratum; the first sample's check of the earlier state was not. The written rule for where a kiln field ends was written after the two samples had been compared, and the relabelling under it was not blind to stratum.

## Corrections and version history

The version of September 2026 reported that bare ground on the karewa terraces rose from 1.84% in 1994 to 8.43% in 2025, with a saffron value at risk built on it. On Landsat alone, with the same polygons, rule and statistic, the 2025 figure is 0.07%. The rise came from comparing Landsat with a differently built Sentinel-2 product, and those figures are withdrawn with everything built on them. In the revised study, the first run of the long series applied the Landsat 8/9 adjustment in the reverse direction; the corrected run raised the three-decade figure for the two belts from about 335 ha to about 407 ha and changed nothing in the 2013–2025 results. Every change is recorded in `SS_Development_Log.md`.

## Use of AI tools

I used Claude (Anthropic), an AI assistant, at several points in this project, including one step of the accuracy assessment. For the 2013–2015 check of the first sample and for every label of the second sample, I took a screen capture of each point and the assistant suggested a first-pass label from it; I then confirmed or changed every label myself on screen in Google Earth Pro, so the final labels are my own decisions. The second opinion I took on roughly eight uncertain points of the first sample was also the assistant's. Beyond that, most of its help was checking: whether the areas and intervals quoted in the paper, executive summary, README and dashboard matched my output tables. When a script failed or returned something I could not explain, I sometimes used it to help trace the problem in my code. I wrote the paper and the other documents myself; I used it to point out sentences that were unclear or too technical, places where something seemed to be missing, and punctuation errors, and I decided what to change. I also used it for the layout of the project pages. It did not download or process the satellite data or run the analysis. The research questions, the terrace rule, the change tests, the sampling design, the rule for where a kiln field ends, the decision to withdraw the earlier estimate and the interpretation are my own. I checked every suggestion before using it and take full responsibility for the content.

## Licence and citation

The code, documentation and paper are released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0). Citation metadata are in `CITATION.cff`.
