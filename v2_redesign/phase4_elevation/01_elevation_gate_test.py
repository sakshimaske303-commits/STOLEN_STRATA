"""v2 Phase 4 — gate test: can free elevation data show the ground getting lower on the converted block?

Inputs in data/raw/ (from gee_03_elevation_gate_test.js) plus the Copernicus DEM from Phase 1:
  StolenStrata_v2_GEDI_ground_2019_2025.tif   dz_YYYY = GEDI ground minus TanDEM-X (m x 100), n_YYYY = shots
  StolenStrata_v2_DEM_SRTM_2000.tif, StolenStrata_v2_DEM_AW3D30_2006_2011.tif
  data/interim/DEM_buffered_UTM43N.tif        Copernicus GLO-30 (2011-2015)

Groups: converted (vegetated 2013-15 -> bare 2023-25, Phase 2), the rest of terraces 5 and 3, all other terraces.
I run it from the repo root:  python v2_redesign/phase4_elevation/01_elevation_gate_test.py
"""
import os
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from rasterio.features import rasterize
from rasterio.warp import reproject, Resampling

RAW = "data/raw/StolenStrata_v2_"
OUT = "v2_redesign/phase4_elevation"

g = rasterio.open(RAW + "GEDI_ground_2019_2025.tif")
G = {d: g.read(i + 1).astype("float32") for i, d in enumerate(g.descriptions)}
terr = gpd.read_file("v2_redesign/phase1_delineation/karewa_terraces_v2.gpkg").to_crs(g.crs)
tid = rasterize([(x, int(i)) for x, i in zip(terr.geometry, terr.terrace_id)], out_shape=g.shape, transform=g.transform)
cp = gpd.read_file("v2_redesign/phase2_timeseries/converted_patches_2013_2025.gpkg").to_crs(g.crs)
conv = rasterize([(x, 1) for x in cp.geometry], out_shape=g.shape, transform=g.transform) == 1
GROUPS = {"converted": conv, "terraces_5_3_unconverted": np.isin(tid, (5, 3)) & ~conv,
          "other_terraces": (tid > 0) & ~np.isin(tid, (5, 3))}


def stats(v):
    v = v[np.isfinite(v)]
    if v.size == 0:
        return dict(n=0, median_m=np.nan, nmad_m=np.nan, p5_m=np.nan, p95_m=np.nan)
    med = np.median(v)
    return dict(n=int(v.size), median_m=med, nmad_m=1.4826 * np.median(np.abs(v - med)),
                p5_m=np.percentile(v, 5), p95_m=np.percentile(v, 95))


rows = []
for y in range(2019, 2026):
    # cells with no shot carry dz = 0 and n = 0 in the export: keep only cells with at least one shot
    dz = np.where((G[f"dz_{y}"] == -32768) | (G[f"n_{y}"] <= 0), np.nan, G[f"dz_{y}"] / 100)
    rows.append(dict(source="GEDI minus TanDEM-X", year=y, group="whole_box", **stats(dz)))
    for k, m in GROUPS.items():
        rows.append(dict(source="GEDI minus TanDEM-X", year=y, group=k, **stats(dz[m])))


def onto_gedi_grid(path):
    with rasterio.open(path) as s:
        out = np.full(g.shape, np.nan, "float32")
        reproject(rasterio.band(s, 1), out, dst_transform=g.transform, dst_crs=g.crs,
                  resampling=Resampling.bilinear, src_nodata=s.nodata, dst_nodata=np.nan)
    return out


cop = onto_gedi_grid("data/interim/DEM_buffered_UTM43N.tif")
srtm = onto_gedi_grid(RAW + "DEM_SRTM_2000.tif")
aw3d = onto_gedi_grid(RAW + "DEM_AW3D30_2006_2011.tif")
for name, d in [("Copernicus(2011-15) minus SRTM(2000)", cop - srtm),
                ("Copernicus(2011-15) minus AW3D30(2006-11)", cop - aw3d)]:
    for k, m in GROUPS.items():
        rows.append(dict(source=name, year="", group=k, **stats(d[m])))

tab = pd.DataFrame(rows)
tab.round(2).to_csv(os.path.join(OUT, "elevation_gate_test.csv"), index=False)
pd.set_option("display.width", 200)
print(tab.round(2).to_string(index=False))
