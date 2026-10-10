"""v2 extended box: a second, independent draw of sample points to enlarge the accuracy sample.

The first sample (04_accuracy_sample.py) has 25 strict, 60 drop-only and 35 unflagged points. This draw adds 35, 60 and 25,
from the same strata and by the same rule, leaving out the pixels already sampled, so the two draws can be pooled
(60 / 120 / 60). Point ids continue from 121. As before, the points file carries no stratum; the key is a separate file.

I run it from the repo root:  python v2_redesign/west_extension/12_accuracy_sample_supplement.py
Output: accuracy_sample2_points.csv, accuracy_sample2_key.csv, accuracy_sample2_points.kml
"""
import geopandas as gpd, numpy as np, pandas as pd, rasterio
from rasterio.features import rasterize
from rasterio.transform import rowcol, xy
from rasterio.warp import transform as warp_xy

SEED = 20261007
N = {"A_strict": 35, "B_drop_only": 60, "C_not_flagged": 25}
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

first = pd.read_csv(OUT + "accuracy_sample_points.csv")
x, y = warp_xy("EPSG:4326", crs, first.lon.tolist(), first.lat.tolist())
r0, c0 = rowcol(T, x, y)
used = np.zeros(shape, bool); used[np.array(r0), np.array(c0)] = True
assert used.sum() == len(first)

rng = np.random.default_rng(SEED)
rows = []
for name, m in strata.items():
    r, c = np.nonzero(m & ~used)
    for k in rng.choice(len(r), N[name], replace=False):
        px, py = xy(T, r[k], c[k]); lon, lat = warp_xy(crs, "EPSG:4326", [px], [py])
        rows.append(dict(stratum=name, stratum_px=int(m.sum()), terrace_id=int(tid[r[k], c[k]]), lat=round(lat[0], 6), lon=round(lon[0], 6),
                         p90_2013_15=round(float(me[r[k], c[k]]), 3), p90_2023_25=round(float(ml[r[k], c[k]]), 3)))
df = pd.DataFrame(rows).sample(frac=1, random_state=SEED).reset_index(drop=True)
df.insert(0, "point_id", range(121, 121 + len(df)))
df["google_maps"] = "https://www.google.com/maps/@" + df.lat.astype(str) + "," + df.lon.astype(str) + ",18z/data=!3m1!1e3"
pts = df[["point_id", "lat", "lon", "google_maps"]].copy()
for col in ["my_label", "in_kiln_field", "before_label", "image_date", "basis"]:
    pts[col] = ""
pts.to_csv(OUT + "accuracy_sample2_points.csv", index=False)
df[["point_id", "stratum", "stratum_px", "terrace_id", "p90_2013_15", "p90_2023_25"]].to_csv(OUT + "accuracy_sample2_key.csv", index=False)
kml = ['<?xml version="1.0" encoding="UTF-8"?>', '<kml xmlns="http://www.opengis.net/kml/2.2"><Document><name>Accuracy sample points, second draw</name>',
       '<Style id="p"><IconStyle><scale>0.9</scale><Icon><href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png</href></Icon></IconStyle><LabelStyle><scale>0.9</scale></LabelStyle></Style>']
kml += ['<Placemark><name>%d</name><styleUrl>#p</styleUrl><Point><coordinates>%s,%s,0</coordinates></Point></Placemark>' % (p.point_id, p.lon, p.lat) for p in pts.itertuples()]
open(OUT + "accuracy_sample2_points.kml", "w", encoding="utf-8").write("\n".join(kml + ["</Document></kml>"]))
print("points:", len(df))
