"""Settlement-proximity test, parallel to 09_road_proximity.py — same terrace
polygons, same Mann-Whitney design, this time against OSM building footprints
instead of the road network. Building data came from 14a (run locally, no
internet in this environment)."""

import geopandas as gpd
from scipy.stats import mannwhitneyu

buildings = gpd.read_file("data/processed/settlement_footprints_osm.gpkg")
buildings = buildings.to_crs("EPSG:32643")
buildings_union = buildings.geometry.union_all()
print(f"Loaded {len(buildings)} building footprints")

gdf = gpd.read_file("data/processed/karewa_road_proximity.gpkg")  # already has status, dist_to_road_m

gdf["dist_to_settlement_m"] = gdf.geometry.apply(lambda g: g.distance(buildings_union))

print("\n--- Distance to nearest building (meters), by degradation status ---")
print(gdf.groupby("status")["dist_to_settlement_m"].describe())

intact_dist = gdf[gdf["status"] == "intact"]["dist_to_settlement_m"]
degraded_dist = gdf[gdf["status"] == "likely_degraded"]["dist_to_settlement_m"]

stat, p_value = mannwhitneyu(degraded_dist, intact_dist, alternative="less")
print(f"\nMann-Whitney U test (degraded vs intact settlement-distance): p = {p_value:.4f}")
if p_value < 0.05:
    print("Degraded terraces are significantly closer to settlements than intact terraces (p < 0.05)")
else:
    print("Difference is not statistically significant at the 0.05 level")

gdf.to_file("data/processed/karewa_settlement_proximity.gpkg", driver="GPKG")
print("\nSaved to data/processed/karewa_settlement_proximity.gpkg")

print(f"\nMean dist degraded: {degraded_dist.mean():.1f} m (median {degraded_dist.median():.1f} m)")
print(f"Mean dist intact:    {intact_dist.mean():.1f} m (median {intact_dist.median():.1f} m)")
