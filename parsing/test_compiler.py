import json
from shapely.geometry import LineString
from shapely.ops import linemerge

# Загрузка JSON
with open("parsing/results/rep1/segments_routes.json", "r") as f:
    data = json.load(f)

line_strings = []
for seg in data:
    coords = seg["geom"]["coordinates"]
    line_strings.append(LineString(coords))

# Объединяем все сегменты в один трек
merged_line = linemerge(line_strings)

# Результат: WKT или GeoJSON


# Опционально: сохранить в GeoJSON
merged_geojson = {
    "type": "Feature",
    "geometry": json.loads(json.dumps(merged_line.__geo_interface__)),
    "properties": {}
}

with open("merged_track.geojson", "w") as f:
    json.dump(merged_geojson, f, indent=2)
