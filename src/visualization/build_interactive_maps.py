"""build_interactive_maps.py — folium exports for the dashboard's Interactive Maps page."""
import os
import folium
import geopandas as gpd
import branca.colormap as cm

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "outputs", "interactive_maps")
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data", "processed")

MAROON = "#8B1E3F"
GOLD = "#D4AF37"
TEAL = "#2EC4B6"
CREAM = "#F5F1E8"

def gp(name):
    return gpd.read_file(os.path.join(DATA_DIR, name))

def save(fmap, folder):
    d = os.path.join(OUT_DIR, folder)
    os.makedirs(d, exist_ok=True)
    fmap.save(os.path.join(d, "index.html"))
    print(f"saved {folder}/index.html")

def base_map(center=[33.99, 74.95], zoom=11):
    return folium.Map(location=center, zoom_start=zoom, tiles="CartoDB positron", control_scale=True)

def status_style(feature):
    s = feature["properties"]["status"]
    return {"fillColor": MAROON if s == "likely_degraded" else TEAL, "color": MAROON if s == "likely_degraded" else "#1a7a70", "weight": 1, "fillOpacity": 0.55}

def terrace_popup_fields(gdf):
    fields = ["terrace_candidate", "status", "area_km2", "bare_frac_2025"]
    aliases = ["Terrace #", "Status", "Area (km²)", "Bare-earth 2025"]
    return folium.GeoJsonPopup(fields=fields, aliases=aliases, localize=True)

# ============================================================
# 01 — Study area overview
# ============================================================
def build_01_study_area_overview():
    aoi = gp("aoi_bbox.gpkg")
    districts = gp("kashmir_3districts.gpkg")
    terraces = gp("karewa_final_with_geomorphometrics.gpkg").to_crs(4326)

    m = base_map()
    folium.GeoJson(districts, name="Districts", style_function=lambda f: {"fillColor": "none", "color": GOLD, "weight": 2, "dashArray": "4,3"},
                    tooltip=folium.GeoJsonTooltip(fields=["DISTRICT"], aliases=["District"])).add_to(m)
    folium.GeoJson(aoi, name="Study Area (AOI)", style_function=lambda f: {"fillColor": "none", "color": MAROON, "weight": 3}).add_to(m)
    folium.GeoJson(terraces, name="201 Candidate Terraces", style_function=lambda f: {"fillColor": TEAL, "color": "#1a7a70", "weight": 0.6, "fillOpacity": 0.5},
                    tooltip=folium.GeoJsonTooltip(fields=["terrace_candidate", "area_km2"], aliases=["Terrace #", "Area (km²)"])).add_to(m)
    folium.LayerControl(collapsed=False).add_to(m)
    save(m, "01_study_area_overview")

# ============================================================
# 02 — Terrace degradation status
# ============================================================
def build_02_terrace_degradation_status():
    terraces = gp("karewa_final_with_geomorphometrics.gpkg").to_crs(4326)
    m = base_map()
    folium.GeoJson(terraces, name="Degradation Status", style_function=status_style,
                    popup=terrace_popup_fields(terraces),
                    tooltip=folium.GeoJsonTooltip(fields=["terrace_candidate", "status"], aliases=["Terrace #", "Status"])).add_to(m)
    legend = f"""
    <div style="position: fixed; bottom: 30px; left: 30px; z-index:9999; background: white; padding: 10px 14px; border-radius: 6px; box-shadow: 0 1px 4px rgba(0,0,0,0.3); font-size: 13px;">
    <b>Status</b><br>
    <span style="color:{MAROON};">&#9632;</span> Likely degraded (25)<br>
    <span style="color:{TEAL};">&#9632;</span> Intact (176)
    </div>"""
    m.get_root().html.add_child(folium.Element(legend))
    save(m, "02_terrace_degradation_status")

# ============================================================
# 03 — Delineated terrace boundaries
# ============================================================
def build_03_terrace_boundaries():
    terraces = gp("karewa_final_with_geomorphometrics.gpkg").to_crs(4326)
    m = base_map()
    folium.GeoJson(terraces, name="Terrace Boundaries", style_function=lambda f: {"fillColor": "none", "color": GOLD, "weight": 1.4},
                    popup=folium.GeoJsonPopup(fields=["terrace_candidate", "area_km2", "mean_elevation", "compactness"],
                                               aliases=["Terrace #", "Area (km²)", "Mean elevation (m)", "Compactness"], localize=True)).add_to(m)
    save(m, "03_terrace_boundaries")

# ============================================================
# 04 — Validation at Lethpora saffron fields
# ============================================================
def build_04_validation_lethpora():
    saffron = gp("karewa_saffron_overlay.gpkg").to_crs(4326)
    m = base_map(center=[33.9358, 74.9128], zoom=13)  # Lethpora, Pampore
    folium.GeoJson(saffron, name="Terraces", style_function=lambda f: {
        "fillColor": GOLD if f["properties"]["likely_saffron"] else "#cccccc",
        "color": "#8a6d1a" if f["properties"]["likely_saffron"] else "#999999",
        "weight": 1, "fillOpacity": 0.6 if f["properties"]["likely_saffron"] else 0.15},
        tooltip=folium.GeoJsonTooltip(fields=["terrace_candidate", "saffron_index", "likely_saffron"],
                                       aliases=["Terrace #", "Saffron index", "Likely saffron"])).add_to(m)
    save(m, "04_validation_lethpora")

