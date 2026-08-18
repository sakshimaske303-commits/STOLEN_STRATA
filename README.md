# 🏔️ STOLEN STRATA — A Landform Under Erasure

**Quantifying how much of Kashmir's karewa terraces have been lost to unregulated mining — and what that means for the saffron economy they sustain.**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21766464.svg)](https://doi.org/10.5281/zenodo.21766464)

## 🔗 Live Dashboard

**[View the interactive dashboard →](https://stolenstrata-ekmgvmukfnfkpigxtgsak6.streamlit.app/)**

## 📄 Project Documentation

| Document | What's Inside |
|---|---|
| ⚡ [`SS_Executive_Summary.pdf`](./SS_Executive_Summary.pdf) | One-page executive summary — question, method, headline finding, robustness checklist (start here) |
| 📘 [`SS_Project_Report.md`](./SS_Project_Report.md) | Polished project summary — methodology, findings, conclusions |
| 📗 [`SS_Research_Paper.md`](./SS_Research_Paper.md) | Formal academic paper — literature review, statistical methodology, results, discussion |
| 📙 [`SS_Development_Log.md`](./SS_Development_Log.md) | Full technical development log — every bug, debugging session, and methodology iteration |

---

STOLEN STRATA is a geospatial framework that algorithmically delineates Kashmir's karewa terraces from terrain data alone, then tracks their loss to unregulated soil mining and urban expansion across a 31-year satellite record. Rather than relying on site-specific or anecdotal reporting, every terrace boundary, degradation flag, and proximity risk in this project is derived from a fully scripted pipeline — connecting a geologically singular landform to the saffron economy it sustains, valued in rupee terms rather than left as a hectare count, to the road and settlement infrastructure that makes its unregulated extraction economically viable in the first place, and to the legal framework — or near-total absence of one — currently governing that extraction.

Built on the same **"Trust, But Verify"** philosophy as the rest of this portfolio — every hypothesis is tested rigorously, and every finding is reported honestly, including a saffron-detection shortfall against an independent baseline and a governance question this study could not yet answer for lack of accessible data.

---

## 🗺️ Interactive Maps

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

**Interactive Plots**
- [Distance to Nearest Settlement by Degradation Status](outputs/figures/06_settlement_distance_by_status.png)
- [Degradation vs Settlement Proximity (static map)](outputs/maps/07_settlement_proximity.png)
- [Saffron Economic Value-at-Risk (static map)](outputs/maps/08_economic_value_at_risk.png)

*(Settlement-proximity, economic-valuation, and legal-status findings are also presented as live charts and cards on the dashboard's Governance and Saffron Vulnerability pages — visit the [live dashboard](https://stolenstrata-ekmgvmukfnfkpigxtgsak6.streamlit.app/) for the full interactive versions)*

---

## 📊 What This Project Does

- Delineates 201 karewa terrace boundaries algorithmically from a Copernicus DEM using a Topographic Position Index and slope threshold — no manual digitization
- Tracks bare-earth land-cover fraction across four independent time points (1994, 2005, 2015, 2025) using season-matched Landsat and Sentinel-2 composites, revealing when degradation actually accelerated rather than assuming a steady multi-decadal trend
- Identifies saffron-cultivating terraces using an inverted-phenology signature, then quantifies their proximity to already-degraded terraces as a leading-indicator risk metric, converted into an estimated ₹/year value-at-risk figure using official state saffron yield and price data
- Tests whether degraded terraces are statistically closer to infrastructure than intact ones, using Mann-Whitney U tests against both the OpenStreetMap road network and building footprints — two independent accessibility signals
- Benchmarks detected saffron extent against an independent FAO baseline, reporting the resulting shortfall transparently as a detection-recall limitation rather than a land-loss claim
- Investigates whether any legal protection regime currently governs karewa excavation in Jammu & Kashmir, through J&K legislative reporting rather than a fabricated policy-alignment table
- Presents all findings through a nine-page interactive Streamlit dashboard combining live charts, static QGIS cartography, and interactive QGIS-based web maps

## 🔬 Key Findings

**Degradation is recent and accelerating, not a slow multi-decadal process.** Mean bare-earth fraction across all 201 terraces was essentially flat from 1994 to 2015, then more than tripled between 2015 and 2025 — 190.3 hectares converted to bare-earth land cover overall, 67% of it concentrated within just 12.4% of terraces.

**Degradation follows both roads and settlements.** Degraded terraces sit a mean 75.6 m from the nearest drivable road (vs. 133.1 m for intact terraces, p = 0.0116) and a mean 455.9 m from the nearest building footprint (vs. 999.7 m for intact terraces, p = 0.0001) — two independent infrastructure signals, both statistically significant, consistent with an accessibility-driven model of unregulated mining rather than randomly distributed loss. Settlement proximity is the strongest statistical effect in the entire study.

**Saffron is not yet directly overlapped by degradation — but it is close, and worth real money.** Of 14 detected saffron-cultivating terraces, 43% sit within 1 km of an already-degraded terrace, and the nearest is just 80 m away. At official 2024-25 state saffron yield and value figures, that at-risk subset represents an estimated ₹17.8 crore in annual production value — 55% of the ₹32.4 crore this study's detected saffron area is estimated to generate in total. This is reported as an encroachment-risk finding, not a direct-loss one, and the underlying detected-area shortfall against the FAO baseline is documented openly rather than glossed over.

**No law currently protects karewa land from excavation.** A private member's bill proposing a dedicated Karewa Protection Authority, mandatory environmental impact assessment, and penalties of up to ₹10 lakh and five years' imprisonment remains pending as of the most recent reporting located, while the Revenue and Geology & Mining Departments continue to issue the excavation permissions the bill would restrict. This means the infrastructure-proximity findings above describe extraction proceeding in a genuinely unregulated space, not enforcement failure against an existing rule.

Full methodology, including the governance-alignment question this study could not yet test, is documented in the dashboard's Methodology page and in `SS_Project_Report.md`.

## 🗂️ Repository Structure

```text
STOLEN_STRATA/
├── dashboard/                       # Streamlit dashboard (9 pages)
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
│   ├── maps/                        # Static print-layout map exports (8 maps)
│   ├── interactive_maps/            # Interactive Leaflet web-map exports (8 maps)
│   ├── figures/dashboard_charts/    # Exported Plotly chart PNGs
│   ├── ground_truth_sample_points.gpkg  # Stratified sample for manual accuracy-assessment labelling
│   └── economic_valuation_results.json
├── notebooks/                       # Exploratory analysis notebooks
├── SS_Executive_Summary.pdf         # One-page executive summary
├── SS_Project_Report.md             # Polished project summary and methodology
├── SS_Research_Paper.md             # Formal academic research paper
├── SS_Development_Log.md            # Full technical development log
└── requirements.txt                 # Full pipeline dependencies (see also dashboard/requirements.txt)
```

## 🛠️ Tech Stack

Python · GeoPandas · Rasterio · NumPy / SciPy · Plotly · Kaleido · Folium · Matplotlib · Streamlit · QGIS · GitHub Pages · Google Earth Engine · OSMnx

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

## 📜 License

This project is licensed under [CC BY 4.0](LICENSE). See `CITATION.cff` for citation metadata.

---

*This project's full development process — including every debugging session, methodology iteration, and technical decision — is documented in `SS_Development_Log.md` for full transparency and reproducibility.*