from hackerland.type_defs import Hackerland


def sum_pairs_of_unconnected_cities(
    hackerland: Hackerland,
    verbose: bool = False,
):
    cumulative_unconnected_pairs = 0
    for origin_city in hackerland.list_all_cities():
        if verbose:
            print("\n\n")

        n_unconnected = sum_cities_unconnected_to_given(
            origin_city,
            hackerland,
            verbose,
        )
        cumulative_unconnected_pairs += n_unconnected

    # Have to half this, as each unconnected city is counted twice, from each end.
    cumulative_unconnected_pairs = cumulative_unconnected_pairs / 2
    return cumulative_unconnected_pairs


def sum_cities_unconnected_to_given(
    origin_city: int,
    hackerland: Hackerland,
    verbose: bool = False,
):
    if verbose:
        print(f"Finding all cities unconnected with city {origin_city}")

    visited_cities: dict = {city: False for city in hackerland.list_all_cities()}
    visited_cities[origin_city] = True

    # Recursion pattern.
    # Traverse all cities that have not already been visited in depth-first manner.
    def traverse_city(city: int):
        if verbose:
            print(f"Traversing city {city}; visited cities = {visited_cities}")
        visited_cities[city] = True
        # Examine all roads.
        # Seek those from the `city`, and traverse the destinations only if they have not already been visited.
        for i in range(hackerland.n_roads):
            if hackerland.from_cities[i] == city:
                destination_city = hackerland.to_cities[i]
                if not visited_cities[destination_city]:
                    traverse_city(destination_city)

                elif verbose:
                    print(
                        f"Found road connecting {city} to {destination_city}, "
                        f"but {destination_city} has already been visisted"
                    )

            # Roads are specified as 'from' and 'to', but are bi-directional,
            # So the reverse traversal needs to be examined also.
            if hackerland.to_cities[i] == city:
                destination_city = hackerland.from_cities[i]
                if not visited_cities[destination_city]:
                    traverse_city(destination_city)

                elif verbose:
                    print(
                        f"Found road connecting {city} to {destination_city}, "
                        f"but {destination_city} has already been visisted"
                    )

    # Commence recursion
    traverse_city(city=origin_city)

    n_cities_not_connected_to_origin = sum(
        status is False for status in visited_cities.values()
    )
    return n_cities_not_connected_to_origin
