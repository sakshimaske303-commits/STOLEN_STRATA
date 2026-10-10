"""lib.py: shared paths, loaders and chart helpers for the dashboard.

Numbers shown on the pages are read from the result tables in v2_redesign/ (written by the analysis scripts)
or from dashboard/map_data/ (written by dashboard/build_data.py). The few exceptions are agreement figures that the
scripts only print; those are quoted from the paper.
"""
import json
import os

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from style import BG_PANEL, CREAM, MUTED

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
V2 = os.path.join(ROOT, "v2_redesign")
MAPDATA = os.path.join(HERE, "map_data")

# chart colours (checked for colour-blind separation on the dark background)
ORANGE = "#DD6B33"   # strict test, kiln ground
TEAL = "#1FA89C"     # terraces, Landsat-only
OCHRE = "#B38F1B"    # drop test
ROSE = "#C2456B"     # the earlier, withdrawn estimate
GREY = "#9AA5B8"     # comparison land, context

GITHUB = "https://github.com/sakshimaske303-commits/STOLEN_STRATA"


def table(rel):
    """A result table from v2_redesign/, e.g. table('west_extension/accuracy_result.csv')."""
    path = os.path.join(V2, rel)
    return _table(path, os.path.getmtime(path))


@st.cache_data
def _table(path, mtime):
    return pd.read_csv(path)


def mapfile(name):
    """A file from dashboard/map_data/. The file's modification time is part of the cache key, so a new file is read
    again after a redeploy instead of an older cached copy being served."""
    path = os.path.join(MAPDATA, name)
    return _mapfile(path, os.path.getmtime(path))


@st.cache_data
def _mapfile(path, mtime):
    name = path
    if name.endswith(".csv"):
        return pd.read_csv(path)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


@st.cache_data
def numbers():
    """The handful of figures that several pages quote."""
    cs = table("west_extension/conversion_by_stratum_wide.csv")
    cs = cs[(cs.series == "Landsat 8/9 only") & (cs.early == "2013-2014-2015") & (cs.late == "2023-2024-2025") & (cs.part == "whole box")].set_index("stratum")
    dt = table("west_extension/drop_test_by_stratum_wide.csv")
    dt = dt[dt.test == "OLI 13-15>23-25"].groupby("stratum")[["drop_ha", "reverse_ha", "net_ha"]].sum()
    ap = table("west_extension/accuracy_by_labelling_pass.csv")
    ap = ap[ap.stratum != "C_not_flagged"].groupby("definition").est_ha.sum()
    pa = table("west_extension/pooled_accuracy_result.csv")
    pa = pa[pa.stratum == "A_and_B"].set_index(["sample", "measure"])
    pb = table("west_extension/pooled_before_result.csv")
    pb = pb[pb.stratum == "A_and_B"].set_index(["sample", "measure"])
    k, kb = pa.loc[("pooled", "kiln")], pb.loc[("pooled", "vegetated before and inside a kiln field today")]
    nv, gn = pa.loc[("pooled", "not vegetated")], pb.loc[("pooled", "vegetated before and not vegetated today")]
    return dict(
        terraces=int(table("west_extension/conversion_by_terrace_wide.csv").shape[0]),
        terrace_km2=float(cs.loc["terraces", "stratum_km2"]), flat_km2=float(cs.loc["other_flat", "stratum_km2"]),
        strict_ha=float(cs.loc["terraces", "veg_to_bare_ha"]), strict_rev_ha=float(cs.loc["terraces", "bare_to_veg_ha"]),
        strict_pct=float(cs.loc["terraces", "veg_to_bare_pct"]), strict_pct_flat=float(cs.loc["other_flat", "veg_to_bare_pct"]),
        drop_ha=float(dt.loc["terraces", "drop_ha"]), drop_rev_ha=float(dt.loc["terraces", "reverse_ha"]), drop_net_ha=float(dt.loc["terraces", "net_ha"]),
        kiln_ha=float(k.est_ha), kiln_lo=float(k.est_ha_low), kiln_hi=float(k.est_ha_high),
        kiln_draw1_ha=float(pa.loc[("draw 1", "kiln")].est_ha), kiln_draw2_ha=float(pa.loc[("draw 2", "kiln")].est_ha),
        notveg_ha=float(nv.est_ha), notveg_lo=float(nv.est_ha_low), notveg_hi=float(nv.est_ha_high),
        lost_ha=float(gn.est_ha), lost_lo=float(gn.est_ha_low), lost_hi=float(gn.est_ha_high),
        kiln_first_ha=float(ap[[i for i in ap.index if i.startswith("first pass")][0]]),
        kiln_second_ha=float(ap[[i for i in ap.index if i.startswith("added by second")][0]]),
        kiln_before_ha=float(kb.est_ha), kiln_before_lo=float(kb.est_ha_low), kiln_before_hi=float(kb.est_ha_high),
    )


