import cfpq_data
import networkx
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, State


def get_graph_description(graph: networkx.MultiDiGraph) -> (int, int, set):
    """Returns number of nodes, number of edges, set of labels

    :param graph: A directed graph class that can store multiedges
    :type graph: networkx.MultiDiGraph
    """

    return (
        graph.number_of_nodes(),
        graph.number_of_edges(),
        cfpq_data.get_labels(graph, verbose=False),
    )


def generate_two_cycles_graph(
    first_cycle_vertices: int, second_cycle_vertices, edge_labels: (str, str)
) -> networkx.MultiDiGraph:
    """Creates a graph of two loops

    :param first_cycle_vertices: The number of nodes in the first cycle without a common node
    :type first_cycle_vertices: int
    :param second_cycle_vertices: The number of nodes in the second cycle without a common node
    :type second_cycle_vertices: int
    :param edge_labels: Labels that will be used to mark the edges of the graph
    :type edge_labels: (str, str)
    """
    two_cycles_graph = cfpq_data.labeled_two_cycles_graph(
        first_cycle_vertices,
        second_cycle_vertices,
        edge_labels=edge_labels,
        verbose=False,
    )

    return two_cycles_graph


def write_two_cycles_graph(graph: networkx.MultiDiGraph, path: str) -> None:
    """Writes a graph of two cycles to the file.
    Parameters
    ----------
    graph : MultiDiGraph
        The graph to be written.
    path : str
        Path to the file where the graph will be written.
    """
    networkx.drawing.nx_pydot.write_dot(graph, path)


def graph_to_nfa(
    graph: networkx.MultiDiGraph, start_nodes: set = None, final_nodes: set = None
) -> NondeterministicFiniteAutomaton:

    nfa = NondeterministicFiniteAutomaton.from_networkx(graph)

    if not start_nodes:
        start_nodes = set(graph.nodes)
    if not final_nodes:
        final_nodes = set(graph.nodes)

    for state in start_nodes:
        nfa.add_start_state(State(state))

    for state in final_nodes:
        nfa.add_final_state(State(state))

    return nfa
