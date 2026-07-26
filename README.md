# 🏔️ STOLEN STRATA — A Landform Under Erasure

**Quantifying how much of Kashmir's karewa terraces have been lost to unregulated mining — and what that means for the saffron economy they sustain.**

## 🔗 Live Dashboard

**[View the interactive dashboard →](#)** *(link to be added upon deployment)*

## 📄 Project Documentation

| Document | What's Inside |
|---|---|
| 📘 [`Project_Journal.md`](./Project_Journal.md) | Polished project summary — methodology, findings, conclusions (start here) |
| 📗 [`Research_Paper.md`](./Research_Paper.md) | Formal academic paper — literature review, statistical methodology, results, discussion |
| 📙 [`Development_Log.md`](./Development_Log.md) | Full technical development log — every bug, debugging session, and methodology iteration |

---

STOLEN STRATA is a geospatial framework that algorithmically delineates Kashmir's karewa terraces from terrain data alone, then tracks their loss to unregulated soil mining and urban expansion across a 31-year satellite record. Rather than relying on site-specific or anecdotal reporting, every terrace boundary, degradation flag, and proximity risk in this project is derived from a fully scripted pipeline — connecting a geologically singular landform to the saffron economy it sustains, and to the road infrastructure that makes its unregulated extraction economically viable in the first place.

Built on the same **"Trust, But Verify"** philosophy as the rest of this portfolio — every hypothesis is tested rigorously, and every finding is reported honestly, including a saffron-detection shortfall against an independent baseline and a governance question this study could not yet answer for lack of accessible data.

---

Interactive geospatial maps are hosted separately via GitHub Pages. Sample links:

**Terrace Delineation and Degradation**
- [Study Area Overview](https://sakshimaske303-commits.github.io/STOLEN_STRATA/outputs/interactive_maps/01_study_area_overview/index.html)
- [Terrace Degradation Status](https://sakshimaske303-commits.github.io/STOLEN_STRATA/outputs/interactive_maps/02_terrace_degradation_status/index.html)
- [Delineated Terrace Boundaries](https://sakshimaske303-commits.github.io/STOLEN_STRATA/outputs/interactive_maps/03_terrace_boundaries/index.html)
- [Validation at Saffron Fields, Lethpora](https://sakshimaske303-commits.github.io/STOLEN_STRATA/outputs/interactive_maps/04_validation_lethpora/index.html)

**Infrastructure**
- [Road Network Proximity](https://sakshimaske303-commits.github.io/STOLEN_STRATA/outputs/interactive_maps/06_road_network_proximity/index.html)

*(For the full interactive experience with dynamic legends and key observations, visit the [live dashboard](#) → Interactive Maps page)*

---

## 📊 What This Project Does

- Delineates 201 karewa terrace boundaries algorithmically from a Copernicus DEM using a Topographic Position Index and slope threshold — no manual digitization
- Tracks bare-earth land-cover fraction across four independent time points (1994, 2005, 2015, 2025) using season-matched Landsat and Sentinel-2 composites, revealing when degradation actually accelerated rather than assuming a steady multi-decadal trend
- Identifies saffron-cultivating terraces using an inverted-phenology signature, then quantifies their proximity to already-degraded terraces as a leading-indicator risk metric
- Tests whether degraded terraces are statistically closer to road infrastructure than intact ones, using a Mann-Whitney U test against the OpenStreetMap road network
- Benchmarks detected saffron extent against an independent FAO baseline, reporting the resulting shortfall transparently as a detection-recall limitation rather than a land-loss claim
- Presents all findings through a nine-page interactive Streamlit dashboard combining live charts, static QGIS cartography, and interactive QGIS-based web maps

## 🔬 Key Findings

**Degradation is recent and accelerating, not a slow multi-decadal process.** Mean bare-earth fraction across all 201 terraces was essentially flat from 1994 to 2015, then more than tripled between 2015 and 2025 — 190.3 hectares converted to bare-earth land cover overall, 67% of it concentrated within just 12.4% of terraces.

**Degradation follows roads.** Degraded terraces sit a mean 75.6 m from the nearest drivable road, against 133.1 m for intact terraces — a difference confirmed statistically significant (Mann-Whitney p = 0.0116), consistent with an accessibility-driven model of unregulated mining rather than randomly distributed loss.

**Saffron is not yet directly overlapped by degradation — but it is close.** Of 14 detected saffron-cultivating terraces, 43% sit within 1 km of an already-degraded terrace, and the nearest is just 80 m away. This is reported as an encroachment-risk finding, not a direct-loss one, and the underlying detected-area shortfall against the FAO baseline is documented openly rather than glossed over.

Full methodology, including the governance-alignment question this study could not yet test, is documented in the dashboard's Methodology page and in `Project_Journal.md`.

## 🗂️ Repository Structure

```text
STOLEN_STRATA/
├── dashboard/                       # Streamlit dashboard (9 pages)
│   └── pages/                       # Individual dashboard pages
├── data/
│   ├── raw/                         # DEM, satellite composites (gitignored)
│   └── processed/                   # Terrace, saffron, and road-proximity datasets
├── src/
│   ├── analysis/                    # Terrace delineation, change detection, statistical tests
│   └── visualization/               # AOI, settlement, and road-network export scripts
├── outputs/
│   ├── maps/                        # Static QGIS print-layout map exports
│   ├── interactive_maps/            # QGIS2Web interactive web-map exports
│   └── figures/dashboard_charts/    # Exported Plotly chart PNGs
├── notebooks/                       # Exploratory analysis notebooks
├── docs/                            # Project documentation
├── Project_Journal.md               # Polished project summary and methodology
├── Research_Paper.md                # Formal academic research paper
├── Development_Log.md               # Full technical development log
└── requirements.txt
```

## 🛠️ Tech Stack

Python · GeoPandas · Rasterio · NumPy / SciPy · Plotly · Kaleido · Streamlit · QGIS · QGIS2Web · GitHub Pages · Google Earth Engine · OSMnx

## 📚 Data Sources

| Dataset | Provider |
|---|---|
| Elevation, Slope | Copernicus DEM GLO-30 |
| Multi-Temporal Land Cover (1994, 2005, 2015) | Landsat 5/7/8/9 Archive |
| Multi-Temporal Land Cover (2025) | Sentinel-2 |
| Road Network | OpenStreetMap (via OSMnx) |
| Saffron Cultivation Baseline | FAO GIAHS — Saffron Heritage Site of Kashmir |

## ▶️ Running Locally

```bash
git clone https://github.com/sakshimaske303-commits/STOLEN_STRATA.git
cd STOLEN_STRATA
pip install -r requirements.txt
cd dashboard
streamlit run app.py
```

## 👤 Author

**Sakshi D. Maske**

Independent Geospatial Researcher

---

*This project's full development process — including every debugging session, methodology iteration, and technical decision — is documented in `Development_Log.md` for full transparency and reproducibility.*