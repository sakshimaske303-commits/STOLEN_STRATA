"""v2 Phase 2 — Landsat-only bare-surface time series on the v2 karewa terraces.

Inputs (data/raw/, exported by gee_01_annual_composites.js and gee_02_summer_counts.js):
  StolenStrata_v2_LS_p90_1990_2025.tif      yearly 90th-percentile NDVI, Landsat 5/7/8/9 (8/9 adjusted to ETM+)
  StolenStrata_v2_LS_summer_1990_2025.tif   June-September median NDVI (the v1-style measure)
  StolenStrata_v2_LS_counts_1990_2025.tif   clear observations per pixel per year
  StolenStrata_v2_L7only_p90_2013_2021.tif  Landsat 7 only
  StolenStrata_v2_OLIonly_p90_2013_2025.tif Landsat 8/9 only, not adjusted
  StolenStrata_v2_S2_p90_2019_2025.tif      Sentinel-2 only

Three strata are compared:  terraces (the 57 v2 polygons), other_flat (flat, elevated land the
Phase 1 rule rejected: fans / valley fill), rest (everything else in the study box).

"Bare" = yearly p90 NDVI < BARE. "Converted" = p90 >= VEG in all three early years AND < BARE in
all three late years, so one cloudy or dry year cannot create or remove a conversion.

Run from the repo root:  python v2_redesign/phase2_timeseries/02_persistent_bare_analysis.py
"""
import os
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from rasterio.features import rasterize, shapes
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RAW = "data/raw/StolenStrata_v2_"
P1 = "v2_redesign/phase1_delineation"
OUT = "v2_redesign/phase2_timeseries"
BARE, VEG = 0.25, 0.35
V1_SUMMER_BARE = 0.15            # the v1 threshold on summer NDVI
MIN_OBS = 10                     # a year needs this many clear observations (terrace median) to be used
HA = 0.09                        # one 30 m pixel


def load(name, scale=1e4):
    with rasterio.open(RAW + name) as s:
        a = s.read().astype("float32")
        a[a == -32768] = np.nan
        return s.transform, s.crs, s.shape, {d: a[i] / scale for i, d in enumerate(s.descriptions)}


T, crs, shape, P90 = load("LS_p90_1990_2025.tif")
LS = {int(k[-4:]): v for k, v in P90.items()}
SUM = {int(k[-4:]): v for k, v in load("LS_summer_1990_2025.tif")[3].items()}
CNT = load("LS_counts_1990_2025.tif", 1)[3]
L7 = {int(k[-4:]): v for k, v in load("L7only_p90_2013_2021.tif")[3].items()}
OLI = {int(k[-4:]): v for k, v in load("OLIonly_p90_2013_2025.tif")[3].items()}
S2 = {int(k[-4:]): v for k, v in load("S2_p90_2019_2025.tif")[3].items()}

terr = gpd.read_file(os.path.join(P1, "karewa_terraces_v2.gpkg")).to_crs(crs)
proto = gpd.read_file(os.path.join(P1, "karewa_flat_tops_prototype.gpkg")).to_crs(crs)
tid = rasterize([(g, int(i)) for g, i in zip(terr.geometry, terr.terrace_id)], out_shape=shape, transform=T)
m_terr = tid > 0
m_flat = (rasterize([(g, 1) for g in proto.geometry], out_shape=shape, transform=T) == 1) & ~m_terr
STRATA = {"terraces": m_terr, "other_flat": m_flat, "rest": ~m_terr & ~m_flat}


def share(img, mask, thr):
    v = img[mask]
    v = v[np.isfinite(v)]
    return float((v < thr).mean() * 100) if v.size else np.nan


