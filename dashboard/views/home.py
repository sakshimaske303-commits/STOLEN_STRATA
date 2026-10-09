import streamlit as st

from lib import GITHUB, caption, note, numbers, stats
from style import GOLD, MUTED, card

n = numbers()

st.markdown(
    f"""
    <div style="text-align:center; padding: 1.2rem 0 0.4rem 0;">
        <div class="ss-badge" style="font-size:0.85rem;">TERRAIN ANALYSIS · LANDSAT TIME SERIES · ACCURACY ASSESSMENT</div>
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
       ("Vegetated then, not now", f"≈ {n['lost_ha']:.0f} ha", f"of the flagged land, 95% interval {n['lost_lo']:.0f}–{n['lost_hi']:.0f} ha"),
       ("Inside brick-kiln fields", f"≈ {n['kiln_ha']:.0f} ha", f"95% interval {n['kiln_lo']:.0f}–{n['kiln_hi']:.0f} ha")])
st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
caption("Landsat 8/9 only, 30 m pixels, 2013–2015 compared with 2023–2025. The last two figures come from two hand-labelled samples, 240 points in all. "
        f"The kiln figure depends on how the edges of kiln fields are counted: the first sample gives about {n['kiln_draw1_ha']:.0f} ha and the second "
        f"about {n['kiln_draw2_ha']:.0f} ha. Counting only points that imagery of 2013–2015 also shows as vegetated it is about {n['kiln_before_ha']:.0f} ha.")

st.markdown("<br>", unsafe_allow_html=True)

card(
    "The question",
    """
    <p>Karewas are the flat-topped, scarp-bounded tablelands left by the old lake and river deposits of the Kashmir Valley.
    Reporting from Kashmir has said for years that they are being dug away for brick clay and fill. Using one family of sensors at a time, this project asks:</p>
    <ol><li>How much tableland that was vegetated in 2013–2015 was no longer vegetated in 2023–2025, and does it convert faster than comparable land?</li>
    <li>What did that land become, and how much of it now lies inside brick-kiln fields?</li>
    <li>Where and when did the change happen?</li></ol>
    """,
    badge="Research question",
)
card(
    "What the study shows",
    f"""
    <p><b>Conversion is rare and concentrated.</b> Across {n['terrace_km2']:.0f} km² of mapped tableland, {n['strict_ha']:.0f} ha went from clearly
    vegetated to bare between 2013–2015 and 2023–2025 by a strict test, and {n['drop_ha']:.0f} ha by a looser one. Taken as a whole, terraces convert
    several times faster than other flat, raised land, but only because of two belts: outside them, and compared polygon by polygon,
    terraces convert at the same rate as comparable land.</p>
    <p><b>It sits in two brick-kiln belts in Budgam.</b> At Rangeen Kultreh a kiln field opens in 2017–2018 on land that was green in the
    satellite record until 2016. On the Bandagam–Batapora tablelands low-vegetation land is older, and the looser test finds the largest
    post-2013 loss there.</p>
    <p><b>About {n['notveg_ha']:.0f} ha of the 331 ha flagged is not vegetated today, and about {n['lost_ha']:.0f} ha of it was vegetated in imagery of 2013–2015.</b>
    About {n['kiln_ha']:.0f} ha lies inside brick-kiln fields ({n['kiln_lo']:.0f}–{n['kiln_hi']:.0f} ha), but the two samples give {n['kiln_draw1_ha']:.0f} and
    {n['kiln_draw2_ha']:.0f} ha depending on how the edges of kiln fields are counted, so the kiln share is less certain than the loss itself.</p>
    """,
    badge="Findings",
)
card(
    "What it does not show",
    """
    <p>How deep the ground was dug. Any link to the saffron land at Pampore. The whole Karewa formation: the map covers scarp-bounded
    tablelands only. And a blind check of the past: older imagery was looked at only for points already flagged.
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
