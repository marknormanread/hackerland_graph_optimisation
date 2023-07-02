from dataclasses import dataclass
import networkx as nx  # type: ignore
from typing import List, Tuple


@dataclass
class Hackerland:
    n_cities: int
    n_roads: int
    from_cities: List[int]
    to_cities: List[int]
    road_weights: List[float]

    def list_all_cities(self) -> List[int]:
        all_cities = list(range(self.n_cities))
        return all_cities

    def as_networkX(self) -> nx.Graph:
        graph = nx.Graph()
        graph.add_nodes_from(self.list_all_cities())

        edges: List[Tuple[int, int]] = []
        for road in range(self.n_roads):
            edge = (self.from_cities[road], self.to_cities[road])
            edges.append(edge)

        graph.add_edges_from(edges)
        return graph

    def sum_weights(self) -> float:
        return sum(self.road_weights)