# ---- 1. yearly table ---------------------------------------------------------
rows = []
for y in range(1990, 2026):
    r = dict(year=y, n_obs_year=float(np.median(CNT[f"n_{y}"][m_terr])),
             n_obs_summer=float(np.median(CNT[f"ns_{y}"][m_terr])),
             summer_valid_share=float(np.isfinite(SUM[y][m_terr]).mean()))
    r["usable"] = r["n_obs_year"] >= MIN_OBS
    r["bare_p90_landsat"] = share(LS[y], m_terr, BARE)
    r["bare_p90_landsat_other_flat"] = share(LS[y], m_flat, BARE)
    r["bare_summer_landsat_v1rule"] = share(SUM[y], m_terr, V1_SUMMER_BARE)
    r["bare_p90_L7only"] = share(L7[y], m_terr, BARE) if y in L7 else np.nan
    r["bare_p90_OLIonly"] = share(OLI[y], m_terr, BARE) if y in OLI else np.nan
    r["bare_p90_OLIonly_other_flat"] = share(OLI[y], m_flat, BARE) if y in OLI else np.nan
    r["bare_p90_S2"] = share(S2[y], m_terr, BARE) if y in S2 else np.nan
    rows.append(r)
yearly = pd.DataFrame(rows)
yearly.round(3).to_csv(os.path.join(OUT, "yearly_bare_share.csv"), index=False)


# ---- 2. persistent conversion between two 3-year windows -----------------------
def windows(D, early, late):
    e_veg = np.all([D[y] >= VEG for y in early], axis=0)
    l_bare = np.all([D[y] < BARE for y in late], axis=0)
    e_bare = np.all([D[y] < BARE for y in early], axis=0)
    l_veg = np.all([D[y] >= VEG for y in late], axis=0)
    return e_veg & l_bare, e_bare & l_veg, e_bare, l_bare


TESTS = [("Landsat 8/9 only", OLI, (2013, 2014, 2015), (2023, 2024, 2025)),
         ("Landsat 8/9 only", OLI, (2013, 2014, 2015), (2019, 2020, 2021)),
         ("Landsat 7 only", L7, (2013, 2014, 2015), (2019, 2020, 2021)),
         ("Landsat harmonised", LS, (2013, 2014, 2015), (2023, 2024, 2025)),
         ("Landsat harmonised", LS, (2003, 2004, 2005), (2023, 2024, 2025)),
         ("Landsat harmonised", LS, (1993, 1994, 1996), (2023, 2024, 2025))]
rows = []
for name, D, e, l in TESTS:
    c, rev, eb, lb = windows(D, e, l)
    for sname, mk in STRATA.items():
        rows.append(dict(series=name, early="-".join(map(str, e)), late="-".join(map(str, l)), stratum=sname,
                         stratum_km2=mk.sum() * HA / 100,
                         veg_to_bare_ha=c[mk].sum() * HA, veg_to_bare_pct=c[mk].mean() * 100,
                         bare_to_veg_ha=rev[mk].sum() * HA,
                         persistent_bare_early_ha=eb[mk].sum() * HA, persistent_bare_late_ha=lb[mk].sum() * HA))
conv = pd.DataFrame(rows)
conv.round(3).to_csv(os.path.join(OUT, "conversion_by_stratum.csv"), index=False)

# ---- 3. main conversion layer (Landsat 8/9 only, 2013-15 -> 2023-25) ---------------
c_main = windows(OLI, (2013, 2014, 2015), (2023, 2024, 2025))[0]
c_terr = c_main & m_terr
s2_late = np.all([S2[y] < BARE for y in (2023, 2024, 2025)], axis=0)
s2_agree = float(s2_late[c_terr].mean())
l7_agree = float(np.all([L7[y] < BARE for y in (2019, 2020, 2021)], axis=0)[
    windows(OLI, (2013, 2014, 2015), (2019, 2020, 2021))[0] & m_terr].mean())

# onset = first year from which the pixel stays below BARE up to 2025
yrs = list(range(2013, 2026))
stack = np.stack([OLI[y] < BARE for y in yrs])
stay = np.flip(np.cumprod(np.flip(stack, 0), 0), 0).astype(bool)
onset = np.where(stay.any(0), np.array(yrs)[stay.argmax(0)], 0)
onset_tab = pd.Series(onset[c_terr]).value_counts().sort_index() * HA
onset_tab.rename_axis("onset_year").rename("ha").round(2).to_csv(os.path.join(OUT, "conversion_onset_year.csv"))

