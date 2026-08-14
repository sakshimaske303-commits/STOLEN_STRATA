import streamlit as st
from style import inject_css, card, map_placeholder, page_title, map_image, GOLD
import data as d

st.set_page_config(page_title="GOVERNANCE AND INFRASTRUCTURE | Stolen Strata", page_icon="🛣️", layout="wide")
inject_css()

page_title("🛣️ GOVERNANCE AND INFRASTRUCTURE", "Is degradation an accessibility story, and is any policy or law targeting the right land?")

col1, col2, col3 = st.columns(3)
col1.metric("Road proximity p-value", f"{d.ROAD_PROXIMITY_MANNWHITNEY_P}")
col2.metric("Settlement proximity p-value", f"{d.SETTLEMENT_PROXIMITY_MANNWHITNEY_P}")
col3.metric("Legal protection status", "No statute")

st.image(map_image("06_road_network_proximity.png"), use_container_width=True)

card(
    "Method",
    """
    <p>The OpenStreetMap road network within the study bounding box is extracted via
    <code>osmnx.graph_from_bbox(..., network_type='drive')</code>, and OpenStreetMap building
    footprints (3,266 features) via <code>osmnx.features_from_bbox(..., tags={'building': True})</code>.
    Straight-line distance from each terrace <b>polygon</b> — its full boundary, not a reduced
    centroid point — to the nearest road edge and to the nearest building is computed for each
    infrastructure layer independently, then compared between degraded and non-degraded terraces
    using a <b>Mann-Whitney U test</b> — a non-parametric test appropriate here because terrace-to-
    infrastructure distances are non-normally distributed and zero-inflated near dense settlement
    edges (a terrace whose boundary touches or is crossed by a road correctly registers 0 m).</p>
    """,
    badge="Pipeline Stage 4",
)

card(
    "Result — Roads and Settlements",
    f"""
    <p>{d.ROAD_PROXIMITY_FINDING}</p>
    <p>{d.SETTLEMENT_PROXIMITY_FINDING}</p>
    <p>Both results are consistent with an accessibility-driven model of unregulated mining: extraction
    is economically viable where the marginal cost of transporting excavated material to a construction
    or brick-kiln market is lowest, i.e. near existing roads and built-up areas — rather than being
    randomly distributed across the karewa landscape irrespective of infrastructure. That settlement
    proximity is the stronger of the two signals (Section on effect sizes below) is consistent with
    this model, but also with the more basic fact that mining activity tends to be staffed and serviced
    from nearby built-up areas — settlement distance may capture a general human-activity gradient as
    well as a road-specific transport-economics one.</p>
    <p style="color:#9AA5B8; font-size:0.92rem;">Both are correlational results, not causal ones — no
    dated road- or settlement-expansion record was available to establish whether infrastructure was
    built to service pre-existing degradation, or whether access itself enabled the mining that
    followed. Both are consistent with an accessibility-driven model; disentangling them is future
    work.</p>
    """,
    badge="Finding",
)

card(
    "Effect Size and Multiple-Comparison Correction",
    f"""
    <p>Four Mann-Whitney tests are reported across this project against degradation status (settlement
    proximity, road proximity, compactness, slope). Reporting only p-values overstates precision, and
    running four tests without correction inflates the family-wise false-positive rate. Rank-biserial
    effect sizes — settlement proximity r={d.EFFECT_SIZE_SETTLEMENT_R}, compactness
    r={d.EFFECT_SIZE_COMPACTNESS_R}, road proximity r={d.EFFECT_SIZE_ROAD_R}, slope
    r={d.EFFECT_SIZE_SLOPE_R} — show settlement proximity as the strongest effect in the study
    (moderate-to-large), with road proximity and compactness small-to-moderate and slope negligible.
    Applying a Holm-Bonferroni correction across the 4-test family (α=0.05): settlement proximity
    (p=0.0001, adjusted threshold 0.0125), compactness (p=0.0044, adjusted threshold 0.0167), and road
    proximity (p=0.0116, adjusted threshold 0.025) all remain significant; slope was already
    non-significant before correction.</p>
    """,
    badge="Robustness Check",
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
    road- and settlement-proximity and degradation-hotspot layers developed here nonetheless provide an
    evidentiary basis that a future policy-alignment overlay — ideally built in partnership with the
    scheme's implementing agency, which would hold the disaggregated data this comparison needs —
    could build on directly.</p>
    """,
    badge="Governance Question",
)

card(
    "Legal Protection Status",
    f"""
    <p>{d.KAREWA_LEGAL_STATUS_FINDING}</p>
    <p>This reframes how the road- and settlement-proximity results above should be read: they are not
    evidence of enforcement failure against an existing rule, since no rule currently exists to enforce.
    They describe the spatial signature of extraction proceeding in a genuinely unregulated space. That
    changes the policy ask this study supports — from "enforce existing protections more consistently"
    to "establish a protection regime in the first place" — informed by the terrace-level risk map this
    study produces.</p>
    <p style="color:#9AA5B8; font-size:0.92rem;">Reflects the most recent legislative reporting located
    as of this study's research date; legislative status can change and should be independently
    re-checked before being treated as current.</p>
    """,
    badge="Regulatory Context",
)