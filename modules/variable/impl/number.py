from __future__ import annotations

import math
import random

from modules.utility.colorizer import Color, colorize
from modules.utility.exit_failure import exit_failure
from modules.utility.printer import error
from modules.variable.definition import Number, VariableType
from modules.variable.impl.definition import number_of_trial


def generate_int(variable_name: str, variables: dict[str, VariableType],
                 is_generated: list[bool], generated_values: list[list]) -> None:
    from modules.variable.generator import generate_value

    id = variables[variable_name].id

    low_evaluable_expr = ''
    low_v: int

    for token in variables[variable_name].low_expr:
        if token in variables:
            if token == variable_name:
                error(f'There is a circular reference in the lower limit of {colorize(Color.CODE, variable_name)}.')
                exit_failure()
            elif isinstance(variables[token], Number):
                if not generate_value(token, variables, is_generated, generated_values):
                    return
                low_evaluable_expr += f'({generated_values[variables[token].id][0]})'
            else:
                error('{} is used in the lower limit of {} but is not a number.'.format(
                    colorize(Color.CODE, token),
                    colorize(Color.CODE, variable_name)
                ))
                exit_failure()
        elif token in ('_i', '_j'):
            error(f'{colorize(Color.CODE, variable_name)} is not subscriptable.')
            exit_failure()
        else:
            low_evaluable_expr += token

    try:
        raw_value = eval(low_evaluable_expr)
        low_v = math.ceil(raw_value)
        if (not variables[variable_name].low_incl) and (low_v == raw_value):
            low_v += 1
    except:
        error('Failed to evaluate the lower limit of {} (= {}).'.format(
            colorize(Color.CODE, variable_name),
            colorize(Color.CODE, low_evaluable_expr)
        ))
        exit_failure()

    high_evaluable_expr = ''
    high_v: int

    for token in variables[variable_name].high_expr:
        if token in variables:
            if token == variable_name:
                error(f'There is a circular reference in the upper limit of {colorize(Color.CODE, variable_name)}.')
                exit_failure()
            elif isinstance(variables[token], Number):
                if not generate_value(token, variables, is_generated, generated_values):
                    return
                high_evaluable_expr += f'({generated_values[variables[token].id][0]})'
            else:
                error('{} is used in the upper limit of {} but is not a number.'.format(
                    colorize(Color.CODE, token),
                    colorize(Color.CODE, variable_name)
                ))
                exit_failure()
        elif token in ('_i', '_j'):
            error(f'{colorize(Color.CODE, variable_name)} is not subscriptable.')
            exit_failure()
        else:
            high_evaluable_expr += token

    try:
        raw_value = eval(high_evaluable_expr)
        high_v = math.floor(raw_value)
        if (not variables[variable_name].high_incl) and (high_v == raw_value):
            high_v -= 1
    except:
        error('Failed to evaluate the upper limit of {} (= {}).'.format(
            colorize(Color.CODE, variable_name),
            colorize(Color.CODE, high_evaluable_expr)
        ))
        exit_failure()

    if low_v <= high_v:
        generated_values[id].append(random.randint(low_v, high_v))
        is_generated[id] = True


def generate_float(variable_name: str, variables: dict[str, VariableType],
                   is_generated: list[bool], generated_values: list[list]) -> None:
    from modules.variable.generator import generate_value

    id = variables[variable_name].id

    low_evaluable_expr = ''
    low_v: float

    for token in variables[variable_name].low_expr:
        if token in variables:
            if token == variable_name:
                error(f'There is a circular reference in the lower limit of {colorize(Color.CODE, variable_name)}.')
                exit_failure()
            elif isinstance(variables[token], Number):
                if not generate_value(token, variables, is_generated, generated_values):
                    return
                low_evaluable_expr += f'({generated_values[variables[token].id][0]})'
            else:
                error('{} is used in the lower limit of {} but is not a number.'.format(
                    colorize(Color.CODE, token),
                    colorize(Color.CODE, variable_name)
                ))
                exit_failure()
        elif token in ('_i', '_j'):
            error(f'{colorize(Color.CODE, variable_name)} is not subscriptable.')
            exit_failure()
        else:
            low_evaluable_expr += token

    try:
        low_v = float(eval(low_evaluable_expr))
    except:
        error('Failed to evaluate the lower limit of {} (= {}).'.format(
            colorize(Color.CODE, variable_name),
            colorize(Color.CODE, low_evaluable_expr)
        ))
        exit_failure()

    high_evaluable_expr = ''
    high_v: float

    for token in variables[variable_name].high_expr:
        if token in variables:
            if token == variable_name:
                error(f'There is a circular reference in the upper limit of {colorize(Color.CODE, variable_name)}.')
                exit_failure()
            elif isinstance(variables[token], Number):
                if not generate_value(token, variables, is_generated, generated_values):
                    return
                high_evaluable_expr += f'({generated_values[variables[token].id][0]})'
            else:
                error('{} is used in the upper limit of {} but is not a number.'.format(
                    colorize(Color.CODE, token),
                    colorize(Color.CODE, variable_name)
                ))
                exit_failure()
        elif token in ('_i', '_j'):
            error(f'{colorize(Color.CODE, variable_name)} is not subscriptable.')
            exit_failure()
        else:
            high_evaluable_expr += token

    try:
        high_v = float(eval(high_evaluable_expr))
    except:
        error('Failed to evaluate the upper limit of {} (= {}).'.format(
            colorize(Color.CODE, variable_name),
            colorize(Color.CODE, high_evaluable_expr)
        ))
        exit_failure()

    if low_v == high_v:
        if variables[variable_name].low_incl and variables[variable_name].high_incl:
            generated_values[id].append(low_v)
            is_generated[id] = True
    elif low_v <= high_v:
        for _ in range(number_of_trial):
            v = random.uniform(low_v, high_v)
            if (variables[variable_name].low_incl or v != low_v) and (variables[variable_name].high_incl or v != high_v):
                generated_values[id].append(v)
                break
        is_generated[id] = True


def generate_number(variable_name: str, variables: dict[str, VariableType],
                    is_generated: list[bool], generated_values: list[list]) -> bool:
    if variables[variable_name].is_integer:
        generate_int(variable_name, variables, is_generated, generated_values)
        return is_generated[variables[variable_name].id]
    else:
        generate_float(variable_name, variables, is_generated, generated_values)
        return is_generated[variables[variable_name].id]
