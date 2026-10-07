import streamlit as st

from lib import GITHUB, caption, note, numbers, stats
from style import GOLD, MUTED, card

n = numbers()

st.markdown(
    f"""
    <div style="text-align:center; padding: 1.2rem 0 0.4rem 0;">
        <div class="ss-badge" style="font-size:0.85rem;">GEOMORPHOLOGY · LANDSAT TIME SERIES · ACCURACY ASSESSMENT</div>
        <div class="ss-hero-title">STOLEN STRATA</div>
        <p style="color:{GOLD} !important; font-family:'Montserrat',sans-serif; font-weight:700; font-size:1.15rem; margin-top:0.2rem;">
            Brick kilns and the loss of karewa tableland in Budgam, Kashmir, 1993–2025<br>with a correction to an earlier estimate
        </p>
        <p style="color:{MUTED} !important; font-size:0.95rem;">Sakshi D. Maske &nbsp;·&nbsp; Independent Geospatial Researcher &nbsp;·&nbsp; revised October 2026</p>
    </div>
    """,
    unsafe_allow_html=True,
)

note(
    "<b>This dashboard replaces the version of September 2026.</b> That version reported a rise in bare ground on karewa terraces "
    "from 1.84% to 8.43%, a net increase of 190.3 ha, 25 degraded terraces and a saffron value at risk of ₹17.8 crore. "
    "Those numbers came from comparing two differently built satellite products and are withdrawn, with everything that was built on them. "
    "The page <i>The Correction</i> shows the check.",
    "withdrawn",
)

stats([("Terraces mapped", f"{n['terraces']}", f"{n['terrace_km2']:.1f} km² of scarp-bounded tableland"),
       ("Strict test, on terraces", f"{n['strict_ha']:.0f} ha", "vegetated in 2013–15, bare in 2023–25"),
       ("Drop test, on terraces", f"{n['drop_ha']:.0f} ha", f"{n['drop_net_ha']:.0f} ha net of change the other way"),
       ("Inside brick-kiln fields", f"≈ {n['kiln_ha']:.0f} ha", f"95% interval {n['kiln_lo']:.0f}–{n['kiln_hi']:.0f} ha")])
st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
caption("Landsat 8/9 only, 30 m pixels, 2013–2015 compared with 2023–2025. The kiln figure comes from a hand-labelled sample of 120 points; "
        f"counting only points that fall directly on kilns or rows of bricks it is about {n['kiln_first_ha']:.0f} ha.")

st.markdown("<br>", unsafe_allow_html=True)

card(
    "The question",
    """
    <p>Karewas are the flat-topped, scarp-bounded tablelands left by the old lake and river deposits of the Kashmir Valley.
    Reporting from Kashmir has said for years that they are being dug away for brick clay and fill. I did not find a study that
    measures how much, where and when from satellite data. This project tries to, and reports only what one family of sensors can show.</p>
    """,
    badge="Research question",
)
card(
    "What the study shows",
    f"""
    <p><b>Conversion is rare and concentrated.</b> Across {n['terrace_km2']:.0f} km² of mapped tableland, {n['strict_ha']:.0f} ha went from clearly
    vegetated to bare between 2013–2015 and 2023–2025 by a strict test, and {n['drop_ha']:.0f} ha by a looser one. Terraces convert several
    times faster than other flat, raised land in every variant tried.</p>
    <p><b>It sits in two brick-kiln belts in Budgam.</b> At Rangeen Kultreh a kiln field opens in 2017–2018 on land that was green in the
    satellite record until 2016. On the Bandagam–Batapora tablelands the low-vegetation land is larger and older.</p>
    <p><b>About {n['kiln_ha']:.0f} ha of the flagged land lies inside brick-kiln fields today</b> ({n['kiln_lo']:.0f}–{n['kiln_hi']:.0f} ha),
    of which about {n['kiln_first_ha']:.0f} ha is directly under kilns and rows of bricks.</p>
    """,
    badge="Findings",
)
card(
    "What it does not show",
    """
    <p>How deep the ground was dug. Any link to the saffron land at Pampore. The whole Karewa formation: the map covers scarp-bounded
    tablelands only. And, at each sample point, what was there in 2013: that check against older imagery is not finished.
    The page <i>What It Cannot Show</i> lists these in full.</p>
    """,
    badge="Limits",
)

st.markdown("---")
st.markdown(
    f"""
    <p style="text-align:center;">
    <a href="{GITHUB}" target="_blank">Code, tables and the labelled sample on GitHub ↗</a></p>
    <p style="text-align:center; color:{MUTED} !important; font-size:0.9rem;">
    The September 2026 preprint (<a href="https://eartharxiv.org/repository/view/14805/" target="_blank">EarthArXiv</a>,
    <a href="https://doi.org/10.5281/zenodo.21766464" target="_blank">Zenodo</a>) is the earlier version with the withdrawn numbers. It has not yet been replaced.</p>
    """,
    unsafe_allow_html=True,
)
