from __future__ import annotations

import concurrent.futures
import shutil

from modules.case.saver import save_case_and_verdict_double
from modules.command.commands.impl.definition import Result
from modules.command.commands.impl.generate_one_case import generate_one_case
from modules.command.commands.impl.test_one_case import test_one_case
from modules.command.definition import Command
from modules.utility.colorizer import Color, colorize
from modules.utility.exit_failure import exit_failure
from modules.utility.printer import info, progress, progress_bar
from modules.variable.definition import VariableType


def generate_and_test_one_case(program_1: str, program_2: str, time_limit: int, variables: dict[str, VariableType],
                               override_statements: str, format: list[list[str]]) -> tuple[bool, str, Result, Result]:
    success, test_case = generate_one_case(variables, override_statements, format)

    if not success:
        return False, '', Result(), Result()

    return True, test_case, test_one_case(program_1, test_case, time_limit), test_one_case(program_2, test_case, time_limit)


def test_double_with_progress_bar(command: Command, variables: dict[str, VariableType],
                                  override_statements: str, format: list[list[str]]) -> None:
    pad_length = len(str(command.cases)) + 1

    progress('Start running tests.')
    print('-' * shutil.get_terminal_size().columns + '\n')

    print(f'Test #{"1".rjust(pad_length, " ")}')
    progress_bar(0, command.cases, 50)
    print()
    print()

    with concurrent.futures.ProcessPoolExecutor() as executor:
        try_number = 0
        test_number = 0
        detected_number = 0
        futures = [executor.submit(generate_and_test_one_case, command.program_1, command.program_2,
                                   command.time_limit, variables, override_statements, format)
                   for _ in range(command.cases)]

        for future in concurrent.futures.as_completed(futures):
            try_number += 1
            success, test_case, test_result_1, test_result_2 = future.result()

            if success:
                test_number += 1

                if hasattr(test_result_1, 'exit_code') and (test_result_1.exit_code != 0):
                    test_result_1.verdict = 'RE'
                elif test_result_1.time > command.time_limit:
                    test_result_1.verdict = 'TLE'

                if hasattr(test_result_2, 'exit_code') and (test_result_2.exit_code != 0):
                    test_result_2.verdict = 'RE'
                elif test_result_2.time > command.time_limit:
                    test_result_2.verdict = 'TLE'

                if (test_result_1.verdict != '') or (test_result_2.verdict != ''):
                    detected_number += 1
                    case_name, verdict_name = save_case_and_verdict_double(test_case, detected_number,
                                                                        command.cases, command.prefix,
                                                                        command.suffix, command.time_limit,
                                                                        command.program_1, test_result_1,
                                                                        command.program_2, test_result_2)

                    if (test_result_1.verdict != '') and (test_result_2.verdict != ''):
                        if test_result_1.verdict == test_result_2.verdict:
                            print('Test #{}: {} on both programs --> saved as {} and {}'.format(
                                str(test_number).rjust(pad_length, ' '),
                                colorize(Color[f'{test_result_1.verdict}'], test_result_1.verdict),
                                colorize(Color.CODE, case_name),
                                colorize(Color.CODE, verdict_name)
                            ))
                        else:
                            print('Test #{}: {} on program 1, {} on program 2 --> saved as {} and {}'.format(
                                str(test_number).rjust(pad_length, ' '),
                                colorize(Color[f'{test_result_1.verdict}'], test_result_1.verdict),
                                colorize(Color[f'{test_result_2.verdict}'], test_result_2.verdict),
                                colorize(Color.CODE, case_name),
                                colorize(Color.CODE, verdict_name)
                            ))

                    elif test_result_1.verdict != '':
                        print('Test #{}: {} on program 1 --> saved as {} and {}'.format(
                            str(test_number).rjust(pad_length, ' '),
                            colorize(Color[f'{test_result_1.verdict}'], test_result_1.verdict),
                            colorize(Color.CODE, case_name),
                            colorize(Color.CODE, verdict_name)
                        ))
                    elif test_result_2.verdict != '':
                        print('Test #{}: {} on program 2 --> saved as {} and {}'.format(
                            str(test_number).rjust(pad_length, ' '),
                            colorize(Color[f'{test_result_2.verdict}'], test_result_2.verdict),
                            colorize(Color.CODE, case_name),
                            colorize(Color.CODE, verdict_name)
                        ))
                elif hasattr(test_result_1, 'stdout') and hasattr(test_result_2, 'stdout') and test_result_1.stdout != test_result_2.stdout:
                    detected_number += 1
                    case_name, verdict_name = save_case_and_verdict_double(test_case, detected_number,
                                                                        command.cases, command.prefix,
                                                                        command.suffix, command.time_limit,
                                                                        command.program_1, test_result_1,
                                                                        command.program_2, test_result_2)
                    print('Test #{}: {} --> saved as {} and {}'.format(
                        str(test_number).rjust(pad_length, ' '),
                        colorize(Color.WA, 'WA'),
                        colorize(Color.CODE, case_name),
                        colorize(Color.CODE, verdict_name)
                    ))
                elif (not hasattr(test_result_1, 'stdout')) or (not hasattr(test_result_2, 'stdout')):
                    detected_number += 1
                    case_name, verdict_name = save_case_and_verdict_double(test_case, detected_number,
                                                                        command.cases, command.prefix,
                                                                        command.suffix, command.time_limit,
                                                                        command.program_1, test_result_1,
                                                                        command.program_2, test_result_2)
                    print('Test #{}: Failed to capture the output --> saved as {} and {} (maybe not your fault! just in case.)'.format(
                        str(test_number).rjust(pad_length, ' '),
                        colorize(Color.CODE, case_name),
                        colorize(Color.CODE, verdict_name)
                    ))

            for _ in range(detected_number + 3):
                print('\033[A', end='')

            if try_number == command.cases:
                print(f'Test: Done!\033[K')
                progress_bar(try_number, command.cases, 50)

                for _ in range(2 if (detected_number == 0) else detected_number + 3):
                    print()
            else:
                print(f'Test #{str(try_number + 1).rjust(pad_length, " ")}')
                progress_bar(try_number, command.cases, 50)

                for _ in range(detected_number + 2):
                    print()

    print('-' * shutil.get_terminal_size().columns)
    if test_number != command.cases:
        info(f'Failed to generate {command.cases - test_number} cases.')

    progress('{} (out of {}) tests run successfully.'.format(
        colorize(Color.CODE, test_number),
        colorize(Color.CODE, command.cases)
    ))

    if command.is_unit_test and test_number < command.cases // 2:
        exit_failure()


