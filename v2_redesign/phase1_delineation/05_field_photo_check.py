"""Ground check: where my four field photographs at Lethpora fall on the terrace map and on the flagged land.

The photographs were taken on 3 September 2026 with a GPS camera app that prints the position on each image
(field_photos/lethpora_01.jpg to lethpora_04.jpg); the coordinates below are read off those prints.
They are one place on one day, so this is a ground check of one spot, not a validation of the map.

I run it from the repo root:  python v2_redesign/phase1_delineation/05_field_photo_check.py
Uses the terrace and flagged-land layers of the dashboard (dashboard/map_data/terraces.geojson, flagged.geojson).
Output: v2_redesign/phase1_delineation/field_photo_check.csv
"""
import csv
import json
import math

PHOTOS = [("lethpora_01.jpg", 33.973730, 74.951189), ("lethpora_02.jpg", 33.973596, 74.951186),
          ("lethpora_03.jpg", 33.973788, 74.951186), ("lethpora_04.jpg", 33.973365, 74.950956)]
M_LAT = 110_900                                    # metres per degree of latitude at 34 N
M_LON = 111_320 * math.cos(math.radians(33.97))    # metres per degree of longitude at 34 N


def polygons(geom):
    return [geom["coordinates"]] if geom["type"] == "Polygon" else geom["coordinates"]


def in_ring(x, y, ring):
    inside = False
    for (x1, y1), (x2, y2) in zip(ring, ring[1:] + ring[:1]):
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            inside = not inside
    return inside


def contains(geom, x, y):
    return any(in_ring(x, y, p[0]) and not any(in_ring(x, y, h) for h in p[1:]) for p in polygons(geom))


def to_edge_m(geom, x, y):
    best = float("inf")
    for p in polygons(geom):
        for ring in p:
            for (x1, y1), (x2, y2) in zip(ring, ring[1:] + ring[:1]):
                ax, ay, bx, by = (x1 - x) * M_LON, (y1 - y) * M_LAT, (x2 - x) * M_LON, (y2 - y) * M_LAT
                dx, dy = bx - ax, by - ay
                t = 0 if dx == dy == 0 else max(0, min(1, -(ax * dx + ay * dy) / (dx * dx + dy * dy)))
                best = min(best, math.hypot(ax + t * dx, ay + t * dy))
    return best


terr = json.load(open("dashboard/map_data/terraces.geojson"))["features"]
flag = {f["properties"]["test"]: f["geometry"] for f in json.load(open("dashboard/map_data/flagged.geojson"))["features"]}
rows = []
for name, lat, lon in PHOTOS:
    t = [f for f in terr if contains(f["geometry"], lon, lat)]
    row = dict(photo=name, lat=lat, lon=lon, date="2026-09-03",
               terrace_id=t[0]["properties"]["terrace_id"] if t else "",
               terrace_km2=t[0]["properties"]["area_km2"] if t else "",
               m_inside_terrace_edge=round(to_edge_m(t[0]["geometry"], lon, lat)) if t else "",
               on_strict=contains(flag["strict"], lon, lat), on_drop_only=contains(flag["drop_only"], lon, lat),
               m_to_strict=round(to_edge_m(flag["strict"], lon, lat)), m_to_drop_only=round(to_edge_m(flag["drop_only"], lon, lat)))
    rows.append(row)
    print(row)
with open("v2_redesign/phase1_delineation/field_photo_check.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
