import geopandas as gpd

gdf = gpd.read_file('data/processed/karewa_saffron_overlay.gpkg')
saffron = gdf[gdf['likely_saffron'] == True]

total_area_ha = saffron.geometry.area.sum() / 10000
print(f"Total detected saffron-signature area: {total_area_ha:.1f} hectares")
print(f"FAO GIAHS 2012 baseline: 3200 hectares")
print(f"Apparent shortfall: {3200 - total_area_ha:.1f} hectares ({100*(3200-total_area_ha)/3200:.1f}%)")