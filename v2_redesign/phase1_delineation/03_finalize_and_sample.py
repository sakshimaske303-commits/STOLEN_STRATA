"""v2 Phase 1 — (a) final v2 terrace layer from the prototype + review, (b) blind reference sample.

(a) karewa_terraces_v2.gpkg : flat-top polygons whose scarp share is >= SCARP_MIN. The 0.25
    cut-off comes from the comparison with the published Karewa Group map (04_geology_check.py):
    above it, 90% of the larger polygons sit on mapped Karewa formations. Polygons labelled
    `not_karewa` in review_checklist.csv (my_label if filled, else first_pass_label) are removed and
    listed in excluded_by_review.csv. Clipped to the study-area box because the NDVI rasters
    only cover the box.
(b) reference_sample_points.csv / .gpkg : stratified random points for the accuracy assessment.
    The labelling file carries NO stratum or predicted class (blind labelling); the key is in
    reference_sample_key.csv and must not be opened while labelling.

Run from the repo root:  python v2_redesign/phase1_delineation/03_finalize_and_sample.py
"""
import os
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from shapely.geometry import box, Point

OUT = "v2_redesign/phase1_delineation"
AOI_LONLAT = (74.75, 33.85, 75.15, 34.15)
DEM = "data/interim/DEM_buffered_UTM43N.tif"
VALLEY_ELEV_MAX = 2000.0          # sampling domain: valley land below this elevation
BOUNDARY_M = 60.0
N = {"karewa": 150, "excluded_flat": 100, "other_valley": 150, "boundary": 60}
SEED = 20261002
SCARP_MIN = 0.25

g = gpd.read_file(os.path.join(OUT, "karewa_flat_tops_prototype.gpkg"))
chk = pd.read_csv(os.path.join(OUT, "review_checklist.csv"))
lab = chk["my_label"].where(chk["my_label"].notna() & (chk["my_label"].astype(str).str.strip() != ""), chk["first_pass_label"])
review = dict(zip(chk["terrace_id"], lab.astype(str).str.strip()))
g["review_label"] = g["terrace_id"].map(review)

aoi = gpd.GeoSeries([box(*AOI_LONLAT)], crs=4326).to_crs(g.crs).iloc[0]
by_rule = g["scarp_frac"] >= SCARP_MIN
vetoed = by_rule & (g["review_label"] == "not_karewa")
g[vetoed][["terrace_id", "area_km2", "scarp_frac", "mean_elev"]].merge(
    chk[["terrace_id", "first_pass_reason"]], on="terrace_id", how="left").round(2).to_csv(
    os.path.join(OUT, "excluded_by_review.csv"), index=False)
v2 = g[by_rule & ~vetoed & (g["share_in_aoi"] > 0)].copy()
v2["basis"] = np.where(v2["scarp_frac"] >= 0.45, "scarp>=0.45", "scarp 0.25-0.45")
v2["geometry"] = v2.intersection(aoi)
v2 = v2[~v2.is_empty].explode(index_parts=False)
v2["area_km2"] = v2.area / 1e6
v2 = v2[v2["area_km2"] >= 0.05].copy()                       # drop slivers created by clipping
v2 = v2.sort_values("area_km2", ascending=False).reset_index(drop=True)
v2["proto_id"] = v2["terrace_id"]
v2["terrace_id"] = range(1, len(v2) + 1)
v2 = v2[["terrace_id", "proto_id", "basis", "area_km2", "scarp_frac", "mean_elev", "mean_hand", "mean_slope", "geometry"]]
v2.to_file(os.path.join(OUT, "karewa_terraces_v2.gpkg"), driver="GPKG")
print(f"v2 terraces: {len(v2)} polygons, {v2.area_km2.sum():.1f} km2 "
      f"({v2.basis.value_counts().to_dict()}); removed after review: {int(vetoed.sum())}")

# ---------------- reference sample ----------------
rng = np.random.default_rng(SEED)
kept_u = v2.union_all()
excl = g[~g["terrace_id"].isin(v2["proto_id"])]
excl_u = excl.intersection(aoi).union_all()
ring = kept_u.boundary.buffer(BOUNDARY_M).intersection(aoi)

with rasterio.open(DEM) as src:
    def elev(xs, ys):
        return np.array([v[0] for v in src.sample(zip(xs, ys))], dtype=float)

    def draw(n, region, cond=None):
        minx, miny, maxx, maxy = region.bounds
        pts = []
        while len(pts) < n:
            xs, ys = rng.uniform(minx, maxx, 4000), rng.uniform(miny, maxy, 4000)
            e = elev(xs, ys)
            for x, y, z in zip(xs, ys, e):
                p = Point(x, y)
                if z < VALLEY_ELEV_MAX and region.contains(p) and (cond is None or cond(p)):
                    pts.append(p)
                    if len(pts) == n:
                        break
        return pts

    core_kept = kept_u.difference(ring)
    core_excl = excl_u.difference(ring)
    other = aoi.difference(kept_u).difference(excl_u).difference(ring)
    rows = []
    for stratum, region in [("karewa", core_kept), ("excluded_flat", core_excl), ("other_valley", other), ("boundary", ring)]:
        for p in draw(N[stratum], region):
            rows.append(dict(stratum=stratum, predicted_karewa=bool(kept_u.contains(p)), geometry=p))

s = gpd.GeoDataFrame(rows, crs=g.crs).sample(frac=1, random_state=SEED).reset_index(drop=True)   # shuffle
s["point_id"] = range(1, len(s) + 1)
ll = s.to_crs(4326)
s["lat"], s["lon"] = ll.geometry.y.round(6), ll.geometry.x.round(6)
s["google_maps"] = "https://www.google.com/maps/@" + s["lat"].astype(str) + "," + s["lon"].astype(str) + ",16z/data=!3m1!1e3"
s["reference_label"] = ""     # karewa_top | scarp_or_gully | valley_floor_or_fan | hill_or_mountain | unsure
s["labeller"] = ""
s["notes"] = ""
blind = ["point_id", "lat", "lon", "google_maps", "reference_label", "labeller", "notes"]
s[blind].to_csv(os.path.join(OUT, "reference_sample_points.csv"), index=False)
s[blind + ["geometry"]].to_file(os.path.join(OUT, "reference_sample_points.gpkg"), driver="GPKG")
s[["point_id", "stratum", "predicted_karewa"]].to_csv(os.path.join(OUT, "reference_sample_key.csv"), index=False)

# stratum areas restricted to the sampling domain (elevation < VALLEY_ELEV_MAX), needed for
# area-weighted accuracy and area estimates
from rasterio.features import geometry_mask
with rasterio.open(DEM) as src:
    z = src.read(1).astype(float)
    low = z < VALLEY_ELEV_MAX
    if src.nodata is not None:
        low &= z != src.nodata
    cell = abs(src.transform.a * src.transform.e)
    def domain_area(region):
        inside = ~geometry_mask([region], z.shape, src.transform)
        return float((inside & low).sum() * cell / 1e6)
    areas = {"karewa": domain_area(core_kept), "excluded_flat": domain_area(core_excl),
             "other_valley": domain_area(other), "boundary": domain_area(ring)}
pd.DataFrame({"stratum": list(N), "n_points": list(N.values()),
              "stratum_area_km2": [round(areas[k], 2) for k in N]}).to_csv(os.path.join(OUT, "reference_sample_strata.csv"), index=False)
print(s.groupby("stratum").size().to_dict(), "| total", len(s))
