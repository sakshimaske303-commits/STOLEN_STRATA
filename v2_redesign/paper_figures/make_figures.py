"""Figures 2 and 4 of the revised paper, drawn from the result tables.
I run it from the repo root:  python v2_redesign/paper_figures/make_figures.py
"""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = "v2_redesign/paper_figures/"
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})

# Figure 2: the earlier estimate against the same rule and the same statistic on one sensor family
v = pd.read_csv("v2_redesign/phase2_timeseries/v1_rule_matched_statistic.csv")
fig, ax = plt.subplots(figsize=(6.4, 3.9))
x = range(len(v)); w = 0.38
b1 = ax.bar([i - w / 2 for i in x], v.earlier_reported_mean_of_polygons_pct, w, color="#b2182b", label="Earlier estimate (Landsat to 2015, Sentinel-2 in 2025)")
b2 = ax.bar([i + w / 2 for i in x], v.landsat_only_mean_of_polygons_pct, w, color="#4d4d4d", label="Same polygons, rule and statistic, Landsat only")
for bars in (b1, b2):
    for r in bars:
        ax.text(r.get_x() + r.get_width() / 2, r.get_height() + 0.12, f"{r.get_height():.2f}", ha="center", fontsize=8.5)
ax.set_xticks(list(x)); ax.set_xticklabels(v.year.astype(str)); ax.set_ylabel("Bare-earth share, mean of 201 polygons (%)")
ax.set_ylim(0, 9.8); ax.legend(frameon=False, fontsize=8.5, loc="upper left"); ax.grid(axis="y", alpha=.25)
plt.tight_layout(); plt.savefig(OUT + "Figure_2_earlier_estimate_vs_landsat_only.png", dpi=300); plt.close()

# Figure 4: terrace land that never greens up, by site and period, on a true time axis
s = pd.read_csv("v2_redesign/west_extension/long_series_low_ndvi_stock.csv")
order = ["1993-1998", "1999-2002", "2003-2007", "2008-2012", "2013-2015", "2018-2020", "2023-2025"]
YEARS = {"1993-1998": (1993, 1994, 1998), "1999-2002": (1999, 2000, 2002), "2003-2007": (2003, 2005, 2007), "2008-2012": (2008, 2010, 2012),
         "2013-2015": (2013, 2014, 2015), "2018-2020": (2018, 2019, 2020), "2023-2025": (2023, 2024, 2025)}   # as in 08_long_series_wide.py
mid = [sum(YEARS[k]) / 3 for k in order]
sites = [("Bandagam-Batapora terraces", "Bandagam–Batapora terraces", "#b2182b", "o"),
         ("Rangeen Kultreh terraces", "Rangeen Kultreh terraces", "#ef8a62", "s"),
         ("other terraces", "All other terraces", "#4d4d4d", "^"), ("other flat land", "Other flat, raised land", "#999999", "D")]
fig, ax = plt.subplots(figsize=(7.4, 4.0))
ax.axvspan(2012.5, 2026, color="#f0f0f0", zorder=0)
ax.axvline(2013, color="#777777", lw=0.8, ls="--", zorder=1)
ax.text(2013.3, 0.97, "Landsat 8 from 2013:\npeak NDVI steps up", transform=ax.get_xaxis_transform(), va="top", fontsize=7.5, color="#555555")
for key, lab, col, mk in sites:
    d = s[s.site == key].set_index("period").loc[order]
    ax.plot(mid, d.below_035_pct, marker=mk, color=col, lw=1.6, ms=5, label=lab, zorder=3)
    ax.annotate(f"{d.below_035_pct.iloc[-1]:.1f}%", (mid[-1], d.below_035_pct.iloc[-1]), xytext=(6, 3 if key == "other flat land" else -8 if key == "other terraces" else -3), textcoords="offset points", fontsize=8.5, color=col)
ax.set_ylabel("Land with yearly peak NDVI < 0.35 (%)"); ax.set_xlabel("Year (each point: median of three usable years, plotted at their mean)")
ax.set_xlim(1991.5, 2027.5); ax.legend(frameon=False, fontsize=8.5, loc="upper left"); ax.grid(axis="y", alpha=.25)
plt.tight_layout(); plt.savefig(OUT + "Figure_4_low_ndvi_share_by_site.png", dpi=300); plt.close()
print("ok")
