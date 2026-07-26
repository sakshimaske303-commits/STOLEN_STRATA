import geopandas as gpd

gdf = gpd.read_file('data/processed/karewa_bare_earth_change.gpkg')

total_terrace_area_km2 = gdf['area_km2'].sum()
print(f"Total mapped karewa terrace area (201 polygons): {total_terrace_area_km2:.2f} km2 "
      f"({total_terrace_area_km2*100:.1f} hectares)")

# Bare-earth area in each period = polygon area * bare fraction, summed across all polygons
bare_area_1994_km2 = (gdf['area_km2'] * gdf['bare_frac_1994']).sum()
bare_area_2025_km2 = (gdf['area_km2'] * gdf['bare_frac_2025']).sum()
area_converted_km2 = bare_area_2025_km2 - bare_area_1994_km2

print(f"\nBare-earth area in 1994: {bare_area_1994_km2:.3f} km2 ({bare_area_1994_km2*100:.1f} ha)")
print(f"Bare-earth area in 2025: {bare_area_2025_km2:.3f} km2 ({bare_area_2025_km2*100:.1f} ha)")
print(f"Net karewa area converted to bare-earth (1994-2025): {area_converted_km2:.3f} km2 "
      f"({area_converted_km2*100:.1f} hectares)")

pct_of_total = 100 * area_converted_km2 / total_terrace_area_km2
print(f"This represents {pct_of_total:.1f}% of the total mapped karewa terrace area (201 polygons)")

# Also break it down just for the 25 flagged "likely_degraded" polygons
degraded = gdf[gdf['status'] == 'likely_degraded']
degraded_area_km2 = degraded['area_km2'].sum()
degraded_bare_converted_km2 = (degraded['area_km2'] * degraded['bare_frac_change']).sum()
print(f"\nWithin the 25 flagged 'likely_degraded' polygons "
      f"(total area {degraded_area_km2:.2f} km2 / {degraded_area_km2*100:.1f} ha):")
print(f"  Area converted to bare-earth within these: {degraded_bare_converted_km2:.3f} km2 "
      f"({degraded_bare_converted_km2*100:.1f} hectares)")