per = pd.DataFrame({"terrace_id": tid[c_terr]}).value_counts("terrace_id").mul(HA).rename("veg_to_bare_ha").reset_index()
per = terr[["terrace_id", "area_km2", "scarp_frac"]].merge(per, how="left").fillna({"veg_to_bare_ha": 0})
per["veg_to_bare_pct"] = per.veg_to_bare_ha / (per.area_km2 * 100) * 100
per = per.sort_values("veg_to_bare_ha", ascending=False)
per.round(3).to_csv(os.path.join(OUT, "conversion_by_terrace.csv"), index=False)

feats = [{"properties": {"onset_year": int(v)}, "geometry": g}
         for g, v in shapes(np.where(c_terr, onset, 0).astype("int16"), mask=c_terr, transform=T)]
cg = gpd.GeoDataFrame.from_features(feats, crs=crs)
cg["area_ha"] = cg.area / 1e4
cg.to_file(os.path.join(OUT, "converted_patches_2013_2025.gpkg"), driver="GPKG")

# ---- 4. figure -------------------------------------------------------------------
u = yearly[yearly.usable]
fig, ax = plt.subplots(1, 2, figsize=(13, 4.6))
ax[0].plot(u.year, u.bare_p90_landsat, "o-", color="#444", ms=3, lw=1, label="Landsat 5/7/8/9, harmonised")
ax[0].plot(yearly.year, yearly.bare_p90_L7only, "s-", color="#1b7837", ms=3, lw=1, label="Landsat 7 only")
ax[0].plot(yearly.year, yearly.bare_p90_OLIonly, "^-", color="#2166ac", ms=4, lw=1.4, label="Landsat 8/9 only")
ax[0].plot(yearly.year, yearly.bare_p90_S2, "D-", color="#b2182b", ms=3, lw=1, label="Sentinel-2 only")
ax[0].set(xlabel="Year", ylabel="Share of terrace area (%)",
          title=f"Karewa terraces: yearly p90 NDVI < {BARE}\n(years with < {MIN_OBS} clear Landsat observations left out)")
ax[0].legend(frameon=False, fontsize=8); ax[0].grid(alpha=.3)
main = conv[(conv.series == "Landsat 8/9 only") & (conv.late == "2023-2024-2025")].set_index("stratum")
ax[1].bar(["Karewa terraces", "Other flat,\nelevated land", "Rest of study box"],
          main.loc[["terraces", "other_flat", "rest"], "veg_to_bare_pct"], color=["#b2182b", "#999", "#ccc"])
for i, k in enumerate(["terraces", "other_flat", "rest"]):
    ax[1].text(i, main.loc[k, "veg_to_bare_pct"], f'{main.loc[k, "veg_to_bare_ha"]:.0f} ha', ha="center", va="bottom")
ax[1].set(ylabel="Share of stratum area (%)",
          title="Vegetated in 2013–15, persistently bare in 2023–25\n(Landsat 8/9 only)")
ax[1].grid(alpha=.3, axis="y")
plt.tight_layout(); plt.savefig(os.path.join(OUT, "phase2_summary.png"), dpi=200); plt.close()

# ---- 5. printout -------------------------------------------------------------------
pd.set_option("display.width", 250)
print("years not usable (median clear obs <", MIN_OBS, "):", yearly[~yearly.usable].year.tolist())
print(yearly[["year", "n_obs_year", "n_obs_summer", "bare_p90_landsat", "bare_summer_landsat_v1rule",
              "bare_p90_L7only", "bare_p90_OLIonly", "bare_p90_S2"]].round(2).to_string(index=False))
print(conv.round(2).to_string(index=False))
print(f"Sentinel-2 agrees (bare in all of 2023-25) on {s2_agree:.1%} of the converted terrace pixels")
print(f"Landsat 7 agrees (bare in all of 2019-21) on {l7_agree:.1%} of pixels Landsat 8 converts by 2019-21")
print("onset year (ha):"); print(onset_tab.round(1).to_string())
print("top terraces:"); print(per.head(10).round(2).to_string(index=False))
print("terraces with any conversion:", int((per.veg_to_bare_ha > 0).sum()), "of", len(per),
      "| top 5 share: %.0f%%" % (per.veg_to_bare_ha.head(5).sum() / per.veg_to_bare_ha.sum() * 100))
print("patches:", len(cg), "| >= 1 ha:", int((cg.area_ha >= 1).sum()), "| largest ha: %.1f" % cg.area_ha.max())
