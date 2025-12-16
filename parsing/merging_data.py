import json


all_pois = []
id_map = []  
new_id = 1

for i in range(1,11):
    with open(f"parsing/results/rep{i}/pois{i}.json", "r") as f:
        pois_temp = json.load(f)
    temp_id_map = {}
    for p in pois_temp:
        old_id = p["id"]
        temp_id_map[old_id] =  new_id
        p["id"] = new_id
        all_pois.append(p)
        new_id += 1
    id_map.append(temp_id_map)




with open("parsing/results/unique_data/all_pois.json", 'w', encoding="utf-8") as f:
    json.dump(all_pois, f, ensure_ascii=False, indent=2)


all_segments = []
it = 1




for i in range(1,11):
    with open(f"parsing/results/rep{i}/segments{i}.json", "r") as f:
        segments_temp = json.load(f)
    temp_id_map = id_map[i-1]
    for s in segments_temp:
        old_start, old_end = s["start_end"]

        s["start_end"] = [
            temp_id_map[old_start],
            temp_id_map[old_end]
        ]
        it += 1
        all_segments.append(s)
with open("parsing/results/unique_data/all_segments.json", 'w', encoding="utf-8") as f:
    json.dump(all_segments,f, ensure_ascii=False, indent=2)


with open("parsing/results/unique_data/all_pois.json", "r", encoding="utf-8") as f:
    all_pois = json.load(f)

with open("parsing/results/unique_data/all_segments.json", "r", encoding="utf-8") as f:
    all_segments = json.load(f)


seen = {}  
unique_pois = []
old_to_new_id = {}
new_id = 1

for p in all_pois:
    key = (p["name"].strip().lower(), p.get("category", "").strip().lower())
    
    if key not in seen:
        seen[key] = new_id
        old_to_new_id[p["id"]] = new_id
        p["id"] = new_id
        unique_pois.append(p)
        new_id += 1
    else:
        old_to_new_id[p["id"]] = seen[key]


for s in all_segments:
    s["start_end"] = [
        old_to_new_id[s["start_end"][0]],
        old_to_new_id[s["start_end"][1]]
    ]



with open("parsing/results/unique_data/all_pois_unique.json", "w", encoding="utf-8") as f:
    json.dump(unique_pois, f, ensure_ascii=False, indent=2)

with open("parsing/results/unique_data/all_segments_updated.json", "w", encoding="utf-8") as f:
    json.dump(all_segments, f, ensure_ascii=False, indent=2)


