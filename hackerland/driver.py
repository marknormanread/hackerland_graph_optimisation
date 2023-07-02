from typing import List

from hackerland.type_defs import Hackerland
from hackerland.generate_graph import (
    create_hackerland_fully_connected,
    create_hackerland_partially_connected,
)
from hackerland.evaluation import sum_pairs_of_unconnected_cities
from hackerland import plot


### SET UP ORIGINAL HACKERLAND. 
# ALL CITIES CONNECTED WITH RANDOM WEIGHT ROADS.
# THE OPTIMISATION PROCESS WILL REMOVE SUPERFLUOUS ROADS. 

orig_hackerland: Hackerland = create_hackerland_fully_connected(n_cities=5)
connectivity = sum_pairs_of_unconnected_cities(
    hackerland=orig_hackerland, verbose=False
)
print(connectivity)


plot.plot_hackerland(orig_hackerland)


### START OPTIMISATION HERE

# The UNSGA3 package is something I wrote many years ago when no implementation
# of this algorithm existed.
# It's been ages since I used it (and my documentation should have been a LOT better).
# It is a multi-objective optimisation algorithm.
# Underpinning it is a genetic algorithm.
# It attempts to find solutions that offer an optimal balance of
# 1) Number of unconnected pairs of cities and
# 2) The sum of road weights retained.
#
# Though the original problem demanded all optimised cities be fully connected,
# by allowing some flexibility in this you may allow paths through solution space
# that might otherwise be cut-off.
import unsga3
from unsga3.unsga3 import Candidate
from optimisation_utils import GenerationalInspector


def fitness_evaluator(population: List[Candidate], generation: int):
    training_fitnesses = []
    validation_fitnesses = []

    for candidate in population:
        train_fit, valid_fit = evaluate_candiate(candidate)
        training_fitnesses.append(train_fit)
        validation_fitnesses.append(valid_fit)

    return training_fitnesses, None


def evaluate_candiate(candidate: Candidate) -> float:
    cand_hackerland = convert_candidate_to_hackerland(candidate)

    sum_of_road_weights = cand_hackerland.sum_weights()
    disconnected_city_pairs = sum_pairs_of_unconnected_cities(cand_hackerland)

    return [sum_of_road_weights, disconnected_city_pairs], None


def convert_candidate_to_hackerland(candidate: Candidate) -> Hackerland:
    cand_from_cities: List[int] = []
    cand_to_cities: List[int] = []
    cand_road_weights: List[float] = []
    cand_n_roads = 0
    for i, road_inclusion in enumerate(candidate.solution):
        if road_inclusion > 0.5:
            # Include the road
            cand_from_cities.append(orig_hackerland.from_cities[i])
            cand_to_cities.append(orig_hackerland.to_cities[i])
            cand_road_weights.append(orig_hackerland.road_weights[i])
            cand_n_roads += 1

    cand_hackerland = Hackerland(
        n_cities=orig_hackerland.n_cities,
        n_roads=cand_n_roads,
        from_cities=cand_from_cities,
        to_cities=cand_to_cities,
        road_weights=cand_road_weights,
    )
    return cand_hackerland


# Problem representation, one item per road that is either included or
# deleted from the final representation.
solution_dimensions = tuple(
    [
        unsga3.SolutionDimension(min_val=0.0, max_val=1.0, granularity=0.33)
        for road in range(orig_hackerland.n_roads)
    ]
)
num_objectives = 2
inspector = GenerationalInspector(attr="training_fitness")
op = unsga3.UNSGA3(
    solution_dimensions=solution_dimensions,
    fitness_evaluator=fitness_evaluator,
    num_objectives=num_objectives,
    max_generations=60,
    population_size=None,  # Auto-determine.
    reference_point_increments=5,
    generatonal_inspector_function=inspector.inspect,
)
op.run()

"""
This graph shows the best solutions across each generation of the genetic algorithm. 
Pink coloured solutions are the last generations (the best solutions). 
Performance is shown against two criteria, labelled in the graph. 
Where a generation does not offer any candidates improving over those aquired 
previously, that generation's solutions will be omitted from the graph. 
"""

inspector.plot_all_generations_2d(
    xlabel="sum of road weights",
    ylabel="pairs of unconnected cities",
)

"""
These are the best solutions found
"""

final_solutions: List[Candidate] = op.training_pareto_front
for cand in final_solutions:
    cand_pairs_unconnected_cities = cand.fitness[1]
    cand_sum_road_weights = cand.fitness[0]
    if cand_pairs_unconnected_cities == 0:
        print(
            f"This solution had no unconnected cities. "
            f"Sum of road weights = {cand_sum_road_weights}"
        )
        plot.plot_hackerland(convert_candidate_to_hackerland(cand))
