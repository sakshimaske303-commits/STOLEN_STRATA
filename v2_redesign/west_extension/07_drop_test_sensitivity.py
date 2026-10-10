"""v2 extended box — sensitivity of the drop test to its three cut-offs (early >= 0.45, late < 0.40, fall >= 0.20).
Also splits the result by the accuracy strata so the reference labels can be re-used for nearby settings.

I run it from the repo root:  python v2_redesign/west_extension/07_drop_test_sensitivity.py
"""
import itertools
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from rasterio.features import rasterize

RAW = "data/raw/StolenStrata_v2w_"; OUT = "v2_redesign/west_extension/"; HA = 0.09
with rasterio.open(RAW + "OLIonly_p90_2013_2025.tif") as s:
    a = s.read().astype("float32"); a[a == -32768] = np.nan
    D = {int(n[-4:]): a[i] / 1e4 for i, n in enumerate(s.descriptions)}; T, crs, shape = s.transform, s.crs, s.shape
t = gpd.read_file(OUT + "karewa_terraces_wide.gpkg").to_crs(crs)
p = gpd.read_file(OUT + "karewa_flat_tops_wide.gpkg").to_crs(crs)
tid = rasterize([(g, int(i)) for g, i in zip(t.geometry, t.terrace_id)], out_shape=shape, transform=T)
mt = tid > 0
mf = (rasterize([(g, 1) for g in p.geometry], out_shape=shape, transform=T) == 1) & ~mt
me = np.median([D[y] for y in (2013, 2014, 2015)], 0); ml = np.median([D[y] for y in (2023, 2024, 2025)], 0)
top = np.isin(tid, (9, 3))            # Rangeen Kultreh terraces
rows = []
for emin, lmax, dmin in itertools.product((0.40, 0.45, 0.50), (0.35, 0.40, 0.45), (0.15, 0.20, 0.25)):
    c = (me >= emin) & (ml < lmax) & (me - ml >= dmin)
    r = (ml >= emin) & (me < lmax) & (ml - me >= dmin)
    per = pd.Series(tid[c & mt]).value_counts() * HA
    rows.append(dict(early_min=emin, late_max=lmax, fall_min=dmin, terraces_drop_ha=c[mt].sum() * HA, terraces_reverse_ha=r[mt].sum() * HA,
                     terraces_net_ha=(c[mt].sum() - r[mt].sum()) * HA, terraces_pct=c[mt].mean() * 100, other_flat_pct=c[mf].mean() * 100,
                     ratio_vs_other_flat=c[mt].mean() / max(c[mf].mean(), 1e-9), terraces_with_1ha=int((per >= 1).sum()),
                     share_on_rangeen_kultreh=c[top].sum() / max(c[mt].sum(), 1)))
tab = pd.DataFrame(rows)
tab.round(3).to_csv(OUT + "drop_test_sensitivity.csv", index=False)
pd.set_option("display.width", 250)
print(tab.round(2).to_string(index=False))
print("net ha range: %.0f - %.0f | ratio range: %.1f - %.1f" % (tab.terraces_net_ha.min(), tab.terraces_net_ha.max(), tab.ratio_vs_other_flat.min(), tab.ratio_vs_other_flat.max()))
