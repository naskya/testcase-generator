from __future__ import annotations

import io
import re
import sys
import typing
import warnings

from modules.utility.colorizer import Color, colorize
from modules.utility.exit_failure import exit_failure
from modules.utility.printer import error, prompt, warning
from modules.variable.definition import (
    Graph,
    Number,
    NumberArray,
    NumberMatrix,
    String,
    StringArray,
    VariableType,
    reserved_words
)


def ensure(expr: bool):
    if not expr:
        exit_failure()


# tokens in expressions
token_pattern = re.compile(
    r'\s*(<<=|>>=|\/\/=|==|!=|\+=|-=|\*=|\/=|%=|^=|\|=|&=|<=|>=|\*\*|<<|>>|\/\/|\\\'|\\\"|\'|\"|\+|-|\*|\/|%|~|\||&|\^|<|>|=|!|\.|,|:|\(|\)|\[|\]|[^\'\"<=>!+\-\*/\^\\|&%~.,:()[\]\s]+)\s*'
)


def parse_character_set(name: str, characters: str) -> str:
    #    characters 'a-f0-9.#\\'
    # ->     tokens ['af' '09' '.' '#' '\']
    # ->     result 'abcdef0123456789.#\'
    tokens: list[str] = []
    result = ''

    skip = 0
    in_character_range = False

    for i in range(len(characters)):
        if skip > 0:
            skip -= 1
            continue

        if characters[i] == '\\':
            if i == len(characters) - 1:
                error('{} (in the character set of {}) must be escaped like {}.'.format(
                    colorize(Color.CODE, '\\'),
                    colorize(Color.CODE, name),
                    colorize(Color.CODE, '\\\\')
                ))
                exit_failure()
            elif not characters[i + 1] in ('\\', '-', '>'):
                error('{} (in the character set of {}) must not be escaped. Do you mean {}?'.format(
                    colorize(Color.CODE, characters[i + 1]),
                    colorize(Color.CODE, name),
                    colorize(Color.CODE, characters[:i] + '\\\\' + characters[i + 1:])
                ))
                exit_failure()
            elif in_character_range:
                ensure(len(tokens) != 0)
                ensure(len(tokens[-1]) == 1)
                tokens[-1] += characters[i + 1]
                in_character_range = False
                skip = 1
            else:
                tokens.append(characters[i + 1])
                skip = 1

        elif characters[i] == '-':
            if in_character_range:
                error('{} (in the character set of {}) must be escaped like {}.'.format(
                    colorize(Color.CODE, '-'),
                    colorize(Color.CODE, name),
                    colorize(Color.CODE, '\\-')
                ))
                exit_failure()
            else:
                ensure(len(tokens) != 0)
                ensure(len(tokens[-1]) == 1)
                in_character_range = True

        elif in_character_range:
            ensure(len(tokens) != 0)
            ensure(len(tokens[-1]) == 1)
            tokens[-1] += characters[i]
            in_character_range = False

        else:
            tokens.append(characters[i])

    for t in tokens:
        if len(t) == 1:
            result += t
        elif len(t) == 2:
            if ord(t[0]) > ord(t[1]):
                error('Character range {} (in the character set of {}) is invalid.'.format(
                    colorize(Color.CODE, f'{t[0]}-{t[1]}'),
                    colorize(Color.CODE, name)
                ))
                exit_failure()
            else:
                result += ''.join(map(chr, range(ord(t[0]), ord(t[1]) + 1)))
        else:
            exit_failure()

    result_reduced = ''.join(set(result))

    if len(result) < len(result_reduced):
        warning('There are duplicate characters in the character set of {} (= {}).'.format(
            colorize(Color.CODE, name),
            colorize(Color.CODE, characters)
        ))

    return result_reduced


