"""v2 extended box — the long view, 1993-2025, one sensor family (Landsat 5/7/8/9, 8/9 adjusted to ETM+).

The 2008-2025 stack is the corrected export of gee_05_long_series_fixed.js (October 2026); the earlier
export of gee_04_extended_box.js applied the Landsat 8/9 adjustment in the reverse direction.

(a) how much terrace land had a low yearly peak NDVI in each period (3-year median of p90 below 0.35 / 0.30);
(b) the drop test run from the 1990s to today.
Only years with a median of >= 10 clear observations on terraces are used.

Run from the repo root:  python v2_redesign/west_extension/08_long_series_wide.py
"""
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from rasterio.features import rasterize
from rasterio.warp import transform as warp_xy
from shapely.geometry import box

RAW = "data/raw/StolenStrata_v2w_"; OUT = "v2_redesign/west_extension/"; HA = 0.09


def load(name, scale=1e4):
    with rasterio.open(RAW + name) as s:
        a = s.read().astype("float32"); a[a == -32768] = np.nan
        return s.transform, s.crs, s.shape, {int(d[-4:]): a[i] / scale for i, d in enumerate(s.descriptions)}


T, crs, shape, LS = load("LS_p90_1990_2007.tif")
LS.update(load("LS_p90_2008_2025_fixed.tif")[3])   # Landsat 8/9 adjusted OLI -> ETM+ (gee_05_long_series_fixed.js)
CNT = load("LS_counts_1990_2025.tif", 1)[3]
t = gpd.read_file(OUT + "karewa_terraces_wide.gpkg").to_crs(crs)
p = gpd.read_file(OUT + "karewa_flat_tops_wide.gpkg").to_crs(crs)
tid = rasterize([(g, int(i)) for g, i in zip(t.geometry, t.terrace_id)], out_shape=shape, transform=T); mt = tid > 0
mf = (rasterize([(g, 1) for g in p.geometry], out_shape=shape, transform=T) == 1) & ~mt
usable = [y for y in range(1990, 2026) if np.median(CNT[y][mt]) >= 10]


def window(lon0, lat0, lon1, lat1):
    g = gpd.GeoSeries([box(lon0, lat0, lon1, lat1)], crs=4326).to_crs(crs).iloc[0]
    return rasterize([(g, 1)], out_shape=shape, transform=T) == 1


SITES = {"all terraces": mt, "Rangeen Kultreh terraces": mt & window(74.83, 33.925, 74.87, 33.958),
         "Bandagam-Batapora terraces": mt & window(74.60, 33.99, 74.72, 34.05),
         "other terraces": mt & ~window(74.83, 33.925, 74.87, 33.958) & ~window(74.60, 33.99, 74.72, 34.05),
         "other flat land": mf}
PERIODS = {"1993-1998": (1993, 1994, 1998), "1999-2002": (1999, 2000, 2002), "2003-2007": (2003, 2005, 2007), "2008-2012": (2008, 2010, 2012),
           "2013-2015": (2013, 2014, 2015), "2018-2020": (2018, 2019, 2020), "2023-2025": (2023, 2024, 2025)}
for k, ys in PERIODS.items():
    assert all(y in usable for y in ys), (k, usable)
MED = {k: np.median([LS[y] for y in ys], 0) for k, ys in PERIODS.items()}

rows = []
for site, m in SITES.items():
    for k in PERIODS:
        v = MED[k][m]
        rows.append(dict(site=site, site_km2=m.sum() * HA / 100, period=k, median_p90=float(np.nanmedian(v)),
                         below_035_ha=(v < .35).sum() * HA, below_035_pct=(v < .35).mean() * 100,
                         below_030_ha=(v < .30).sum() * HA, below_030_pct=(v < .30).mean() * 100))
stock = pd.DataFrame(rows)
stock.round(3).to_csv(OUT + "long_series_low_ndvi_stock.csv", index=False)

rows = []
for e, l in [("1993-1998", "2023-2025"), ("1993-1998", "2008-2012"), ("2008-2012", "2023-2025"), ("2013-2015", "2023-2025")]:
    a, b = MED[e], MED[l]
    c = (a >= .45) & (b < .40) & (a - b >= .20); r = (b >= .45) & (a < .40) & (b - a >= .20)
    for site, m in SITES.items():
        rows.append(dict(early=e, late=l, site=site, drop_ha=c[m].sum() * HA, reverse_ha=r[m].sum() * HA, net_ha=(c[m].sum() - r[m].sum()) * HA,
                         drop_pct=c[m].mean() * 100, reverse_pct=r[m].mean() * 100))
dl = pd.DataFrame(rows)
dl.round(3).to_csv(OUT + "long_series_drop_test.csv", index=False)
pd.set_option("display.width", 250)
print("usable years:", usable)
print(stock.pivot(index="site", columns="period", values="below_035_ha").round(0).to_string())
print(stock.pivot(index="site", columns="period", values="below_035_pct").round(2).to_string())
print(stock.pivot(index="site", columns="period", values="median_p90").round(2).to_string())
print(dl.round(2).to_string(index=False))
