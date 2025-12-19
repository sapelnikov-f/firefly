import json
from collections import defaultdict


POINTS_IN = "parsing/results/unique_data/all_pois_unique_with_coords.json"
SEGMENTS_IN = "parsing/results/unique_data/all_segments_unique.json"

POINTS_OUT = "parsing/results/unique_data/pois_only_with_coords.json"
SEGMENTS_OUT = "parsing/results/unique_data/segments_with_coords_only.json"

with open(POINTS_IN, encoding="utf-8") as f:
    points = json.load(f)

with open(SEGMENTS_IN, encoding="utf-8") as f:
    segments = json.load(f)

points_with_coords = {}
points_without_coords = set()

for p in points:
    if p.get("coords") and all(p["coords"]):
        points_with_coords[p["id"]] = p
    else:
        points_without_coords.add(p["id"])

edges_by_point = defaultdict(list)

for seg in segments:
    a, b = seg["start_end"]
    edges_by_point[a].append(seg)
    edges_by_point[b].append(seg)

def other_end(seg, point):
    a, b = seg["start_end"]
    return b if a == point else a


used_segments = set()
new_segments = []

for x in points_without_coords:
    connected = edges_by_point.get(x, [])
    if len(connected) == 1:
        used_segments.add(id(connected[0]))
        continue

    neighbors = [
        other_end(seg, x)
        for seg in connected
        if other_end(seg, x) in points_with_coords
    ]

    if not neighbors:
        for seg in connected:
            used_segments.add(id(seg))
        continue

    anchor = neighbors[0]
    if len(connected) == 2:
        s1, s2 = connected
        a = other_end(s1, x)
        b = other_end(s2, x)

        if a in points_with_coords and b in points_with_coords:
            new_segments.append({
                "start_end": [a, b],
                "segment_description": (
                    s1.get("segment_description", "").strip() + " " +
                    s2.get("segment_description", "").strip()
                ).strip(),
                "difficulty": max(
                    s1.get("difficulty", 0),
                    s2.get("difficulty", 0)
                ),
                "is_camp": (
                    s1.get("is_camp", False) or
                    s2.get("is_camp", False)
                )
            })
            used_segments.add(id(s1))
            used_segments.add(id(s2))
            continue

    # --- ВЕТВЛЕНИЯ / РАДИАЛКИ ---
    for seg in connected:
        other = other_end(seg, x)
        if other == anchor:
            continue

        new_segments.append({
            "start_end": [anchor, other],
            "segment_description": seg.get("segment_description", "").strip(),
            "difficulty": seg.get("difficulty", 0),
            "is_camp": seg.get("is_camp", False)
        })

        used_segments.add(id(seg))


for seg in segments:
    if id(seg) in used_segments:
        continue

    a, b = seg["start_end"]
    if a in points_with_coords and b in points_with_coords:
        new_segments.append(seg)

with open(POINTS_OUT, "w", encoding="utf-8") as f:
    json.dump(
        points_with_coords,
        f,
        ensure_ascii=False,
        indent=2
    )

new_segments = [
    seg for seg in new_segments
    if seg["start_end"][0] in points_with_coords
    and seg["start_end"][1] in points_with_coords
]


with open(SEGMENTS_OUT, "w", encoding="utf-8") as f:
    json.dump(
        new_segments,
        f,
        ensure_ascii=False,
        indent=2
    )

print(f"Готово:")
print(f"- точек с координатами: {len(points_with_coords)}")
print(f"- сегментов после сжатия: {len(new_segments)}")
