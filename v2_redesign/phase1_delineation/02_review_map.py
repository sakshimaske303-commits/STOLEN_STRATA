"""v2 Phase 1 — interactive review map + checklist for the prototype flat-top polygons.

Builds (in v2_redesign/phase1_delineation/):
  review_map.html       satellite map; open in a browser (needs internet for the imagery)
  review_checklist.csv  the polygons that need a human decision; fill in `my_label`

Run from the repo root:  python v2_redesign/phase1_delineation/02_review_map.py
"""
import os
import folium
import geopandas as gpd
from shapely.geometry import box

OUT_DIR = "v2_redesign/phase1_delineation"
AOI_LONLAT = (74.75, 33.85, 75.15, 34.15)
REVIEW_REJECTED_MIN_KM2 = 1.0     # big rejected polygons are worth a second look
COLORS = {"scarp_bounded": "#FFD400", "ambiguous": "#FF7A00", "rejected": "#B0B7BF"}
LABELS = {"scarp_bounded": "Scarp-bounded (karewa-like)", "ambiguous": "Ambiguous — REVIEW",
          "rejected": "Rejected (fan / valley fill)"}

g = gpd.read_file(os.path.join(OUT_DIR, "karewa_flat_tops_prototype.gpkg"))
g["review"] = (g["cls"] == "ambiguous") | ((g["cls"] == "rejected") & (g["area_km2"] >= REVIEW_REJECTED_MIN_KM2))
pts = g.representative_point().to_crs(4326)
g["lat"], g["lon"] = pts.y.round(5), pts.x.round(5)
w = g.to_crs(4326)
for c in ["area_km2", "scarp_frac", "mean_elev", "mean_hand", "mean_slope", "share_in_aoi"]:
    w[c] = w[c].round(2)

m = folium.Map(location=[34.0, 74.95], zoom_start=11, tiles=None, control_scale=True)
folium.TileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
                 attr="Esri World Imagery", name="Satellite (Esri)", max_zoom=19).add_to(m)
folium.TileLayer("https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}", attr="Google", name="Satellite + labels (Google)",
                 max_zoom=20, show=False).add_to(m)
folium.TileLayer("OpenStreetMap", name="OpenStreetMap", show=False).add_to(m)

folium.GeoJson(gpd.GeoSeries([box(*AOI_LONLAT)], crs=4326), name="Study-area box",
               style_function=lambda f: {"fillOpacity": 0, "color": "#00E5FF", "weight": 2, "dashArray": "6,4"}).add_to(m)

fields = ["terrace_id", "cls", "area_km2", "scarp_frac", "mean_elev", "mean_hand", "mean_slope", "share_in_aoi"]
aliases = ["Terrace ID", "Class", "Area (km²)", "Scarp share of boundary", "Mean elevation (m)",
           "Mean height above drainage (m)", "Mean slope (°)", "Share inside study box"]
for cls in ["rejected", "scarp_bounded", "ambiguous"]:
    sub = w[w["cls"] == cls]
    folium.GeoJson(
        sub[fields + ["geometry"]], name=f"{LABELS[cls]} ({len(sub)})",
        style_function=lambda f, c=COLORS[cls]: {"color": c, "weight": 2.5, "fillColor": c, "fillOpacity": 0.12},
        highlight_function=lambda f: {"weight": 4, "fillOpacity": 0.3},
        tooltip=folium.GeoJsonTooltip(fields=fields, aliases=aliases),
    ).add_to(m)

lab = folium.FeatureGroup(name="ID labels for polygons to review")
for _, r in w[w["review"]].iterrows():
    folium.Marker([r["lat"], r["lon"]], icon=folium.DivIcon(html=(
        f'<div style="font:bold 13px sans-serif;color:#fff;background:{COLORS[r["cls"]] if r["cls"]=="ambiguous" else "#5f6770"};'
        f'border:1px solid #000;border-radius:10px;padding:1px 6px;white-space:nowrap;'
        f'transform:translate(-50%,-50%);display:inline-block">{r["terrace_id"]}</div>'))).add_to(lab)
lab.add_to(m)

legend = "".join(f'<div><span style="display:inline-block;width:14px;height:14px;background:{COLORS[k]};'
                 f'border:1px solid #000;margin-right:6px"></span>{LABELS[k]}</div>' for k in COLORS)
m.get_root().html.add_child(folium.Element(
    f'<div style="position:fixed;bottom:28px;left:12px;z-index:9999;background:#fff;padding:10px 12px;'
    f'border-radius:6px;box-shadow:0 1px 5px rgba(0,0,0,.4);font:13px sans-serif"><b>Prototype flat tops</b>{legend}'
    f'<div style="margin-top:4px;color:#555">Numbered badges = polygons to review</div></div>'))
folium.LayerControl(collapsed=False).add_to(m)
m.save(os.path.join(OUT_DIR, "review_map.html"))

chk = g[g["review"]].sort_values(["cls", "area_km2"], ascending=[True, False])
chk = chk[["terrace_id", "cls", "area_km2", "scarp_frac", "mean_elev", "share_in_aoi", "lat", "lon"]].round(2)
chk["lat"], chk["lon"] = g.loc[chk.index, "lat"], g.loc[chk.index, "lon"]
chk["google_maps"] = "https://www.google.com/maps/@" + chk["lat"].astype(str) + "," + chk["lon"].astype(str) + ",2500m/data=!3m1!1e3"
chk["my_label"] = ""      # karewa / not_karewa / unsure
chk["notes"] = ""
chk.to_csv(os.path.join(OUT_DIR, "review_checklist.csv"), index=False)
print(f"saved review_map.html and review_checklist.csv ({len(chk)} polygons to review: "
      f"{(chk.cls=='ambiguous').sum()} ambiguous, {(chk.cls=='rejected').sum()} large rejected)")
