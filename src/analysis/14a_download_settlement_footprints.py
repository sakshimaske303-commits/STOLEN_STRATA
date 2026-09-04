"""14a_download_settlement_footprints.py — run locally, needs live internet (Overpass)."""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import config

import osmnx as ox
import geopandas as gpd

# Same AOI as 09_road_proximity.py
north, south, east, west = config.AOI_NORTH, config.AOI_SOUTH, config.AOI_EAST, config.AOI_WEST

print("Downloading building footprints from OpenStreetMap...")
tags = {"building": True}
buildings = ox.features_from_bbox(bbox=(west, south, east, north), tags=tags)
buildings = buildings[buildings.geometry.type.isin(["Polygon", "MultiPolygon", "Point"])]
print(f"Downloaded {len(buildings)} building footprints")

buildings = buildings[["geometry"]].reset_index(drop=True)
buildings.to_file("data/processed/settlement_footprints_osm.gpkg", driver="GPKG")
print("Saved data/processed/settlement_footprints_osm.gpkg")
