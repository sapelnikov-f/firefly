import networkx as nx
import heapq
from data_loader import DataLoader

import matplotlib.pyplot as plt
class GraphService:
    
    def __init__(self):
        self.G = nx.Graph() 

    def build_graph(self, pois, segments):
        self.G.clear()
        for poi in pois:
            self.G.add_node(poi["id"], **poi)
        MIN_DIST = 237.175712991383
        MAX_DIST = 26754.8033600389
        for seg in segments:
            d_norm = (seg["distance_m"] - MIN_DIST) / (MAX_DIST - MIN_DIST)
            s_norm = (seg["difficulty"] - 1) / 4
            weight = 0.5 * d_norm + 0.5 * s_norm
            self.G.add_edge(
                seg["start_id"],
                seg["end_id"],
                weight=weight,
                difficulty=seg["difficulty"],
                is_camp=seg["is_camp"]
            )
        components = list(nx.connected_components(self.G))
        largest_component = max(components, key=len)
        self.G = self.G.subgraph(largest_component).copy()

    def plan_day(self, start, poi_to_visit, max_weight, used_edges):
        """Планируем один день маршрута"""
        path = [start]
        current_weight = 0
        current_node = start
        visited_poi = set()
        poi_to_visit = set(poi_to_visit)

        while poi_to_visit:
            nearest_poi, shortest_path, path_weight = None, None, None
            for poi in poi_to_visit:
                try:
                    sp = nx.shortest_path(self.G, current_node, poi, weight='weight')
                    w = sum(self.G[u][v]['weight'] for u, v in zip(sp[:-1], sp[1:]))
                    # учитываем, сколько рёбер уже использовано
                    reuse_penalty = sum(0.001 for u, v in zip(sp[:-1], sp[1:]) if (u, v) in used_edges or (v, u) in used_edges)
                    w += reuse_penalty
                    if nearest_poi is None or w < path_weight:
                        nearest_poi, shortest_path, path_weight = poi, sp, w
                except nx.NetworkXNoPath:
                    continue

            if nearest_poi is None or current_weight + path_weight > max_weight:
                break  # лимит дня достигнут

            # идём к POI
            path += shortest_path[1:]
            current_weight += path_weight
            current_node = nearest_poi
            visited_poi.add(nearest_poi)
            poi_to_visit.remove(nearest_poi)

            # отмечаем рёбра как использованные
            for u, v in zip(shortest_path[:-1], shortest_path[1:]):
                used_edges.add((u, v))

        return path, visited_poi

    def plan_route(self, start, poi_list, days, max_weight, loop=False):
        """Планируем весь маршрут по дням"""
        remaining_poi = set(poi_list)
        current_start = start
        route = []
        used_edges = set()

        for _ in range(days):
            day_path, visited = self.plan_day(current_start, remaining_poi, max_weight, used_edges)
            if not day_path:
                break
            route.append(day_path)
            remaining_poi -= visited
            current_start = day_path[-1]
            if not remaining_poi:
                break

        # Если нужно закольцевать маршрут
        if loop and route and route[-1][-1] != start:
            try:
                sp = nx.shortest_path(self.G, route[-1][-1], start, weight='weight')
                route[-1].extend(sp[1:])
            except nx.NetworkXNoPath:
                pass

        return route

# ---------- тест ----------
if __name__ == "__main__":

    loader = DataLoader()


    pois = loader.load_pois()
    segments = loader.load_segments()
    gs = GraphService()
    gs.build_graph(pois, segments)
    # components = list(nx.connected_components(gs))


    difficulty = 5 
    max_days = 6
    start = 100
    poi_to_visit = [46, 33, start]
    start = 100
    route = gs.plan_route(start, poi_to_visit, max_days, 1.5)
#     G = gs.G  # ваш граф из GraphService

#     pos = nx.spring_layout(G)  # позиционирование вершин
#     nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=800)
#     nx.draw_networkx_edges(G, pos, edge_color='gray')
#     edge_labels = nx.get_edge_attributes(G, 'weight')

# # округляем до 2 знаков после запятой
#     edge_labels_rounded = {k: round(v, 2) for k, v in edge_labels.items()}

# # рисуем граф с округлёнными подписями
#     nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels_rounded)
    

#     plt.title("Граф POI")
#     plt.show()  
    
    print(route)
    

