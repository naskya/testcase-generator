from __future__ import annotations

import math
import random

from modules.utility.colorizer import Color, colorize
from modules.utility.exit_failure import exit_failure
from modules.utility.printer import error
from modules.variable.definition import Number, String, VariableType
from modules.variable.impl.definition import number_of_trial
from modules.variable.impl.string import generate_string_impl


def generate_string_array_impl(variable_name: str, variables: dict[str, VariableType],
                               is_generated: list[bool], generated_values: list[list]) -> None:
    from modules.variable.generator import generate_value

    id = variables[variable_name].id

    size_evaluable_expr = ''

    for token in variables[variable_name].size_expr:
        if token in variables:
            if token == variable_name:
                error(f'There is a circular reference in the size of {colorize(Color.CODE, variable_name)}.')
                exit_failure()
            elif isinstance(variables[token], (Number, String)):
                if not generate_value(token, variables, is_generated, generated_values):
                    return
                size_evaluable_expr += f'({generated_values[variables[token].id][0]})'
            else:
                if not generate_value(token, variables, is_generated, generated_values):
                    return
                size_evaluable_expr += f'({generated_values[variables[token].id]})'
        elif token in ('_i', '_j'):
            error(f'The size of {variable_name} is not subscriptable.')
            exit_failure()
        elif token == '.' or token.isnumeric():
            size_evaluable_expr += token
        else:
            size_evaluable_expr += (token + ' ')

    size_v: int

    try:
        size_v = round(eval(size_evaluable_expr))
    except:
        error('Failed to evaluate the size of {} (= {}).'.format(
            colorize(Color.CODE, variable_name),
            colorize(Color.CODE, size_evaluable_expr.strip())
        ))
        exit_failure()

    generated_values[variables[variable_name].id] = []
    number_of_characters = len(variables[variable_name].element.character_set)

    for i in range(size_v):
        length_low_evaluable_expr = ''
        length_low_v: int

        for token in variables[variable_name].element.length_low_expr:
            if token in variables:
                if token == variable_name:
                    error(f'There is a circular reference in the lower limit of the length of {colorize(Color.CODE, variable_name)}.')
                    exit_failure()
                elif isinstance(variables[token], (Number, String)):
                    if not generate_value(token, variables, is_generated, generated_values):
                        return
                    length_low_evaluable_expr += f'({generated_values[variables[token].id][0]})'
                else:
                    if not generate_value(token, variables, is_generated, generated_values):
                        return
                    length_low_evaluable_expr += f'({generated_values[variables[token].id]})'
            elif token == '_i':
                length_low_evaluable_expr += str(i)
            elif token == '_j':
                error('{} is unavailable for {} since {} is not a matrix.'.format(
                    colorize(Color.CODE, '_j'),
                    colorize(Color.CODE, variable_name),
                    colorize(Color.CODE, variable_name)
                ))
            elif token == '.' or token.isnumeric():
                length_low_evaluable_expr += token
            else:
                length_low_evaluable_expr += (token + ' ')

        try:
            raw_value = eval(length_low_evaluable_expr)
            length_low_v = math.ceil(raw_value)
            if (not variables[variable_name].element.length_low_incl) and (length_low_v == raw_value):
                length_low_v += 1
        except:
            error('Failed to evaluate the lower limit of the length of {} (= {}).'.format(
                colorize(Color.CODE, variable_name),
                colorize(Color.CODE, length_low_evaluable_expr.strip())
            ))
            exit_failure()

        length_high_evaluable_expr = ''
        length_high_v: int

        for token in variables[variable_name].element.length_high_expr:
            if token in variables:
                if token == variable_name:
                    error(f'There is a circular reference in the upper limit of the length of {colorize(Color.CODE, variable_name)}.')
                    exit_failure()
                elif isinstance(variables[token], (Number, String)):
                    if not generate_value(token, variables, is_generated, generated_values):
                        return
                    length_high_evaluable_expr += f'({generated_values[variables[token].id][0]})'
                else:
                    if not generate_value(token, variables, is_generated, generated_values):
                        return
                    length_high_evaluable_expr += f'({generated_values[variables[token].id]})'
            elif token == '_i':
                length_high_evaluable_expr += str(i)
            elif token == '_j':
                error('{} is unavailable for {} since {} is not a matrix.'.format(
                    colorize(Color.CODE, '_j'),
                    colorize(Color.CODE, variable_name),
                    colorize(Color.CODE, variable_name)
                ))
            elif token == '.' or token.isnumeric():
                length_high_evaluable_expr += token
            else:
                length_high_evaluable_expr += (token + ' ')

        try:
            raw_value = eval(length_high_evaluable_expr)
            length_high_v = math.floor(raw_value)
            if (not variables[variable_name].element.length_high_incl) and (length_high_v == raw_value):
                length_high_v -= 1
        except:
            error('Failed to evaluate the upper limit of the length of {} (= {}).'.format(
                colorize(Color.CODE, variable_name),
                colorize(Color.CODE, length_high_evaluable_expr.strip())
            ))
            exit_failure()

        if length_low_v > length_high_v:
            return

        length_v = random.randint(length_low_v, length_high_v)

        if variables[variable_name].element.is_characterwise_unique and (length_v > number_of_characters):
            error('There are not enough characters to form a string {} of length {}.'.format(
                colorize(Color.CODE, f'{variable_name}[{i}]'),
                colorize(Color.CODE, length_v)
            ))
            exit_failure()

        success, s = generate_string_impl(length_v,
                                          variables[variable_name].element.character_set,
                                          variables[variable_name].element.is_characterwise_unique)

        if variables[variable_name].is_elementwise_unique:
            for _ in range(number_of_trial):
                if success and (not s in generated_values[id]):
                    break

                success, s = generate_string_impl(length_v,
                                                  variables[variable_name].element.character_set,
                                                  variables[variable_name].element.is_characterwise_unique)

            if (not success) or (s in generated_values[id]):
                return
        elif not success:
            for _ in range(number_of_trial):
                success, s = generate_string_impl(length_v,
                                                  variables[variable_name].element.character_set,
                                                  variables[variable_name].element.is_characterwise_unique)
                if success:
                    break

            if not success:
                return

        generated_values[id].append(s)

    is_generated[id] = True


def generate_string_array(variable_name: str, variables: dict[str, VariableType],
                          is_generated: list[bool], generated_values: list[list]) -> bool:
    for _ in range(number_of_trial):
        generate_string_array_impl(variable_name, variables, is_generated, generated_values)

        if is_generated[variables[variable_name].id]:
            return True

    return False
