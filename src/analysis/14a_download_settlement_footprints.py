"""14a_download_settlement_footprints.py — run locally, needs live internet (Overpass)."""
import osmnx as ox
import geopandas as gpd

# Same AOI as 09_road_proximity.py
north, south, east, west = 34.15, 33.85, 75.15, 74.75

print("Downloading building footprints from OpenStreetMap...")
tags = {"building": True}
buildings = ox.features_from_bbox(bbox=(west, south, east, north), tags=tags)
buildings = buildings[buildings.geometry.type.isin(["Polygon", "MultiPolygon", "Point"])]
print(f"Downloaded {len(buildings)} building footprints")

buildings = buildings[["geometry"]].reset_index(drop=True)
buildings.to_file("data/processed/settlement_footprints_osm.gpkg", driver="GPKG")
print("Saved data/processed/settlement_footprints_osm.gpkg")
