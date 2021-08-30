from __future__ import annotations

from modules.utility.exit_failure import exit_failure
from modules.utility.printer import error
from modules.variable.definition import (
    Graph,
    Number,
    NumberArray,
    NumberMatrix,
    String,
    StringArray,
    VariableType
)


def generate_case(variables: dict[str, VariableType], generated_values: list[list], format: list[list[str]]) -> str:
    result = ''

    for line in format:
        number_of_rows = -1

        # determine the number of rows
        for variable_name in line:
            if variable_name in variables:
                if isinstance(variables[variable_name], (NumberArray, StringArray)):
                    if variables[variable_name].is_printed_horizontally:
                        if number_of_rows == -1:
                            number_of_rows = 1
                        elif number_of_rows != 1:
                            error(f'The number of rows in {", ".join(line)} do not match.')
                            exit_failure()
                    else:
                        if number_of_rows == -1:
                            number_of_rows = len(generated_values[variables[variable_name].id])
                        elif number_of_rows != len(generated_values[variables[variable_name].id]):
                            error(f'The number of rows in {", ".join(line)} do not match.')
                            exit_failure()
                else:
                    if number_of_rows == -1:
                        number_of_rows = len(generated_values[variables[variable_name].id])
                    elif number_of_rows != len(generated_values[variables[variable_name].id]):
                        error(f'The number of rows in {", ".join(line)} do not match.')
                        exit_failure()

        if number_of_rows == -1:
            number_of_rows = 1

        # format
        for i in range(number_of_rows):
            for variable_name in line:
                if variable_name in variables:
                    if isinstance(variables[variable_name], Number):
                        if variables[variable_name].is_integer:
                            result += f'{generated_values[variables[variable_name].id][0]} '
                        else:
                            d = variables[variable_name].float_digits
                            result += f'{generated_values[variables[variable_name].id][0]:.{d}f} '
                    elif isinstance(variables[variable_name], String):
                        result += f'{"".join(generated_values[variables[variable_name].id][0])} '
                    elif isinstance(variables[variable_name], NumberArray):
                        if variables[variable_name].element.is_integer:
                            if variables[variable_name].is_printed_horizontally:
                                result += ' '.join(map(str, generated_values[variables[variable_name].id]))
                                result += ' '
                            else:
                                result += f'{generated_values[variables[variable_name].id][i]} '
                        else:
                            d = variables[variable_name].element.float_digits
                            if variables[variable_name].is_printed_horizontally:
                                result += ' '.join(map(lambda x: f'{x:.{d}f}', generated_values[variables[variable_name].id]))
                                result += ' '
                            else:
                                result += f'{generated_values[variables[variable_name].id][i]:.{d}f} '
                    elif isinstance(variables[variable_name], StringArray):
                        if variables[variable_name].is_printed_horizontally:
                            for s_i_as_list_of_char in generated_values[variables[variable_name].id]:
                                result += ''.join(s_i_as_list_of_char)
                                result += ' '
                        else:
                            result += f'{"".join(generated_values[variables[variable_name].id][i])} '
                    elif isinstance(variables[variable_name], NumberMatrix):
                        if variables[variable_name].element.is_integer:
                            result += ' '.join(map(str, generated_values[variables[variable_name].id][i]))
                            result += ' '
                        else:
                            d = variables[variable_name].element.float_digits
                            result += ' '.join(map(lambda x: f'{x:.{d}f}', generated_values[variables[variable_name].id][i]))
                            result += ' '
                    elif isinstance(variables[variable_name], Graph):
                        u, v = generated_values[variables[variable_name].id][i]
                        result += f'{u} {v} '
                    else:
                        result += ' '.join(map(str, generated_values[variables[variable_name].id]))
                        result += ' '
                else:
                    result += f'{variable_name} '

            if (len(result) > 0) and (result[-1] == ' '):
                result = result[:-1] + '\n'
            else:
                result += '\n'

    return result
