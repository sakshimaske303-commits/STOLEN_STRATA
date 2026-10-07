import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import config

import geopandas as gpd
from shapely.geometry import box

# Study area bounding box (from project brief)
minx, maxx = config.AOI_WEST, config.AOI_EAST
miny, maxy = config.AOI_SOUTH, config.AOI_NORTH

aoi = gpd.GeoDataFrame(
    {"name": ["Study Area AOI"]},
    geometry=[box(minx, miny, maxx, maxy)],
    crs="EPSG:4326",
)
aoi.to_file("data/processed/aoi_bbox.gpkg", driver="GPKG")
print("Saved AOI rectangle to data/processed/aoi_bbox.gpkg")