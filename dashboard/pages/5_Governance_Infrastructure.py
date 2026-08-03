import streamlit as st
from style import inject_css, card, map_placeholder, page_title, map_image, GOLD
import data as d

st.set_page_config(page_title="GOVERNANCE AND INFRASTRUCTURE | Stolen Strata", page_icon="🛣️", layout="wide")
inject_css()

page_title("🛣️ GOVERNANCE AND INFRASTRUCTURE", "Is degradation an accessibility story, and is policy targeting the right land?")

col1, col2 = st.columns(2)
col1.metric("Mann-Whitney U p-value", f"{d.ROAD_PROXIMITY_MANNWHITNEY_P}")
col2.metric("Test", "Degraded vs Non-Degraded Road Distance")

st.image(map_image("06_road_network_proximity.png"), use_container_width=True)

card(
    "Method",
    """
    <p>The OpenStreetMap road network within the study bounding box is extracted via
    <code>osmnx.graph_from_bbox(..., network_type='drive')</code>. Straight-line distance from each
    terrace <b>polygon</b> — its full boundary, not a reduced centroid point — to the nearest road edge
    is computed, then compared between degraded and non-degraded terraces using a
    <b>Mann-Whitney U test</b> — a non-parametric test appropriate here because terrace-to-road
    distances are non-normally distributed and zero-inflated near dense settlement edges (a terrace
    whose boundary touches or is crossed by a road correctly registers 0 m).</p>
    """,
    badge="Pipeline Stage 4",
)

card(
    "Result",
    f"""
    <p>{d.ROAD_PROXIMITY_FINDING}</p>
    <p>This is consistent with an accessibility-driven model of unregulated mining: extraction is
    economically viable where the marginal cost of transporting excavated material to a construction
    or brick-kiln market is lowest, i.e. near existing drivable roads — rather than being randomly
    distributed across the karewa landscape irrespective of infrastructure.</p>
    <p style="color:#9AA5B8; font-size:0.92rem;">This is a correlational result, not a causal one — no
    dated road-construction record was available to establish whether roads were built to service
    pre-existing degradation, or whether road access itself enabled the mining that followed. Both are
    consistent with an accessibility-driven model; disentangling them is future work.</p>
    """,
    badge="Finding",
)

card(
    "Effect Size and Multiple-Comparison Correction",
    f"""
    <p>Three Mann-Whitney tests are reported across this project against degradation status (road
    proximity, compactness, slope). Reporting only p-values overstates precision, and running three
    tests without correction inflates the family-wise false-positive rate. Rank-biserial effect sizes —
    road proximity r={d.EFFECT_SIZE_ROAD_R}, compactness r={d.EFFECT_SIZE_COMPACTNESS_R}, slope
    r={d.EFFECT_SIZE_SLOPE_R} — indicate small-to-moderate effects, not overwhelming ones. Applying a
    Holm-Bonferroni correction across the 3-test family (α=0.05): road proximity (p=0.0116, adjusted
    threshold 0.025) and compactness (p=0.0044, adjusted threshold 0.0167) both remain significant;
    slope was already non-significant before correction.</p>
    """,
    badge="Added: External AI Review",
)

card(
    "Policy Framing (RQ4)",
    """
    <p>The project's fourth research question asks whether current agricultural policy investment
    (e.g. National Saffron Mission funding) is spatially aligned with karewa land that remains
    geomorphologically and agronomically intact — or is instead directed toward land already under
    active erosion pressure. A targeted search for spatially resolved PM Saffron Mission site- or
    district-level allocation data found only aggregate, valley-wide figures (2,598 ha under
    rejuvenation, Rs 400 crore) — no dataset at a resolution this study's terrace-level map could be
    meaningfully overlaid against. This page is framed honestly around that constraint rather than
    fabricating a district-level comparison from figures that don't exist at that resolution. The
    road-proximity and degradation-hotspot layers developed here nonetheless provide an evidentiary
    basis that a future policy-alignment overlay — ideally built in partnership with the scheme's
    implementing agency, which would hold the disaggregated data this comparison needs — could build
    on directly.</p>
    """,
    badge="Governance Question",
)