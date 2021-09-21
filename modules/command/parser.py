from __future__ import annotations

import sys

from modules.command.definition import (
    Command,
    Feature,
    default_cases_for_gen,
    default_cases_for_test,
    default_prefix,
    default_show_progress,
    default_suffix,
    default_time_limit,
    default_is_verification
)
from modules.utility.colorizer import Color, colorize
from modules.utility.exit_failure import exit_failure
from modules.utility.printer import error, usage, warning


def parse_command(args: list[str]) -> Command:
    result = Command()
    skip = 0

    if len(args) < 2:
        error('The command line arguments are not sufficient.')
        usage()
        exit_failure()

    if args[1] == 'gen':
        result.feature = Feature.GENERATE
        skip = 2
    elif args[1] == 'test':
        if len(args) == 2:
            error('You need to provide program(s) to test.')
            usage()
            exit_failure()
        elif (len(args) == 3) or args[3] in ('-i', '--input', '-p', '--prefix', '-s', '--suffix', '-c', '--cases',
                                             '-t', '--time-limit', '-n', '--no-progress-bar', '--unit-test'):
            result.feature = Feature.TEST_SINGLE
            result.program_1 = args[2]
            skip = 3
        else:
            result.feature = Feature.TEST_DOUBLE
            result.program_1 = args[2]
            result.program_2 = args[3]
            skip = 4
    else:
        error('Only {} or {} is accepted as the first command line argument.'.format(
            colorize(Color.CODE, 'gen'),
            colorize(Color.CODE, 'test')
        ))
        usage()
        exit_failure()

    for i in range(len(args)):
        if skip > 0:
            skip -= 1
            continue

        if args[i] in ('-i', '--input'):
            if hasattr(result, 'source'):
                error('More than one input files ({} or {}) are provided.'.format(
                    colorize(Color.CODE, '-i'),
                    colorize(Color.CODE, '--input')
                ))
                usage()
                exit_failure()
            elif i == len(args) - 1:
                error('The input file is missing.')
                usage()
                exit_failure()
            else:
                try:
                    result.source = open(args[i + 1], encoding='utf-8')
                except:
                    error(f'Failed to open {colorize(Color.CODE, args[i + 1])}.')
                    exit_failure()

            skip = 1

        elif args[i] in ('-p', '--prefix'):
            if hasattr(result, 'prefix'):
                error('More than one prefixes ({} or {}) are provided.'.format(
                    colorize(Color.CODE, '-p'),
                    colorize(Color.CODE, '--prefix')
                ))
                usage()
                exit_failure()
            elif i == len(args) - 1:
                error('The prefix is missing.')
                usage()
                exit_failure()
            else:
                result.prefix = args[i + 1]

            skip = 1

        elif args[i] in ('-s', '--suffix'):
            if hasattr(result, 'suffix'):
                error('More than one suffixes ({} or {}) are provided.'.format(
                    colorize(Color.CODE, '-s'),
                    colorize(Color.CODE, '--suffix')
                ))
                usage()
                exit_failure()
            elif i == len(args) - 1:
                error('The suffix is missing.')
                usage()
                exit_failure()
            else:
                result.suffix = args[i + 1]

            skip = 1

        elif args[i] in ('-c', '--cases'):
            if hasattr(result, 'cases'):
                error('More than one numbers of test cases ({} or {}) are provided.'.format(
                    colorize(Color.CODE, '-c'),
                    colorize(Color.CODE, '--cases')
                ))
                usage()
                exit_failure()
            elif i == len(args) - 1:
                error('The number of test cases is missing.')
                usage()
                exit_failure()
            else:
                try:
                    result.cases = int(args[i + 1])
                except:
                    error(f'The number of test cases (= {colorize(Color.CODE, args[i + 1])})'
                          ' does not seem to be an integer.')
                    usage()
                    exit_failure()

            skip = 1

        elif args[i] in ('-t', '--time-limit'):
            if hasattr(result, 'time_limit'):
                error('More than one time limits ({} or {}) are provided.'.format(
                    colorize(Color.CODE, '-t'),
                    colorize(Color.CODE, '--time-limit')
                ))
                usage()
                exit_failure()
            elif i == len(args) - 1:
                error('The time limit is missing.')
                usage()
                exit_failure()
            else:
                try:
                    result.time_limit = float(args[i + 1])
                except:
                    error(f'The time limit (= {colorize(Color.CODE, args[i + 1])}) does not seem to be a number.')
                    usage()
                    exit_failure()

            if result.feature == Feature.GENERATE:
                warning('The argument {} is ignored since it is unnecessary for {} command.'.format(
                    colorize(Color.CODE, f'{args[i]} {args[i + 1]}'),
                    colorize(Color.CODE, 'gen')
                ))

            skip = 1

        elif args[i] in ('-n', '--no-progress-bar'):
            if hasattr(result, 'show_progress'):
                warning('{} or {} are provided more than once.'.format(
                    colorize(Color.CODE, '-n'),
                    colorize(Color.CODE, '--no-progress-bar')
                ))
            result.show_progress = False

        elif args[i] == '--verify':
            if hasattr(result, 'is_verification'):
                warning(f'{colorize(Color.CODE, "--verify")} is provided more than once.')

            result.is_verification = True

        else:
            error(f'The argument {colorize(Color.CODE, args[i])} is unknown.')
            usage()
            exit_failure()

    # default settings
    if not hasattr(result, 'source'):
        result.source = sys.stdin
    if not hasattr(result, 'prefix'):
        result.prefix = default_prefix
    if not hasattr(result, 'suffix'):
        result.suffix = default_suffix
    if not hasattr(result, 'cases'):
        result.cases = (default_cases_for_gen if (result.feature == Feature.GENERATE) else default_cases_for_test)
    if not hasattr(result, 'time_limit'):
        result.time_limit = default_time_limit
    if not hasattr(result, 'show_progress'):
        result.show_progress = default_show_progress
    if not hasattr(result, 'is_verification'):
        result.is_verification = default_is_verification

    return result
