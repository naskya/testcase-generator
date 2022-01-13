from __future__ import annotations

import math
import random

from modules.utility.colorizer import code
from modules.utility.exit_failure import exit_failure
from modules.utility.printer import error
from modules.variable.definition import Number, String, Variable


def generate_int(variable_name: str, variables: dict[str, Variable],
                 is_generated: list[bool], generated_values: list[list]) -> None:
    from modules.variable.generator import generate_value

    id = variables[variable_name].id

    low_evaluable_expr = ''
    low_v: int

    for token in variables[variable_name].low_expr:
        if token in variables:
            if token == variable_name:
                error(f'There is a circular reference in the lower limit of {code(variable_name)}.')
                exit_failure()
            elif isinstance(variables[token], (Number, String)):
                if not generate_value(token, variables, is_generated, generated_values):
                    return
                low_evaluable_expr += f'({generated_values[variables[token].id][0]})'
            else:
                if not generate_value(token, variables, is_generated, generated_values):
                    return
                low_evaluable_expr += f'({generated_values[variables[token].id]})'
        elif token in ('_i', '_j'):
            error(f'{code(variable_name)} is not subscriptable.')
            exit_failure()
        elif token == '.' or token.isnumeric():
            low_evaluable_expr += token
        else:
            low_evaluable_expr += (token + ' ')


    try:
        low_v = math.ceil(eval(low_evaluable_expr))
    except:
        error('Failed to evaluate the lower limit of {} (= {}).'.format(
            code(variable_name),
            code(low_evaluable_expr.strip())
        ))
        exit_failure()

    high_evaluable_expr = ''
    high_v: int

    for token in variables[variable_name].high_expr:
        if token in variables:
            if token == variable_name:
                error(f'There is a circular reference in the upper limit of {code(variable_name)}.')
                exit_failure()
            elif isinstance(variables[token], (Number, String)):
                if not generate_value(token, variables, is_generated, generated_values):
                    return
                high_evaluable_expr += f'({generated_values[variables[token].id][0]})'
            else:
                if not generate_value(token, variables, is_generated, generated_values):
                    return
                high_evaluable_expr += f'({generated_values[variables[token].id]})'
        elif token in ('_i', '_j'):
            error(f'{code(variable_name)} is not subscriptable.')
            exit_failure()
        elif token == '.' or token.isnumeric():
            high_evaluable_expr += token
        else:
            high_evaluable_expr += (token + ' ')

    try:
        high_v = math.floor(eval(high_evaluable_expr))
    except:
        error('Failed to evaluate the upper limit of {} (= {}).'.format(
            code(variable_name),
            code(high_evaluable_expr.strip())
        ))
        exit_failure()

    if low_v <= high_v:
        generated_values[id].append(random.randint(low_v, high_v))
        is_generated[id] = True


def generate_float(variable_name: str, variables: dict[str, Variable],
                   is_generated: list[bool], generated_values: list[list]) -> None:
    from modules.variable.generator import generate_value

    id = variables[variable_name].id

    low_evaluable_expr = ''
    low_v: float

    for token in variables[variable_name].low_expr:
        if token in variables:
            if token == variable_name:
                error(f'There is a circular reference in the lower limit of {code(variable_name)}.')
                exit_failure()
            elif isinstance(variables[token], (Number, String)):
                if not generate_value(token, variables, is_generated, generated_values):
                    return
                low_evaluable_expr += f'({generated_values[variables[token].id][0]})'
            else:
                if not generate_value(token, variables, is_generated, generated_values):
                    return
                low_evaluable_expr += f'({generated_values[variables[token].id]})'
        elif token in ('_i', '_j'):
            error(f'{code(variable_name)} is not subscriptable.')
            exit_failure()
        elif token == '.' or token.isnumeric():
            low_evaluable_expr += token
        else:
            low_evaluable_expr += (token + ' ')

    try:
        low_v = float(eval(low_evaluable_expr))
    except:
        error('Failed to evaluate the lower limit of {} (= {}).'.format(
            code(variable_name),
            code(low_evaluable_expr.strip())
        ))
        exit_failure()

    high_evaluable_expr = ''
    high_v: float

    for token in variables[variable_name].high_expr:
        if token in variables:
            if token == variable_name:
                error(f'There is a circular reference in the upper limit of {code(variable_name)}.')
                exit_failure()
            elif isinstance(variables[token], (Number, String)):
                if not generate_value(token, variables, is_generated, generated_values):
                    return
                high_evaluable_expr += f'({generated_values[variables[token].id][0]})'
            else:
                if not generate_value(token, variables, is_generated, generated_values):
                    return
                high_evaluable_expr += f'({generated_values[variables[token].id]})'
        elif token in ('_i', '_j'):
            error(f'{code(variable_name)} is not subscriptable.')
            exit_failure()
        elif token == '.' or token.isnumeric():
            high_evaluable_expr += token
        else:
            high_evaluable_expr += (token + ' ')

    try:
        high_v = float(eval(high_evaluable_expr))
    except:
        error('Failed to evaluate the upper limit of {} (= {}).'.format(
            code(variable_name),
            code(high_evaluable_expr.strip())
        ))
        exit_failure()

    if low_v == high_v:
        if low_v == round(low_v, variables[variable_name].float_digits):
            generated_values[id].append(low_v)
        else:
            error('There is no value (to assign to {}) within {}.'.format(
                code(variable_name),
                code(f'[{low_v}, {high_v}]')
            ))
            exit_failure()
    elif low_v <= high_v:
        v = round(random.uniform(low_v, high_v), variables[variable_name].float_digits)
        generated_values[id].append(v)
    else:
        error('The lower limit of {} (= {}) is greater than the upper limit of {} (= {}).'.format(
            code(variable_name),
            code(low_v),
            code(variable_name),
            code(high_v)
        ))
        exit_failure()

    is_generated[id] = True


def generate_number(variable_name: str, variables: dict[str, Variable],
                    is_generated: list[bool], generated_values: list[list]) -> bool:
    if variables[variable_name].float_digits == 0:
        generate_int(variable_name, variables, is_generated, generated_values)
        return is_generated[variables[variable_name].id]
    else:
        generate_float(variable_name, variables, is_generated, generated_values)
        return is_generated[variables[variable_name].id]
