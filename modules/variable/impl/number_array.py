from __future__ import annotations

import math
import random

from modules.utility.colorizer import Color, colorize
from modules.utility.exit_failure import exit_failure
from modules.utility.printer import error
from modules.variable.definition import Number, NumberArray, VariableType
from modules.variable.impl.definition import epsilon, number_of_trial


def generate_permutation(start: int, size: int) -> list[int]:
    result = [i for i in range(start, start + size)]
    random.shuffle(result)
    return result


def generate_increasing_int_array(low: int, high: int, size: int, strict: bool) -> list[int]:
    result = [0] * size

    if strict:
        high -= (size - 1)

    generate_freely = (random.random() < 0.05)
    if generate_freely:
        for i in range(size):
            result[i] = random.randint(low, high)
            low = result[i]
    else:
        low_orig = low
        for i in range(size):
            result[i] = random.randint(low, max(low, min(high, low_orig + round((high - low_orig) / size * (i + 1)))))
            low = result[i]

    if strict:
        for i in range(size):
            result[i] += i

    return result


def generate_increasing_float_array(low: float, high: float, size: int, strict: bool) -> list[float]:
    result = [0.0] * size

    min_diff = 0.0 if (size == 1) else min(epsilon, (high - low) / (size - 1))
    if strict:
        high -= min_diff * (size - 1)

    generate_freely = (random.random() < 0.05)
    if generate_freely:
        for i in range(size):
            result[i] = random.uniform(low, high)
            low = result[i]
    else:
        low_orig = low
        for i in range(size):
            result[i] = random.uniform(low, max(low, low_orig + (high - low_orig) / size * (i + 1)))
            low = result[i]

    if strict:
        for i in range(size):
            result[i] += i * min_diff

    return result


def generate_decreasing_int_array(low: int, high: int, size: int, strict: bool) -> list[int]:
    return generate_increasing_int_array(low, high, size, strict)[::-1]


def generate_decreasing_float_array(low: float, high: float, size: int, strict: bool) -> list[float]:
    return generate_increasing_float_array(low, high, size, strict)[::-1]


def generate_int_array_with_fixed_range(low: int, high: int, size: int, unique: bool) -> list[int]:
    result: list[int] = []

    for _ in range(size):
        v = random.randint(low, high)

        if unique:
            while v in result:
                v = random.randint(low, high)

        result.append(v)

    return result


def generate_float_array_with_fixed_range(low: float, high: float, size: int, unique: bool) -> list[float]:
    result: list[float] = []

    for _ in range(size):
        v = random.uniform(low, high)

        if unique:
            while v in result:
                v = random.uniform(low, high)

        result.append(v)

    return result


