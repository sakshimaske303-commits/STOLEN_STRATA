import streamlit as st
import os
from style import inject_css, card, GOLD, MAROON, BG_CARD, BG_PANEL, CREAM, MUTED

st.set_page_config(page_title="Quaternary Geomorphology — STOLEN STRATA", page_icon="🏔️", layout="wide")
inject_css()

st.markdown(
    f"""
    <div style="text-align:center; padding: 1rem 0 0.4rem 0;">
        <div class="ss-hero-title" style="font-size:2.2rem;">READING THE KAREWAS</div>
        <p style="color:{GOLD}; font-family:'Montserrat',sans-serif; font-weight:700; font-size:1.1rem; margin-top:0.2rem;">
            The Quaternary Geomorphology and Paleoclimatology Behind Stolen Strata's Evidence
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown("---")

# ============================================================
# DIAGRAM
# ============================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # .../dashboard
ROOT_DIR = os.path.dirname(BASE_DIR)                                     # repo root
IMG_PATH = os.path.join(ROOT_DIR, "outputs", "figures", "imgg1.png")

col_a, col_b, col_c = st.columns([0.2, 5.9, 0.2])
with col_b:
    if os.path.exists(IMG_PATH):
        st.image(IMG_PATH, use_container_width=True)
    else:
        st.warning("Diagram not found at outputs/figures/imgg1.png")
    st.markdown(
        f"<p style='text-align:center; color:{MUTED}; font-size:0.85rem; margin-top:6px;'>"
        "AI was used to help generate this image, but the concept and every detail in it are mine.</p>",
        unsafe_allow_html=True,
    )

st.markdown("---")

# ============================================================
# THREE CARDS — matching the app.py stacked-card pattern
# ============================================================
card(
    "How an Ice-Age Lake Became a Farmland Terrace",
    f"""
    <p>The karewas began as an ancient <b>intermontane lake</b> that filled the Kashmir Valley
    during parts of the Pleistocene, accumulating thick, flat-lying layers of lacustrine and
    glacio-fluvial sediment on its floor. Later <b>tectonic uplift</b> of the valley, combined
    with progressive incision by the Jhelum River and its tributaries, drained the lake and cut
    into those soft sediments — leaving behind the flat-topped, steep-sided terrace landform
    seen across the valley today. The loess capping many terraces is itself geomorphically
    significant: wind-blown silt deposited during colder, drier glacial phases, whose fine,
    well-drained texture is exactly what makes karewa soil so suited to saffron cultivation.</p>
    """,
    badge="Landform Genesis",
)

card(
    "A Climate Record Written in the Strata Themselves",
    f"""
    <p>The layered sediment sequence inside each karewa is not just a foundation for cultivation —
    it is a physical <b>paleoclimate archive</b>. Alternating lacustrine and glacio-fluvial layers
    record successive glacial–interglacial cycles as the ice margins in the surrounding mountains
    advanced and retreated, changing how much and what kind of sediment reached the lake floor in
    each phase. This is the same principle behind loess–paleosol sequences used elsewhere in
    Quaternary science to reconstruct past climate — which is what makes the karewas a landform of
    genuine scientific value, independent of the agricultural economy built on top of them.</p>
    """,
    badge="Paleoclimatology",
)

card(
    "Why This Loss Cannot Be Undone",
    f"""
    <p>This is the piece of theory that gives Stolen Strata's headline number its weight: the
    lake that built the karewas is gone, and the tectonic and fluvial conditions that formed
    these terraces operated over millennia and are not active today in any way that could rebuild
    a mined terrace. A karewa is a <b>relict landform</b> — once its strata are stripped by
    unregulated mining, both the saffron-suitable soil <em>and</em> the paleoclimate record inside
    it are lost permanently, not on a renewable or recoverable timescale. That is what makes this
    project's central measurement — hectares of terrace converted to bare earth — a record of
    genuinely irreversible geomorphic and scientific loss, not a routine land-use change.</p>
    """,
    badge="Why It Matters",
)

st.markdown("---")
st.markdown(
    f"<p style='text-align:center; color:{MUTED}; font-size:0.9rem;'>STOLEN STRATA — The Deep-Time Landform Behind the Headline Number</p>",
    unsafe_allow_html=True,
)
