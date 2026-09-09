import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
from matplotlib.lines import Line2D

# ============================================================
# STOLEN STRATA — GRAPHICAL ABSTRACT
# ============================================================
#
# Main reported numbers:
# 201 karewa terraces
# 3,305.3 ha mapped area
# BEF: 1.84% (1994) -> 8.43% (2025)
# 190.3 ha net bare-earth conversion
# 25 / 201 terraces degraded
# 67% of loss concentrated in those 25 terraces
# 14 detected saffron terraces
# 43% within 1 km of degradation
# Rs 17.8 crore/year estimated value at risk
# Road proximity p = 0.0116
# Settlement proximity p = 0.0001
# Compactness p = 0.0044
# Slope p = 0.1711
# Resolution-matched conversion = 165.2 ha
#
# IMPORTANT:
# 1994–2025 = 31-year satellite record
# ============================================================


# ------------------------------------------------------------
# CANVAS
# ------------------------------------------------------------

fig, ax = plt.subplots(figsize=(16, 9), dpi=180)

ax.set_xlim(0, 16)
ax.set_ylim(0, 9)

ax.axis("off")


# ------------------------------------------------------------
# COLOURS
# ------------------------------------------------------------

BG = "#FFFFFF"

DARK = "#202020"
GREY = "#666666"
MID_GREY = "#888888"
LIGHT_GREY = "#D5D5D5"

TEAL = "#36B7B2"
TEAL_DARK = "#238C89"
TEAL_LIGHT = "#F0FBFA"

GREEN = "#5E9F55"
GREEN_LIGHT = "#F2F8F1"

RED = "#B84A4A"
RED_LIGHT = "#FCF1F1"

GOLD = "#C49A3A"
GOLD_LIGHT = "#FCF8EA"


fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def rounded_box(
    x,
    y,
    w,
    h,
    title,
    body_lines=None,
    edge=TEAL,
    face=TEAL_LIGHT,
    title_size=13.5,
    body_size=10.5
):

    box = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.025,rounding_size=0.10",
        linewidth=2,
        edgecolor=edge,
        facecolor=face
    )

    ax.add_patch(box)

    ax.text(
        x + w / 2,
        y + h - 0.25,
        title,
        ha="center",
        va="top",
        fontsize=title_size,
        fontweight="bold",
        color=DARK
    )

    if body_lines:

        body = "\n".join(body_lines)

        ax.text(
            x + w / 2,
            y + h / 2 - 0.05,
            body,
            ha="center",
            va="center",
            fontsize=body_size,
            color=GREY,
            linespacing=1.25
        )


def arrow(x1, y1, x2, y2):

    arr = FancyArrowPatch(
        (x1, y1),
        (x2, y2),
        arrowstyle="-|>",
        mutation_scale=15,
        linewidth=1.7,
        color=MID_GREY
    )

    ax.add_patch(arr)


def metric(
    x,
    y,
    number,
    label,
    color=DARK,
    size=25,
    label_size=9.5
):

    ax.text(
        x,
        y,
        number,
        ha="center",
        va="center",
        fontsize=size,
        fontweight="bold",
        color=color
    )

    ax.text(
        x,
        y - 0.42,
        label,
        ha="center",
        va="center",
        fontsize=label_size,
        color=GREY,
        linespacing=1.10
    )


# ============================================================
# TITLE
# ============================================================

ax.text(
    8,
    8.68,
    "STOLEN STRATA: Quantifying the Anthropogenic Erasure of Kashmir's Karewa Terraces",
    ha="center",
    va="center",
    fontsize=20.5,
    fontweight="bold",
    color=DARK
)

ax.text(
    8,
    8.24,
    "and Its Threat to the Saffron Economy",
    ha="center",
    va="center",
    fontsize=15,
    fontweight="bold",
    color=TEAL_DARK
)

ax.text(
    8,
    7.88,
    "Central Kashmir Valley   |   Multi-temporal remote sensing   |   1994–2025",
    ha="center",
    va="center",
    fontsize=10.8,
    color=GREY
)


# ============================================================
# TOP PIPELINE
# ============================================================

y = 6.25
w = 2.55
h = 1.28

xs = [0.55, 3.45, 6.35, 9.25, 12.15]


# ------------------------------------------------------------
# 1 — LANDSCAPE
# ------------------------------------------------------------

rounded_box(
    xs[0],
    y,
    w,
    h,
    "LANDSCAPE",
    [
        "Kashmir Valley",
        "Karewa terrace belt",
        "Saffron-growing region"
    ],
    edge=TEAL,
    face=TEAL_LIGHT,
    title_size=13.5,
    body_size=9.8
)


# ------------------------------------------------------------
# 2 — TERRACE MAPPING
# ------------------------------------------------------------

rounded_box(
    xs[1],
    y,
    w,
    h,
    "TERRACE MAPPING",
    [
        "TPI > 3",
        "Slope < 8°",
        "1550–2000 m elevation"
    ],
    edge=TEAL,
    face=TEAL_LIGHT,
    title_size=13.5,
    body_size=9.8
)


