"""v2 extended box — terraces and the vegetated -> persistently bare test on 74.55–75.15 E, 33.80–34.15 N.

Same rules as the original box: terraces = flat tops with scarp share >= 0.25 (Phase 1), conversion = yearly p90 NDVI
>= 0.35 in all of 2013-15 and < 0.25 in all of 2023-25, Landsat 8/9 only (Phase 2).
Also: the same test inside the Landsat 5/7 era (1993/94/98 -> 2005/06/07) and the stock of persistently bare land.

I run it from the repo root, after 01_flat_top_delineation_wide.py:
    python v2_redesign/west_extension/02_conversion_wide_box.py
"""
import os
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from rasterio.features import rasterize, shapes
from rasterio.transform import xy
from rasterio.warp import transform as warp_xy, reproject, Resampling
from scipy import ndimage as ndi
from shapely.geometry import box
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource

RAW = "data/raw/StolenStrata_v2w_"
OUT = "v2_redesign/west_extension"
P1 = "v2_redesign/phase1_delineation"
AOI = (74.55, 33.80, 75.15, 34.15)
OLD = (74.75, 33.85, 75.15, 34.15)
SCARP_MIN, BARE, VEG, HA = 0.25, 0.25, 0.35, 0.09
MIN_OBS = 10


def load(name, scale=1e4):
    with rasterio.open(RAW + name) as s:
        a = s.read().astype("float32"); a[a == -32768] = np.nan
        return s.transform, s.crs, s.shape, {int(d[-4:]): a[i] / scale for i, d in enumerate(s.descriptions)}


T, crs, shape, OLI = load("OLIonly_p90_2013_2025.tif")
L7 = load("L7only_p90_2013_2021.tif")[3]
S2 = load("S2_p90_2019_2025.tif")[3]
LSA = load("LS_p90_1990_2007.tif")[3]
CNT = load("LS_counts_1990_2025.tif", 1)[3]

# ---- terraces --------------------------------------------------------------------------
proto = gpd.read_file(os.path.join(OUT, "karewa_flat_tops_wide.gpkg")).to_crs(crs)
aoi = gpd.GeoSeries([box(*AOI)], crs=4326).to_crs(crs).iloc[0]
old = gpd.GeoSeries([box(*OLD)], crs=4326).to_crs(crs).iloc[0]
keep = proto[proto.scarp_frac >= SCARP_MIN].copy()
# the 5 polygons removed by hand in the original box stay removed (matched by overlap)
old_proto = gpd.read_file(os.path.join(P1, "karewa_flat_tops_prototype.gpkg")).to_crs(crs)
excl_ids = pd.read_csv(os.path.join(P1, "excluded_by_review.csv")).iloc[:, 0].tolist()
excl = old_proto[old_proto.terrace_id.isin(excl_ids)].union_all()
keep = keep[keep.intersection(excl).area / keep.area < 0.5].copy()
keep["geometry"] = keep.intersection(aoi)
keep = keep[~keep.is_empty].copy()
keep["area_km2"] = keep.area / 1e6
keep = keep[keep.area_km2 >= 0.05].sort_values("area_km2", ascending=False).reset_index(drop=True)
keep["terrace_id"] = range(1, len(keep) + 1)
keep["in_old_box_share"] = keep.intersection(old).area / keep.area
keep[["terrace_id", "area_km2", "scarp_frac", "mean_elev", "mean_hand", "mean_slope", "in_old_box_share", "geometry"]].to_file(
    os.path.join(OUT, "karewa_terraces_wide.gpkg"), driver="GPKG")

tid = rasterize([(g, int(i)) for g, i in zip(keep.geometry, keep.terrace_id)], out_shape=shape, transform=T)
m_terr = tid > 0
m_flat = (rasterize([(g, 1) for g in proto.geometry], out_shape=shape, transform=T) == 1) & ~m_terr
m_old = rasterize([(old, 1)], out_shape=shape, transform=T) == 1
STRATA = {"terraces": m_terr, "other_flat": m_flat, "rest": ~m_terr & ~m_flat}


