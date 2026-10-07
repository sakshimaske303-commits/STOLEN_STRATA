"""v2 Phase 2 — (a) threshold sensitivity of the 2013-15 -> 2023-25 conversion, (b) the v1-rule check on the
v1 polygons with Landsat only, (c) year-by-year map of the conversion on terraces 5 and 3.

Run from the repo root:  python v2_redesign/phase2_timeseries/03_sensitivity_and_kiln_map.py
"""
import os
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from rasterio.features import rasterize
from rasterio.windows import from_bounds
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm, LightSource

RAW = "data/raw/StolenStrata_v2_"
P1 = "v2_redesign/phase1_delineation"
OUT = "v2_redesign/phase2_timeseries"
HA = 0.09


def load(name):
    with rasterio.open(RAW + name) as s:
        a = s.read().astype("float32"); a[a == -32768] = np.nan
        return s.transform, s.crs, s.shape, {int(d[-4:]): a[i] / 1e4 for i, d in enumerate(s.descriptions)}


T, crs, shape, OLI = load("OLIonly_p90_2013_2025.tif")
SUM = load("LS_summer_1990_2025.tif")[3]
terr = gpd.read_file(os.path.join(P1, "karewa_terraces_v2.gpkg")).to_crs(crs)
proto = gpd.read_file(os.path.join(P1, "karewa_flat_tops_prototype.gpkg")).to_crs(crs)
tid = rasterize([(g, int(i)) for g, i in zip(terr.geometry, terr.terrace_id)], out_shape=shape, transform=T)
m_terr = tid > 0
m_flat = (rasterize([(g, 1) for g in proto.geometry], out_shape=shape, transform=T) == 1) & ~m_terr
m_rest = ~m_terr & ~m_flat

# ---- (a) sensitivity -------------------------------------------------------------
E, L = (2013, 2014, 2015), (2023, 2024, 2025)
rows = []
for bare in (0.20, 0.25, 0.30):
    for gap in (0.05, 0.10, 0.15, 0.20):
        veg = bare + gap
        for k in (3, 2):                      # all 3 years, or at least 2 of 3
            e = np.sum([OLI[y] >= veg for y in E], 0) >= k
            l = np.sum([OLI[y] < bare for y in L], 0) >= k
            c = e & l
            rows.append(dict(bare_below=bare, veg_at_least=round(veg, 2), years_required=f"{k} of 3",
                             terraces_ha=c[m_terr].sum() * HA, terraces_pct=c[m_terr].mean() * 100,
                             other_flat_pct=c[m_flat].mean() * 100, rest_pct=c[m_rest].mean() * 100,
                             ratio_vs_other_flat=c[m_terr].mean() / max(c[m_flat].mean(), 1e-9),
                             share_on_terraces_5_and_3=np.isin(tid[c & m_terr], (5, 3)).mean()))
sens = pd.DataFrame(rows)
sens.round(3).to_csv(os.path.join(OUT, "conversion_sensitivity.csv"), index=False)

# ---- (b) v1 rule, v1 polygons, Landsat only ----------------------------------------
v1 = gpd.read_file("data/processed/karewa_bare_earth_change.gpkg").to_crs(crs)
m_v1 = rasterize([(g, 1) for g in v1.geometry], out_shape=shape, transform=T) == 1
rows = []
for y, v1val in [(1994, 1.84), (2005, 2.62), (2015, 2.63), (2025, 8.43)]:
    a, b = SUM[y][m_v1], SUM[y][m_terr]
    rows.append(dict(year=y, v1_reported_pct=v1val,
                     landsat_only_v1_polygons_pct=(a[np.isfinite(a)] < 0.15).mean() * 100,
                     landsat_only_v2_terraces_pct=(b[np.isfinite(b)] < 0.15).mean() * 100))
v1chk = pd.DataFrame(rows)
v1chk.round(2).to_csv(os.path.join(OUT, "v1_rule_landsat_only.csv"), index=False)

# ---- (c) year-by-year state on terraces 5 and 3 --------------------------------------
yrs = list(range(2013, 2026))
kiln = np.isin(tid, (5, 3))
state = pd.DataFrame({"year": yrs,
                      "bare_ha_terrace_5": [(OLI[y][tid == 5] < 0.25).sum() * HA for y in yrs],
                      "bare_ha_terrace_3": [(OLI[y][tid == 3] < 0.25).sum() * HA for y in yrs]})
