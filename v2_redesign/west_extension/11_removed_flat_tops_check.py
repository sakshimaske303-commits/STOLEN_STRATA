"""v2 extended box: does any result depend on the flat tops removed by review?

Flat tops that pass the scarp rule but match the five polygons removed in the original box (foothill aprons and valley
floors inside the mountains, listed in phase1_delineation/excluded_by_review.csv) are left out of the terrace map.
This script measures how much land they cover inside the box and how much of it either conversion test flags, so a
reader can see what keeping them would change.

I run it from the repo root:  python v2_redesign/west_extension/11_removed_flat_tops_check.py
Output: v2_redesign/west_extension/removed_flat_tops_check.csv
"""
import geopandas as gpd, numpy as np, pandas as pd, rasterio
from rasterio.features import rasterize
from shapely.geometry import box

W = "v2_redesign/west_extension/"; P1 = "v2_redesign/phase1_delineation/"
s = rasterio.open("data/raw/StolenStrata_v2w_OLIonly_p90_2013_2025.tif")
a = s.read().astype("float32"); a[a == -32768] = np.nan
D = {int(d[-4:]): a[i] / 1e4 for i, d in enumerate(s.descriptions)}
proto = gpd.read_file(W + "karewa_flat_tops_wide.gpkg").to_crs(s.crs)
old = gpd.read_file(P1 + "karewa_flat_tops_prototype.gpkg").to_crs(s.crs)
ids = pd.read_csv(P1 + "excluded_by_review.csv").iloc[:, 0].tolist()
excl = old[old.terrace_id.isin(ids)].union_all()
aoi = gpd.GeoSeries([box(74.55, 33.80, 75.15, 34.15)], crs=4326).to_crs(s.crs).iloc[0]
k = proto[proto.scarp_frac >= 0.25]
m = k[k.intersection(excl).area / k.area >= 0.5].copy()

E, L = (2013, 2014, 2015), (2023, 2024, 2025)
strict = np.all([D[y] >= .35 for y in E], 0) & np.all([D[y] < .25 for y in L], 0)
e, l = np.median([D[y] for y in E], 0), np.median([D[y] for y in L], 0)
drop = (e >= .45) & (l < .40) & (e - l >= .20)
rows = []
for g in m.geometry:
    gi = g.intersection(aoi)
    r = rasterize([(gi, 1)], out_shape=s.shape, transform=s.transform) == 1
    lon, lat = gpd.GeoSeries([gi.centroid], crs=s.crs).to_crs(4326).iloc[0].coords[0]
    rows.append(dict(lat=round(lat, 4), lon=round(lon, 4), area_km2=round(g.area / 1e6, 3), area_in_box_km2=round(gi.area / 1e6, 3),
                     strict_ha=round(float(strict[r].sum()) * .09, 2), drop_ha=round(float(drop[r].sum()) * .09, 2)))
t = pd.DataFrame(rows)
t.loc[len(t)] = ["all", "", round(t.area_km2.sum(), 3), round(t.area_in_box_km2.sum(), 3), round(t.strict_ha.sum(), 2), round(t.drop_ha.sum(), 2)]
t.to_csv(W + "removed_flat_tops_check.csv", index=False); print(t.to_string(index=False))
