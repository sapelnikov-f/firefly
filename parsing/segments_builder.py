

import osmnx as ox
import networkx as nx
from shapely.geometry import LineString, mapping
from shapely.ops import linemerge
import json

REGION = "Arkhyz, Karachay-Cherkessia, Russia"
OUTPUT_FILE = "segments_routes.json"


print("Загружаем граф OSM...")
G = ox.graph_from_place(REGION, network_type="walk", simplify=False)
G = ox.project_graph(G)

with open("parsing/results/pois_with_coords.json", "r", encoding="utf-8") as f:
    pois = json.load(f)

def build_route(segment):
    start_id, end_id = segment["start_end"]
    start = pois[int(start_id)-1]
    end = pois[int(end_id)-1]
    print(f"Строим маршрут от {start['coords']} до {end['coords']}")

    # ближайшие узлы
    start_node = ox.nearest_nodes(G, X=start["coords"][1], Y=start["coords"][0])
    end_node = ox.nearest_nodes(G, X=end["coords"][1], Y=end["coords"][0])

    # кратчайший путь
    route_nodes = nx.shortest_path(G, start_node, end_node, weight="length")

    if len(route_nodes) < 2:
        print("⚠️ Маршрут выродился в одну точку")
        segment["geom"] = None
        segment["distance_m"] = 0
        return segment

    # 🔥 ГЕОМЕТРИЯ ИЗ OSMnx
    route_gdf = ox.utils_graph.route_to_gdf(G, route_nodes)

    # объединяем рёбра в одну линию
    line = linemerge(route_gdf.geometry.tolist())

    segment["geom"] = line.__geo_interface__
    segment["distance_m"] = float(route_gdf["length"].sum())
    
    return segment


with open("parsing/results/segments.json", "r", encoding="utf-8") as f:
    segments = json.load(f)

print(build_route(segments[8]))  # тестируем на первом сегменте

# segments_with_routes = []
# for seg in segments:
#     seg_start = seg["start_end"][0]
#     seg_end = seg["start_end"][1]
#     start_poi = pois[int(seg_start)-1]
#     end_poi = pois[int(seg_end)-1]
#     if start_poi["coords"][0] == None or end_poi["coords"][0] == None:
#         print(f"Пропускаем сегмент {seg['id']} из-за отсутствующих координат.")
#         continue    
#     seg_with_route = build_route(seg)
#     segments_with_routes.append(seg_with_route)


# --- сохраняем результат ---
# with open("parsing/results/segments_routes.json", "w", encoding="utf-8") as f:
#     json.dump(segments_with_routes, f, ensure_ascii=False, indent=2)



