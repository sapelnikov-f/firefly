import json
from supabase import create_client
from shapely.geometry import LineString

supabase = create_client("https://rhgazdnloccrierufgvk.supabase.co", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJoZ2F6ZG5sb2NjcmllcnVmZ3ZrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjQ5NjI5MDEsImV4cCI6MjA4MDUzODkwMX0.7uMMmehcpXcxQcKT398CIt_ygCA75S2E-EXP872Mkt0")

with open("parsing/results/unique_data/all_pois_unique_with_coords.json", encoding="utf-8") as f:
    pois = json.load(f)

rows = []


for p in pois:
    if p["coords"][0] != None:
        lon, lat = p["coords"]
        rows.append({
        "id": p["id"],
        "name" : p["name"],
        "description": p["description"],
        "pass_category": p["pass_category"],
        "category": p["category"],
        "geom": f"SRID=4326;POINT({lon} {lat})"
    })
    else:
        rows.append({
        "id": p["id"],
        "name" : p["name"],
        "description": p["description"],
        "pass_category": p["pass_category"],
        "category": p["category"],
        "geom": None
    })

# batch insert
supabase.table("pois").insert(rows).execute()

rows = []
with open("parsing/results/unique_data/all_segments_unique.json", encoding="utf-8") as f:
    segments = json.load(f)
it = 1
for seg in segments:
  
    start_id, end_id = seg["start_end"]

    rows.append({
        "id": it,
        "start_id" : start_id,
        "end_id" : end_id,
        "difficulty": seg["difficulty"],
        "is_camp": seg["is_camp"],
        "segment_description": seg["segment_description"],
    })
    it +=1


supabase.table("segments").insert(rows).execute()