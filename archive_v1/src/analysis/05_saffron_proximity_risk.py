import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import config

import geopandas as gpd

gdf = gpd.read_file('data/processed/karewa_saffron_overlay.gpkg')

saffron = gdf[gdf['likely_saffron'] == True].copy()
degraded = gdf[gdf['status'] == 'likely_degraded'].copy()

print(f"Saffron polygons: {len(saffron)}, Degraded polygons: {len(degraded)}")

degraded_union = degraded.geometry.union_all()
saffron['dist_to_nearest_degraded_m'] = saffron.geometry.apply(lambda g: g.distance(degraded_union))

print(saffron['dist_to_nearest_degraded_m'].describe())

near_threshold_m = config.SAFFRON_RISK_DISTANCE_M  # 1 km — tune after seeing describe()
saffron['at_risk'] = saffron['dist_to_nearest_degraded_m'] <= near_threshold_m
print(saffron['at_risk'].value_counts())

saffron.to_file('data/processed/saffron_proximity_risk.gpkg', driver='GPKG')
print("Saved to data/processed/saffron_proximity_risk.gpkg")

print("\n--- Sensitivity check across distance thresholds ---")
for threshold_m in [500, 750, 1000, 1500, 2000, 2500]:
    at_risk_count = (saffron['dist_to_nearest_degraded_m'] <= threshold_m).sum()
    pct = 100 * at_risk_count / len(saffron)
    print(f"Within {threshold_m}m: {at_risk_count}/{len(saffron)} ({pct:.0f}%)")