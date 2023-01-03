#!/usr/bin/env python3

import sys

import colorama

from modules.case.saver import case_file_name
from modules.command.commands.gen import gen_with_progress_bar, gen_without_progress_bar
from modules.command.commands.test_double import test_double_with_progress_bar, test_double_without_progress_bar
from modules.command.commands.test_single import test_single_with_progress_bar, test_single_without_progress_bar
from modules.command.parser import parse_command_line_argument
from modules.format.parser import parse_format
from modules.utility.colorizer import code
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

    args = parse_command_line_argument()

    if args.verify:
        info('You are in the verification mode.')

    # parse variables & output format
    using_tty = False

    if args.input == '':
        info('The input will be read from standard input.')
        if sys.stdin.isatty():
            using_tty = True
            hint(f'In terminal, enter EOF manually (typically {code("Ctrl + D")}) '
                 'when the input is finished.')
        hint('Use {} or {} argument to use file input.'.format(
            code('--input'),
            code('-i')
        ))

    if (args.prefix == '') and (args.suffix == ''):
        if args.cases == 1:
            info(f'The output will be named {code(case_file_name(1, 1, "", ""))}.')
        else:
            info('The output will be named {}, {}, ....'.format(
                code(case_file_name(1, args.cases, '', '')),
                code(case_file_name(2, args.cases, '', '')),
            ))
        hint('Specify prefix ({} or {}) and/or suffix ({} or {}) if this is not what you want.'.format(
            code('--prefix'),
            code('-p'),
            code('--suffix'),
            code('-s')
        ))

    source = sys.stdin if args.input == '' else open(args.input, encoding='utf-8')

    progress('Start parsing variables and output format.')
    variables, override_statements, variable_inputs = parse_variable(using_tty, source, args.verify)
    format, format_inputs = parse_format(using_tty, source, variables)

    if using_tty:
        print(flush=True)
        if input('Do you want to save your input as a text file? [y/N] ').lower() in ['y', 'yes']:
            with open(input('Enter file name: '), 'w') as f:
                f.write(''.join(variable_inputs))
                f.write(''.join(format_inputs))

    progress('Variables and output format have been parsed successfully.')

    # execute command
    if args.subcommand == 'gen':
        if args.no_progress_bar:
            gen_without_progress_bar(args.cases, args.prefix, args.suffix,
                                     args.verify, variables, override_statements, format)
        else:
            gen_with_progress_bar(args.cases, args.prefix, args.suffix,
                                  args.verify, variables, override_statements, format)
    elif args.subcommand == 'test' and len(args.programs) == 1:
        if args.no_progress_bar:
            test_single_without_progress_bar(args.cases, args.programs[0], args.time_limit,
                                             args.prefix, args.suffix, args.verify,
                                             variables, override_statements, format)
        else:
            test_single_with_progress_bar(args.cases, args.programs[0], args.time_limit,
                                          args.prefix, args.suffix, args.verify,
                                          variables, override_statements, format)
    elif args.subcommand == 'test' and len(args.programs) == 2:
        if args.no_progress_bar:
            test_double_without_progress_bar(args.cases, args.programs[0], args.programs[1], args.time_limit,
                                             args.prefix, args.suffix, args.verify,
                                             variables, override_statements, format)
        else:
            test_double_with_progress_bar(args.cases, args.programs[0], args.programs[1], args.time_limit,
                                          args.prefix, args.suffix, args.verify,
                                          variables, override_statements, format)
    else:
        error(f'Too many (= {len(args.programs)}) programs are provided.')
        exit_failure()

    colorama.deinit()


if __name__ == '__main__':
    main()
