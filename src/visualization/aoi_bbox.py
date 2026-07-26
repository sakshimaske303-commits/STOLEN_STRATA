import geopandas as gpd
from shapely.geometry import box

# Study area bounding box (from project brief)
minx, maxx = 74.75, 75.15
miny, maxy = 33.85, 34.15

aoi = gpd.GeoDataFrame(
    {"name": ["Study Area AOI"]},
    geometry=[box(minx, miny, maxx, maxy)],
    crs="EPSG:4326",
)
aoi.to_file("data/processed/aoi_bbox.gpkg", driver="GPKG")
print("Saved AOI rectangle to data/processed/aoi_bbox.gpkg")