state.round(1).to_csv(os.path.join(OUT, "kiln_terraces_bare_by_year.csv"), index=False)

stack = np.stack([OLI[y] < 0.25 for y in yrs])
stay = np.flip(np.cumprod(np.flip(stack, 0), 0), 0).astype(bool)        # bare from that year to 2025
first = np.where(stay.any(0), np.array(yrs)[stay.argmax(0)], 0)
cls = np.zeros(shape, "uint8")                                           # 1 already bare 2013, 2..5 onset groups
cls[(first == 2013)] = 1
cls[(first >= 2014) & (first <= 2016)] = 2
cls[(first >= 2017) & (first <= 2018)] = 3
cls[(first >= 2019) & (first <= 2021)] = 4
cls[(first >= 2022) & (first <= 2023)] = 5
cls[~kiln] = 0

sub = terr[terr.terrace_id.isin([5, 3])]
x0, y0, x1, y1 = sub.total_bounds
pad = 300
with rasterio.open("data/interim/DEM_buffered_UTM43N.tif") as d:
    w = from_bounds(x0 - pad, y0 - pad, x1 + pad, y1 + pad, d.transform)
    dem = d.read(1, window=w).astype(float); dT = d.window_transform(w)
hs = LightSource(315, 45).hillshade(dem, vert_exag=3, dx=dT.a, dy=dT.a)
r0, c0 = rasterio.transform.rowcol(T, x0 - pad, y1 + pad); r1, c1 = rasterio.transform.rowcol(T, x1 + pad, y0 - pad)
r0, c0 = max(r0, 0), max(c0, 0)
crop = np.ma.masked_equal(cls[r0:r1, c0:c1], 0)
ext_c = (T.c + c0 * 30, T.c + c1 * 30, T.f - r1 * 30, T.f - r0 * 30)
ext_d = (dT.c, dT.c + dem.shape[1] * dT.a, dT.f - dem.shape[0] * dT.a, dT.f)
cols = ["#555555", "#fee08b", "#f46d43", "#a50026", "#542788"]
labels = ["Bare already in 2013", "Bare since 2014–16", "Bare since 2017–18", "Bare since 2019–21", "Bare since 2022–23"]
fig, ax = plt.subplots(figsize=(8.5, 10))
ax.imshow(hs, cmap="gray", extent=ext_d, vmin=0, vmax=1)
ax.imshow(crop, cmap=ListedColormap(cols), norm=BoundaryNorm(np.arange(.5, 6), 5), extent=ext_c, interpolation="nearest")
sub.boundary.plot(ax=ax, color="#00b7ff", lw=1.2)
for _, r in sub.iterrows():
    p = r.geometry.representative_point(); ax.text(p.x, p.y, f"Terrace {r.terrace_id}", color="#00b7ff", fontsize=10, ha="center", weight="bold")
ha_by = [(cls == i).sum() * HA for i in range(1, 6)]
ax.legend(handles=[plt.Rectangle((0, 0), 1, 1, color=c) for c in cols],
          labels=[f"{l} ({h:.0f} ha)" for l, h in zip(labels, ha_by)], loc="lower left", fontsize=8, framealpha=.9)
ax.plot([x1 - 1200, x1 - 200], [y0 - 150, y0 - 150], color="k", lw=3); ax.text(x1 - 700, y0 - 100, "1 km", ha="center", fontsize=8)
ax.set(xlim=(x0 - pad, x1 + pad), ylim=(y0 - pad, y1 + pad), xticks=[], yticks=[],
       title="Terraces 5 and 3: year from which a pixel stays bare (p90 NDVI < 0.25) to 2025\nLandsat 8/9 only, 30 m; backdrop Copernicus DEM hillshade")
plt.tight_layout(); plt.savefig(os.path.join(OUT, "kiln_field_onset_map.png"), dpi=200); plt.close()

pd.set_option("display.width", 250)
print(sens.round(2).to_string(index=False)); print(v1chk.round(2).to_string(index=False)); print(state.round(1).to_string(index=False))
print("onset groups ha:", dict(zip(labels, np.round(ha_by, 1))))
