"""15_economic_valuation.py — saffron value-at-risk in rupees, not just hectares."""

import json
import geopandas as gpd

# Official 2024-25 J&K figures — J&K Legislative Assembly, Agriculture Production
# Dept, reply to MLA Hasnain Masoodi, Feb 2026 (Greater Kashmir / Kashmir Life).
STATEWIDE_PRODUCTION_KG = 19.58 * 1000
STATEWIDE_AREA_HA = 3715
STATEWIDE_VALUE_RS = 534.53 * 1e7

YIELD_KG_PER_HA = STATEWIDE_PRODUCTION_KG / STATEWIDE_AREA_HA          # ~5.27, matches official figure
PRICE_PER_KG_RS = STATEWIDE_VALUE_RS / STATEWIDE_PRODUCTION_KG         # implied, ~Rs 2.73 lakh/kg

# --- This study's detected saffron terraces (map4/5 output) ---
gdf = gpd.read_file("data/processed/saffron_proximity_risk.gpkg")
gdf["area_ha"] = gdf["area_km2"] * 100

total_ha = gdf["area_ha"].sum()
at_risk_ha = gdf.loc[gdf["at_risk"] == True, "area_ha"].sum()

def value_for_area(ha):
    kg = ha * YIELD_KG_PER_HA
    rs = kg * PRICE_PER_KG_RS
    return kg, rs

total_kg, total_value_rs = value_for_area(total_ha)
at_risk_kg, at_risk_value_rs = value_for_area(at_risk_ha)

results = {
    "yield_kg_per_ha": round(YIELD_KG_PER_HA, 3),
    "implied_price_per_kg_rs": round(PRICE_PER_KG_RS, 0),
    "detected_saffron_area_ha": round(total_ha, 1),
    "detected_saffron_annual_value_rs_crore": round(total_value_rs / 1e7, 2),
    "at_risk_area_ha": round(at_risk_ha, 1),
    "at_risk_share_pct": round(at_risk_ha / total_ha * 100, 1),
    "at_risk_annual_value_rs_crore": round(at_risk_value_rs / 1e7, 2),
    "source": "J&K Legislative Assembly, Agriculture Production Dept, reply to MLA Hasnain Masoodi, Feb 2026 "
              "(Greater Kashmir / Kashmir Life) — 19.58 MT from 3,715 ha, Rs 534.53 crore, 2024-25",
}

print(json.dumps(results, indent=2))

with open("outputs/economic_valuation_results.json", "w") as f:
    json.dump(results, f, indent=2)
print("\nSaved outputs/economic_valuation_results.json")
