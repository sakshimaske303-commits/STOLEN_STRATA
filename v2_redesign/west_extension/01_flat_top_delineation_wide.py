"""v2 extended box — the Phase 1 flat-top rule, unchanged, on the wider box (74.55–75.15 E, 33.80–34.15 N).

Replaces the v1 rule (TPI > 3 m & slope < 8 deg), which picked up terrace rims and
spurs and left the flat plateau interiors out.

Rule (all thresholds are provisional and must be calibrated in the Phase 1 validation):
  1. low slope            : slope < SLOPE_MAX on a lightly smoothed DEM
  2. elevated above drain : HAND (height above nearest drainage) > HAND_MIN
  3. valley-side elevation: elevation < ELEV_MAX
  4. scarp-bounded        : share of the component's outer ring steeper than SCARP_DEG
                            -> >= 0.45 'scarp-bounded', 0.20-0.45 'ambiguous',
                               < 0.20 'rejected' (alluvial fan / valley fill)

I run it from the repo root:  python v2_redesign/west_extension/01_flat_top_delineation_wide.py
Needs: data/raw/StolenStrata_v2w_DEM_GLO30_buffered.tif (study box + ~10 km buffer, so that
plateaus are not cut by the DEM edge), and `pip install pysheds`.
Terrain is processed on the buffered DEM; only plateaus that intersect the original
study-area box are kept, with their full outline and the share inside the box.
Known limit: a fan and a karewa can only be told apart here by scarps, so the geology
map / reference points are the real arbiter.
"""
import os
import numpy as np
if not hasattr(np, "in1d"):          # pysheds 0.5 still calls np.in1d (removed in NumPy 2.4)
    np.in1d = np.isin
import pandas as pd
import geopandas as gpd
import rasterio
from rasterio.features import shapes
from rasterio.warp import calculate_default_transform, reproject, Resampling
from shapely.geometry import box
from scipy import ndimage as ndi
from pysheds.grid import Grid

DEM_RAW = "data/raw/StolenStrata_v2w_DEM_GLO30_buffered.tif"
DEM_PATH = "data/interim/DEM_wide_buffered_UTM43N.tif"
UTM = "EPSG:32643"
AOI_LONLAT = (74.55, 33.80, 75.15, 34.15)   # extended study box (west, south, east, north)
OUT_DIR = "v2_redesign/west_extension"

SLOPE_MAX = 4.0        # degrees
HAND_MIN = 15.0        # metres above nearest drainage
STREAM_KM2 = 3.0       # contributing area that defines a drainage line
ELEV_MAX = 1950.0      # metres
OPEN_R = 2             # pixels; removes thin necks before labelling
MIN_KM2 = 0.05
RING_PX = 3            # width of the outer ring tested for scarps
SCARP_DEG = 6.0
CLASS_BINS = [-1, 0.20, 0.45, 2]
CLASS_LABELS = ["rejected", "ambiguous", "scarp_bounded"]

os.makedirs(OUT_DIR, exist_ok=True)

# --- reproject the buffered DEM to UTM 43N ----------------------------------------
with rasterio.open(DEM_RAW) as src:
    nd = src.nodata if src.nodata is not None else -9999.0
    tr, w_, h_ = calculate_default_transform(src.crs, UTM, src.width, src.height, *src.bounds)
    meta = src.meta.copy(); meta.update(crs=UTM, transform=tr, width=w_, height=h_, nodata=nd, dtype="float32")
    with rasterio.open(DEM_PATH, "w", **meta) as dst:
        reproject(rasterio.band(src, 1), rasterio.band(dst, 1), src_transform=src.transform, src_crs=src.crs,
                  dst_transform=tr, dst_crs=UTM, src_nodata=src.nodata, dst_nodata=nd, resampling=Resampling.bilinear)

# --- DEM, nodata fill, slope ---------------------------------------------------
with rasterio.open(DEM_PATH) as src:
    dem = src.read(1).astype(float)
    T, crs, profile = src.transform, src.crs, src.profile
    px = T.a
    if src.nodata is not None:
        dem[dem == src.nodata] = np.nan
nodata_mask = np.isnan(dem)
idx = ndi.distance_transform_edt(nodata_mask, return_distances=False, return_indices=True)
demf = dem[tuple(idx)]
dy, dx = np.gradient(ndi.gaussian_filter(demf, 1.0), px)
slope = np.degrees(np.arctan(np.hypot(dx, dy)))

# --- HAND ------------------------------------------------------------------------
tmp = os.path.join(OUT_DIR, "_dem_filled_tmp.tif")
p2 = profile.copy(); p2.update(dtype="float32", nodata=-9999.0)
with rasterio.open(tmp, "w", **p2) as dst:
    dst.write(demf.astype("float32"), 1)
