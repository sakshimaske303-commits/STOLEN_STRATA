# Stolen Strata — Dashboard

A dark, maroon-and-gold themed Streamlit dashboard for the Stolen Strata project
(Kashmir karewa terrace degradation and saffron vulnerability).

## Run it

```bash
cd dashboard
pip install -r requirements.txt
streamlit run app.py
```

## Structure

- `app.py` — Home page
- `style.py` — Shared "Loess Noir" theme (colors, fonts, card/placeholder helpers). Imported by every page.
- `data.py` — Single source of truth for every number shown on the dashboard. Update this file when you re-run an analysis script; every page re-reads from it automatically.
- `pages/` — One file per sidebar page, numbered so Streamlit orders them correctly:
  1. Study Design
  2. Geomorphological Delineation
  3. Degradation Analysis
  4. Saffron Vulnerability
  5. Governance & Infrastructure
  6. Explore Trends (interactive Plotly charts)
  7. Interactive Maps (placeholder — for your future GitHub-pushed live maps)
  8. Methodology & Data
  9. About & GitHub

## Before you share this

1. Drop this whole `dashboard/` folder into your `Stolen_Strata/` project root (it replaces the empty placeholder folder from the original directory setup).
2. Wherever you see **"Map will be uploaded here"**, that's intentional — swap in your static map images once they're ready (e.g. with `st.image("outputs/maps/your_map.png")`).
3. Open `data.py` and set `GITHUB_URL_PLACEHOLDER` to your real repository URL once it's public — this feeds the button on the final "About & GitHub" page.
4. Once `10_geomorphometrics_and_figures.py` output is confirmed, update `GEOMORPHOMETRICS_CONFIRMED = True` and fill in the real compactness/slope statistics in `data.py` and on the Geomorphological Delineation page.

Every page has been tested end-to-end with Streamlit's `AppTest` harness — no runtime errors on any page.

## Exporting charts as PNG (for the research paper)

`export_charts.py` regenerates all five dashboard charts as high-resolution PNGs
(same maroon/gold/navy theme), saved to `../outputs/figures/dashboard_charts/`:

```bash
cd dashboard
python export_charts.py
```

Re-run it any time you update numbers in `data.py` — it always reflects the
latest figures. If it errors about Chrome/kaleido, make sure
`kaleido==0.2.1` (pinned in `requirements.txt`) is the version installed —
newer kaleido releases need a separate Chrome install, and 0.2.1 avoids that.
