import networkx as nx
import heapq
from data_loader import DataLoader
class GraphService:
    DIFFICULTY_DAYS = {
        1: (1, 4),
        2: (3, 6),
        3: (5, 10),
        4: (9, 14),
        5: (12, 21),
    }

    DAILY_LIMIT = {
        1: 1.2,
        2: 1.8,
        3: 2.5,
        4: 3.2,
        5: 4.0
    }

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

    
    def find_route(self, difficulty, days, pois):
        Gf = nx.Graph()
        for u, v, data in self.G.edges(data=True):
            if data["difficulty"] <= difficulty:
                Gf.add_edge(u, v, **data)
        
        distances = {}
        paths = {}

        for p in pois:
            lengths, path = nx.single_source_dijkstra(Gf, p, weight="weight")
            for q in pois:
                if q != p and q in lengths:
                    distances[(p, q)] = lengths[q]
                    paths[(p, q)] = path[q]

        Gp = nx.Graph()
        for (u, v), w in distances.items():
            Gp.add_edge(u, v, weight=w)

        cycle = nx.approximation.traveling_salesman_problem(
            Gp,
            cycle=False,
            weight="weight"
        )
        full = []
        for a, b in zip(cycle[:-1], cycle[1:]):
            segment = paths[(a, b)]
            if full:
                full.extend(segment[1:])
            else:
                full.extend(segment)
        return full


# ---------- тест ----------
if __name__ == "__main__":
    # pois = [
    #     {"id": "A"},
    #     {"id": "B"},
    #     {"id": "C"},
    #     {"id": "D"}
    # ]

    # segments = [
    #     {"start_poi": "A", "end_poi": "B", "distance_m": 1000, "difficulty": 2, "is_camp": False},
    #     {"start_poi": "B", "end_poi": "C", "distance_m": 2000, "difficulty": 2, "is_camp": True},
    #     {"start_poi": "C", "end_poi": "D", "distance_m": 1500, "difficulty": 3, "is_camp": False},
    #     {"start_poi": "A", "end_poi": "C", "distance_m": 2500, "difficulty": 3, "is_camp": False},
    #     {"start_poi": "B", "end_poi": "D", "distance_m": 3000, "difficulty": 4, "is_camp": True},
    # ]
    loader = DataLoader()


    pois = loader.load_pois()
    segments = loader.load_segments()
    gs = GraphService()
    gs.build_graph(pois, segments)
    components = list(nx.connected_components(gs.G))
    # print("Компоненты связности:", components)
    difficulty = 5 
    max_days = 6
    poi_to_visit = [46, 53]

    route = gs.find_route(difficulty, max_days, poi_to_visit)
    
    
    
    
    print("Маршрут по дням:")
    for i, day in enumerate(route, 1):
        print(f"День {i}: {day}")
