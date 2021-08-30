from __future__ import annotations

import keyword
import typing


class VariableBase:
    name: str
    id: int


class Number (VariableBase):
    low_expr: list[str]
    high_expr: list[str]
    low_incl: bool
    high_incl: bool
    is_integer: bool
    float_digits: int


class String (VariableBase):
    length_low_expr: list[str]
    length_high_expr: list[str]
    length_low_incl: bool
    length_high_incl: bool
    is_characterwise_unique: bool
    character_set: str


class NumberArray (VariableBase):
    element: Number
    size_expr: list[str]
    is_increasing: bool
    is_decreasing: bool
    is_unique: bool
    is_printed_horizontally: bool


class StringArray (VariableBase):
    element: String
    size_expr: list[str]
    is_elementwise_unique: bool
    is_printed_horizontally: bool


class NumberMatrix (VariableBase):
    element: Number
    size_r_expr: list[str]
    size_c_expr: list[str]
    is_unique: bool


class Graph (VariableBase):
    number_of_vertices_expr: list[str]
    number_of_edges_expr: list[str]
    n_indexed: int
    is_tree: bool
    is_directed: bool
    is_connected: bool
    is_acyclic: bool
    no_multiple_edge: bool
    no_self_loop: bool


# type alias
VariableType = typing.Union[Number, String, NumberArray, StringArray, NumberMatrix, Graph]

reserved_words: list[str] = ['min', 'max', 'sum'] + keyword.kwlist
