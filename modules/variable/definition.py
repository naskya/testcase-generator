from __future__ import annotations

import keyword


class Variable:
    name: str
    id: int


class Number (Variable):
    low_expr: list[str]
    high_expr: list[str]
    float_digits: int


class String (Variable):
    length_low_expr: list[str]
    length_high_expr: list[str]
    is_characterwise_unique: bool
    character_set: str


class NumberArray (Variable):
    element: Number
    size_expr: list[str]
    is_increasing: bool
    is_decreasing: bool
    is_unique: bool
    is_printed_horizontally: bool


class StringArray (Variable):
    element: String
    size_expr: list[str]
    is_elementwise_unique: bool
    is_printed_horizontally: bool


class NumberMatrix (Variable):
    element: Number
    size_r_expr: list[str]
    size_c_expr: list[str]
    is_unique: bool


class Graph (Variable):
    number_of_vertices_expr: list[str]
    number_of_edges_expr: list[str]
    n_indexed: int
    is_printed_horizontally: bool
    is_tree: bool
    is_directed: bool
    is_connected: bool
    is_acyclic: bool
    no_multiple_edge: bool
    no_self_loop: bool


reserved_words: list[str] = ['min', 'max', 'sum'] + keyword.kwlist
