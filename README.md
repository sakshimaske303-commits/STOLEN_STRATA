# STOLEN STRATA — A Landform Under Erasure

**Quantifying how much of Kashmir's karewa terraces have been lost to unregulated mining — and what that means for the saffron economy they sustain.**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21766464.svg)](https://doi.org/10.5281/zenodo.21766464)

## Live Dashboard

**[View the interactive dashboard →](https://stolenstrata-ekmgvmukfnfkpigxtgsak6.streamlit.app/)**

## Project Documentation

| Document | What's Inside |
|---|---|
| [`SS_Executive_Summary.pdf`](./SS_Executive_Summary.pdf) ([.md source](./SS_Executive_Summary.md)) | One-page executive summary — project overview, question, method, headline finding, robustness checklist (start here) |
| [`SS_Research_Paper.md`](./SS_Research_Paper.md) | Formal academic paper — literature review, statistical methodology, results, discussion |
| [`SS_Development_Log.md`](./SS_Development_Log.md) | Full technical development log — every bug, debugging session, and methodology iteration |

---

STOLEN STRATA is a geospatial framework that automatically delineates Kashmir's karewa terraces from terrain data and tracks their disappearance to unchecked soil mining and urbanization, using a 31-year satellite record of the region (1994-2025). Every terrace boundary, degradation flag, and proximity-risk figure in this project runs through one fully scripted pipeline connecting a geologically unique landform to the economy it makes possible — saffron, valued here in rupees rather than just hectares — and to the reason its extraction remains economically viable: there's currently no legal framework regulating it.

This isn't a marketing brochure — it's built in the same "trust, but check" spirit as the rest of this portfolio: every hypothesis is tested thoroughly and every finding reported honestly, including the saffron-detection shortfall against an independent FAO baseline, and the governance-alignment question this study couldn't test due to a lack of accessible data.

---

## Interactive Maps

Eight fully interactive, pannable/zoomable maps, built directly from this project's own geopackages and hosted via GitHub Pages:

**Terrace Delineation and Degradation**
- [Study Area Overview](https://sakshimaske303-commits.github.io/STOLEN_STRATA/outputs/interactive_maps/01_study_area_overview/index.html)
- [Terrace Degradation Status](https://sakshimaske303-commits.github.io/STOLEN_STRATA/outputs/interactive_maps/02_terrace_degradation_status/index.html)
- [Delineated Terrace Boundaries](https://sakshimaske303-commits.github.io/STOLEN_STRATA/outputs/interactive_maps/03_terrace_boundaries/index.html)
- [Validation at Saffron Fields, Lethpora](https://sakshimaske303-commits.github.io/STOLEN_STRATA/outputs/interactive_maps/04_validation_lethpora/index.html)

**Saffron and Economic Risk**
- [Saffron Proximity Risk](https://sakshimaske303-commits.github.io/STOLEN_STRATA/outputs/interactive_maps/05_saffron_proximity_risk/index.html)
- [Saffron Economic Value-at-Risk](https://sakshimaske303-commits.github.io/STOLEN_STRATA/outputs/interactive_maps/08_economic_value_at_risk/index.html)

**Infrastructure**
- [Road Network Proximity](https://sakshimaske303-commits.github.io/STOLEN_STRATA/outputs/interactive_maps/06_road_network_proximity/index.html)
- [Settlement Proximity](https://sakshimaske303-commits.github.io/STOLEN_STRATA/outputs/interactive_maps/07_settlement_proximity/index.html)

*(Same eight maps are also browsable from a single dropdown on the [live dashboard](https://stolenstrata-ekmgvmukfnfkpigxtgsak6.streamlit.app/) → Interactive Maps page)*

**Additional Static Figures**
- [Distance to Nearest Settlement by Degradation Status](outputs/figures/06_settlement_distance_by_status.png)
- [Degradation vs Settlement Proximity (static map)](outputs/maps/07_settlement_proximity.png)
- [Saffron Economic Value-at-Risk (static map)](outputs/maps/08_economic_value_at_risk.png)

*(Settlement-proximity, economic-valuation, and legal-status findings are also presented as live charts and cards on the dashboard's Governance and Saffron Vulnerability pages — visit the [live dashboard](https://stolenstrata-ekmgvmukfnfkpigxtgsak6.streamlit.app/) for the full interactive versions)*

---

## What This Project Does

- Automatically delineates the boundaries of 201 karewa terraces from the Copernicus DEM using a TPI and slope threshold — no manual digitization.
- Reveals the point in time when bare-earth land-cover conversion actually accelerated — showing this isn't a steady multi-decadal process — using season-matched Landsat and Sentinel-2 composites at four time points (1994, 2005, 2015, 2025).
- Detects saffron-cultivating terraces using an inverted-phenology signature, and quantifies each one's distance to the nearest degraded terrace as a leading risk indicator, expressed as an estimated rupee value-at-risk using official state saffron yield and price data.
- Compares degraded terraces against the OpenStreetMap road network and building footprints — two independent accessibility measures — using Mann-Whitney U tests to check whether degraded terraces are more accessible.
- Benchmarks detected saffron area against an independent FAO baseline rather than claiming a loss of cropland, and reports the resulting detection-recall shortfall transparently.
- Identifies whether any legislation currently exists to block unregulated karewa excavation in J&K.
- Shares all results on an interactive 11-page Streamlit dashboard with live charts, static QGIS-rendered maps, and interactive maps.

## Key Findings

The fraction of bare earth (bare-earth land cover) in 201 terraces was close to unchanged from 1994 to 2015 but jumped more than threefold between 2015 and 2025 (190.3 hectares of bare-earth land cover overall, most of which came from just 12.4% of terraces).

Degraded terraces sit significantly closer to both drivable roads (75.6 m vs. 133.1 m for intact terraces, p = 0.0116) and building footprints (455.9 m vs. 999.7 m for intact terraces, p = 0.0001) than intact terraces do. Both infrastructure signals agree in direction, and settlement proximity is the single strongest statistical effect in the entire study — evidence that the pattern of loss isn't random.

Fourteen saffron-cultivating terraces were detected; 43% sit within 1 km of an already-degraded terrace, with the nearest just 80 m away. That at-risk subset represents an estimated ₹17.8 crore in annual production value at official 2024-25 saffron yield and price figures — 55% of the total production value this study attributes to the detected saffron area. This is a value-at-risk finding, not a claim of loss already incurred, and the shortfall against the FAO baseline is documented openly rather than glossed over.

At present there is no legislation to protect karewa surfaces from being dug up. As of the last update reported, a private member's bill for a separate Karewa Protection Authority and for a mandatory environmental impact assessment and penalty of up to five years' imprisonment or ₹10 lakh is pending; the Revenue and Geology & Mining Department continue to grant the excavation licences it would prohibit. This means the infrastructure-proximity findings aren't evidence that enforcement is failing — there's no rule yet to fail against. They simply show extraction happening in a genuinely unregulated space.

The methodology in this study, including the governance-alignment question this study wasn't yet able to test, is described on the dashboard's Methodology page and in `SS_Research_Paper.md`.

## Repository Structure

```text
STOLEN_STRATA/
├── dashboard/                       # Streamlit dashboard (11 pages: app.py home + 10 pages/)
│   └── pages/                       # Individual dashboard pages
├── data/
│   ├── raw/                         # DEM, satellite composites (gitignored)
│   └── processed/                   # Terrace, saffron, road-, and settlement-proximity datasets
├── src/
│   ├── analysis/                    # Terrace delineation, change detection, statistical tests,
│   │                                 #   settlement proximity, economic valuation, ground-truth sampling
│   └── visualization/               # AOI/settlement/road exports, interactive map builder (folium),
│                                     #   static print-layout map builder (matplotlib)
├── outputs/
│   ├── maps/                        # Static print-layout map exports (8 maps, plus chart-image duplicates also available in outputs/figures/)
│   ├── interactive_maps/            # Interactive Leaflet web-map exports (8 maps)
│   ├── figures/                     # Static maps, matplotlib figures, and exported Plotly chart PNGs
│   ├── ground_truth_sample_points.gpkg  # Stratified sample for manual accuracy-assessment labelling
│   └── economic_valuation_results.json
├── notebooks/                       # Exploratory analysis notebooks
├── SS_Executive_Summary.pdf         # One-page executive summary
├── SS_Executive_Summary.md          # Executive summary source (incl. Project Overview)
├── SS_Research_Paper.md             # Formal academic research paper
├── SS_Development_Log.md            # Full technical development log
└── requirements.txt                 # Full pipeline dependencies (see also dashboard/requirements.txt)
```

## Tech Stack

Python · GeoPandas · Rasterio · NumPy / SciPy · Plotly · Kaleido · Folium · Matplotlib · Streamlit · QGIS · GitHub Pages · Google Earth Engine · OSMnx

## Data Sources

| Dataset | Provider |
|---|---|
| Elevation, Slope | Copernicus DEM GLO-30 |
| Multi-Temporal Land Cover (1994, 2005, 2015) | Landsat 5/7/8/9 Archive |
| Multi-Temporal Land Cover (2025) | Sentinel-2 |
| Road Network | OpenStreetMap (via OSMnx) |
| Saffron Cultivation Baseline | FAO GIAHS — Saffron Heritage Site of Kashmir |

## Running Locally

```bash
git clone https://github.com/sakshimaske303-commits/STOLEN_STRATA.git
cd STOLEN_STRATA
pip install -r requirements.txt
cd dashboard
streamlit run app.py
```

## Author

**Sakshi D. Maske**

Independent Geospatial Researcher

## License

This project is licensed under [CC BY 4.0](LICENSE). See `CITATION.cff` for citation metadata.

---

*This project's full development process — including every debugging session, methodology iteration, and technical decision — is documented in `SS_Development_Log.md` for full transparency and reproducibility.*