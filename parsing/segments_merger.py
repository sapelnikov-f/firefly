import json
from shapely.geometry import LineString
from shapely.ops import linemerge

# Загрузка JSON
with open("parsing/results/unique_data/segments_with_routes.json", "r") as f:
    data = json.load(f)

line_strings = []
for seg in data:
    coords = seg["geom"]["coordinates"]
    line_strings.append(LineString(coords))


merged_line = linemerge(line_strings)

merged_geojson = {
    "type": "Feature",
    "geometry": json.loads(json.dumps(merged_line.__geo_interface__)),
    "properties": {}
}

with open("parsing/results/unique_data/merged_linestring.geojson", "w") as f:
    json.dump( merged_geojson, f, indent=2)



with open("parsing/results/unique_data/all_pois_unique_with_coords.json", "r", encoding="utf-8") as f:
    data = json.load(f)

features = []

for item in data:
    lat, lon = item["coords"]

    if lon is None or lat is None:
        continue

    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [lon, lat]
        },
        "properties": {
            "id": item["id"],
            "name": item["name"],
            "description": item["description"],
            "category": item["category"],
            "pass_category": item["pass_category"]
        }
    }

    features.append(feature)

geojson = {
    "type": "FeatureCollection",
    "features": features
}

with open("points.geojson", "w", encoding="utf-8") as f:
    json.dump(geojson, f, ensure_ascii=False, indent=2)
