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
        "limit": 1
    }

    response = requests.get(URL, params=params, headers=HEADERS)
    response.raise_for_status()
    data = response.json()

    if data:
        return float(data[0]["lat"]), float(data[0]["lon"])
    return None, None


with open("parsing/results/pois.json", "r", encoding="utf-8") as f:
    pois = json.load(f)


lat, lon = geocode(pois[1]["name"])
print(f"Geocoded '{pois[1]['name']}': {lat}, {lon}")