import osmnx as ox
import networkx as nx
from shapely.geometry import LineString, mapping
from shapely.ops import linemerge
import json

REGION = " Karachay-Cherkessia, Russia"
region = (43.345, 40.699,43.6559, 41.6904)
report = 3

print("Загружаем граф OSM...")
G = ox.graph_from_bbox(region, network_type="walk", simplify=False)
with open(f"parsing/results/rep{report}/pois{report}_with_coords.json", "r", encoding="utf-8") as f:
    pois = json.load(f)
def build_route(segment):
    start_id, end_id = segment["start_end"]
    start = pois[int(start_id) - 1]
    end = pois[int(end_id) - 1]

    print(f"Маршрут: {start['name']} → {end['name']}")

    # ищем ближайшие РЁБРА, а не узлы
    start_edge = ox.distance.nearest_edges(
        G,
        X=start["coords"][1],
        Y=start["coords"][0]
    )
    end_edge = ox.distance.nearest_edges(
        G,
        X=end["coords"][1],
        Y=end["coords"][0]
    )

    # берём узлы рёбер
    start_node = start_edge[0]
    end_node = end_edge[1]

 

    route = nx.shortest_path(G, start_node, end_node, weight="length")

    coords = [(G.nodes[n]['x'], G.nodes[n]['y']) for n in route]

    distance_m = sum(G.edges[u, v, 0]['length'] for u, v in zip(route[:-1], route[1:]))

    line = LineString(coords)
    segment["geom"] = mapping(line)  # GeoJSON LineString
    segment["distance_m"] = distance_m

    
    return segment



with open(f"parsing/results/rep{report}/segments{report}.json", "r", encoding="utf-8") as f:
    segments = json.load(f)


print(build_route(segments[0]))

# segments_with_routes = []
# for seg in segments:
#     seg_start = seg["start_end"][0]
#     seg_end = seg["start_end"][1]
#     start_poi = pois[int(seg_start)-1]
#     end_poi = pois[int(seg_end)-1]
#     if start_poi["coords"][0] == None or end_poi["coords"][0] == None:
#         print(f"Пропускаем сегмент {seg['index']} из-за отсутствующих координат.")
#         continue    
#     seg_with_route = build_route(seg)
#     segments_with_routes.append(seg_with_route)
# with open("parsing/results/segments3_routes.json", "w", encoding="utf-8") as f:
#     json.dump(segments_with_routes, f, ensure_ascii=False, indent=2)
