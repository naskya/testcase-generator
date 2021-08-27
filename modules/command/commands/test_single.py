from __future__ import annotations

import concurrent.futures
import shutil
import sys

from modules.case.saver import save_case_and_verdict_single
from modules.command.commands.impl.definition import Result
from modules.command.commands.impl.generate_one_case import generate_one_case
from modules.command.commands.impl.test_one_case import test_one_case
from modules.command.definition import Command
from modules.utility.colorizer import Color, colorize
from modules.utility.printer import progress, progress_bar
from modules.variable.definition import VariableType


def generate_and_test_one_case(program: str, time_limit: int, variables: dict[str, VariableType],
                               override_statements: str, format: list[list[str]]) -> tuple[str, Result]:
    test_case = generate_one_case(variables, override_statements, format)
    return test_case, test_one_case(program, test_case, time_limit)


def test_single_with_progress_bar(command: Command, variables: dict[str, VariableType],
                                  override_statements: str, format: list[list[str]]) -> None:
    pad_length = len(str(command.cases)) + 1

    progress('Start running tests.')
    print('-' * shutil.get_terminal_size().columns + '\n')

    print(f'Testing case #{"1".rjust(pad_length, " ")}')
    progress_bar(0, command.cases, 50)
    print()
    print()

    with concurrent.futures.ProcessPoolExecutor() as executor:
        test_number = 0
        detected_number = 0
        futures = [executor.submit(generate_and_test_one_case, command.program_1, command.time_limit,
                                   variables, override_statements, format) for _ in range(command.cases)]

        for future in concurrent.futures.as_completed(futures):
            test_number += 1

            test_case, test_result = future.result()

            if hasattr(test_result, 'exit_code') and (test_result.exit_code != 0):
                test_result.verdict = 'RE'
            elif test_result.time > command.time_limit:
                test_result.verdict = 'TLE'

            if test_result.verdict != '':
                detected_number += 1
                case_name, verdict_name = save_case_and_verdict_single(test_case, detected_number,
                                                                       command.cases, command.prefix,
                                                                       command.suffix, command.time_limit,
                                                                       command.program_1, test_result)

                print('Test #{}: {} --> saved as {} and {}'.format(
                    str(test_number).rjust(pad_length, ' '),
                    colorize(Color[test_result.verdict], test_result.verdict.ljust(3, ' ')),
                    colorize(Color.CODE, case_name),
                    colorize(Color.CODE, verdict_name)
                ))
            elif not hasattr(test_result, 'stdout'):
                detected_number += 1
                case_name, verdict_name = save_case_and_verdict_single(test_case, detected_number,
                                                                       command.cases, command.prefix,
                                                                       command.suffix, command.time_limit,
                                                                       command.program_1, test_result)
                print('Test #{}: Failed to capture the output --> saved as {} and {} (maybe not your fault! just in case.)'.format(
                    str(test_number).rjust(pad_length, ' '),
                    colorize(Color.CODE, case_name),
                    colorize(Color.CODE, verdict_name)
                ))

            for _ in range(detected_number + 3):
                print('\033[A', end='')

            if test_number == command.cases:
                print(f'Testing cases: Done!\033[K')
                progress_bar(test_number, command.cases, 50)

                for _ in range(2 if (detected_number == 0) else detected_number + 3):
                    print()
            else:
                print(f'Testing case #{str(test_number + 1).rjust(pad_length, " ")}')
                progress_bar(test_number, command.cases, 50)

                for _ in range(detected_number + 2):
                    print()

    print('-' * shutil.get_terminal_size().columns)
    progress('{} (out of {}) tests run successfully.'.format(
        colorize(Color.CODE, test_number),
        colorize(Color.CODE, command.cases)
    ))


def test_single_without_progress_bar(command: Command, variables: dict[str, VariableType],
                                     override_statements: str, format: list[list[str]]) -> None:
    pad_length = len(str(command.cases)) + 1
    progress('Start running tests.\n')

    with concurrent.futures.ProcessPoolExecutor() as executor:
        test_number = 0
        detected_number = 0
        futures = [executor.submit(generate_and_test_one_case, command.program_1, command.time_limit,
                                   variables, override_statements, format) for _ in range(command.cases)]

        for future in concurrent.futures.as_completed(futures):
            test_number += 1

            test_case, test_result = future.result()

            if hasattr(test_result, 'exit_code') and (test_result.exit_code != 0):
                test_result.verdict = 'RE'
            elif test_result.time > command.time_limit:
                test_result.verdict = 'TLE'

            if test_result.verdict != '':
                detected_number += 1
                case_name, verdict_name = save_case_and_verdict_single(test_case, detected_number,
                                                                       command.cases, command.prefix,
                                                                       command.suffix, command.time_limit,
                                                                       command.program_1, test_result)

                print('Test #{}: {} --> saved as {} and {}'.format(
                    str(test_number).rjust(pad_length, ' '),
                    colorize(Color[test_result.verdict], test_result.verdict.ljust(3, ' ')),
                    colorize(Color.CODE, case_name),
                    colorize(Color.CODE, verdict_name)
                ))
            elif not hasattr(test_result, 'stdout'):
                detected_number += 1
                case_name, verdict_name = save_case_and_verdict_single(test_case, detected_number,
                                                                       command.cases, command.prefix,
                                                                       command.suffix, command.time_limit,
                                                                       command.program_1, test_result)
                print('Test #{}: Failed to capture the output --> saved as {} and {} (maybe not your fault! just in case.)'.format(
                    str(test_number).rjust(pad_length, ' '),
                    colorize(Color.CODE, case_name),
                    colorize(Color.CODE, verdict_name)
                ))

        if detected_number > 0:
            print()

    progress('{} (out of {}) tests run successfully.'.format(
        colorize(Color.CODE, test_number),
        colorize(Color.CODE, command.cases)
    ))
