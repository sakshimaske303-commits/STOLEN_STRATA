"""v2 extended box — do the results depend on the two terrace cut-offs chosen by hand (slope < 4 deg, height above drainage > 15 m)?

Re-runs the Phase 1 flat-top rule for 3 x 3 combinations (slope 3/4/5 deg, HAND 10/15/20 m), everything else unchanged
(elevation < 1950 m, opening 2 px, min 0.05 km2, scarp share >= 0.25), and repeats both conversion tests on each terrace set.

Run from the repo root:  python v2_redesign/west_extension/06_delineation_sensitivity.py   (about 3 minutes)
"""
import os
import numpy as np
if not hasattr(np, "in1d"):
    np.in1d = np.isin
import pandas as pd
import rasterio
from rasterio.warp import reproject, Resampling, transform_bounds
from rasterio.features import rasterize
from scipy import ndimage as ndi
from pysheds.grid import Grid
import geopandas as gpd
from shapely.geometry import box

DEM = "data/interim/DEM_wide_buffered_UTM43N.tif"
RAW = "data/raw/StolenStrata_v2w_"
OUT = "v2_redesign/west_extension/"
AOI = (74.55, 33.80, 75.15, 34.15)
ELEV_MAX, OPEN_R, MIN_KM2, RING_PX, SCARP_DEG, SCARP_MIN, STREAM_KM2 = 1950.0, 2, 0.05, 3, 6.0, 0.25, 3.0
HA = 0.09

with rasterio.open(DEM) as src:
    dem = src.read(1).astype(float); T, crs, profile = src.transform, src.crs, src.profile; px = T.a
    if src.nodata is not None:
        dem[dem == src.nodata] = np.nan
nod = np.isnan(dem)
demf = dem[tuple(ndi.distance_transform_edt(nod, return_distances=False, return_indices=True))]
gy, gx = np.gradient(ndi.gaussian_filter(demf, 1.0), px)
slope = np.degrees(np.arctan(np.hypot(gx, gy)))
tmp = OUT + "_tmp_dem.tif"
p2 = profile.copy(); p2.update(dtype="float32", nodata=-9999.0)
with rasterio.open(tmp, "w", **p2) as dst:
    dst.write(demf.astype("float32"), 1)
grid = Grid.from_raster(tmp); d = grid.read_raster(tmp)
infl = grid.resolve_flats(grid.fill_depressions(grid.fill_pits(d)))
fdir = grid.flowdir(infl); acc = grid.accumulation(fdir)
hand = lambda km2: np.asarray(grid.compute_hand(fdir, infl, acc > km2 * 1e6 / (px * px)), dtype=float)
h = hand(STREAM_KM2); h = np.where(np.isfinite(h), h, hand(1.0))
w = int(round(8000 / px)) | 1
h = np.where(np.isfinite(h), h, demf - ndi.gaussian_filter(ndi.minimum_filter(demf, size=w), w / 4))
os.remove(tmp)

# Landsat 8/9 grid and tests
with rasterio.open(RAW + "OLIonly_p90_2013_2025.tif") as s:
    a = s.read().astype("float32"); a[a == -32768] = np.nan
    D = {int(n[-4:]): a[i] / 1e4 for i, n in enumerate(s.descriptions)}; LT, lshape = s.transform, s.shape
E_, L_ = (2013, 2014, 2015), (2023, 2024, 2025)
strict = np.all([D[y] >= .35 for y in E_], 0) & np.all([D[y] < .25 for y in L_], 0)
me, ml = np.median([D[y] for y in E_], 0), np.median([D[y] for y in L_], 0)
drop = (me >= .45) & (ml < .40) & (me - ml >= .20)
aoi_utm = gpd.GeoSeries([box(*AOI)], crs=4326).to_crs(crs).iloc[0]
aoi_dem = rasterize([(aoi_utm, 1)], out_shape=dem.shape, transform=T) == 1
st4, st8 = ndi.generate_binary_structure(2, 1), np.ones((3, 3), bool)


def to_landsat(mask):
    out = np.zeros(lshape, "uint8")
    reproject(mask.astype("uint8"), out, src_transform=T, src_crs=crs, dst_transform=LT, dst_crs=crs, resampling=Resampling.nearest)
    return out == 1


def delineate(slope_max, hand_min):
    core = (slope < slope_max) & (h > hand_min) & (demf < ELEV_MAX) & ~nod
    lab, n = ndi.label(ndi.binary_opening(core, structure=ndi.iterate_structure(st4, OPEN_R)))
    area = ndi.sum(np.ones_like(lab), lab, np.arange(1, n + 1)) * px * px / 1e6
    keep = ndi.binary_dilation(np.r_[False, area >= MIN_KM2][lab], structure=st4, iterations=OPEN_R, mask=core)
    mask = ndi.binary_fill_holes(keep)
    lab, n = ndi.label(mask)
    terr = np.zeros(mask.shape, bool); flat = np.zeros(mask.shape, bool); nt = 0
    for i, sl in enumerate(ndi.find_objects(lab), 1):
        r0, r1 = max(sl[0].start - RING_PX - 1, 0), min(sl[0].stop + RING_PX + 1, mask.shape[0])
        c0, c1 = max(sl[1].start - RING_PX - 1, 0), min(sl[1].stop + RING_PX + 1, mask.shape[1])
        comp = lab[r0:r1, c0:c1] == i
        if comp.sum() * px * px / 1e6 < MIN_KM2:
            continue
        ring = ndi.binary_dilation(comp, structure=st8, iterations=RING_PX) & ~comp & ~mask[r0:r1, c0:c1]
        if ring.sum() == 0:
            continue
        if (slope[r0:r1, c0:c1][ring] > SCARP_DEG).mean() >= SCARP_MIN:
            terr[r0:r1, c0:c1] |= comp; nt += (comp & aoi_dem[r0:r1, c0:c1]).any()
        else:
            flat[r0:r1, c0:c1] |= comp
    return terr & aoi_dem, flat & aoi_dem, int(nt)


base_t = None
rows = []
for sm in (3.0, 4.0, 5.0):
    for hm in (10.0, 15.0, 20.0):
        t, f, nt = delineate(sm, hm)
        tl, fl = to_landsat(t), to_landsat(f)
        if (sm, hm) == (4.0, 15.0):
            base_t = tl
        rows.append(dict(slope_max_deg=sm, hand_min_m=hm, terraces=nt, terrace_km2=tl.sum() * HA / 100,
                         strict_ha=strict[tl].sum() * HA, strict_pct=strict[tl].mean() * 100,
                         strict_pct_other_flat=strict[fl].mean() * 100,
                         drop_ha=drop[tl].sum() * HA, drop_pct=drop[tl].mean() * 100, drop_pct_other_flat=drop[fl].mean() * 100,
                         _mask=tl))
for r in rows:
    m = r.pop("_mask")
    r["overlap_with_base_terraces"] = (m & base_t).sum() / (m | base_t).sum()
    r["strict_ratio_vs_other_flat"] = r["strict_pct"] / max(r["strict_pct_other_flat"], 1e-9)
    r["drop_ratio_vs_other_flat"] = r["drop_pct"] / max(r["drop_pct_other_flat"], 1e-9)
tab = pd.DataFrame(rows)
tab.round(3).to_csv(OUT + "delineation_sensitivity.csv", index=False)
pd.set_option("display.width", 250)
print(tab.round(2).to_string(index=False))