# ============================================================
# 05 — Saffron proximity risk (rebuilt — fixes prior broken buffer symbology)
# ============================================================
def build_05_saffron_proximity_risk():
    saf = gp("saffron_proximity_risk.gpkg")
    degraded = gp("likely_degraded.gpkg")
    degraded_union = degraded.union_all()
    buffer_1km = gpd.GeoSeries([degraded_union.buffer(1000)], crs=degraded.crs).to_crs(4326)
    saf_wgs = saf.to_crs(4326)
    degraded_wgs = degraded.to_crs(4326)

    m = base_map()
    folium.GeoJson(buffer_1km, name="1 km Risk Buffer", style_function=lambda f: {"fillColor": MAROON, "color": MAROON, "weight": 1, "fillOpacity": 0.10, "dashArray": "5,4"}).add_to(m)
    folium.GeoJson(degraded_wgs, name="Degraded Terraces", style_function=lambda f: {"fillColor": MAROON, "color": MAROON, "weight": 1, "fillOpacity": 0.5}).add_to(m)
    folium.GeoJson(saf_wgs, name="Saffron Terraces", style_function=lambda f: {
        "fillColor": "#B8860B" if f["properties"]["at_risk"] else GOLD,
        "color": "#5c4508", "weight": 1.5, "fillOpacity": 0.75},
        tooltip=folium.GeoJsonTooltip(fields=["terrace_candidate", "dist_to_nearest_degraded_m", "at_risk"],
                                       aliases=["Terrace #", "Distance to degradation (m)", "Within 1km risk radius"])).add_to(m)
    folium.LayerControl(collapsed=False).add_to(m)
    save(m, "05_saffron_proximity_risk")

# ============================================================
# 06 — Road network proximity
# ============================================================
def build_06_road_network_proximity():
    roads = gp("road_network.gpkg")
    roads_simplified = roads.geometry.simplify(0.0001)
    roads_merged = gpd.GeoSeries([roads_simplified.union_all()], crs=roads.crs)  # one feature, not 44k — keeps the file browser-loadable
    terraces = gp("karewa_final_with_geomorphometrics.gpkg").to_crs(4326)

    m = base_map()
    folium.GeoJson(roads_merged, name="Road Network", style_function=lambda f: {"color": "#555555", "weight": 1}).add_to(m)
    folium.GeoJson(terraces, name="Terrace Status", style_function=status_style,
                    tooltip=folium.GeoJsonTooltip(fields=["terrace_candidate", "status", "dist_to_road_m"],
                                                   aliases=["Terrace #", "Status", "Distance to road (m)"])).add_to(m)
    folium.LayerControl(collapsed=False).add_to(m)
    save(m, "06_road_network_proximity")

# ============================================================
# 07 — Settlement / building-footprint proximity (new)
# ============================================================
def build_07_settlement_proximity():
    buildings = gp("settlement_footprints_osm.gpkg")
    terraces = gp("karewa_settlement_proximity.gpkg").to_crs(4326)

    m = base_map()
    folium.GeoJson(buildings, name="Building Footprints (3,266)", style_function=lambda f: {"fillColor": "#555555", "color": "#333333", "weight": 0.4, "fillOpacity": 0.6},
                    marker=folium.CircleMarker(radius=1.5, color="#333333", fill=True, fill_opacity=0.6)).add_to(m)
    folium.GeoJson(terraces, name="Terrace Status", style_function=status_style,
                    tooltip=folium.GeoJsonTooltip(fields=["terrace_candidate", "status", "dist_to_settlement_m"],
                                                   aliases=["Terrace #", "Status", "Distance to settlement (m)"])).add_to(m)
    folium.LayerControl(collapsed=False).add_to(m)
    save(m, "07_settlement_proximity")

# ============================================================
# 08 — Economic value-at-risk (new)
# ============================================================
def build_08_economic_value_at_risk():
    YIELD_KG_PER_HA = 5.27
    PRICE_PER_KG_RS = 272998
    saf = gp("saffron_proximity_risk.gpkg")
    saf["area_ha"] = saf.geometry.area / 10000
    saf["annual_value_rs"] = saf["area_ha"] * YIELD_KG_PER_HA * PRICE_PER_KG_RS
    saf["annual_value_lakh"] = (saf["annual_value_rs"] / 1e5).round(1)
    saf_wgs = saf.to_crs(4326)
    degraded = gp("likely_degraded.gpkg").to_crs(4326)

    colormap = cm.LinearColormap(colors=["#F5E6A8", MAROON], vmin=saf["annual_value_lakh"].min(), vmax=saf["annual_value_lakh"].max(),
                                  caption="Estimated annual saffron value (Rs lakh)")
    m = base_map()
    folium.GeoJson(degraded, name="Degraded Terraces", style_function=lambda f: {"fillColor": "#555555", "color": "#333333", "weight": 1, "fillOpacity": 0.35}).add_to(m)
    folium.GeoJson(saf_wgs, name="Saffron Value-at-Risk", style_function=lambda f: {
        "fillColor": colormap(f["properties"]["annual_value_lakh"]), "color": "#5c4508", "weight": 1.5, "fillOpacity": 0.85},
        tooltip=folium.GeoJsonTooltip(fields=["terrace_candidate", "area_ha", "annual_value_lakh", "at_risk"],
                                       aliases=["Terrace #", "Area (ha)", "Est. annual value (Rs lakh)", "Within 1km risk radius"])).add_to(m)
    colormap.add_to(m)
    folium.LayerControl(collapsed=False).add_to(m)
    save(m, "08_economic_value_at_risk")

if __name__ == "__main__":
    build_01_study_area_overview()
    build_02_terrace_degradation_status()
    build_03_terrace_boundaries()
    build_04_validation_lethpora()
    build_05_saffron_proximity_risk()
    build_06_road_network_proximity()
    build_07_settlement_proximity()
    build_08_economic_value_at_risk()
    print("\nAll 8 interactive maps built.")
