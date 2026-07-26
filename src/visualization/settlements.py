import geopandas as gpd
from shapely.geometry import Point

settlements = {
    "name": ["Pampore", "Pulwama", "Budgam", "Srinagar"],
    "geometry": [
        Point(74.9203, 33.9331),
        Point(74.8992, 33.8712),
        Point(74.7300, 34.0186),
        Point(74.7973, 34.0837),
    ],
}

gdf = gpd.GeoDataFrame(settlements, crs="EPSG:4326")
gdf.to_file("data/processed/settlements.gpkg", driver="GPKG")
print("Saved settlement points to data/processed/settlements.gpkg")