def generate_int_array(variable_name: str, variables: dict[str, VariableType],
                       is_generated: list[bool], generated_values: list[list]) -> None:
    from modules.variable.generator import generate_value

    id = variables[variable_name].id

    size_evaluable_expr = ''
    size_v: int

    for token in variables[variable_name].size_expr:
        if token in variables:
            if isinstance(variables[token], Number):
                if not generate_value(token, variables, is_generated, generated_values):
                    return
                size_evaluable_expr += f'({generated_values[variables[token].id][0]})'
            else:
                error('{} is used in the size of {} but is not a number.'.format(
                    colorize(Color.CODE, token),
                    colorize(Color.CODE, variable_name)
                ))
                exit_failure()
        elif token in ('_i', '_j'):
            error(f'The size of {colorize(Color.CODE, variable_name)} is not subscriptable.')
            exit_failure()
        else:
            size_evaluable_expr += (token + ' ')

    try:
        size_v = round(eval(size_evaluable_expr))
    except:
        error('Failed to evaluate the size of {} (= {}).'.format(
            colorize(Color.CODE, variable_name),
            colorize(Color.CODE, size_evaluable_expr.strip())
        ))
        exit_failure()

    if size_v == 0:
        is_generated[id] = True
        return

    low_v = [0] * size_v

    for i in range(size_v):
        low_evaluable_expr = ''

        for token in variables[variable_name].element.low_expr:
            if token in variables:
                if i == 0:
                    if token == variable_name:
                        error(f'There is a circular reference in the lower limit of {colorize(Color.CODE, variable_name)}.')
                        exit_failure()
                    else:
                        if not generate_value(token, variables, is_generated, generated_values):
                            return

                if isinstance(variables[token], Number):
                    low_evaluable_expr += f'({generated_values[variables[token].id][0]})'
                elif isinstance(variables[token], NumberArray):
                    if i == 0:
                        if size_v != len(generated_values[variables[token].id]):
                            error('The size of {} (= {}) is not equal to that of {} (= {}).'.format(
                                colorize(Color.CODE, token),
                                colorize(Color.CODE, len(generated_values[variables[token].id])),
                                colorize(Color.CODE, variable_name),
                                colorize(Color.CODE, size_v)
                            ))
                            exit_failure()
                    low_evaluable_expr += f'({generated_values[variables[token].id][i]})'
                else:
                    error('{} is not comparable with {}.'.format(
                        colorize(Color.CODE, token),
                        colorize(Color.CODE, variable_name)
                    ))
                    exit_failure()
            elif token == '_i':
                low_evaluable_expr += str(i)
            elif token == '_j':
                error('{} is unavailable for {} since {} is not a matrix.'.format(
                    colorize(Color.CODE, '_j'),
                    colorize(Color.CODE, variable_name),
                    colorize(Color.CODE, variable_name)
                ))
                exit_failure()
            else:
                low_evaluable_expr += (token + ' ')

        try:
            raw_val = eval(low_evaluable_expr)
            low_v[i] = math.ceil(raw_val)

            if (not variables[variable_name].element.low_incl) and (raw_val == low_v[i]):
                low_v[i] += 1
        except:
            error('Failed to evaluate the lower limit of {} (= {}).'.format(
                colorize(Color.CODE, f'{variable_name}[{i}]'),
                colorize(Color.CODE, low_evaluable_expr.strip())
            ))
            exit_failure()

    high_v = [0] * size_v

    for i in range(size_v):
        high_evaluable_expr = ''

        for token in variables[variable_name].element.high_expr:
            if token in variables:
                if i == 0:
                    if token == variable_name:
                        error(f'There is a circular reference in the upper limit of {colorize(Color.CODE, variable_name)}.')
                        exit_failure()
                    else:
                        if not generate_value(token, variables, is_generated, generated_values):
                            return

                if isinstance(variables[token], Number):
                    high_evaluable_expr += f'({generated_values[variables[token].id][0]})'
                elif isinstance(variables[token], NumberArray):
                    if i == 0:
                        if size_v != len(generated_values[variables[token].id]):
                            error('The size of {} (= {}) is not equal to that of {} (= {}).'.format(
                                colorize(Color.CODE, token),
                                colorize(Color.CODE, len(generated_values[variables[token].id])),
                                colorize(Color.CODE, variable_name),
                                colorize(Color.CODE, size_v)
                            ))
                            exit_failure()
                    high_evaluable_expr += f'({generated_values[variables[token].id][i]})'
                else:
                    error('{} is not comparable with {}.'.format(
                        colorize(Color.CODE, token),
                        colorize(Color.CODE, variable_name)
                    ))
                    exit_failure()
            elif token == '_i':
                high_evaluable_expr += str(i)
            elif token == '_j':
                error('{} is unavailable for {} since {} is not a matrix.'.format(
                    colorize(Color.CODE, '_j'),
                    colorize(Color.CODE, variable_name),
                    colorize(Color.CODE, variable_name)
                ))
                exit_failure()
            else:
                high_evaluable_expr += (token + ' ')

        try:
            raw_val = eval(high_evaluable_expr)
            high_v[i] = math.floor(raw_val)

            if (not variables[variable_name].element.high_incl) and (raw_val == high_v[i]):
                high_v[i] -= 1
        except:
            error('Failed to evaluate the upper limit of {} (= {}).'.format(
                colorize(Color.CODE, f'{variable_name}[{i}]'),
                colorize(Color.CODE, high_evaluable_expr.strip())
            ))
            exit_failure()

    is_fixed_limit = all((l == low_v[0]) for l in low_v) and all((h == high_v[0]) for h in high_v)

    if is_fixed_limit and (low_v[0] > high_v[0]):
        return

    # is it a permutation?
    if is_fixed_limit and (low_v[0] + size_v - 1 == high_v[0]) and variables[variable_name].is_unique:
        generated_values[id] = generate_permutation(low_v[0], size_v)
        is_generated[id] = True
        return

    # is it an increasing sequence with a fixed limit?
    if is_fixed_limit and variables[variable_name].is_increasing:
        generated_values[id] = generate_increasing_int_array(
            low_v[0], high_v[0], size_v, variables[variable_name].is_unique)
        is_generated[id] = True
        return

    # is it a decreasing sequence with a fixed limit?
    if is_fixed_limit and variables[variable_name].is_decreasing:
        generated_values[id] = generate_decreasing_int_array(
            low_v[0], high_v[0], size_v, variables[variable_name].is_unique)
        is_generated[id] = True
        return

    # is it a sequence with a fixed limit?
    if is_fixed_limit:
        if variables[variable_name].is_unique and (high_v[0] - low_v[0] + 1 < size_v):
            return
        generated_values[id] = generate_int_array_with_fixed_range(
            low_v[0], high_v[0], size_v, variables[variable_name].is_unique)
        is_generated[id] = True
        return

    if variables[variable_name].is_increasing:
        low = low_v[0]

        for i in range(size_v):
            if max(low, low_v[i]) > high_v[i]:
                return

            v = random.randint(max(low, low_v[i]), high_v[i])

            if variables[variable_name].is_unique:
                for _ in range(number_of_trial):
                    if not v in generated_values[id]:
                        break
                    v = random.randint(max(low, low_v[i]), high_v[i])

                if v in generated_values[id]:
                    return

            generated_values.append(v)
            low = v

        is_generated[id] = True
        return

    if variables[variable_name].is_decreasing:
        high = high_v[0]

        for i in range(size_v):
            if low_v[i] > min(high, high_v[i]):
                return

            v = random.randint(low_v[i], min(high, high_v[i]))

            if variables[variable_name].is_unique:
                for _ in range(number_of_trial):
                    if not v in generated_values[id]:
                        break
                    v = random.randint(low_v[i], min(high, high_v[i]))

                if v in generated_values[id]:
                    return

            generated_values[id].append(v)
            high = v

        is_generated[id] = True
        return

    for i in range(size_v):
        if low_v[i] > high_v[i]:
            return

        v = random.randint(low_v[i], high_v[i])

        if variables[variable_name].is_unique:
            for _ in range(number_of_trial):
                if not v in generated_values[id]:
                    break
                v = random.randint(low_v[i], high_v[i])

            if v in generated_values[id]:
                return

        generated_values[id].append(v)

    is_generated[id] = True