def split_two_expr(expressions: str) -> tuple[str, str]:
    paren_depth = 0
    inside_single_quote = False
    inside_double_quote = False

    comma_position = -1

    for i in range(len(expressions)):
        if (expressions[i] == ',') and (not inside_single_quote) and (not inside_double_quote) and (paren_depth == 0):
            comma_position = i
            break

        elif expressions[i] == '\'':
            if (i == 0) or (expressions[i - 1] != '\\'):
                inside_single_quote ^= True

        elif expressions[i] == '\"':
            if (i == 0) or (expressions[i - 1] != '\\'):
                inside_double_quote ^= True

        elif (not inside_single_quote) and (not inside_double_quote) and (expressions[i] == '('):
            paren_depth += 1

        elif (not inside_single_quote) and (not inside_double_quote) and (expressions[i] == ')'):
            paren_depth -= 1

    if comma_position == -1:
        error(f'Failed to split {colorize(Color.CODE, expressions)} into two expressions.')
        exit_failure()

    return expressions[:comma_position], expressions[comma_position + 1:]


def process_expr(expr: str) -> list[str]:
    return [token[0].strip() for token in re.finditer(token_pattern, expr)]


def parse_variable(source: typing.TextIO | io.typing.TextIOWrapper) -> tuple[
    # key: variable name, value: variable (Number | String | NumberArray | ...)
    dict[str, VariableType],
    # override statements
    str
]:
    # comments are begin with '%%'
    comment_pattern = re.compile(r'%%.*$')
    # variable names must be consisted of alphanumeric characters and _, must not be empty, and must not begin with _.
    name_pattern = re.compile(r'[A-Za-z0-9][A-Za-z0-9_]*')
    warnings.simplefilter('ignore', FutureWarning)
    int_pattern = re.compile(
        # int   name         [|(   expr]|)
        r'int\s+([^[(\s]+)\s*([[(])(.+)([\])])'
    )
    float_pattern = re.compile(
        # float   <   digits  >   name         [|(   expr]|)
        r'float\s*<\s*(\d+)\s*>\s+([^[(\s]+)\s*([[(])(.+)([\])])'
    )
    str_pattern = re.compile(
        # str   <char>   name        [|(   expr]|)       attribute
        r'str\s*<(.+)>\s*([^[(\s])\s*([[(])(.+)([\])])\s*(.*)'
    )
    int_array_pattern = re.compile(
        # row|col     <   int   ,expr>   name         [|(   expr]|)       attribute
        r'(row|col)\s*<\s*int\s*,(.+)>\s*([^[(\s]+)\s*([[(])(.+)([\])])\s*(.*)'
    )
    float_array_pattern = re.compile(
        # row|col     <   float   <   digits  >   ,expr>   name         [|(   expr]|)       attribute
        r'(row|col)\s*<\s*float\s*<\s*(\d+)\s*>\s*,(.+)>\s*([^[(\s]+)\s*([[(])(.+)([\])])\s*(.*)'
    )
    str_array_pattern = re.compile(
        # row|col     <   str<char>,expr>   name         [|(   expr]|)       attribute
        r'(row|col)\s*<\s*str<(.+)>,(.+)>\s*([^[(\s]+)\s*([[(])(.+)([\])])\s*(.*)'
    )
    int_matrix_pattern = re.compile(
        # mat   <   int   ,expr>   name         [|(   expr]|)       attribute
        r'mat\s*<\s*int\s*,(.+)>\s*([^[(\s]+)\s*([[(])(.+)([\])])\s*(.*)'
    )
    float_matrix_pattern = re.compile(
        # mat   <   float   <   digits  >   ,expr>   name         [|(   expr]|)       attribute
        r'mat\s*<\s*float\s*<\s*(\d+)\s*>\s*,(.+)>\s*([^[(\s]+)\s*([[(])(.+)([\])])\s*(.*)'
    )
    tree_pattern = re.compile(
        # tree   <expr>   name       attribute
        r'tree\s*<(.+)>\s*([^\s]+)\s*(.*)'
    )
    graph_pattern = re.compile(
        # graph   <expr>   name       attribute
        r'graph\s*<(.+)>\s*([^\s]+)\s*(.*)'
    )
    warnings.simplefilter('default', FutureWarning)

    variables: dict[str, VariableType] = {}
    has_override_statement = False

    if (source == sys.stdin) and (sys.stdin.isatty()):
        prompt()

    for line in source:
        line = re.sub(comment_pattern, '', line).strip()

        if len(line) == 0:
            continue
        elif line == '---':
            break
        elif line == '+++':
            has_override_statement = True
            break

        # is it an integer?
        if (match_obj := re.fullmatch(int_pattern, line)) != None:
            name = match_obj[1]

            if name in variables:
                error(f'Variable called {colorize(Color.CODE, name)} has already been declared.')
                exit_failure()
            elif re.fullmatch(name_pattern, name) == None:
                error(f'{colorize(Color.CODE, name)} is not a valid name.')
                exit_failure()
            elif name in reserved_words:
                error(f'{colorize(Color.CODE, name)} is one of the reserved words.')
                exit_failure()

            var = Number()
            var.name = name
            var.id = len(variables)
            var.float_digits = 0

            var.low_expr, var.high_expr = map(process_expr, split_two_expr(match_obj[3]))
            if match_obj[2] == '(':
                var.low_expr = ['('] + var.low_expr + [')', '+', '1']
            if match_obj[4] == ')':
                var.high_expr = ['('] + var.high_expr + [')', '-', '1']

            variables[name] = var

        # is it a floating point number?
        elif (match_obj := re.fullmatch(float_pattern, line)) != None:
            name = match_obj[2]

            if name in variables:
                error(f'Variable called {colorize(Color.CODE, name)} has already been declared.')
                exit_failure()
            elif re.fullmatch(name_pattern, name) == None:
                error(f'{colorize(Color.CODE, name)} is not a valid name.')
                exit_failure()
            elif name in reserved_words:
                error(f'{colorize(Color.CODE, name)} is one of the reserved words.')
                exit_failure()

            var = Number()
            var.name = name
            var.id = len(variables)
            var.float_digits = int(match_obj[1])

            var.low_expr, var.high_expr = map(process_expr, split_two_expr(match_obj[4]))
            if match_obj[3] == '(':
                var.low_expr = ['('] + var.low_expr + [')', '+', '10', '**', '(', '-', f'{var.float_digits}', ')', '/', '2']
            if match_obj[5] == ')':
                var.high_expr = ['('] + var.high_expr + [')', '-', '10', '**', '(', '-', f'{var.float_digits}', ')', '/', '2']

            variables[name] = var

        # is it a string?
        elif (match_obj := re.fullmatch(str_pattern, line)) != None:
            name = match_obj[2]

            if name in variables:
                error(f'Variable called {colorize(Color.CODE, name)} has already been declared.')
                exit_failure()
            elif re.fullmatch(name_pattern, name) == None:
                error(f'{colorize(Color.CODE, name)} is not a valid name.')
                exit_failure()
            elif name in reserved_words:
                error(f'{colorize(Color.CODE, name)} is one of the reserved words.')
                exit_failure()
            elif not match_obj[6] in ('', 'distinct'):
                warning('The attribute {} (for {}) is ignored since it is unknown.'.format(
                    colorize(Color.CODE, match_obj[7]),
                    colorize(Color.CODE, name)
                ))

            var = String()
            var.name = name
            var.id = len(variables)

            var.character_set = parse_character_set(name, match_obj[1])
            var.is_characterwise_unique = (match_obj[6] == 'distinct')

            var.length_low_expr, var.length_high_expr = map(process_expr, split_two_expr(match_obj[4]))
            if match_obj[3] == '(':
                var.length_low_expr = ['('] + var.length_low_expr + [')', '+', '1']
            if match_obj[5] == ')':
                var.length_high_expr = ['('] + var.length_high_expr + [')', '-', '1']

            variables[name] = var

        # is it an array of integers?
        elif (match_obj := re.fullmatch(int_array_pattern, line)) != None:
            name = match_obj[3]

            if name in variables:
                error(f'Variable called {colorize(Color.CODE, name)} has already been declared.')
                exit_failure()
            elif re.fullmatch(name_pattern, name) == None:
                error(f'{colorize(Color.CODE, name)} is not a valid name.')
                exit_failure()
            elif name in reserved_words:
                error(f'{colorize(Color.CODE, name)} is one of the reserved words.')
                exit_failure()

            var = NumberArray()
            var.element = Number()

            var.name = name
            var.id = len(variables)
            var.element.float_digits = 0

            var.is_unique = False
            var.is_increasing = False
            var.is_decreasing = False
            var.is_printed_horizontally = (match_obj[1] == 'row')

            var.size_expr = process_expr(match_obj[2])

            var.element.low_expr, var.element.high_expr = map(process_expr, split_two_expr(match_obj[5]))
            if match_obj[4] == '(':
                var.element.low_expr = ['('] + var.element.low_expr + [')', '+', '1']
            if match_obj[6] == ')':
                var.element.high_expr = ['('] + var.element.high_expr + [')', '-', '1']

            for attr in match_obj[7].split():
                if attr == 'unique':
                    if var.is_unique:
                        warning('{} is set multiple times as an attribute of {}.'.format(
                            colorize(Color.CODE, 'unique'),
                            colorize(Color.CODE, name)
                        ))
                    var.is_unique = True
                elif attr == 'inc':
                    if var.is_increasing:
                        warning('{} is set multiple times as an attribute of {}.'.format(
                            colorize(Color.CODE, 'inc'),
                            colorize(Color.CODE, name)
                        ))
                    if var.is_decreasing:
                        error('{} and {} cannot be set at the same time (check for the attributes of {}).'.format(
                            colorize(Color.CODE, 'inc'),
                            colorize(Color.CODE, 'dec'),
                            colorize(Color.CODE, name)
                        ))
                        exit_failure()
                    var.is_increasing = True
                elif attr == 'dec':
                    if var.is_decreasing:
                        warning('{} is set multiple times as an attribute of {}.'.format(
                            colorize(Color.CODE, 'dec'),
                            colorize(Color.CODE, name)
                        ))
                    if var.is_increasing:
                        error('{} and {} cannot be set at the same time (check for the attributes of {}).'.format(
                            colorize(Color.CODE, 'inc'),
                            colorize(Color.CODE, 'dec'),
                            colorize(Color.CODE, name)
                        ))
                        exit_failure()
                    var.is_decreasing = True
                else:
                    warning('The attribute {} (for {}) is ignored since it is unknown.'.format(
                        colorize(Color.CODE, attr),
                        colorize(Color.CODE, name)
                    ))

            variables[name] = var

        # is it an array of floating point numbers?
        elif (match_obj := re.fullmatch(float_array_pattern, line)) != None:
            name = match_obj[4]

            if name in variables:
                error(f'Variable called {colorize(Color.CODE, name)} has already been declared.')
                exit_failure()
            elif re.fullmatch(name_pattern, name) == None:
                error(f'{colorize(Color.CODE, name)} is not a valid name.')
                exit_failure()
            elif name in reserved_words:
                error(f'{colorize(Color.CODE, name)} is one of the reserved words.')
                exit_failure()

            var = NumberArray()
            var.element = Number()

            var.name = name
            var.id = len(variables)
            var.element.float_digits = int(match_obj[2])

            var.is_unique = False
            var.is_increasing = False
            var.is_decreasing = False
            var.is_printed_horizontally = (match_obj[1] == 'row')

            var.size_expr = process_expr(match_obj[3])

            var.element.low_expr, var.element.high_expr = map(process_expr, split_two_expr(match_obj[6]))
            if match_obj[5] == '(':
                var.element.low_expr = ['('] + var.element.low_expr + [')', '+', '10', '**',
                                                                       '(', '-', f'{var.element.float_digits}', ')', '/', '2']
            if match_obj[7] == ')':
                var.element.high_expr = ['('] + var.element.high_expr + [')', '-', '10', '**',
                                                                         '(', '-', f'{var.element.float_digits}', ')', '/', '2']

            for attr in match_obj[8].split():
                if attr == 'unique':
                    if var.is_unique:
                        warning('{} is set multiple times as an attribute of {}.'.format(
                            colorize(Color.CODE, 'unique'),
                            colorize(Color.CODE, name)
                        ))
                    var.is_unique = True
                elif attr == 'inc':
                    if var.is_increasing:
                        warning('{} is set multiple times as an attribute of {}.'.format(
                            colorize(Color.CODE, 'inc'),
                            colorize(Color.CODE, name)
                        ))
                    if var.is_decreasing:
                        error('{} and {} cannot be set at the same time (check for the attributes of {}).'.format(
                            colorize(Color.CODE, 'inc'),
                            colorize(Color.CODE, 'dec'),
                            colorize(Color.CODE, name)
                        ))
                        exit_failure()
                    var.is_increasing = True
                elif attr == 'dec':
                    if var.is_decreasing:
                        warning('{} is set multiple times as an attribute of {}.'.format(
                            colorize(Color.CODE, 'dec'),
                            colorize(Color.CODE, name)
                        ))
                    if var.is_increasing:
                        error('{} and {} cannot be set at the same time (check for the attributes of {}).'.format(
                            colorize(Color.CODE, 'inc'),
                            colorize(Color.CODE, 'dec'),
                            colorize(Color.CODE, name)
                        ))
                        exit_failure()
                    var.is_decreasing = True
                else:
                    warning('The attribute {} (for {}) is ignored since it is unknown.'.format(
                        colorize(Color.CODE, attr),
                        colorize(Color.CODE, name)
                    ))

            variables[name] = var

        # is it an array of strings?
        elif (match_obj := re.fullmatch(str_array_pattern, line)) != None:
            name = match_obj[4]

            if name in variables:
                error(f'Variable called {colorize(Color.CODE, name)} has already been declared.')
                exit_failure()
            elif re.fullmatch(name_pattern, name) == None:
                error(f'{colorize(Color.CODE, name)} is not a valid name.')
                exit_failure()
            elif name in reserved_words:
                error(f'{colorize(Color.CODE, name)} is one of the reserved words.')
                exit_failure()

            var = StringArray()
            var.element = String()

            var.name = name
            var.id = len(variables)

            var.element.character_set = parse_character_set(name, match_obj[2])
            var.element.is_characterwise_unique = False
            var.is_elementwise_unique = False
            var.is_printed_horizontally = (match_obj[1] == 'row')

            var.size_expr = process_expr(match_obj[3])

            var.element.length_low_expr, var.element.length_high_expr = map(process_expr, split_two_expr(match_obj[6]))
            if match_obj[5] == '(':
                var.element.length_low_expr = ['('] + var.element.length_low_expr + [')', '+', '1']
            if match_obj[7] == ')':
                var.element.length_high_expr = ['('] + var.element.length_high_expr + [')', '-', '1']

            for attr in match_obj[8].split():
                if attr == 'unique':
                    if var.is_elementwise_unique:
                        warning('{} is set multiple times as an attribute of {}.'.format(
                            colorize(Color.CODE, 'unique'),
                            colorize(Color.CODE, name)
                        ))
                    var.is_elementwise_unique = True
                elif attr == 'distinct':
                    if var.element.is_characterwise_unique:
                        warning('{} is set multiple times as an attribute of {}.'.format(
                            colorize(Color.CODE, 'distinct'),
                            colorize(Color.CODE, name)
                        ))
                    var.element.is_characterwise_unique = True
                else:
                    warning('The attribute {} (for {}) is ignored since it is unknown.'.format(
                        colorize(Color.CODE, attr),
                        colorize(Color.CODE, name)
                    ))

            variables[name] = var

        # is it a matrix of integers?
        elif (match_obj := re.fullmatch(int_matrix_pattern, line)) != None:
            name = match_obj[2]

            if name in variables:
                error(f'Variable called {colorize(Color.CODE, name)} has already been declared.')
                exit_failure()
            elif re.fullmatch(name_pattern, name) == None:
                error(f'{colorize(Color.CODE, name)} is not a valid name.')
                exit_failure()
            elif name in reserved_words:
                error(f'{colorize(Color.CODE, name)} is one of the reserved words.')
                exit_failure()

            if not match_obj[6] in ('', 'unique'):
                warning('The attribute {} (for {}) is ignored since it is unknown.'.format(
                    colorize(Color.CODE, match_obj[6]),
                    colorize(Color.CODE, name)
                ))

            var = NumberMatrix()
            var.element = Number()

            var.name = name
            var.id = len(variables)
            var.element.float_digits = 0

            var.is_unique = (match_obj[6] == 'unique')
            var.size_r_expr, var.size_c_expr = map(process_expr, split_two_expr(match_obj[1]))

            var.element.low_expr, var.element.high_expr = map(process_expr, split_two_expr(match_obj[4]))
            if match_obj[3] == '(':
                var.element.low_expr = ['('] + var.element.low_expr + [')', '+', '1']
            if match_obj[5] == ')':
                var.element.high_expr = ['('] + var.element.high_expr + [')', '-', '1']

            variables[name] = var

        # is it a matrix of floating point numbers?
        elif (match_obj := re.fullmatch(float_matrix_pattern, line)) != None:
            name = match_obj[3]

            if name in variables:
                error(f'Variable called {colorize(Color.CODE, name)} has already been declared.')
                exit_failure()
            elif re.fullmatch(name_pattern, name) == None:
                error(f'{colorize(Color.CODE, name)} is not a valid name.')
                exit_failure()
            elif name in reserved_words:
                error(f'{colorize(Color.CODE, name)} is one of the reserved words.')
                exit_failure()

            if not match_obj[7] in ('', 'unique'):
                warning('The attribute {} (for {}) is ignored since it is unknown.'.format(
                    colorize(Color.CODE, match_obj[7]),
                    colorize(Color.CODE, name)
                ))

            var = NumberMatrix()
            var.element = Number()

            var.name = name
            var.id = len(variables)
            var.element.float_digits = int(match_obj[1])

            var.is_unique = (match_obj[7] == 'unique')
            var.size_r_expr, var.size_c_expr = map(process_expr, split_two_expr(match_obj[2]))

            var.element.low_expr, var.element.high_expr = map(process_expr, split_two_expr(match_obj[5]))
            if match_obj[4] == '(':
                var.element.low_expr = ['('] + var.element.low_expr + [')', '+', '1']
            if match_obj[6] == ')':
                var.element.high_expr = ['('] + var.element.high_expr + [')', '-', '1']

            variables[name] = var

        # is it a tree?
        elif (match_obj := re.fullmatch(tree_pattern, line)) != None:
            name = match_obj[2]

            if name in variables:
                error(f'Variable called {colorize(Color.CODE, name)} has already been declared.')
                exit_failure()
            elif re.fullmatch(name_pattern, name) == None:
                error(f'{colorize(Color.CODE, name)} is not a valid name.')
                exit_failure()
            elif name in reserved_words:
                error(f'{colorize(Color.CODE, name)} is one of the reserved words.')
                exit_failure()

            var = Graph()
            var.name = name
            var.id = len(variables)
            var.number_of_vertices_expr = process_expr(match_obj[1])

            var.is_printed_horizontally = True
            var.is_tree = True
            var.is_directed = False
            var.is_connected = True
            var.is_acyclic = True
            var.no_multiple_edge = True
            var.no_self_loop = True
            var.n_indexed = 1

            for attr in match_obj[3].split():
                if attr == 'directed':
                    if var.is_directed:
                        warning('{} is set multiple times as an attribute of {}.'.format(
                            colorize(Color.CODE, 'directed'),
                            colorize(Color.CODE, name)
                        ))
                    var.is_directed = True
                elif attr.endswith('_indexed') and (attr[0] != '_'):
                    if var.n_indexed != 1:
                        warning(f'The index attributes of {colorize(Color.CODE, name)} is set multiple times.')
                    try:
                        var.n_indexed = int(attr[: attr.index('_')])
                    except:
                        error('{} (in the attribute of {}) does not seem to be an integer.'.format(
                            colorize(Color.CODE, attr[: attr.index('_')]),
                            colorize(Color.CODE, name)
                        ))
                        exit_failure()
                else:
                    warning('The attribute {} (for {}) is ignored since it is unknown.'.format(
                        colorize(Color.CODE, attr),
                        colorize(Color.CODE, name)
                    ))

            variables[name] = var
            continue

        # is it a graph?
        elif (match_obj := re.fullmatch(graph_pattern, line)) != None:
            name = match_obj[2]

            if name in variables:
                error(f'Variable called {colorize(Color.CODE, name)} has already been declared.')
                exit_failure()
            elif re.fullmatch(name_pattern, name) == None:
                error(f'{colorize(Color.CODE, name)} is not a valid name.')
                exit_failure()
            elif name in reserved_words:
                error(f'{colorize(Color.CODE, name)} is one of the reserved words.')
                exit_failure()

            var = Graph()
            var.name = name
            var.id = len(variables)
            var.number_of_vertices_expr, var.number_of_edges_expr = map(process_expr, split_two_expr(match_obj[1]))

            var.is_printed_horizontally = True
            var.is_tree = False
            var.is_directed = False
            var.is_connected = False
            var.is_acyclic = False
            var.no_multiple_edge = False
            var.no_self_loop = False
            var.n_indexed = 1

            for attr in match_obj[3].split():
                if attr == 'simple':
                    var.no_multiple_edge = True
                    var.no_self_loop = True
                elif attr == 'connected':
                    if var.is_connected:
                        warning('{} is set multiple times as an attribute of {}.'.format(
                            colorize(Color.CODE, 'connected'),
                            colorize(Color.CODE, name)
                        ))
                    var.is_connected = True
                elif attr == 'directed':
                    if var.is_directed:
                        warning('{} is set multiple times as an attribute of {}.'.format(
                            colorize(Color.CODE, 'directed'),
                            colorize(Color.CODE, name)
                        ))
                    var.is_directed = True
                elif attr == 'acyclic':
                    if var.is_acyclic:
                        warning('{} is set multiple times as an attribute of {}.'.format(
                            colorize(Color.CODE, 'acyclic'),
                            colorize(Color.CODE, name)
                        ))
                    var.is_acyclic = True
                elif attr == 'no_self_loop':
                    if var.no_self_loop:
                        warning('{} is set multiple times as an attribute of {}.'.format(
                            colorize(Color.CODE, 'no_self_loop'),
                            colorize(Color.CODE, name)
                        ))
                    var.no_self_loop = True
                elif attr == 'no_multiple_edge':
                    if var.no_multiple_edge:
                        warning('{} is set multiple times as an attribute of {}.'.format(
                            colorize(Color.CODE, 'no_multiple_edge'),
                            colorize(Color.CODE, name)
                        ))
                    var.no_multiple_edge = True
                elif attr.endswith('_indexed') and (attr[0] != '_'):
                    if var.n_indexed != 1:
                        warning(f'The index attributes of {colorize(Color.CODE, name)} is set multiple times.')
                    try:
                        var.n_indexed = int(attr[: attr.index('_')])
                    except:
                        error('{} (in the attribute of {}) does not seem to be an integer.'.format(
                            colorize(Color.CODE, attr[: attr.index('_')]),
                            colorize(Color.CODE, name)
                        ))
                        exit_failure()
                else:
                    warning('The attribute {} (for {}) is ignored since it is unknown.'.format(
                        colorize(Color.CODE, attr),
                        colorize(Color.CODE, name)
                    ))

            variables[name] = var

        # fallback
        else:
            error(f'Failed to interpret {colorize(Color.CODE, line)}.')
            exit_failure()

        if (source == sys.stdin) and (sys.stdin.isatty()):
            prompt()

    override_statement = ''

    if has_override_statement:
        inside_single_quote = False
        inside_double_quote = False

        if (source == sys.stdin) and (sys.stdin.isatty()):
            prompt()

        for line in source:
            for i in range(len(line)):
                if (line[i] != ' ') and (line[i] != '\t'):
                    break
                override_statement += line[i]

            line = re.sub(comment_pattern, '', line.strip())

            if line == '---':
                break

            for token in re.finditer(token_pattern, line):
                t = token[0].strip()

                if t == '\'':
                    inside_single_quote ^= True
                elif t == '\"':
                    inside_double_quote ^= True

                if inside_single_quote or inside_double_quote:
                    override_statement += t
                elif t in variables:
                    if isinstance(variables[t], (Number, String)):
                        override_statement += f'generated_values[{variables[t].id}][0] '
                    else:
                        override_statement += f'generated_values[{variables[t].id}] '
                elif (t == '.') or t.isnumeric():
                    override_statement += t
                else:
                    override_statement += t + ' '

            override_statement += '\n'

            if (source == sys.stdin) and (sys.stdin.isatty()):
                prompt()

    return variables, override_statement
