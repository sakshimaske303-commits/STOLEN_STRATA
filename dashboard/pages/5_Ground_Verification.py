import streamlit as st
import os
from style import inject_css, card, page_title, GOLD

st.set_page_config(page_title="GROUND VERIFICATION | Stolen Strata", page_icon="🧭", layout="wide")
inject_css()

page_title("🧭 GROUND VERIFICATION", "Field-checking the pipeline against the Lethpora saffron belt")

card(
    "Why Check the Ground at All",
    """
    <p>Every finding in this project so far comes from satellite data, run through an algorithmic
    pipeline. In keeping with this portfolio's "Trust, But Verify" approach, that pipeline is worth
    checking against something physical wherever possible — not as a replacement for the systematic
    accuracy-assessment sample already built into the methodology
    (<code>outputs/ground_truth_sample_points.gpkg</code>), but as an independent, on-the-ground
    look at the same belt used in the <b>Validation at Saffron Fields, Lethpora</b> interactive map
    (see Interactive Maps).</p>
    """,
    badge="Field Check",
)

c1, c2, c3 = st.columns(3)
c1.metric("Photos Captured", "4")
c2.metric("Location", "Lethpora, Pulwama")
c3.metric("Coordinate Cluster", "33.97°N, 74.95°E")

st.markdown("## Field Photographs")
st.markdown(
    "Four GPS-tagged photographs, captured 3 September 2026 directly on the karewa terraces this "
    "study delineates, within the same saffron belt as the Lethpora validation map."
)

GT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "outputs", "ground_truth_photos")
gt_photos = [
    ("lethpora_groundtruth_01.jpg", "33.97373°N, 74.951189°E — 3 Sep 2026, 7:00 PM"),
    ("lethpora_groundtruth_02.jpg", "33.973596°N, 74.951186°E — 3 Sep 2026, 6:59 PM"),
    ("lethpora_groundtruth_03.jpg", "33.973788°N, 74.951186°E — 3 Sep 2026, 7:00 PM"),
    ("lethpora_groundtruth_04.jpg", "33.973365°N, 74.950956°E — 3 Sep 2026, 6:58 PM"),
]
gt_cols = st.columns(4)
for gt_col, (fname, caption) in zip(gt_cols, gt_photos):
    with gt_col:
        fpath = os.path.join(GT_DIR, fname)
        if os.path.exists(fpath):
            st.image(fpath, caption=caption, use_container_width=True)
        else:
            st.caption(f"Photo not added yet — save it as `outputs/ground_truth_photos/{fname}`.")

card(
    "Reading These Photos Honestly",
    """
    <p><i>Crocus sativus</i> flowers for only a 2–3 week window in October–November, so these
    pre-flowering photos show freshly tilled, dormant terrace soil rather than visible crop —
    exactly what a cultivated saffron plot looks like at this point in the season, not an absence
    of one. A return visit is planned for peak bloom in October 2026 to complete this as a
    before/after pair on the same coordinates.</p>
    <p style="color:#9AA5B8; font-size:0.92rem;">Worth flagging explicitly: this bare, tilled
    appearance is agricultural dormancy on an active saffron field, not the bare-earth signature
    this study's own degradation classifier looks for (Methodology &amp; Data, Stage 3) — that
    classifier is built on a <i>persistent</i> multi-year bare-earth increase, not a single seasonal
    snapshot, so a pre-flowering photo like this one is not itself evidence of degradation.</p>
    """,
    badge="Interpretation",
)

st.markdown("---")
st.markdown(
    f"<p style='text-align:center; color:#8A94AD; font-size:0.9rem;'>STOLEN STRATA — Ground Verification, Lethpora Saffron Belt</p>",
    unsafe_allow_html=True,
)
