import osmnx as ox
import geopandas as gpd

# Same bbox jo script 09 mein use ki thi
north, south, east, west = 34.15, 33.85, 75.15, 74.75

G = ox.graph_from_bbox(bbox=(west, south, east, north), network_type="drive")
edges = ox.graph_to_gdfs(G, nodes=False, edges=True)

edges = edges.reset_index()[["geometry"]]
edges.to_file("data/processed/road_network.gpkg", driver="GPKG")
print(f"Saved {len(edges)} road segments to data/processed/road_network.gpkg")