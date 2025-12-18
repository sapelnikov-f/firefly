import json
from supabase import create_client
from shapely.geometry import LineString

supabase = create_client("https://rhgazdnloccrierufgvk.supabase.co", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJoZ2F6ZG5sb2NjcmllcnVmZ3ZrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjQ5NjI5MDEsImV4cCI6MjA4MDUzODkwMX0.7uMMmehcpXcxQcKT398CIt_ygCA75S2E-EXP872Mkt0")

with open("parsing/results/unique_data/pois_only_with_coords.json", encoding="utf-8") as f:
    pois = json.load(f)

rows = []


for p in pois.values():
    if not p.get("coords"):
        continue

    lon, lat = p["coords"]

    rows.append({
        "id": p["id"],
        "name" : p["name"],
        "description": p["description"],
        "pass_category": p["pass_category"],
        "category": p["category"],
        "geom": f"SRID=4326;POINT({lon} {lat})"
    })

# batch insert
supabase.table("pois").insert(rows).execute()


with open("parsing/results/unique_data/segments_with_routes.json", encoding="utf-8") as f:
    segments = json.load(f)

for seg in segments:
    start_id, end_id = seg["start_end"]
    distance = seg["distance_m"]

    # Обновляем существующую строку по start_id и end_id
    supabase.table("segments").update({
        "distance_m": distance
    }).eq("start_id", start_id).eq("end_id", end_id).execute()


