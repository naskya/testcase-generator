#!/usr/bin/env python3

import sys

import colorama

from modules.case.saver import case_file_name
from modules.command.commands.gen import gen_with_progress_bar, gen_without_progress_bar
from modules.command.commands.test_double import test_double_with_progress_bar, test_double_without_progress_bar
from modules.command.commands.test_single import test_single_with_progress_bar, test_single_without_progress_bar
from modules.command.definition import Feature
from modules.command.parser import parse_command
from modules.format.parser import parse_format
from modules.utility.colorizer import Color, colorize
from modules.utility.exit_failure import exit_failure
from modules.utility.printer import error, hint, info, progress
from modules.variable.parser import parse_variable


def main() -> None:
    colorama.init()

    # check version
    if (sys.version_info[0] < 3) or ((sys.version_info[0] == 3) and sys.version_info[1] < 9):
        error('This program requires Python 3.9.0 (or higher) but you are using Python {}.{}.{}.'.format(
            sys.version_info[0],
            sys.version_info[1],
            sys.version_info[2]
        ))
        exit_failure()

    # parse command
    progress('Start parsing the command.')
    command = parse_command(sys.argv)
    progress('The command has been parsed successfully.')

    if command.is_verification:
        info('Verification mode is enabled.')

    # parse variables & output format
    if command.source == sys.stdin:
        info('The input will be read from standard input.')
        if sys.stdin.isatty():
            hint(f'In terminal, enter EOF manually (typically {colorize(Color.CODE, "Ctrl + D")}) '
                 'when the input is finished.')
        hint('Use {} or {} argument to use file input.'.format(
            colorize(Color.CODE, '--input'),
            colorize(Color.CODE, '-i')
        ))

    if (command.prefix == '') and (command.suffix == ''):
        if command.cases == 1:
            info(f'The output will be named {colorize(Color.CODE, case_file_name(1, 1, "", ""))}.')
        else:
            info('The output will be named {}, {}, ....'.format(
                colorize(Color.CODE, case_file_name(1, command.cases, '', '')),
                colorize(Color.CODE, case_file_name(2, command.cases, '', '')),
            ))
        hint('Specify prefix ({} or {}) and/or suffix ({} or {}) if this is not what you want.'.format(
            colorize(Color.CODE, '--prefix'),
            colorize(Color.CODE, '-p'),
            colorize(Color.CODE, '--suffix'),
            colorize(Color.CODE, '-s')
        ))

    progress('Start parsing the variables and output format.')
    variables, override_statements = parse_variable(command.source, command.is_verification)
    format = parse_format(command.source, variables)

    if (command.source == sys.stdin) and (sys.stdin.isatty()):
        print(flush=True)
    progress('The variables and output format have been parsed successfully.')

    # execute command
    if command.feature == Feature.GENERATE:
        if command.show_progress:
            gen_with_progress_bar(command, variables, override_statements, format)
        else:
            gen_without_progress_bar(command, variables, override_statements, format)
    elif command.feature == Feature.TEST_SINGLE:
        if command.show_progress:
            test_single_with_progress_bar(command, variables, override_statements, format)
        else:
            test_single_without_progress_bar(command, variables, override_statements, format)
    elif command.feature == Feature.TEST_DOUBLE:
        if command.show_progress:
            test_double_with_progress_bar(command, variables, override_statements, format)
        else:
            test_double_without_progress_bar(command, variables, override_statements, format)
    else:
        exit_failure()

    colorama.deinit()


if __name__ == '__main__':
    main()
