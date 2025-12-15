import osmnx as ox
import networkx as nx
from shapely.geometry import LineString, mapping
from shapely.ops import linemerge
import json

REGION = " Karachay-Cherkessia, Russia"
OUTPUT_FILE = "segments_routes.json"


print("Загружаем граф OSM...")
G = ox.graph_from_place(REGION, network_type="walk", simplify=False)

with open("parsing/results/pois_with_coords.json", "r", encoding="utf-8") as f:
    pois = json.load(f)
def build_route(segment):
    start_id, end_id = segment["start_end"]
    start = pois[int(start_id) - 1]
    end = pois[int(end_id) - 1]

    print(f"Маршрут: {start['coords']} → {end['coords']}")

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

    print("Стартовый узел:", G.nodes[start_node]['y'], G.nodes[start_node]['x'])
    print("Конечный узел:", G.nodes[end_node]['y'], G.nodes[end_node]['x'])

    route = nx.shortest_path(G, start_node, end_node, weight="length")
    length = nx.shortest_path_length(G, start_node, end_node, weight="length")

    return route, length

# Длина пути
    path_length = nx.shortest_path_length(G, start_node, end_node, weight='length')
    print(f"Длина маршрута: {path_length:.2f} метров")
    # кратчайший путь 

with open("parsing/results/segments.json", "r", encoding="utf-8") as f:
    segments = json.load(f)

print(build_route(segments[0])) 