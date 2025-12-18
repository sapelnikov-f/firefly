import json


#Скрипт чистит json файлы полученные после парсинга llm
for i in range (1,11):
    with open(f"parsing/results/rep{i}/segments{i}.json", "r") as f:
        segments = json.load(f)

    for seg in segments:
        if "index" in seg:
            seg["id"] = seg.pop("index")
        if type(seg["start_end"][0]) == str:
            seg["start_end"][0] = int(seg["start_end"][0])
            seg["start_end"][1] = int(seg["start_end"][1])


    with open(f"parsing/results/rep{i}/segments{i}.json", "w") as f:
        json.dump(segments, f, indent=2, ensure_ascii=False)

    with open(f"parsing/results/rep{i}/pois{i}.json", "r") as f:
        pois = json.load(f)

    for poi in pois:
        if "type" in poi:
            poi["category"] = poi.pop("type")

    with open(f"parsing/results/rep{i}/pois{i}.json", "w") as f:
        json.dump(pois, f, indent=2, ensure_ascii=False)

