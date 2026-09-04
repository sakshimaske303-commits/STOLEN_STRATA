import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import config

import osmnx as ox
import geopandas as gpd

# Same bbox used in script 09
north, south, east, west = config.AOI_NORTH, config.AOI_SOUTH, config.AOI_EAST, config.AOI_WEST

G = ox.graph_from_bbox(bbox=(west, south, east, north), network_type="drive")
edges = ox.graph_to_gdfs(G, nodes=False, edges=True)

edges = edges.reset_index()[["geometry"]]
edges.to_file("data/processed/road_network.gpkg", driver="GPKG")
print(f"Saved {len(edges)} road segments to data/processed/road_network.gpkg")