# ------------------------------------------------------------
# 3 — SATELLITE CHANGE
# ------------------------------------------------------------

rounded_box(
    xs[2],
    y,
    w,
    h,
    "31-YEAR CHANGE",
    [
        "Landsat + Sentinel-2",
        "1994 | 2005 | 2015 | 2025",
        "Bare-earth fraction"
    ],
    edge=TEAL,
    face=TEAL_LIGHT,
    title_size=13.5,
    body_size=9.5
)


# ------------------------------------------------------------
# 4 — RISK ANALYSIS
# ------------------------------------------------------------

rounded_box(
    xs[3],
    y,
    w,
    h,
    "RISK ANALYSIS",
    [
        "Saffron signature",
        "Roads + settlements",
        "Geomorphometrics"
    ],
    edge=TEAL,
    face=TEAL_LIGHT,
    title_size=13.5,
    body_size=9.8
)


# ------------------------------------------------------------
# 5 — ROBUSTNESS
# ------------------------------------------------------------

rounded_box(
    xs[4],
    y,
    w,
    h,
    "ROBUSTNESS",
    [
        "Threshold sensitivity",
        "30 m resolution match",
        "Effect-size + Holm correction"
    ],
    edge=TEAL,
    face=TEAL_LIGHT,
    title_size=13.2,
    body_size=9.1
)


# Pipeline arrows

for i in range(4):

    arrow(
        xs[i] + w,
        y + h / 2,
        xs[i + 1],
        y + h / 2
    )


# ============================================================
# KEY RESULTS PANEL
# ============================================================

panel = FancyBboxPatch(
    (0.55, 2.55),
    14.90,
    3.05,
    boxstyle="round,pad=0.025,rounding_size=0.12",
    linewidth=1.5,
    edgecolor=LIGHT_GREY,
    facecolor="#FFFFFF"
)

ax.add_patch(panel)

ax.text(
    8,
    5.30,
    "KEY RESULTS",
    ha="center",
    va="center",
    fontsize=15,
    fontweight="bold",
    color=DARK
)


# ============================================================
# RESULT CARD 1 — SCALE
# ============================================================

rounded_box(
    0.82,
    3.05,
    3.05,
    1.85,
    "MAPPED LANDSCAPE",
    None,
    edge=TEAL,
    face=TEAL_LIGHT
)

metric(
    1.58,
    4.05,
    "201",
    "karewa terraces",
    color=TEAL_DARK,
    size=24,
    label_size=9.5
)

metric(
    3.10,
    4.05,
    "3,305.3 ha",
    "total mapped area",
    color=DARK,
    size=18,
    label_size=9.0
)


# ============================================================
# RESULT CARD 2 — DEGRADATION TREND
# ============================================================

rounded_box(
    4.05,
    3.05,
    3.35,
    1.85,
    "BARE-EARTH FRACTION",
    None,
    edge=RED,
    face=RED_LIGHT
)

metric(
    4.78,
    4.05,
    "1.84%",
    "1994",
    color=TEAL_DARK,
    size=20,
    label_size=9.5
)

ax.text(
    5.65,
    4.05,
    "→",
    ha="center",
    va="center",
    fontsize=23,
    fontweight="bold",
    color=MID_GREY
)

metric(
    6.55,
    4.05,
    "8.43%",
    "2025",
    color=RED,
    size=20,
    label_size=9.5
)

ax.text(
    5.72,
    3.30,
    "sharp acceleration after 2015",
    ha="center",
    va="center",
    fontsize=9.3,
    color=GREY
)


# ============================================================
# RESULT CARD 3 — LOSS CONCENTRATION
# ============================================================

rounded_box(
    7.58,
    3.05,
    3.25,
    1.85,
    "LOSS CONCENTRATION",
    None,
    edge=RED,
    face=RED_LIGHT
)

# Main number

metric(
    8.35,
    4.05,
    "190.3 ha",
    "net conversion",
    color=RED,
    size=20,
    label_size=9.0
)

metric(
    9.95,
    4.05,
    "67%",
    "loss in 25 terraces",
    color=RED,
    size=22,
    label_size=8.8
)

# Bottom caption deliberately shortened
ax.text(
    9.20,
    3.30,
    "25 of 201 terraces flagged as likely degraded",
    ha="center",
    va="center",
    fontsize=8.7,
    color=GREY
)


# ============================================================
# RESULT CARD 4 — SAFFRON VULNERABILITY
# ============================================================

rounded_box(
    11.00,
    3.05,
    4.05,
    1.85,
    "SAFFRON VULNERABILITY",
    None,
    edge=GOLD,
    face=GOLD_LIGHT
)


# Three compact metrics with safer spacing

metric(
    11.62,
    4.05,
    "14",
    "saffron terraces",
    color=GOLD,
    size=22,
    label_size=8.5
)

metric(
    13.00,
    4.05,
    "43%",
    "within 1 km",
    color=GOLD,
    size=21,
    label_size=8.5
)

