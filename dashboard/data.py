"""
data.py — Central results store for the Stolen Strata dashboard.

These figures are transcribed from the outputs of src/analysis/01-09 (and,
where noted, are pending confirmation from 10_geomorphometrics_and_figures.py).
When you re-run any analysis script and the numbers change, update them here —
every dashboard page reads from this single module so there is only one
place to keep in sync.
"""

# ---- Terrace delineation (01, 02) --------------------------------------
TOTAL_CANDIDATES_RAW = 6789          # TPI/slope threshold output, pre-filter
TOTAL_TERRACES = 201                  # after area (>=0.05 km2) + elevation (1550-2000m) filter
TOTAL_AREA_KM2 = 33.05
TOTAL_AREA_HA = 3305.3

# ---- Degradation / bare-earth change (03, 07) ---------------------------
DEGRADED_COUNT = 25
DEGRADED_PCT_OF_TERRACES = round(DEGRADED_COUNT / TOTAL_TERRACES * 100, 1)  # ~12.4%

BARE_1994_HA = 32.2
BARE_2025_HA = 222.6
NET_CONVERSION_HA = 190.3
NET_CONVERSION_PCT = 5.8

DEGRADED_POLY_LOSS_HA = 128.2
DEGRADED_POLY_LOSS_SHARE_OF_TOTAL_LOSS_PCT = 67  # 128.2 / 190.3

# ---- Four-point multi-temporal trend (08) --------------------------------
TREND_YEARS = [1994, 2005, 2015, 2025]
TREND_BARE_FRAC_PCT = [1.84, 2.62, 2.63, 8.43]

# ---- Saffron overlay (04) -------------------------------------------------
SAFFRON_POLYGONS = 14
SAFFRON_AREA_HA = 225.4
SAFFRON_OVERLAP_WITH_DEGRADED = 0  # no saffron polygon itself yet classified degraded

FAO_BASELINE_HA = 3200
FAO_FARM_FAMILIES = 17000
DETECTED_VS_FAO_SHORTFALL_PCT = round((1 - SAFFRON_AREA_HA / FAO_BASELINE_HA) * 100, 0)  # ~93%

# ---- Saffron proximity risk (05) -----------------------------------------
PROXIMITY_MEAN_M = 1177
PROXIMITY_MIN_M = 80
AT_RISK_1000M_COUNT = 6
AT_RISK_1000M_TOTAL = 14
AT_RISK_1000M_PCT = round(AT_RISK_1000M_COUNT / AT_RISK_1000M_TOTAL * 100, 0)

SENSITIVITY_THRESHOLDS_M = [500, 750, 1000, 1500, 2000, 2500]
SENSITIVITY_AT_RISK_PCT = [21, None, 43, None, None, 93]  # endpoints confirmed; interior points indicative

# ---- Road proximity / governance (09) -------------------------------------
ROAD_PROXIMITY_MANNWHITNEY_P = 0.0116
ROAD_PROXIMITY_FINDING = (
    "Degraded karewa terraces sit statistically significantly closer to the "
    "OpenStreetMap road network than non-degraded terraces (Mann-Whitney U test, "
    "p = 0.0116), consistent with an infrastructure-accessibility driver of "
    "unregulated soil mining."
)

# ---- Geomorphometrics (10 — pending confirmed run) ------------------------
GEOMORPHOMETRICS_CONFIRMED = False  # flip to True once 10_geomorphometrics_and_figures.py output is confirmed
COMPACTNESS_NOTE = (
    "Compactness Index (4π·Area/Perimeter²) and mean slope per terrace have been "
    "computed and tested against degradation status via Mann-Whitney U (see "
    "src/analysis/10_geomorphometrics_and_figures.py). Final statistics will populate "
    "this panel once the script's output is confirmed."
)

GITHUB_URL_PLACEHOLDER = "https://github.com/YOUR-USERNAME/Stolen-Strata"
