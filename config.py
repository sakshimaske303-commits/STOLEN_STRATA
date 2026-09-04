"""config.py — shared parameters for the STOLEN STRATA analysis pipeline.

Every numbered script in src/analysis/ and src/visualization/ that used to
hardcode its own copy of the study-area bounding box, the projection, or one
of the calibrated thresholds now imports the value from here instead. That
guarantees every stage of the pipeline is reading the exact same number --
previously the same constant (e.g. DST_CRS, the AOI bbox, BARE_THRESHOLD)
was retyped independently in several files, which is harmless as long as
every copy stays in sync by hand, but is exactly the kind of thing that goes
quietly wrong later if only one copy gets edited.

None of the values below are new -- each one is copied unchanged from
wherever it was already hardcoded. Where a value was calibrated rather than
just chosen, the comment says where that calibration is documented:
SS_Development_Log.md for the narrative, src/analysis/11_threshold_sensitivity.py
for the actual sensitivity sweep.
"""

# --- CRS / projection ---
DST_CRS = 'EPSG:32643'  # UTM Zone 43N -- used for all area and distance calculations

# --- Study area bounding box (WGS84 lon/lat) ---
AOI_NORTH = 34.15
AOI_SOUTH = 33.85
AOI_EAST = 75.15
AOI_WEST = 74.75

# --- Step 1: Karewa terrace delineation (01_extract_karewa_terraces.py) ---
DEM_EDGE_TRIM_PX = 10    # pixels trimmed from each DEM edge (reprojection artifacts concentrate there)
TPI_WINDOW_SIZE = 17     # uniform_filter window for Topographic Position Index (~510m neighborhood at 30m/px)
TPI_THRESHOLD = 3        # TPI above this = locally elevated
SLOPE_THRESHOLD_DEG = 8  # slope below this (degrees) = relatively flat
# Calibrated per SS_Development_Log.md "Day 1": TPI>5 / slope<5 gave only 115
# thin, sliver-shaped candidates; TPI>3 / slope<8 recovered 201 proper
# blob-shaped ones. Full grid re-check in 11_threshold_sensitivity.py Part 1.

# --- Step 2: Candidate filtering (02_filter_terrace_candidates.py) ---
MIN_TERRACE_AREA_KM2 = 0.05
ELEVATION_MIN_M = 1550
ELEVATION_MAX_M = 2000

# --- Step 3: Bare-earth degradation (03_ndvi_change_detection.py, 08, 12) ---
BARE_EARTH_NDVI_THRESHOLD = 0.15    # pixels below this NDVI = bare earth / mining / built-up
DEGRADATION_LOSS_THRESHOLD = 0.15   # bare-earth-fraction increase (as a fraction, e.g. 0.15 = 15pp) to flag "likely_degraded"
# Sensitivity swept in 11_threshold_sensitivity.py Part 2 (5-30pp): 23-31
# terraces flagged across that range, vs. 25 reported at the chosen threshold.

# --- Step 4: Saffron detection (04_saffron_overlay.py) ---
SAFFRON_INDEX_THRESHOLD = 0.15
# Sensitivity swept in 11_threshold_sensitivity.py Part 3 (0.05-0.25).

# --- Step 5: Saffron proximity risk (05_saffron_proximity_risk.py) ---
SAFFRON_RISK_DISTANCE_M = 1000  # 1 km buffer around degraded terraces
