from __future__ import annotations

import math
import random

from modules.utility.colorizer import Color, colorize
from modules.utility.exit_failure import exit_failure
from modules.utility.printer import error
from modules.variable.definition import (
    Graph,
    Number,
    NumberArray,
    NumberMatrix,
    String,
    StringArray,
    Variable
)
from modules.variable.impl.definition import number_of_trial


def generate_int_matrix(variable_name: str, variables: dict[str, Variable],
                        is_generated: list[bool], generated_values: list[list]) -> None:
    from modules.variable.generator import generate_value

    id = variables[variable_name].id

    size_r_evaluable_expr = ''
    size_r_v: int

    for token in variables[variable_name].size_r_expr:
        if token in variables:
            if token == variable_name:
                error(f'There is a circular reference in the number of rows in {colorize(Color.CODE, variable_name)}.')
                exit_failure()
            elif isinstance(variables[token], (Number, String)):
                if not generate_value(token, variables, is_generated, generated_values):
                    return
                size_r_evaluable_expr += f'({generated_values[variables[token].id][0]})'
            else:
                if not generate_value(token, variables, is_generated, generated_values):
                    return
                size_r_evaluable_expr += f'({generated_values[variables[token].id]})'
        elif token in ('_i', '_j'):
            error(f'The number of rows in {colorize(Color.CODE, variable_name)} is not subscriptable.')
            exit_failure()
        elif token == '.' or token.isnumeric():
            size_r_evaluable_expr += token
        else:
            size_r_evaluable_expr += (token + ' ')

    try:
        size_r_v = round(eval(size_r_evaluable_expr))
    except:
        error('Failed to evaluate the number of rows in {} (= {}).'.format(
            colorize(Color.CODE, variable_name),
            colorize(Color.CODE, size_r_evaluable_expr.strip())
        ))
        exit_failure()

    size_c_evaluable_expr = ''
    size_c_v: int

    for token in variables[variable_name].size_c_expr:
        if token in variables:
            if token == variable_name:
                error(f'There is a circular reference in the number of columns in {colorize(Color.CODE, variable_name)}.')
                exit_failure()
            elif isinstance(variables[token], (Number, String)):
                if not generate_value(token, variables, is_generated, generated_values):
                    return
                size_c_evaluable_expr += f'({generated_values[variables[token].id][0]})'
            else:
                if not generate_value(token, variables, is_generated, generated_values):
                    return
                size_c_evaluable_expr += f'({generated_values[variables[token].id]})'
        elif token in ('_i', '_j'):
            error(f'The number of columns in {colorize(Color.CODE, variable_name)} is not subscriptable.')
            exit_failure()
        elif token == '.' or token.isnumeric():
            size_c_evaluable_expr += token
        else:
            size_c_evaluable_expr += (token + ' ')

    try:
        size_c_v = round(eval(size_c_evaluable_expr))
    except:
        error('Failed to evaluate the number of columns in {} (= {}).'.format(
            colorize(Color.CODE, variable_name),
            colorize(Color.CODE, size_c_evaluable_expr.strip())
        ))
        exit_failure()

    generated_values[id] = [[0] * size_c_v for _ in range(size_r_v)]
    used_values: set[int] = set()

    for i in range(size_r_v):
        for j in range(size_c_v):
            low_evaluable_expr = ''
            low_v: int

            for token in variables[variable_name].element.low_expr:
                if token in variables:
                    if (i == 0) and (j == 0):
                        if token == variable_name:
                            error(f'There is a circular reference in the lower limit of {colorize(Color.CODE, variable_name)}.')
                            exit_failure()
                        elif not generate_value(token, variables, is_generated, generated_values):
                            return

                    token_id = variables[token].id

                    if isinstance(variables[token], (Number, String)):
                        low_evaluable_expr += f'({generated_values[token_id][0]})'
                    elif isinstance(variables[token], (Graph, NumberArray, StringArray)):
                        if (i == 0) and (j == 0):
                            if variables[token].is_printed_horizontally and (size_c_v != len(generated_values[token_id])):
                                error('The number of columns in {} (= {}) is not equal to the size of {} (= {}).'.format(
                                    colorize(Color.CODE, token),
                                    colorize(Color.CODE, len(generated_values[token_id])),
                                    colorize(Color.CODE, variable_name),
                                    colorize(Color.CODE, size_c_v)
                                ))
                                exit_failure()
                            elif (not variables[token].is_printed_horizontally) and (size_r_v != len(generated_values[token_id])):
                                error('The number of rows in {} (= {}) is not equal to the size of {} (= {}).'.format(
                                    colorize(Color.CODE, token),
                                    colorize(Color.CODE, len(generated_values[token_id])),
                                    colorize(Color.CODE, variable_name),
                                    colorize(Color.CODE, size_c_v)
                                ))
                                exit_failure()

                        if variables[token].is_printed_horizontally:
                            low_evaluable_expr += f'({generated_values[token_id][j]})'
                        else:
                            low_evaluable_expr += f'({generated_values[token_id][i]})'

                    elif isinstance(variables[token], NumberMatrix):
                        if (i == 0) and (j == 0):
                            if (size_r_v != len(generated_values[token_id])):
                                error('The number of rows in {} (= {}) is not equal to that of {} (= {}).'.format(
                                    colorize(Color.CODE, token),
                                    colorize(Color.CODE, len(generated_values[token_id])),
                                    colorize(Color.CODE, variable_name),
                                    colorize(Color.CODE, size_r_v)
                                ))
                                exit_failure()
                            elif (size_c_v != len(generated_values[token_id][0])):
                                error('The number of columns in {} (= {}) is not equal to that of {} (= {}).'.format(
                                    colorize(Color.CODE, token),
                                    colorize(Color.CODE, len(generated_values[token_id][0])),
                                    colorize(Color.CODE, variable_name),
                                    colorize(Color.CODE, size_c_v)
                                ))
                                exit_failure()
                        low_evaluable_expr += f'({generated_values[token_id][i][j]})'
                elif token == '_i':
                    low_evaluable_expr += str(i)
                elif token == '_j':
                    low_evaluable_expr += str(j)
                elif token == '.' or token.isnumeric():
                    low_evaluable_expr += token
                else:
                    low_evaluable_expr += (token + ' ')

            try:
                low_v = math.ceil(eval(low_evaluable_expr))
            except:
                error('Failed to evaluate the lower limit of {} (= {}).'.format(
                    colorize(Color.CODE, f'{variable_name}[{i}][{j}]'),
                    colorize(Color.CODE, low_evaluable_expr.strip())
                ))
                exit_failure()

            high_evaluable_expr = ''
            high_v: int

            for token in variables[variable_name].element.high_expr:
                if token in variables:
                    if (i == 0) and (j == 0):
                        if token == variable_name:
                            error(f'There is a circular reference in the upper limit of {colorize(Color.CODE, variable_name)}.')
                            exit_failure()
                        elif not generate_value(token, variables, is_generated, generated_values):
                            return

                    token_id = variables[token].id

                    if isinstance(variables[token], (Number, String)):
                        high_evaluable_expr += f'({generated_values[token_id][0]})'

                    elif isinstance(variables[token], (Graph, NumberArray, StringArray)):
                        if (i == 0) and (j == 0):
                            if variables[token].is_printed_horizontally and (size_c_v != len(generated_values[token_id])):
                                error('The number of columns in {} (= {}) is not equal to the size of {} (= {}).'.format(
                                    colorize(Color.CODE, token),
                                    colorize(Color.CODE, len(generated_values[token_id])),
                                    colorize(Color.CODE, variable_name),
                                    colorize(Color.CODE, size_c_v)
                                ))
                                exit_failure()
                            elif (not variables[token].is_printed_horizontally) and (size_r_v != len(generated_values[token_id])):
                                error('The number of rows in {} (= {}) is not equal to the size of {} (= {}).'.format(
                                    colorize(Color.CODE, token),
                                    colorize(Color.CODE, len(generated_values[token_id])),
                                    colorize(Color.CODE, variable_name),
                                    colorize(Color.CODE, size_c_v)
                                ))
                                exit_failure()

                        if variables[token].is_printed_horizontally:
                            high_evaluable_expr += f'({generated_values[token_id][j]})'
                        else:
                            high_evaluable_expr += f'({generated_values[token_id][i]})'

                    elif isinstance(variables[token], NumberMatrix):
                        if (i == 0) and (j == 0):
                            if (size_r_v != len(generated_values[token_id])):
                                error('The number of rows in {} (= {}) is not equal to that of {} (= {}).'.format(
                                    colorize(Color.CODE, token),
                                    colorize(Color.CODE, len(generated_values[token_id])),
                                    colorize(Color.CODE, variable_name),
                                    colorize(Color.CODE, size_r_v)
                                ))
                                exit_failure()
                            elif (size_c_v != len(generated_values[token_id][0])):
                                error('The number of columns in {} (= {}) is not equal to that of {} (= {}).'.format(
                                    colorize(Color.CODE, token),
                                    colorize(Color.CODE, len(generated_values[token_id][0])),
                                    colorize(Color.CODE, variable_name),
                                    colorize(Color.CODE, size_c_v)
                                ))
                                exit_failure()
                        high_evaluable_expr += f'({generated_values[token_id][i][j]})'
                    else:
                        high_evaluable_expr += f'({generated_values[token_id]})'

                elif token == '_i':
                    high_evaluable_expr += str(i)
                elif token == '_j':
                    high_evaluable_expr += str(j)
                elif token == '.' or token.isnumeric():
                    high_evaluable_expr += token
                else:
                    high_evaluable_expr += (token + ' ')

            try:
                high_v = math.floor(eval(high_evaluable_expr))
            except:
                error('Failed to evaluate the upper limit of {} (= {}).'.format(
                    colorize(Color.CODE, f'{variable_name}[{i}][{j}]'),
                    colorize(Color.CODE, high_evaluable_expr.strip())
                ))
                exit_failure()

            if low_v > high_v:
                return

            v = random.randint(low_v, high_v)

            if variables[variable_name].is_unique:
                for _ in range(number_of_trial):
                    if not v in used_values:
                        break
                    v = random.randint(low_v, high_v)
                if v in used_values:
                    return
                used_values.add(v)

            generated_values[id][i][j] = v

    is_generated[id] = True


