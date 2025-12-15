import json
import requests
import time

URL = "https://nominatim.openstreetmap.org/search"

HEADERS = {
    "User-Agent": "arkhyz-points-geocoder/1.0 (f.sapelnikov@yahoo.com)"
}

def geocode(name):
    params = {
        "q": name,
        "format": "json",
        "limit": 1,
        "viewbox": "41.0,43.3,41.4,43.7",
        "bounded": 1
    }

    response = requests.get(URL, params=params, headers=HEADERS)
    response.raise_for_status()
    data = response.json()

    if data:
        return float(data[0]["lat"]), float(data[0]["lon"])
    return None, None


with open("parsing/results/pois3.json", "r", encoding="utf-8") as f:
    pois = json.load(f)

for point in pois:
    lat, lon = geocode(point["name"])
    point["coords"] = [lat, lon]
 
    time.sleep(1)  # ОБЯЗАТЕЛЬНО: лимит Nominatim

with open("parsing/results/pois3_with_coords.json", "w", encoding="utf-8") as f:
    json.dump(pois, f, ensure_ascii=False, indent=2)
