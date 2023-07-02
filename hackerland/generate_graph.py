# Creates the 'hackerland'.
# A fully connected graph of cities, with roads connecting cities represented as edges with varying weights.
# There are edges superfluous to that necessary for a fully connected graph.
# The aim of the challenge is to create an algorithm that removes all superfluous roads such that the resultant
# fully connected graph has minimal possibly sum of remaining road weights.

from dataclasses import dataclass
from igraph import Graph  # type: ignore
import random
from typing import List

from hackerland.type_defs import Hackerland


MAX_ROAD_WEIGHT = 10


def create_hackerland_fully_connected(n_cities: int):
    return create_hackerland_partially_connected(
        n_cities=n_cities,
        connection_probability=1.0,
    )


def create_hackerland_partially_connected(
    n_cities: int, connection_probability: float, verbose: bool = False
):
    # Cities were encoded as integer values.
    # In the challenge that were encoded from number 1.
    # For simplicity, start from zero instead.
    cities: List[int] = list(range(n_cities))

    from_cities: List[int] = []
    to_cities: List[int] = []
    road_weights: List[float] = []
    n_roads = 0

    for i in list(range(n_cities)):
        # This allows for roads that start and end at the same city.
        for j in list(range(i, n_cities)):
            if random.random() < connection_probability:
                from_city = cities[i]
                to_city = cities[j]
                # Start with ints for now, but can change to float later.
                weight = float(random.randint(1, MAX_ROAD_WEIGHT))

                from_cities.append(from_city)
                to_cities.append(to_city)
                road_weights.append(weight)

                n_roads = n_roads + 1

    assert len(from_cities) == len(to_cities) == len(road_weights) == n_roads

    hackerland = Hackerland(
        n_cities=n_cities,
        n_roads=n_roads,
        from_cities=from_cities,
        to_cities=to_cities,
        road_weights=road_weights,
    )
    return hackerland
