import osmnx as ox
import networkx as nx
from shapely.geometry import LineString, mapping
from shapely.ops import linemerge
import json

REGION = " Karachay-Cherkessia, Russia"



print("Загружаем граф OSM...")
G = ox.graph_from_place(REGION, network_type="walk", simplify=False)
with open("parsing/results/unique_data/pois_only_with_coords.json", "r", encoding="utf-8") as f:
    pois = json.load(f)


def build_route(segment):
    start_id, end_id = segment["start_end"]
    start = pois[str(start_id)]
    end = pois[str(end_id)]

    
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


    start_node = start_edge[0]
    end_node = end_edge[1]

 

    route = nx.shortest_path(G, start_node, end_node, weight="length")

    coords = [(G.nodes[n]['x'], G.nodes[n]['y']) for n in route]

    distance_m = sum(G.edges[u, v, 0]['length'] for u, v in zip(route[:-1], route[1:]))

    line = LineString(coords)
    segment["geom"] = mapping(line) 
    segment["distance_m"] = distance_m

    
    return segment



with open("parsing/results/unique_data/segments_with_coords_only.json", "r", encoding="utf-8") as f:
    segments = json.load(f)



segments_with_routes = []
for seg in segments:
    seg_start = seg["start_end"][0]
    seg_end = seg["start_end"][1]
    start_poi = pois[str(seg_start)]
    end_poi = pois[str(seg_end)]
    if start_poi["coords"][0] == None or end_poi["coords"][0] == None:
        print(f"Пропускаем сегмент {seg['id']} из-за отсутствующих координат.")
        continue    
    seg_with_route = build_route(seg)
    segments_with_routes.append(seg_with_route)
with open("parsing/results/unique_data/segments_with_routes.json", "w", encoding="utf-8") as f:
    json.dump(segments_with_routes, f, ensure_ascii=False, indent=2)

