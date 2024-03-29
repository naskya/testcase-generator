from __future__ import annotations

from modules.case.generator import generate_case
from modules.variable.definition import Variable
from modules.variable.generator import generate_value
from modules.variable.overrider import override_all


def generate_one_case(variables: dict[str, Variable], override_statements: str, format: list[list[str]]) -> tuple[
    # succeeded?
    bool,
    # result
    str
]:
    is_generated = [False] * len(variables)
    generated_values = [[] for _ in variables]

    for variable_name in variables:
        if not generate_value(variable_name, variables, is_generated, generated_values):
            return False, ''

    override_all(override_statements, generated_values)

    return True, generate_case(variables, generated_values, format)
