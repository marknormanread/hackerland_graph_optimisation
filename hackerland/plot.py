import networkx as nx
import matplotlib.pyplot as plt  # type: ignore
from hackerland.type_defs import Hackerland
from hackerland.evaluation import sum_pairs_of_unconnected_cities


def plot_hackerland(hackerland: Hackerland):
    plt.clf()
    graph = hackerland.as_networkX()
    n_unconnected_pairs = sum_pairs_of_unconnected_cities(
        hackerland=hackerland, verbose=False
    )
    sum_road_weights = hackerland.sum_weights()

    # Plot the graph
    # This doesn't show edges
    # nx.draw(
    #     graph,
    #     with_labels=True,
    #     node_color="lightblue",
    #     node_size=500,
    #     font_weight="bold",
    # )

    pos = nx.spring_layout(graph)  # Positions nodes using the spring layout algorithm
    nx.draw_networkx_nodes(graph, pos, node_color="lightblue", node_size=500, alpha=0.8)
    nx.draw_networkx_edges(graph, pos, width=1.0, alpha=0.5)
    nx.draw_networkx_labels(graph, pos, font_weight="bold")
    plt.axis("off")

    plt.title(
        f"{n_unconnected_pairs} unconnected pairs of cities; sum of road weights = {sum_road_weights}"
    )
    plt.show()
    return
