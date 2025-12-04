import networkx as nx

class GraphService:
    def __init__(self):
        self.G = nx.Graph()

    def build_graph(self, pois, segments):
        for poi in pois:
            self.G.add_node(poi["id"], **poi)

        for seg in segments:
            self.G.add_edge(seg["start_poi"], seg["end_poi"], weight=seg["length_m"], elev_gain=seg["elev_gain"])

    def find_route(self, start_id, end_id):
        path = nx.shortest_path(self.G, start_id, end_id, weight="weight")
        distance = sum(self.G[u][v]["weight"] for u, v in zip(path[:-1], path[1:]))
        elev_gain = sum(self.G[u][v]["elev_gain"] for u, v in zip(path[:-1], path[1:]))
        return {"path": path, "distance_m": distance, "elevation_gain_m": elev_gain}