def generate_float_array(variable_name: str, variables: dict[str, VariableType],
                         is_generated: list[bool], generated_values: list[list]) -> None:
    from modules.variable.generator import generate_value

    id = variables[variable_name].id

    size_evaluable_expr = ''
    size_v: int

    for token in variables[variable_name].size_expr:
        if token in variables:
            if isinstance(variables[token], Number):
                if not generate_value(token, variables, is_generated, generated_values):
                    return
                size_evaluable_expr += f'({generated_values[variables[token].id][0]})'
            else:
                error('{} is used in the size of {} but is not a number.'.format(
                    colorize(Color.CODE, token),
                    colorize(Color.CODE, variable_name)
                ))
                exit_failure()
        elif token in ('_i', '_j'):
            error(f'The size of {colorize(Color.CODE, variable_name)} is not subscriptable.')
            exit_failure()
        else:
            size_evaluable_expr += (token + ' ')

    try:
        size_v = round(eval(size_evaluable_expr))
    except:
        error('Failed to evaluate the size of {} (= {}).'.format(
            colorize(Color.CODE, variable_name),
            colorize(Color.CODE, size_evaluable_expr.strip())
        ))
        exit_failure()

    if size_v == 0:
        is_generated[id] = True
        return

    low_v = [0.0] * size_v

    for i in range(size_v):
        low_evaluable_expr = ''

        for token in variables[variable_name].element.low_expr:
            if token in variables:
                if i == 0:
                    if token == variable_name:
                        error(f'There is a circular reference in the lower limit of {colorize(Color.CODE, variable_name)}.')
                        exit_failure()
                    else:
                        if not generate_value(token, variables, is_generated, generated_values):
                            return

                if isinstance(variables[token], Number):
                    low_evaluable_expr += f'({generated_values[variables[token].id][0]})'
                elif isinstance(variables[token], NumberArray):
                    if i == 0:
                        if size_v != len(generated_values[variables[token].id]):
                            error('The size of {} (= {}) is not equal to that of {} (= {}).'.format(
                                colorize(Color.CODE, token),
                                colorize(Color.CODE, len(generated_values[variables[token].id])),
                                colorize(Color.CODE, variable_name),
                                colorize(Color.CODE, size_v)
                            ))
                            exit_failure()
                    low_evaluable_expr += f'({generated_values[variables[token].id][i]})'
                else:
                    error('{} is not comparable with {}.'.format(
                        colorize(Color.CODE, token),
                        colorize(Color.CODE, variable_name)
                    ))
                    exit_failure()
            elif token == '_i':
                low_evaluable_expr += str(i)
            elif token == '_j':
                error('{} is unavailable for {} since {} is not a matrix.'.format(
                    colorize(Color.CODE, '_j'),
                    colorize(Color.CODE, variable_name),
                    colorize(Color.CODE, variable_name)
                ))
                exit_failure()
            else:
                low_evaluable_expr += (token + ' ')

        try:
            low_v[i] = float(eval(low_evaluable_expr))
        except:
            error('Failed to evaluate the lower limit of  {} (= {}).'.format(
                colorize(Color.CODE, f'{variable_name}[{i}]'),
                colorize(Color.CODE, low_evaluable_expr.strip())
            ))
            exit_failure()

        if not variables[variable_name].element.low_incl:
            low_v[i] += epsilon

    high_v = [0.0] * size_v

    for i in range(size_v):
        high_evaluable_expr = ''

        for token in variables[variable_name].element.high_expr:
            if token in variables:
                if i == 0:
                    if token == variable_name:
                        error(f'There is a circular reference in the upper limit of {colorize(Color.CODE, variable_name)}.')
                        exit_failure()
                    else:
                        if not generate_value(token, variables, is_generated, generated_values):
                            return

                if isinstance(variables[token], Number):
                    high_evaluable_expr += f'({generated_values[variables[token].id][0]})'
                elif isinstance(variables[token], NumberArray):
                    if i == 0:
                        if size_v != len(generated_values[variables[token].id]):
                            error('The size of {} (= {}) is not equal to that of {} (= {}).'.format(
                                colorize(Color.CODE, token),
                                colorize(Color.CODE, len(generated_values[variables[token].id])),
                                colorize(Color.CODE, variable_name),
                                colorize(Color.CODE, size_v)
                            ))
                            exit_failure()
                    high_evaluable_expr += f'({generated_values[variables[token].id][i]})'
                else:
                    error('{} is not comparable with {}.'.format(
                        colorize(Color.CODE, token),
                        colorize(Color.CODE, variable_name)
                    ))
                    exit_failure()
            elif token == '_i':
                high_evaluable_expr += str(i)
            elif token == '_j':
                error('{} is unavailable for {} since {} is not a matrix.'.format(
                    colorize(Color.CODE, '_j'),
                    colorize(Color.CODE, variable_name),
                    colorize(Color.CODE, variable_name)
                ))
                exit_failure()
            else:
                high_evaluable_expr += (token + ' ')

        try:
            high_v[i] = float(eval(high_evaluable_expr))
        except:
            error('Failed to evaluate the upper limit of {} (= {}).'.format(
                colorize(Color.CODE, f'{variable_name}[{i}]'),
                colorize(Color.CODE, high_evaluable_expr.strip())
            ))
            exit_failure()

        if not variables[variable_name].element.high_incl:
            high_v[i] -= epsilon

    is_fixed_limit = all((l == low_v[0]) for l in low_v) and all((h == high_v[0]) for h in high_v)

    if is_fixed_limit and (low_v[0] > high_v[0]):
        return

    # is it an increasing sequence with a fixed limit?
    if is_fixed_limit and variables[variable_name].is_increasing:
        generated_values[id] = generate_increasing_float_array(
            low_v[0], high_v[0], size_v, variables[variable_name].is_unique)
        is_generated[id] = True
        return

    # is it a decreasing sequence with a fixed limit?
    if is_fixed_limit and variables[variable_name].is_decreasing:
        generated_values[id] = generate_decreasing_float_array(
            low_v[0], high_v[0], size_v, variables[variable_name].is_unique)
        is_generated[id] = True
        return

    # is it a sequence with a fixed limit?
    if is_fixed_limit:
        generated_values[id] = generate_float_array_with_fixed_range(
            low_v[0], high_v[0], size_v, variables[variable_name].is_unique)
        is_generated[id] = True
        return

    if variables[variable_name].is_increasing:
        low = low_v[0]

        for i in range(size_v):
            if max(low, low_v[i]) > high_v[i]:
                return

            v = random.uniform(max(low, low_v[i]), high_v[i])

            if variables[variable_name].is_unique:
                for _ in range(number_of_trial):
                    if not v in generated_values[id]:
                        break
                    v = random.uniform(max(low, low_v[i]), high_v[i])

                if v in generated_values[id]:
                    return

            generated_values.append(v)
            low = v

        is_generated[id] = True
        return

    if variables[variable_name].is_decreasing:
        high = high_v[0]

        for i in range(size_v):
            if low_v[i] > min(high, high_v[i]):
                return

            v = random.randint(low_v[i], min(high, high_v[i]))

            if variables[variable_name].is_unique:
                for _ in range(number_of_trial):
                    if not v in generated_values[id]:
                        break
                    v = random.randint(low_v[i], min(high, high_v[i]))

                if v in generated_values[id]:
                    return

            generated_values[id].append(v)
            high = v

        is_generated[id] = True
        return

    for i in range(size_v):
        if low_v[i] > high_v[i]:
            return

        v = random.randint(low_v[i], high_v[i])

        if variables[variable_name].is_unique:
            for _ in range(number_of_trial):
                if not v in generated_values[id]:
                    break
                v = random.randint(low_v[i], high_v[i])

            if v in generated_values[id]:
                return

        generated_values[id].append(v)

    is_generated[id] = True


def generate_number_array(variable_name: str, variables: dict[str, VariableType],
                          is_generated: list[bool], generated_values: list[list]) -> bool:
    if variables[variable_name].element.is_integer:
        for _ in range(number_of_trial):
            generate_int_array(variable_name, variables, is_generated, generated_values)

            if is_generated[variables[variable_name].id]:
                return True
    else:
        for _ in range(number_of_trial):
            generate_float_array(variable_name, variables, is_generated, generated_values)

            if is_generated[variables[variable_name].id]:
                return True

    return False