def windows(D, early, late):
    return (np.all([D[y] >= VEG for y in early], 0) & np.all([D[y] < BARE for y in late], 0),
            np.all([D[y] < BARE for y in early], 0) & np.all([D[y] >= VEG for y in late], 0))


# ---- conversion by stratum and half of the box ----------------------------------------------
TESTS = [("Landsat 8/9 only", OLI, (2013, 2014, 2015), (2023, 2024, 2025)),
         ("Landsat 8/9 only", OLI, (2013, 2014, 2015), (2019, 2020, 2021)),
         ("Landsat 7 only", L7, (2013, 2014, 2015), (2019, 2020, 2021)),
         ("Landsat 5/7", LSA, (1993, 1994, 1998), (2005, 2006, 2007))]
rows = []
for name, D, e, l in TESTS:
    c, rev = windows(D, e, l)
    for part, pm in (("whole box", np.ones(shape, bool)), ("old box", m_old), ("west/south extension", ~m_old)):
        for sname, mk in STRATA.items():
            mk = mk & pm
            rows.append(dict(series=name, early="-".join(map(str, e)), late="-".join(map(str, l)), part=part, stratum=sname,
                             stratum_km2=mk.sum() * HA / 100, veg_to_bare_ha=c[mk].sum() * HA,
                             veg_to_bare_pct=c[mk].mean() * 100, bare_to_veg_ha=rev[mk].sum() * HA))
conv_tab = pd.DataFrame(rows)
conv_tab.round(3).to_csv(os.path.join(OUT, "conversion_by_stratum_wide.csv"), index=False)

conv = windows(OLI, (2013, 2014, 2015), (2023, 2024, 2025))[0]
c_terr = conv & m_terr
s2_agree = float(np.all([S2[y] < BARE for y in (2023, 2024, 2025)], 0)[c_terr].mean())

# ---- per terrace ----------------------------------------------------------------------------------
per = pd.Series(tid[c_terr]).value_counts().mul(HA).rename("veg_to_bare_ha").rename_axis("terrace_id").reset_index()
per = keep[["terrace_id", "area_km2", "scarp_frac", "in_old_box_share"]].merge(per, how="left").fillna({"veg_to_bare_ha": 0})
per["veg_to_bare_pct"] = per.veg_to_bare_ha / per.area_km2
pts = keep.representative_point().to_crs(4326)
per["lat"], per["lon"] = pts.y.round(4).values, pts.x.round(4).values
per = per.sort_values("veg_to_bare_ha", ascending=False)
per.round(3).to_csv(os.path.join(OUT, "conversion_by_terrace_wide.csv"), index=False)

# ---- clusters anywhere in the box ---------------------------------------------------------------------
grp, n = ndi.label(ndi.binary_dilation(conv, iterations=3)); grp = np.where(conv, grp, 0)
ha = ndi.sum(conv, grp, np.arange(1, n + 1)) * HA
rows = []
for i in np.nonzero(ha >= 2)[0]:
    m = grp == i + 1
    r, c = np.nonzero(m); x, y = xy(T, r.mean(), c.mean()); lon, lat = warp_xy(crs, "EPSG:4326", [x], [y])
    rows.append(dict(converted_ha=m.sum() * HA, lat=round(lat[0], 4), lon=round(lon[0], 4), on_terrace=float(m_terr[m].mean()),
                     on_other_flat=float(m_flat[m].mean()), in_old_box=bool(m_old[m].mean() > 0.5),
                     google_maps=f"https://www.google.com/maps/@{lat[0]:.5f},{lon[0]:.5f},16z/data=!3m1!1e3"))
cl = pd.DataFrame(rows).sort_values("converted_ha", ascending=False).reset_index(drop=True)
cl.insert(0, "cluster", cl.index + 1)
cl.round(2).to_csv(os.path.join(OUT, "conversion_clusters_wide.csv"), index=False)