metric(
    14.38,
    4.05,
    "₹17.8 Cr",
    "annual value at risk",
    color=RED,
    size=15.5,
    label_size=7.8
)

# Bottom explanatory caption

ax.text(
    13.02,
    3.30,
    "6 terraces / 123.6 ha within 1 km of degradation",
    ha="center",
    va="center",
    fontsize=8.1,
    color=GREY
)


# ============================================================
# SPATIAL + GEOMORPHOMETRIC EVIDENCE
# ============================================================

ax.text(
    0.75,
    2.12,
    "SPATIAL + GEOMORPHOMETRIC EVIDENCE",
    ha="left",
    va="center",
    fontsize=11.5,
    fontweight="bold",
    color=DARK
)


# ------------------------------------------------------------
# ROADS
# ------------------------------------------------------------

ax.text(
    0.82,
    1.65,
    "ROADS",
    ha="left",
    va="center",
    fontsize=10.5,
    fontweight="bold",
    color=TEAL_DARK
)

ax.text(
    2.05,
    1.65,
    "Degraded terraces closer to roads",
    ha="left",
    va="center",
    fontsize=10.5,
    color=DARK
)

ax.text(
    6.25,
    1.65,
    "p = 0.0116",
    ha="left",
    va="center",
    fontsize=10.5,
    fontweight="bold",
    color=TEAL_DARK
)


# ------------------------------------------------------------
# SETTLEMENTS
# ------------------------------------------------------------

ax.text(
    7.25,
    1.65,
    "SETTLEMENTS",
    ha="left",
    va="center",
    fontsize=10.5,
    fontweight="bold",
    color=TEAL_DARK
)

ax.text(
    8.85,
    1.65,
    "Stronger proximity association",
    ha="left",
    va="center",
    fontsize=10.5,
    color=DARK
)

ax.text(
    12.15,
    1.65,
    "p = 0.0001",
    ha="left",
    va="center",
    fontsize=10.5,
    fontweight="bold",
    color=RED
)


# ------------------------------------------------------------
# COMPACTNESS
# ------------------------------------------------------------

ax.text(
    0.82,
    1.17,
    "COMPACTNESS",
    ha="left",
    va="center",
    fontsize=10.5,
    fontweight="bold",
    color=TEAL_DARK
)

ax.text(
    2.30,
    1.17,
    "0.138 degraded vs 0.191 intact",
    ha="left",
    va="center",
    fontsize=10.5,
    color=DARK
)

ax.text(
    6.25,
    1.17,
    "p = 0.0044",
    ha="left",
    va="center",
    fontsize=10.5,
    fontweight="bold",
    color=TEAL_DARK
)


# ------------------------------------------------------------
# SLOPE
# ------------------------------------------------------------

ax.text(
    7.25,
    1.17,
    "SLOPE",
    ha="left",
    va="center",
    fontsize=10.5,
    fontweight="bold",
    color=MID_GREY
)

ax.text(
    8.45,
    1.17,
    "No significant difference",
    ha="left",
    va="center",
    fontsize=10.5,
    color=DARK
)

ax.text(
    12.15,
    1.17,
    "p = 0.1711",
    ha="left",
    va="center",
    fontsize=10.5,
    fontweight="bold",
    color=MID_GREY
)


# ============================================================
# ROBUSTNESS STRIP
# ============================================================

robust = FancyBboxPatch(
    (0.72, 0.58),
    14.55,
    0.42,
    boxstyle="round,pad=0.02,rounding_size=0.08",
    linewidth=1.2,
    edgecolor=LIGHT_GREY,
    facecolor="#FAFAFA"
)

ax.add_patch(robust)

ax.text(
    8,
    0.79,
    "ROBUSTNESS  •  2025 BEF: 8.43% → 7.48% at 30 m  •  Net conversion: 190.3 → 165.2 ha  •  Degraded terraces: 25 → 23",
    ha="center",
    va="center",
    fontsize=8.6,
    color=GREY
)


# ============================================================
# FINAL CONCLUSION
# ============================================================

ax.text(
    0.72,
    0.25,
    "CONCLUSION",
    ha="left",
    va="center",
    fontsize=10.5,
    fontweight="bold",
    color=DARK
)

ax.text(
    2.05,
    0.25,
    "Karewa degradation is recent, spatially concentrated, accessibility-associated, and economically relevant to saffron landscapes.",
    ha="left",
    va="center",
    fontsize=9.9,
    fontweight="bold",
    color=DARK
)


# ============================================================
# EXPORT
# ============================================================

plt.tight_layout(pad=0.35)

plt.savefig(
    "STOLEN_STRATA_Graphical_Abstract.png",
    dpi=300,
    bbox_inches="tight",
    facecolor=BG
)

plt.savefig(
    "STOLEN_STRATA_Graphical_Abstract.pdf",
    dpi=300,
    bbox_inches="tight",
    facecolor=BG
)

plt.show()