def test_double_without_progress_bar(command: Command, variables: dict[str, VariableType],
                                     override_statements: str, format: list[list[str]]) -> None:
    pad_length = len(str(command.cases)) + 1

    progress('Start running tests.\n')

    with concurrent.futures.ProcessPoolExecutor() as executor:
        test_number = 0
        detected_number = 0
        futures = [executor.submit(generate_and_test_one_case, command.program_1, command.program_2,
                                   command.time_limit, variables, override_statements, format)
                   for _ in range(command.cases)]

        for future in concurrent.futures.as_completed(futures):
            success, test_case, test_result_1, test_result_2 = future.result()

            if not success:
                continue

            test_number += 1

            if hasattr(test_result_1, 'exit_code') and (test_result_1.exit_code != 0):
                test_result_1.verdict = 'RE'
            elif test_result_1.time > command.time_limit:
                test_result_1.verdict = 'TLE'

            if hasattr(test_result_2, 'exit_code') and (test_result_2.exit_code != 0):
                test_result_2.verdict = 'RE'
            elif test_result_2.time > command.time_limit:
                test_result_2.verdict = 'TLE'

            if (test_result_1.verdict != '') or (test_result_2.verdict != ''):
                detected_number += 1
                case_name, verdict_name = save_case_and_verdict_double(test_case, detected_number,
                                                                       command.cases, command.prefix,
                                                                       command.suffix, command.time_limit,
                                                                       command.program_1, test_result_1,
                                                                       command.program_2, test_result_2)

                if (test_result_1.verdict != '') and (test_result_2.verdict != ''):
                    if test_result_1.verdict == test_result_2.verdict:
                        print('Test #{}: {} on both programs --> saved as {} and {}'.format(
                            str(test_number).rjust(pad_length, ' '),
                            colorize(Color[f'{test_result_1.verdict}'], test_result_1.verdict),
                            colorize(Color.CODE, case_name),
                            colorize(Color.CODE, verdict_name)
                        ))
                    else:
                        print('Test #{}: {} on program 1, {} on program 2 --> saved as {} and {}'.format(
                            str(test_number).rjust(pad_length, ' '),
                            colorize(Color[f'{test_result_1.verdict}'], test_result_1.verdict),
                            colorize(Color[f'{test_result_2.verdict}'], test_result_2.verdict),
                            colorize(Color.CODE, case_name),
                            colorize(Color.CODE, verdict_name)
                        ))

                elif test_result_1.verdict != '':
                    print('Test #{}: {} on program 1 --> saved as {} and {}'.format(
                        str(test_number).rjust(pad_length, ' '),
                        colorize(Color[f'{test_result_1.verdict}'], test_result_1.verdict),
                        colorize(Color.CODE, case_name),
                        colorize(Color.CODE, verdict_name)
                    ))
                elif test_result_2.verdict != '':
                    print('Test #{}: {} on program 2 --> saved as {} and {}'.format(
                        str(test_number).rjust(pad_length, ' '),
                        colorize(Color[f'{test_result_2.verdict}'], test_result_2.verdict),
                        colorize(Color.CODE, case_name),
                        colorize(Color.CODE, verdict_name)
                    ))
            elif hasattr(test_result_1, 'stdout') and hasattr(test_result_2, 'stdout') and test_result_1.stdout != test_result_2.stdout:
                detected_number += 1
                case_name, verdict_name = save_case_and_verdict_double(test_case, detected_number,
                                                                       command.cases, command.prefix,
                                                                       command.suffix, command.time_limit,
                                                                       command.program_1, test_result_1,
                                                                       command.program_2, test_result_2)
                print('Test #{}: {} --> saved as {} and {}'.format(
                    str(test_number).rjust(pad_length, ' '),
                    colorize(Color.WA, 'WA'),
                    colorize(Color.CODE, case_name),
                    colorize(Color.CODE, verdict_name)
                ))
            elif (not hasattr(test_result_1, 'stdout')) or (not hasattr(test_result_2, 'stdout')):
                detected_number += 1
                case_name, verdict_name = save_case_and_verdict_double(test_case, detected_number,
                                                                       command.cases, command.prefix,
                                                                       command.suffix, command.time_limit,
                                                                       command.program_1, test_result_1,
                                                                       command.program_2, test_result_2)
                print('Test #{}: Failed to capture the output --> saved as {} and {} (maybe not your fault! just in case.)'.format(
                    str(test_number).rjust(pad_length, ' '),
                    colorize(Color.CODE, case_name),
                    colorize(Color.CODE, verdict_name)
                ))

        if detected_number > 0:
            print()

    if test_number != command.cases:
        info(f'Failed to generate {command.cases - test_number} cases.')

    progress('{} (out of {}) tests run successfully.'.format(
        colorize(Color.CODE, test_number),
        colorize(Color.CODE, command.cases)
    ))

    if command.is_unit_test and test_number < command.cases // 2:
        exit_failure()
