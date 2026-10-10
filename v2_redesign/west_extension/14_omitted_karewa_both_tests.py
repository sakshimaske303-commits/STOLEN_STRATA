"""v2 extended box: does karewa ground that the terrace rule leaves out convert like the terraces, or like the valley floor?

Phase 2 (`phase2_timeseries/04_conversion_whole_box.py`) answered this in the original box with the strict test only.
The strict test misses most kiln land (Section 3.4 of the paper), and the original box leaves out the Bandagam-Batapora belt.
This script repeats the check on the wide box, with both tests, as far west as the geological map tile reaches
(about 74.66 E), and once more with the two kiln-belt site boxes removed.

Geology: Dar & Zeeden (2020, Fig. 2), same colour legend and georeferencing as 04_conversion_whole_box.py.
Valley part only: elevation below 2,000 m (Copernicus GLO-30). Rates are a share of the land that was vegetated at the
start under each test's own rule (strict: peak >= 0.35 in each of 2013-15; drop: median peak >= 0.45 in 2013-15).

I run it from the repo root:  python v2_redesign/west_extension/14_omitted_karewa_both_tests.py
Output: v2_redesign/west_extension/omitted_karewa_both_tests.csv
"""
import os
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from PIL import Image
from rasterio.transform import Affine
from rasterio.features import rasterize
from rasterio.warp import reproject, Resampling
from shapely.geometry import box

W = "v2_redesign/west_extension/"
P1 = "v2_redesign/phase1_delineation"
HA = 0.09
with rasterio.open("data/raw/StolenStrata_v2w_OLIonly_p90_2013_2025.tif") as s:
    a = s.read().astype("float32"); a[a == -32768] = np.nan
    D = {int(d[-4:]): a[i] / 1e4 for i, d in enumerate(s.descriptions)}
    T, crs, shape = s.transform, s.crs, s.shape

E, L = (2013, 2014, 2015), (2023, 2024, 2025)
veg_s = np.all([D[y] >= .35 for y in E], 0)
strict = veg_s & np.all([D[y] < .25 for y in L], 0)
me, ml = np.median([D[y] for y in E], 0), np.median([D[y] for y in L], 0)
veg_d = me >= .45
drop = veg_d & (ml < .40) & (me - ml >= .20)

# geology tile -> Landsat grid
REFS = {"alluvium": [(110, 105, 51), (128, 122, 70)], "dilpur_fm": [(85, 48, 25)], "reworked_karewa": [(75, 104, 23)],
        "pampur_mb": [(26, 86, 106)], "hirpur_fm": [(147, 46, 46), (173, 83, 83)],
        "nagum_other": [(126, 79, 116), (90, 30, 80)], "water": [(20, 93, 205)]}
names = list(REFS)
im = np.asarray(Image.open(os.path.join(P1, "geology", "karewa_group_map_tile.jpg")).convert("RGB")).astype(float)
best = np.full(im.shape[:2], -1); bd = np.full(im.shape[:2], 1e9)
for k, n in enumerate(names):
    for c in REFS[n]:
        d = np.sqrt(((im - np.array(c)) ** 2).sum(2)); m = d < bd; bd[m] = d[m]; best[m] = k
gcls = np.where(((im.max(2) - im.min(2)) < 25) | (bd > 45), -1, best).astype("int16")
S = 1 / 0.78125
GT = Affine(S / 1419.0, 0, 75 + (1100 - 1587) / 1419.0, 0, -S / 1417.0, 34 - (800 - 1065) / 1417.0)
geo = np.full(shape, -2, "int16")
reproject(gcls, geo, src_transform=GT, src_crs="EPSG:4326", dst_transform=T, dst_crs=crs,
          resampling=Resampling.nearest, src_nodata=-9999, dst_nodata=-2)
covered = geo != -2                                   # inside the map tile
unit = np.full(shape, "unmapped", dtype=object)
unit[np.isin(geo, [names.index(n) for n in ("dilpur_fm", "pampur_mb", "hirpur_fm", "nagum_other")])] = "karewa_formation"
unit[geo == names.index("reworked_karewa")] = "reworked_karewa"
unit[geo == names.index("alluvium")] = "alluvium"
unit[geo == names.index("water")] = "water"

with rasterio.open("data/raw/StolenStrata_v2w_DEM_GLO30_buffered.tif") as d:
    dem = np.full(shape, np.nan, "float32")
    reproject(rasterio.band(d, 1), dem, dst_transform=T, dst_crs=crs, resampling=Resampling.nearest, dst_nodata=np.nan)
valley = dem < 2000

t = gpd.read_file(W + "karewa_terraces_wide.gpkg").to_crs(crs)
mt = rasterize([(g, 1) for g in t.geometry], out_shape=shape, transform=T) == 1


def window(lon0, lat0, lon1, lat1):
    g = gpd.GeoSeries([box(lon0, lat0, lon1, lat1)], crs=4326).to_crs(crs).iloc[0]
    return rasterize([(g, 1)], out_shape=shape, transform=T) == 1


belt = window(74.83, 33.925, 74.87, 33.958) | window(74.60, 33.99, 74.72, 34.05)

rows = []
for excl in (False, True):
    for u in ("karewa_formation", "reworked_karewa", "alluvium", "unmapped"):
        for where, mk in (("inside terraces", mt), ("outside terraces", ~mt)):
            m = (unit == u) & mk & valley & covered & (~belt if excl else True)
            rows.append(dict(belts_excluded=excl, geology=u, where=where, area_km2=m.sum() * HA / 100,
                             strict_ha=(m & strict).sum() * HA, strict_pct_of_vegetated=(m & strict).sum() / max((m & veg_s).sum(), 1) * 100,
                             drop_ha=(m & drop).sum() * HA, drop_pct_of_vegetated=(m & drop).sum() / max((m & veg_d).sum(), 1) * 100))
r = pd.DataFrame(rows)
r.round(3).to_csv(W + "omitted_karewa_both_tests.csv", index=False)
pd.set_option("display.width", 250)
print(r.round(2).to_string(index=False))