def style_fig(fig, height=420, legend_top=True):
    fig.update_layout(
        height=height, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor=BG_PANEL, font=dict(color=CREAM, family="Inter, sans-serif", size=14),
        margin=dict(l=10, r=10, t=50 if legend_top else 20, b=10), hoverlabel=dict(bgcolor="#1A2236", font_color=CREAM),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0, font=dict(color=CREAM)) if legend_top else dict(font=dict(color=CREAM)),
    )
    fig.update_xaxes(gridcolor="rgba(154,165,184,0.12)", zeroline=False, linecolor="rgba(154,165,184,0.4)", tickfont=dict(color=CREAM), title_font=dict(color=MUTED))
    fig.update_yaxes(gridcolor="rgba(154,165,184,0.18)", zeroline=False, linecolor="rgba(154,165,184,0.4)", tickfont=dict(color=CREAM), title_font=dict(color=MUTED))
    return fig


def show(fig, **kw):
    cfg = {"displayModeBar": False}
    try:
        st.plotly_chart(fig, width="stretch", config=cfg, **kw)
    except TypeError:  # older Streamlit
        st.plotly_chart(fig, use_container_width=True, config=cfg, **kw)


def frame(df, **kw):
    try:
        st.dataframe(df, width="stretch", hide_index=True, **kw)
    except TypeError:
        st.dataframe(df, use_container_width=True, hide_index=True, **kw)


def picture(path, caption=None):
    try:
        st.image(path, caption=caption, width="stretch")
    except TypeError:
        st.image(path, caption=caption, use_container_width=True)


def note(html, kind="note"):
    """A plain framed paragraph. kind: note | caution | withdrawn."""
    edge = {"note": TEAL, "caution": OCHRE, "withdrawn": ROSE}[kind]
    st.markdown(f'<div class="ss-card" style="border-left-color:{edge};"><div style="margin:0;">{html}</div></div>', unsafe_allow_html=True)


def caption(text):
    st.markdown(f'<p style="color:{MUTED} !important; font-size:0.92rem; margin-top:-0.4rem;">{text}</p>', unsafe_allow_html=True)


def bars(x, y, color, text=None, name=None):
    return go.Bar(x=x, y=y, marker=dict(color=color, line=dict(color="#0A0E1A", width=2)), text=text, textposition="outside",
                  textfont=dict(color=CREAM), name=name, cliponaxis=False)


def stats(items):
    """A row of figure tiles: items = [(label, value, small line under it), ...]."""
    from style import BG_CARD, GOLD, MAROON
    for col, (label, value, sub) in zip(st.columns(len(items)), items):
        col.markdown(
            f'<div style="background:{BG_CARD}; border:1px solid {MAROON}; border-radius:10px; padding:0.9rem 1rem; height:100%; box-shadow:0 0 14px rgba(139,30,63,0.25);">'
            f'<div style="color:{MUTED}; font-size:0.78rem; font-weight:600; letter-spacing:0.6px; text-transform:uppercase;">{label}</div>'
            f'<div style="color:{GOLD}; font-family:Montserrat,sans-serif; font-weight:900; font-size:1.9rem; line-height:1.25;">{value}</div>'
            f'<div style="color:{CREAM}; font-size:0.86rem; line-height:1.35;">{sub}</div></div>',
            unsafe_allow_html=True)