grid = Grid.from_raster(tmp)
d = grid.read_raster(tmp)
infl = grid.resolve_flats(grid.fill_depressions(grid.fill_pits(d)))
fdir = grid.flowdir(infl)
acc = grid.accumulation(fdir)
def hand(km2):
    return np.asarray(grid.compute_hand(fdir, infl, acc > km2 * 1e6 / (px * px)), dtype=float)
h = hand(STREAM_KM2)
h = np.where(np.isfinite(h), h, hand(1.0))               # cells that leave the grid before a big stream
w = int(round(8000 / px)) | 1                             # last fallback: height above an 8 km local minimum
base = ndi.gaussian_filter(ndi.minimum_filter(demf, size=w), w / 4)
h = np.where(np.isfinite(h), h, demf - base)
os.remove(tmp)

# --- flat, elevated core -> components ---------------------------------------------
st4 = ndi.generate_binary_structure(2, 1)
core = (slope < SLOPE_MAX) & (h > HAND_MIN) & (demf < ELEV_MAX) & (~nodata_mask)
opened = ndi.binary_opening(core, structure=ndi.iterate_structure(st4, OPEN_R))
lab, n = ndi.label(opened)
area = ndi.sum(np.ones_like(lab), lab, np.arange(1, n + 1)) * px * px / 1e6
keep = np.r_[False, area >= MIN_KM2][lab]
keep = ndi.binary_dilation(keep, structure=st4, iterations=OPEN_R, mask=core)
mask = ndi.binary_fill_holes(keep)

# --- scarp share of each component's outer ring -------------------------------------
lab, n = ndi.label(mask)
st8 = np.ones((3, 3), bool)
rows = []
for i, sl in enumerate(ndi.find_objects(lab), 1):
    r0, r1 = max(sl[0].start - RING_PX - 1, 0), min(sl[0].stop + RING_PX + 1, mask.shape[0])
    c0, c1 = max(sl[1].start - RING_PX - 1, 0), min(sl[1].stop + RING_PX + 1, mask.shape[1])
    comp = lab[r0:r1, c0:c1] == i
    a = comp.sum() * px * px / 1e6
    ring = ndi.binary_dilation(comp, structure=st8, iterations=RING_PX) & ~comp & ~mask[r0:r1, c0:c1]
    if a < MIN_KM2 or ring.sum() == 0:
        continue
    touches_edge = sl[0].start == 0 or sl[1].start == 0 or sl[0].stop == mask.shape[0] or sl[1].stop == mask.shape[1]
    rows.append(dict(cid=i, scarp_frac=float((slope[r0:r1, c0:c1][ring] > SCARP_DEG).mean()),
                     mean_elev=float(demf[r0:r1, c0:c1][comp].mean()),
                     mean_hand=float(h[r0:r1, c0:c1][comp].mean()),
                     mean_slope=float(slope[r0:r1, c0:c1][comp].mean()),
                     touches_dem_edge=bool(touches_edge)))
attrs = pd.DataFrame(rows).set_index("cid")

valid = np.isin(lab, attrs.index.values)
feats = [{"properties": {"cid": int(v)}, "geometry": g}
         for g, v in shapes(lab.astype(np.int32), mask=valid, transform=T)]
gdf = gpd.GeoDataFrame.from_features(feats, crs=crs).dissolve("cid").reset_index()
gdf = gdf.join(attrs, on="cid")
gdf["area_km2"] = gdf.area / 1e6
aoi = gpd.GeoSeries([box(*AOI_LONLAT)], crs=4326).to_crs(crs).iloc[0]
gdf["share_in_aoi"] = gdf.intersection(aoi).area / gdf.area
gdf = gdf[gdf["share_in_aoi"] > 0].copy()
gdf["area_in_aoi_km2"] = gdf["area_km2"] * gdf["share_in_aoi"]
gdf["cls"] = pd.cut(gdf["scarp_frac"], CLASS_BINS, labels=CLASS_LABELS).astype(str)
gdf = gdf.sort_values("area_km2", ascending=False).reset_index(drop=True)
gdf["terrace_id"] = range(1, len(gdf) + 1)          # a real unique ID this time
gdf = gdf.drop(columns="cid")

out = os.path.join(OUT_DIR, "karewa_flat_tops_wide.gpkg")
gdf.to_file(out, driver="GPKG")
print(gdf.groupby("cls").agg(n=("terrace_id", "size"), km2=("area_km2", "sum"), km2_in_aoi=("area_in_aoi_km2", "sum")).round(1))
print("edge-truncated components:", int(gdf.touches_dem_edge.sum()))
print("saved", out)
