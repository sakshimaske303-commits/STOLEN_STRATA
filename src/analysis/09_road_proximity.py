import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import config

import osmnx as ox
import geopandas as gpd
import numpy as np

# Same AOI as before
north, south, east, west = config.AOI_NORTH, config.AOI_SOUTH, config.AOI_EAST, config.AOI_WEST

print("Downloading road network from OpenStreetMap...")
roads_graph = ox.graph_from_bbox(bbox=(west, south, east, north), network_type='drive')
roads_gdf = ox.graph_to_gdfs(roads_graph, nodes=False, edges=True)
print(f"Downloaded {len(roads_gdf)} road segments")

# Reproject roads to match terrace polygons' CRS
roads_gdf = roads_gdf.to_crs(config.DST_CRS)
roads_union = roads_gdf.geometry.union_all()

# Load terrace polygons
gdf = gpd.read_file('data/processed/karewa_multitemporal_trend.gpkg')

# Distance from each terrace to the nearest road
gdf['dist_to_road_m'] = gdf.geometry.apply(lambda g: g.distance(roads_union))

print("\n--- Distance to nearest road (meters), by degradation status ---")
print(gdf.groupby('status')['dist_to_road_m'].describe())

gdf.to_file('data/processed/karewa_road_proximity.gpkg', driver='GPKG')
print("\nSaved to data/processed/karewa_road_proximity.gpkg")

from scipy.stats import mannwhitneyu

intact_dist = gdf[gdf['status'] == 'intact']['dist_to_road_m']
degraded_dist = gdf[gdf['status'] == 'likely_degraded']['dist_to_road_m']

stat, p_value = mannwhitneyu(degraded_dist, intact_dist, alternative='less')
print(f"\nMann-Whitney U test (degraded vs intact road-distance): p = {p_value:.4f}")
if p_value < 0.05:
    print("Degraded terraces are significantly closer to roads than intact terraces (p < 0.05)")
else:
    print("Difference is not statistically significant at the 0.05 level")