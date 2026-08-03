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
SENSITIVITY_AT_RISK_PCT = [21, 29, 43, 71, 86, 93]  # all 6 points independently recomputed from raw data and confirmed exact (Deep Verify, 2026-08-02)

# ---- Road proximity / governance (09) -------------------------------------
ROAD_PROXIMITY_MANNWHITNEY_P = 0.0116
ROAD_PROXIMITY_FINDING = (
    "Degraded karewa terraces sit statistically significantly closer to the "
    "OpenStreetMap road network than non-degraded terraces (Mann-Whitney U test, "
    "p = 0.0116), consistent with an infrastructure-accessibility driver of "
    "unregulated soil mining."
)

# ---- Geomorphometrics (10 — confirmed 2026-08-02) -------------------------
GEOMORPHOMETRICS_CONFIRMED = True
COMPACTNESS_MEAN_INTACT = 0.191      # 4*pi*Area/Perimeter^2; 1.0 = circular/compact
COMPACTNESS_MEAN_DEGRADED = 0.138
COMPACTNESS_MWU_P = 0.0044           # degraded terraces are significantly less compact (more dissected)
SLOPE_MEAN_INTACT_DEG = 2.89
SLOPE_MEAN_DEGRADED_DEG = 3.06
SLOPE_MWU_P = 0.1711                 # not significant — internal slope does not distinguish degraded terraces
COMPACTNESS_NOTE = (
    "Compactness Index (4π·Area/Perimeter²) and mean slope per terrace were computed "
    "and tested against degradation status via Mann-Whitney U (see "
    "src/analysis/10_geomorphometrics_and_figures.py), then independently recomputed "
    "from the raw DEM during Deep Verify and confirmed exact. Degraded terraces are "
    "significantly less compact / more dissected than intact ones (mean 0.138 vs. "
    "0.191, p = 0.0044) — consistent with irregular mining-scarred boundaries replacing "
    "the smooth original terrace outline. Mean internal slope does not differ "
    "significantly by status (2.89° vs. 3.06° for degraded, p = 0.1711)."
)

# ---- Threshold sensitivity, resolution robustness, effect sizes (11, 12 — External AI Review, 2026-08-03)
DEGRADATION_THRESHOLD_SWEEP_PP = [5, 8, 10, 12, 15, 17, 20, 25, 30]
DEGRADATION_THRESHOLD_SWEEP_N = [49, 43, 37, 31, 25, 24, 23, 19, 14]  # terraces flagged at each pp cutoff

SAFFRON_THRESHOLD_SWEEP = [0.05, 0.10, 0.125, 0.15, 0.175, 0.20, 0.25]
SAFFRON_THRESHOLD_SWEEP_N = [25, 18, 16, 14, 12, 6, 4]
SAFFRON_THRESHOLD_SWEEP_AT_RISK_PCT = [40, 39, 44, 43, 42, 67, 50]  # at-risk % noisy below n=6

RESOLUTION_CHECK_10M_PCT = 8.43
RESOLUTION_CHECK_30M_PCT = 7.48   # 2025 Sentinel-2 resampled to match 30m Landsat pixel size
RESOLUTION_CHECK_10M_NET_HA = 190.3
RESOLUTION_CHECK_30M_NET_HA = 165.2
RESOLUTION_CHECK_10M_DEGRADED_N = 25
RESOLUTION_CHECK_30M_DEGRADED_N = 23

EFFECT_SIZE_ROAD_R = 0.268
EFFECT_SIZE_COMPACTNESS_R = 0.352
EFFECT_SIZE_SLOPE_R = -0.170
HOLM_BONFERRONI_NOTE = (
    "Rank-biserial effect sizes: road proximity r=0.268, compactness r=0.352, slope "
    "r=-0.170 (small-to-moderate). Holm-Bonferroni correction across all 3 tests "
    "(family-wise α=0.05): road proximity (p=0.0116, adj. threshold 0.025) and "
    "compactness (p=0.0044, adj. threshold 0.0167) both remain significant; slope was "
    "already non-significant before correction."
)

ROBUSTNESS_NOTE = (
    "Added after 4 independent AI reviews flagged threshold arbitrariness and the "
    "Landsat/Sentinel-2 resolution mismatch. Degradation-threshold sweep (5-30pp): "
    "the reported 25-terrace count sits in a stable 23-31 range across 12-20pp. "
    "Saffron-threshold sweep (0.05-0.25): the 43% proximity-risk share stays within "
    "39-44% across 0.05-0.175, only destabilising below n=6 detected terraces. "
    "Resampling 2025 to 30m (matching earlier years) drops bare-earth fraction from "
    "8.43% to 7.48% and net conversion from 190.3 to 165.2 ha — a real ~13% "
    "resolution effect, but the acceleration survives it (7.48% is still ~2.8x the "
    "flat 2005/2015 baseline)."
)

GITHUB_URL_PLACEHOLDER = "https://github.com/YOUR-USERNAME/Stolen-Strata"
