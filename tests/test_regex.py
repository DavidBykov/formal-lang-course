from typing import List, Iterable

import pytest

import project.regex
from project.regex import regex_to_min_dfa

from project.graph_utils import generate_two_cycles_graph, graph_to_nfa

import pyformlang
from pyformlang import finite_automaton
from pyformlang.finite_automaton import Symbol, DeterministicFiniteAutomaton, State
from pyformlang.regular_expression import MisformedRegexError

from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, State


def test_regex_to_dfa():
    regex = "(1 0) | (1 1) | (0 1) | (0 1 0 1)*"
    dfa = regex_to_min_dfa(regex)
    assert dfa.is_deterministic()


def test_get_min_dfa():
    expected_dfa = DeterministicFiniteAutomaton()

    state_0 = State(0)
    state_1 = State(1)

    symbol_a = Symbol("a")
    symbol_b = Symbol("b")
    symbol_c = Symbol("c")

    expected_dfa.add_start_state(state_0)

    expected_dfa.add_final_state(state_0)

    expected_dfa.add_transition(state_0, symbol_a, state_1)
    expected_dfa.add_transition(state_0, symbol_c, state_1)

    expected_dfa.add_transition(state_1, symbol_b, state_0)

    actual_dfa = regex_to_min_dfa("((a | c) b)*")
    assert expected_dfa.is_equivalent_to(actual_dfa)
    assert len(actual_dfa.states) == len(expected_dfa.states)


def test_regex_to_dfa_accept():
    regexes = ("", "(1 0) | (1 1) | (0 1) | (0 1 0 1)*", "a*")
    expected = (
        [],
        [
            [],
            [Symbol("1"), Symbol("0")],
            [Symbol("1"), Symbol("1")],
            [Symbol("0"), Symbol("1")],
            [Symbol("0"), Symbol("1"), Symbol("0"), Symbol("1")],
            [
                Symbol("0"),
                Symbol("1"),
                Symbol("0"),
                Symbol("1"),
                Symbol("0"),
                Symbol("1"),
                Symbol("0"),
                Symbol("1"),
            ],
        ],
        [[], [Symbol("a")], [Symbol("a"), Symbol("a")]],
    )

    for regex, expected_list in zip(regexes, expected):
        dfa = regex_to_min_dfa(regex)
        for expected_word in expected_list:
            assert dfa.accepts(expected_word)


def test_exception():
    with pytest.raises(MisformedRegexError):
        regex_to_min_dfa("*|wrong|*")


@pytest.fixture
def synt_graph():
    return generate_two_cycles_graph(3, 2, ("a", "b"))


@pytest.fixture
def expected_nfa():
    nfa = NondeterministicFiniteAutomaton()
    nfa.add_transitions(
        [
            (1, "a", 2),
            (2, "a", 3),
            (3, "a", 0),
            (0, "a", 1),
            (0, "b", 4),
            (4, "b", 5),
            (5, "b", 0),
        ]
    )
    return nfa


def test_nondeterministic(synt_graph):
    nfa = graph_to_nfa(synt_graph)
    assert not nfa.is_deterministic()


@pytest.mark.parametrize("start_nodes,final_nodes", [(None, None), ({0, 1}, {2, 3})])
def test_equivalence(synt_graph, expected_nfa, start_nodes, final_nodes):
    if not start_nodes:
        start_nodes = set(synt_graph.nodes)
    if not final_nodes:
        final_nodes = set(synt_graph.nodes)

    for state in start_nodes:
        expected_nfa.add_start_state(State(state))

    for state in final_nodes:
        expected_nfa.add_final_state(State(state))

    actual_nfa = graph_to_nfa(synt_graph, start_nodes, final_nodes)

    assert actual_nfa.is_equivalent_to(expected_nfa)
