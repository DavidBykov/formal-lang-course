import pytest
import cfpq_data
import networkx
from project.graph_utils import get_graph_description, write_two_cycles_graph


def test_get_graph_utils():
    assert (10, "edge_label", {"edge_label"}) == get_graph_description(
        cfpq_data.labeled_cycle_graph(10, edge_label="edge_label"))


def test_two_cycles_graph():
    assert (10, 11, {"edge_label_one, edge_label_two"}) == get_graph_description(
        cfpq_data.labeled_two_cycles_graph(5, 5, edge_labels=("edge_label_one", "edge_label_two"), verbose=False))


def test_write_two_cycles_graph(tmpdir):
    n = 10
    m = 20
    edge_labels = ("edge_label_one", "edge_label_two")

    file = tmpdir.mkdir("test_dir").join("example.dot")
    write_two_cycles_graph(n, m, edge_labels, file)

    expected_graph = cfpq_data.labeled_two_cycles_graph(n, m, edge_labels=edge_labels, verbose=False)
    unexpected_graph = cfpq_data.labeled_two_cycles_graph(n, m + 1, edge_labels=edge_labels, verbose=False)

    actual_graph = networkx.nx.drawing.nx_pydot.read_dot(file)

    assert networkx.nx.is_isomorphic(expected_graph, actual_graph)
    assert not networkx.nx.is_isomorphic(unexpected_graph, actual_graph)