# ---- stock of persistently bare land, and Landsat 5/7 observation counts ----------------------------------
rows = []
for name, D, yrs in [("Landsat 5/7", LSA, (1993, 1994, 1998)), ("Landsat 5/7", LSA, (2005, 2006, 2007)),
                     ("Landsat 8/9 only", OLI, (2013, 2014, 2015)), ("Landsat 8/9 only", OLI, (2023, 2024, 2025)),
                     ("Sentinel-2", S2, (2023, 2024, 2025))]:
    b = np.all([D[y] < BARE for y in yrs], 0)
    for part, pm in (("old box", m_old), ("west/south extension", ~m_old)):
        rows.append(dict(series=name, years="-".join(map(str, yrs)), part=part,
                         terraces_ha=b[m_terr & pm].sum() * HA, terraces_pct=b[m_terr & pm].mean() * 100,
                         other_flat_pct=b[m_flat & pm].mean() * 100, rest_pct=b[~m_terr & ~m_flat & pm].mean() * 100))
stock = pd.DataFrame(rows)
stock.round(3).to_csv(os.path.join(OUT, "persistent_bare_stock_wide.csv"), index=False)
obs = pd.DataFrame({"year": range(1990, 2026), "median_clear_obs_terraces": [float(np.median(CNT[y][m_terr])) for y in range(1990, 2026)]})
obs["usable"] = obs.median_clear_obs_terraces >= MIN_OBS
obs.to_csv(os.path.join(OUT, "landsat_observation_counts_wide.csv"), index=False)

# ---- map -----------------------------------------------------------------------------------------------------
with rasterio.open("data/interim/DEM_wide_buffered_UTM43N.tif") as d:
    dem = np.full(shape, np.nan, "float32")
    reproject(rasterio.band(d, 1), dem, dst_transform=T, dst_crs=crs, resampling=Resampling.bilinear, dst_nodata=np.nan)
ext = (T.c, T.c + shape[1] * 30, T.f - shape[0] * 30, T.f)
fig, ax = plt.subplots(figsize=(14, 9.5))
ax.imshow(LightSource(315, 45).hillshade(np.nan_to_num(dem, nan=np.nanmean(dem)), vert_exag=2, dx=30, dy=30), cmap="gray", extent=ext)
keep.boundary.plot(ax=ax, color="#00b7ff", lw=.6)
gpd.GeoSeries([old]).boundary.plot(ax=ax, color="#ffd400", lw=1.2, ls="--")
ax.imshow(np.ma.masked_where(~ndi.binary_dilation(conv, iterations=2), np.ones(shape)), cmap="autumn", vmin=1, vmax=3, extent=ext, interpolation="nearest")
for _, r in cl.head(10).iterrows():
    x, y = warp_xy("EPSG:4326", crs, [r.lon], [r.lat])
    ax.annotate(f"{int(r.cluster)}: {r.converted_ha:.0f} ha", (x[0], y[0]), xytext=(8, 8), textcoords="offset points", fontsize=8,
                bbox=dict(boxstyle="round,pad=.2", fc="w", ec="none", alpha=.85))
ax.set(xlim=ext[:2], ylim=ext[2:], xticks=[], yticks=[],
       title="Extended box: vegetated in 2013–15, persistently bare in 2023–25 (red, drawn enlarged; Landsat 8/9 only)\n"
             "Blue = terraces (scarp share ≥ 0.25); yellow dashes = original box")
plt.tight_layout(); plt.savefig(os.path.join(OUT, "conversion_wide_box_map.png"), dpi=160); plt.close()

pd.set_option("display.width", 250)
print("terraces:", len(keep), "| km2 %.1f | in old box km2 %.1f | in extension km2 %.1f" % (
    keep.area_km2.sum(), (keep.area_km2 * keep.in_old_box_share).sum(), (keep.area_km2 * (1 - keep.in_old_box_share)).sum()))
print(conv_tab.round(2).to_string(index=False))
print("Sentinel-2 agrees on %.1f%% of converted terrace pixels" % (s2_agree * 100))
print(per.head(12).round(2).to_string(index=False))
print("terraces with >= 1 ha converted:", int((per.veg_to_bare_ha >= 1).sum()), "of", len(per))
print(cl.drop(columns="google_maps").head(20).to_string(index=False))
print(stock.round(2).to_string(index=False))
print("unusable years:", obs[~obs.usable].year.tolist())
