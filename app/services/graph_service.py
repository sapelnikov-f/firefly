import networkx as nx
import heapq
from data_loader import DataLoader
import json
import matplotlib.pyplot as plt




class GraphService:

    def __init__(self):
        self.G = nx.Graph()

    # ---------- Построение графа ----------

    def build_graph(self, pois, segments):
        self.G.clear()

        for poi in pois:
            self.G.add_node(poi["id"], **poi)

        for seg in segments:
            self.G.add_edge(
                seg["start_id"],
                seg["end_id"],
                weight=seg["difficulty"],
                is_camp=seg["is_camp"]
            )

        # оставляем крупнейшую компоненту связности
        components = list(nx.connected_components(self.G))
        largest_component = max(components, key=len)
        self.G = self.G.subgraph(largest_component).copy()

    # ---------- Базовые методы ----------

    def shortest_path(self, a, b):
        return nx.shortest_path(self.G, a, b, weight="weight")

    def shortest_distance(self, a, b):
        return nx.shortest_path_length(self.G, a, b, weight="weight")

    # ---------- Этап 1: единый маршрут ----------

    def build_core_route(self, start, must_visit):
        route = [start]
        current = start
        unvisited = set(must_visit)

        while unvisited:
            next_point = min(
                unvisited,
                key=lambda p: self.shortest_distance(current, p)
            )

            path = self.shortest_path(current, next_point)
            route.extend(path[1:])

            current = next_point
            unvisited.remove(next_point)

        # возврат в старт
        path = self.shortest_path(current, start)
        route.extend(path[1:])

        return route

    # ---------- Разворачивание в шаги с атрибутами ----------

    def expand_to_steps(self, path):
        """
        Превращает путь [v1, v2, v3]
        в шаги с атрибутами вершин и сегментов
        """
        steps = []

        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]

            step = {
                "from": {
                    "id": u,
                    **dict(self.G.nodes[u])
                },
                "to": {
                    "id": v,
                    **dict(self.G.nodes[v])
                },
                "segment": {
                    "from_id": u,
                    "to_id": v,
                    **dict(self.G[u][v])
                }
            }
            steps.append(step)

        return steps

    # ---------- Этап 2: разбиение по дням ----------

    def split_steps_by_days(self, steps, days, daily_limit):
        route = []

        current_day = {
            "day": 1,
            "steps": [],
            "stats": {
                "total_weight": 0,
                "camp_end": False
            }
        }

        for step in steps:
            w = step["segment"]["weight"]

            if current_day["stats"]["total_weight"] + w > daily_limit:
                route.append(current_day)
                current_day = {
                    "day": current_day["day"] + 1,
                    "steps": [],
                    "stats": {
                        "total_weight": 0,
                        "camp_end": False
                    }
                }

            current_day["steps"].append(step)
            current_day["stats"]["total_weight"] += w

            if (
                step["segment"].get("is_camp")
                and current_day["stats"]["total_weight"] >= 0.6 * daily_limit
                and current_day["day"] < days
            ):
                current_day["stats"]["camp_end"] = True
                route.append(current_day)

                current_day = {
                    "day": current_day["day"] + 1,
                    "steps": [],
                    "stats": {
                        "total_weight": 0,
                        "camp_end": False
                    }
                }

        route.append(current_day)

        # дни отдыха
        while len(route) < days:
            route.append({
                "day": len(route) + 1,
                "steps": [],
                "stats": {
                    "total_weight": 0,
                    "camp_end": True
                }
            })

        return route

    # ---------- Публичный метод ----------

    def build_route(self, start, must_visit, days, daily_limit):
        core_path = self.build_core_route(start, must_visit)
        print(core_path)
        steps = self.expand_to_steps(core_path)
        return self.split_steps_by_days(steps, days, daily_limit)

# ---------- тест ----------
if __name__ == "__main__":

    loader = DataLoader()

    reacheble_pois= {
        6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 20,
          21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
            31, 33, 34, 36, 37, 38, 39, 40, 42, 43, 
            44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 
            54, 63, 64, 66, 68, 70, 72, 74, 75, 77, 
            79, 80, 81, 83, 85, 86, 87, 88, 89, 90, 
            91, 92, 93, 94, 95, 96, 97, 98, 99, 100,
              101, 102, 103, 104, 105, 106, 108, 110,
                111, 112, 114, 115, 116, 117, 118, 119, 
                120, 121, 125, 126, 128, 129, 130, 133, 134,
                  135, 136, 137, 138, 139, 140, 141, 143, 145,
                    147, 149, 150, 151, 153}
    
    pois = loader.load_pois()
    segments = loader.load_segments()
    gs = GraphService()
    gs.build_graph(pois, segments)
    start_point=143
    route = gs.build_route(start_point,must_visit=[91,128, 106, 37],days=21,daily_limit=20)

# print(route)
if route:
    for i, day in enumerate(route, 1):
        for step in day["steps"]:
            print(day["day"], ":  ", step["from"]["name"]," (",step["from"]["category"],") ",   " - > ",  step["to"]["name"]," (",step["to"]["category"],") ")
else:
    print("Маршрут не найден")


with open("test_route.json", "w") as f:
        json.dump(route, f, indent=2, ensure_ascii=False)






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
    

