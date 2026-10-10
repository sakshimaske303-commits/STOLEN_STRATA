"""v2 extended box — blind sample to check the two conversion tests against present-day imagery.

Strata, all on terraces:  A = flagged by the strict test, B = flagged by the drop test only, C = not flagged.
The points file carries no stratum; the key is kept in a separate file and only joined after labelling.
Labels to use: kiln_ground (kiln, clay pit, drying yard, worked bare earth in a kiln field), built_up, road,
vegetated (field, orchard, grass, trees), bare_other, water, unclear.

I run it from the repo root:  python v2_redesign/west_extension/04_accuracy_sample.py
"""
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from rasterio.features import rasterize
from rasterio.transform import xy
from rasterio.warp import transform as warp_xy

SEED = 20261003
N = {"A_strict": 25, "B_drop_only": 60, "C_not_flagged": 35}
OUT = "v2_redesign/west_extension/"

with rasterio.open("data/raw/StolenStrata_v2w_OLIonly_p90_2013_2025.tif") as s:
    a = s.read().astype("float32"); a[a == -32768] = np.nan
    D = {int(d[-4:]): a[i] / 1e4 for i, d in enumerate(s.descriptions)}; T, crs, shape = s.transform, s.crs, s.shape
t = gpd.read_file(OUT + "karewa_terraces_wide.gpkg").to_crs(crs)
tid = rasterize([(g, int(i)) for g, i in zip(t.geometry, t.terrace_id)], out_shape=shape, transform=T)
E_, L_ = (2013, 2014, 2015), (2023, 2024, 2025)
strict = np.all([D[y] >= .35 for y in E_], 0) & np.all([D[y] < .25 for y in L_], 0)
me, ml = np.median([D[y] for y in E_], 0), np.median([D[y] for y in L_], 0)
drop = (me >= .45) & (ml < .40) & (me - ml >= .20)
strata = {"A_strict": strict & (tid > 0), "B_drop_only": drop & ~strict & (tid > 0), "C_not_flagged": ~drop & ~strict & (tid > 0)}

rng = np.random.default_rng(SEED)
rows = []
for name, m in strata.items():
    r, c = np.nonzero(m)
    for k in rng.choice(len(r), N[name], replace=False):
        x, y = xy(T, r[k], c[k]); lon, lat = warp_xy(crs, "EPSG:4326", [x], [y])
        rows.append(dict(stratum=name, stratum_px=int(m.sum()), terrace_id=int(tid[r[k], c[k]]), lat=round(lat[0], 6), lon=round(lon[0], 6),
                         p90_2013_15=round(float(me[r[k], c[k]]), 3), p90_2023_25=round(float(ml[r[k], c[k]]), 3)))
df = pd.DataFrame(rows).sample(frac=1, random_state=SEED).reset_index(drop=True)
df.insert(0, "point_id", range(1, len(df) + 1))
df["google_maps"] = "https://www.google.com/maps/@" + df.lat.astype(str) + "," + df.lon.astype(str) + ",18z/data=!3m1!1e3"
pts = df[["point_id", "lat", "lon", "google_maps"]].copy()
pts["draft_label"] = ""; pts["draft_note"] = ""; pts["my_label"] = ""
pts.to_csv(OUT + "accuracy_sample_points.csv", index=False)
df[["point_id", "stratum", "stratum_px", "terrace_id", "p90_2013_15", "p90_2023_25"]].to_csv(OUT + "accuracy_sample_key.csv", index=False)
print({k: int(v.sum()) for k, v in strata.items()}, "points:", len(df))
