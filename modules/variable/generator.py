from __future__ import annotations

from modules.utility.exit_failure import exit_failure
from modules.variable.definition import (
    Graph,
    Number,
    NumberArray,
    NumberMatrix,
    String,
    StringArray,
    Variable
)
from modules.variable.impl.graph import generate_graph
from modules.variable.impl.number import generate_number
from modules.variable.impl.number_array import generate_number_array
from modules.variable.impl.number_matrix import generate_number_matrix
from modules.variable.impl.sting_array import generate_string_array
from modules.variable.impl.string import generate_string


def generate_value(variable_name: str, variables: dict[str, Variable],
                   is_generated: list[bool], generated_values: list[list]) -> bool:
    if is_generated[variables[variable_name].id]:
        return True

    elif isinstance(variables[variable_name], Number):
        return generate_number(variable_name, variables, is_generated, generated_values)

    elif isinstance(variables[variable_name], NumberArray):
        return generate_number_array(variable_name, variables, is_generated, generated_values)

    elif isinstance(variables[variable_name], NumberMatrix):
        return generate_number_matrix(variable_name, variables, is_generated, generated_values)

    elif isinstance(variables[variable_name], String):
        return generate_string(variable_name, variables, is_generated, generated_values)

    elif isinstance(variables[variable_name], StringArray):
        return generate_string_array(variable_name, variables, is_generated, generated_values)

    elif isinstance(variables[variable_name], Graph):
        return generate_graph(variable_name, variables, is_generated, generated_values)

    else:
        exit_failure()