def generate_float_matrix(variable_name: str, variables: dict[str, Variable],
                          is_generated: list[bool], generated_values: list[list]) -> None:
    from modules.variable.generator import generate_value

    id = variables[variable_name].id

    size_r_evaluable_expr = ''
    size_r_v: int

    for token in variables[variable_name].size_r_expr:
        if token in variables:
            if token == variable_name:
                error(f'There is a circular reference in the number of rows in {colorize(Color.CODE, variable_name)}.')
                exit_failure()
            elif isinstance(variables[token], (Number, String)):
                if not generate_value(token, variables, is_generated, generated_values):
                    return
                size_r_evaluable_expr += f'({generated_values[variables[token].id][0]})'
            else:
                if not generate_value(token, variables, is_generated, generated_values):
                    return
                size_r_evaluable_expr += f'({generated_values[variables[token].id]})'
        elif token in ('_i', '_j'):
            error(f'The number of rows in {colorize(Color.CODE, variable_name)} is not subscriptable.')
            exit_failure()
        elif token == '.' or token.isnumeric():
            size_r_evaluable_expr += token
        else:
            size_r_evaluable_expr += (token + ' ')

    try:
        size_r_v = round(eval(size_r_evaluable_expr))
    except:
        error('Failed to evaluate the number of rows in {} (= {}).'.format(
            colorize(Color.CODE, variable_name),
            colorize(Color.CODE, size_r_evaluable_expr.strip())
        ))
        exit_failure()

    size_c_evaluable_expr = ''
    size_c_v: int

    for token in variables[variable_name].size_c_expr:
        if token in variables:
            if token == variable_name:
                error(f'There is a circular reference in the number of columns in {colorize(Color.CODE, variable_name)}.')
                exit_failure()
            elif isinstance(variables[token], (Number, String)):
                if not generate_value(token, variables, is_generated, generated_values):
                    return
                size_c_evaluable_expr += f'({generated_values[variables[token].id][0]})'
            else:
                if not generate_value(token, variables, is_generated, generated_values):
                    return
                size_c_evaluable_expr += f'({generated_values[variables[token].id]})'
        elif token in ('_i', '_j'):
            error(f'The number of columns in {colorize(Color.CODE, variable_name)} is not subscriptable.')
            exit_failure()
        elif token == '.' or token.isnumeric():
            size_c_evaluable_expr += token
        else:
            size_c_evaluable_expr += (token + ' ')

    try:
        size_c_v = round(eval(size_c_evaluable_expr))
    except:
        error('Failed to evaluate the number of columns in {} (= {}).'.format(
            colorize(Color.CODE, variable_name),
            colorize(Color.CODE, size_c_evaluable_expr.strip())
        ))
        exit_failure()

    generated_values[id] = [[0.0] * size_c_v for _ in range(size_r_v)]
    used_values: set[float] = set()

    for i in range(size_r_v):
        for j in range(size_c_v):
            low_evaluable_expr = ''
            low_v: float

            for token in variables[variable_name].element.low_expr:
                if token in variables:
                    if (i == 0) and (j == 0):
                        if token == variable_name:
                            error(f'There is a circular reference in the lower limit of {colorize(Color.CODE, variable_name)}.')
                            exit_failure()
                        elif not generate_value(token, variables, is_generated, generated_values):
                            return

                    token_id = variables[token].id

                    if isinstance(variables[token], (Number, String)):
                        low_evaluable_expr += f'({generated_values[token_id][0]})'

                    elif isinstance(variables[token], (Graph, NumberArray, StringArray)):
                        if (i == 0) and (j == 0):
                            if variables[token].is_printed_horizontally and (size_c_v != len(generated_values[token_id])):
                                error('The number of columns in {} (= {}) is not equal to the size of {} (= {}).'.format(
                                    colorize(Color.CODE, token),
                                    colorize(Color.CODE, len(generated_values[token_id])),
                                    colorize(Color.CODE, variable_name),
                                    colorize(Color.CODE, size_c_v)
                                ))
                                exit_failure()
                            elif (not variables[token].is_printed_horizontally) and (size_r_v != len(generated_values[token_id])):
                                error('The number of rows in {} (= {}) is not equal to the size of {} (= {}).'.format(
                                    colorize(Color.CODE, token),
                                    colorize(Color.CODE, len(generated_values[token_id])),
                                    colorize(Color.CODE, variable_name),
                                    colorize(Color.CODE, size_r_v)
                                ))
                                exit_failure()

                        if variables[token].is_printed_horizontally:
                            low_evaluable_expr += f'({generated_values[token_id][j]})'
                        else:
                            low_evaluable_expr += f'({generated_values[token_id][i]})'

                    elif isinstance(variables[token], NumberMatrix):
                        if (i == 0) and (j == 0):
                            if (size_r_v != len(generated_values[token_id])):
                                error('The number of rows in {} (= {}) is not equal to that of {} (= {}).'.format(
                                    colorize(Color.CODE, token),
                                    colorize(Color.CODE, len(generated_values[token_id])),
                                    colorize(Color.CODE, variable_name),
                                    colorize(Color.CODE, size_r_v)
                                ))
                                exit_failure()
                            elif (size_c_v != len(generated_values[token_id][0])):
                                error('The number of columns in {} (= {}) is not equal to that of {} (= {}).'.format(
                                    colorize(Color.CODE, token),
                                    colorize(Color.CODE, len(generated_values[token_id][0])),
                                    colorize(Color.CODE, variable_name),
                                    colorize(Color.CODE, size_c_v)
                                ))
                                exit_failure()

                        low_evaluable_expr += f'({generated_values[token_id][i][j]})'
                    else:
                        low_evaluable_expr += f'({generated_values[token_id]})'

                elif token == '_i':
                    low_evaluable_expr += str(i)
                elif token == '_j':
                    low_evaluable_expr += str(j)
                elif token == '.' or token.isnumeric():
                    low_evaluable_expr += token
                else:
                    low_evaluable_expr += (token + ' ')

            try:
                low_v = float(eval(low_evaluable_expr))
            except:
                error('Failed to evaluate the lower limit of {} (= {}).'.format(
                    colorize(Color.CODE, f'{variable_name}[{i}][{j}]'),
                    colorize(Color.CODE, low_evaluable_expr.strip())
                ))
                exit_failure()

            high_evaluable_expr = ''
            high_v: float

            for token in variables[variable_name].element.high_expr:
                if token in variables:
                    if (i == 0) and (j == 0):
                        if token == variable_name:
                            error(f'There is a circular reference in the upper limit of {colorize(Color.CODE, variable_name)}.')
                            exit_failure()
                        elif not generate_value(token, variables, is_generated, generated_values):
                            return

                    token_id = variables[token].id

                    if isinstance(variables[token], (Number, String)):
                        high_evaluable_expr += f'({generated_values[token_id][0]})'

                    elif isinstance(variables[token], (Graph, NumberArray, StringArray)):
                        if (i == 0) and (j == 0):
                            if variables[token].is_printed_horizontally and (size_c_v != len(generated_values[token_id])):
                                error('The number of columns in {} (= {}) is not equal to the size of {} (= {}).'.format(
                                    colorize(Color.CODE, token),
                                    colorize(Color.CODE, len(generated_values[token_id])),
                                    colorize(Color.CODE, variable_name),
                                    colorize(Color.CODE, size_c_v)
                                ))
                                exit_failure()
                            elif (not variables[token].is_printed_horizontally) and (size_r_v != len(generated_values[token_id])):
                                error('The number of rows in {} (= {}) is not equal to the size of {} (= {}).'.format(
                                    colorize(Color.CODE, token),
                                    colorize(Color.CODE, len(generated_values[token_id])),
                                    colorize(Color.CODE, variable_name),
                                    colorize(Color.CODE, size_r_v)
                                ))
                                exit_failure()

                        if variables[token].is_printed_horizontally:
                            high_evaluable_expr += f'({generated_values[token_id][j]})'
                        else:
                            high_evaluable_expr += f'({generated_values[token_id][i]})'

                    elif isinstance(variables[token], NumberMatrix):
                        if (i == 0) and (j == 0):
                            if (size_r_v != len(generated_values[token_id])):
                                error('The number of rows in {} (= {}) is not equal to that of {} (= {}).'.format(
                                    colorize(Color.CODE, token),
                                    colorize(Color.CODE, len(generated_values[token_id])),
                                    colorize(Color.CODE, variable_name),
                                    colorize(Color.CODE, size_r_v)
                                ))
                                exit_failure()
                            elif (size_c_v != len(generated_values[token_id][0])):
                                error('The number of columns in {} (= {}) is not equal to that of {} (= {}).'.format(
                                    colorize(Color.CODE, token),
                                    colorize(Color.CODE, len(generated_values[token_id][0])),
                                    colorize(Color.CODE, variable_name),
                                    colorize(Color.CODE, size_c_v)
                                ))
                                exit_failure()

                        high_evaluable_expr += f'({generated_values[token_id][i][j]})'
                    else:
                        high_evaluable_expr += f'({generated_values[token_id]})'

                elif token == '_i':
                    high_evaluable_expr += str(i)
                elif token == '_j':
                    high_evaluable_expr += str(j)
                elif token == '.' or token.isnumeric():
                    high_evaluable_expr += token
                else:
                    high_evaluable_expr += (token + ' ')

            try:
                high_v = float(eval(high_evaluable_expr))
            except:
                error('Failed to evaluate the upper limit of {} (= {}).'.format(
                    colorize(Color.CODE, f'{variable_name}[{i}][{j}]'),
                    colorize(Color.CODE, high_evaluable_expr.strip())
                ))
                exit_failure()

            if low_v > high_v:
                return

            v = round(random.uniform(low_v, high_v), variables[variable_name].element.float_digits)

            if variables[variable_name].is_unique:
                for _ in range(number_of_trial):
                    if not v in used_values:
                        break
                    v = round(random.uniform(low_v, high_v), variables[variable_name].element.float_digits)
                if v in used_values:
                    return
                used_values.add(v)

            generated_values[id][i][j] = v

    is_generated[id] = True


def generate_number_matrix(variable_name: str, variables: dict[str, Variable],
                           is_generated: list[bool], generated_values: list[list]) -> bool:
    if variables[variable_name].element.float_digits == 0:
        for _ in range(number_of_trial):
            generate_int_matrix(variable_name, variables, is_generated, generated_values)

            if is_generated[variables[variable_name].id]:
                return True
    else:
        for _ in range(number_of_trial):
            generate_float_matrix(variable_name, variables, is_generated, generated_values)

            if is_generated[variables[variable_name].id]:
                return True

    return False
