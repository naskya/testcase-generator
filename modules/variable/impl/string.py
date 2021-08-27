from __future__ import annotations

import math
import random

from modules.utility.colorizer import Color, colorize
from modules.utility.exit_failure import exit_failure
from modules.utility.printer import error
from modules.variable.definition import Number, VariableType
from modules.variable.impl.definition import number_of_trial


def generate_string_impl(length: int, character_set: str, is_characterwise_unique: bool) -> tuple[
    # succeeded?
    bool,
    # result (NOT a string but a list of characters (because string is immutable in Python))
    #        (want to use statements like S[0] = 'a' to override characters)
    list[str]
]:
    from modules.variable.impl.number_array import generate_permutation

    number_of_characters = len(character_set)
    result: list[str] = []

    # is it a permutation?
    if is_characterwise_unique and length == number_of_characters:
        indices = generate_permutation(0, length)

        for index in indices:
            result.append(character_set[index])
    else:
        for _ in range(length):
            c = random.randint(0, number_of_characters - 1)

            if is_characterwise_unique:
                for _ in range(number_of_trial):
                    if not character_set[c] in result:
                        break

                    c = random.randint(0, number_of_characters - 1)

                if character_set[c] in result:
                    return (False, '')

            result.append(character_set[c])

    return (True, result)


def generate_string(variable_name: str, variables: dict[str, VariableType],
                    is_generated: list[bool], generated_values: list[list]) -> bool:
    from modules.variable.generator import generate_value

    id = variables[variable_name].id

    length_low_evaluable_expr = ''
    length_low_v: int

    for token in variables[variable_name].length_low_expr:
        if token in variables:
            if isinstance(variables[token], Number):
                if not generate_value(token, variables, is_generated, generated_values):
                    return False
                length_low_evaluable_expr += f'({generated_values[variables[token].id][0]})'
            else:
                error('{} is used in the lower limit of the length of {} but is not a number.'.format(
                    colorize(Color.CODE, token),
                    colorize(Color.CODE, variable_name)
                ))
                exit_failure()
        elif token in ('_i', '_j'):
            error(f'{colorize(Color.CODE, variable_name)} is not subscriptable.')
            exit_failure()
        else:
            length_low_evaluable_expr += (token + ' ')

    try:
        raw_value = eval(length_low_evaluable_expr)
        length_low_v = math.ceil(raw_value)
        if (not variables[variable_name].length_low_incl) and (length_low_v == raw_value):
            length_low_v += 1
    except:
        error('Failed to evaluate the lower limit of the length of {} (= {}).'.format(
            colorize(Color.CODE, variable_name),
            colorize(Color.CODE, length_low_evaluable_expr.strip())
        ))
        exit_failure()

    length_high_evaluable_expr = ''
    length_high_v: int

    for token in variables[variable_name].length_high_expr:
        if token in variables:
            if isinstance(variables[token], Number):
                if not generate_value(token, variables, is_generated, generated_values):
                    return False
                length_high_evaluable_expr += f'({generated_values[variables[token].id][0]})'
            else:
                error('{} is used in the upper limit of the length of {} but is not a number.'.format(
                    colorize(Color.CODE, token),
                    colorize(Color.CODE, variable_name)
                ))
                exit_failure()
        elif token in ('_i', '_j'):
            error(f'{colorize(Color.CODE, variable_name)} is not subscriptable.')
            exit_failure()
        else:
            length_high_evaluable_expr += (token + ' ')

    try:
        raw_value = eval(length_high_evaluable_expr)
        length_high_v = math.floor(raw_value)
        if (not variables[variable_name].length_high_incl) and (length_high_v == raw_value):
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
    number_of_characters = len(variables[variable_name].character_set)

    if variables[variable_name].is_characterwise_unique and (length_v > number_of_characters):
        error('There are not enough characters to form a string {} of length {}.'.format(
            colorize(Color.CODE, variable_name),
            colorize(Color.CODE, length_v)
        ))
        exit_failure()

    generated_values[id].append('')

    is_generated[id], generated_values[id][0] = generate_string_impl(length_v,
                                                                     variables[variable_name].character_set,
                                                                     variables[variable_name].is_characterwise_unique)

    return is_generated[id]
