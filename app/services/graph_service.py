import networkx as nx
from app.services.data_loader import DataLoader



class GraphService:

    def __init__(self):
        self.G = nx.Graph()



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

        components = list(nx.connected_components(self.G))
        largest_component = max(components, key=len)
        self.G = self.G.subgraph(largest_component).copy()



    def shortest_path(self, a, b):
        return nx.shortest_path(self.G, a, b, weight="weight")

    def shortest_distance(self, a, b):
        return nx.shortest_path_length(self.G, a, b, weight="weight")



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


        path = self.shortest_path(current, start)
        route.extend(path[1:])

        return route



    def expand_to_steps(self, path):

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



    def split_steps_by_days(self, steps, daily_limit):

        route = []
        current_day = {
            "day": 1,
            "steps": [],
            "stats": {
                "total_weight": 0
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
                        "total_weight": 0
                    }
                }

            current_day["steps"].append(step)
            current_day["stats"]["total_weight"] += w

        if current_day["steps"]:
            route.append(current_day)

        return route

    def build_route(self, start, must_visit, daily_limit):

        core_path = self.build_core_route(start, must_visit)


        steps = self.expand_to_steps(core_path)

        if steps[-1]["to"]["id"] != start:
            path_back = self.shortest_path(steps[-1]["to"]["id"], start)
            back_steps = self.expand_to_steps(path_back)
            steps.extend(back_steps)

        return self.split_steps_by_days(steps, daily_limit)
    


