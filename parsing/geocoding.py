import json
import requests
import time

URL = "https://nominatim.openstreetmap.org/search"

HEADERS = {
    "User-Agent": "arkhyz-points-geocoder/1.0 (f.sapelnikov@yahoo.com)"
}

category_to_nominatim = {
    "хребет": ("natural", "ridge"),
    "озеро": ("natural", "water"),
    "вершина" : ("natural", "peak"),
    "река": ("waterway", "river"),
    "урочище" : ("place","locality" ),
    "перевал" : ("mountain_pass","yes"),
    "посёлок" : ("place", "village"),
    "долина реки" : ("natural", "river"),
    "ручей" : ("natural","stream"),
    "ледник" : ("natural","glacier"),
    "хутор" : ("place","isolated_dwelling"),
    "стоянка" : ("place","locality"),
    "водопад" : ("waterway","waterfall"),
    "поляна" : ("natural","grassland")

}

def geocode(name, category):
    params = {
        "q": name,
        "format": "json",
        "viewbox": "40.7,43.3,41.5,43.7", 
        "bounded": 1
    }

    response = requests.get(URL, params=params, headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    target = category_to_nominatim.get(category)
    # print(json.dumps(data, indent = 2))
    if not target:
        return None, None

    for d in data:
        if (d.get("class"), d.get("type")) == target:
            try:
                return float(d["lat"]), float(d["lon"])
            except (KeyError, TypeError, ValueError):
                return None, None

    return None, None



    
with open("parsing/results/unique_data/all_pois_unique_with_coords.json", "r", encoding="utf-8") as f:
    pois = json.load(f)

for point in pois:
    if all(point.get("coords")):
        continue
    lat, lon = geocode(point["name"],point["category"])
    point["coords"] = [lat, lon]
 
    time.sleep(1)  # ОБЯЗАТЕЛЬНО: лимит Nominatim

with open("parsing/results/unique_data/1all_pois_unique_with_coords.json", "w", encoding="utf-8") as f:
    json.dump(pois, f, ensure_ascii=False, indent=2)

