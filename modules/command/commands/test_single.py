from __future__ import annotations

import concurrent.futures
import shutil

import python_progress_bar

from modules.case.saver import save_case_and_result_single
from modules.command.commands.impl.definition import Result
from modules.command.commands.impl.generate_one_case import generate_one_case
from modules.command.commands.impl.test_one_case import test_one_case
from modules.utility.colorizer import code, Color, colorize
from modules.utility.exit_failure import exit_failure
from modules.utility.printer import info, progress
from modules.utility.terminal import clear_current_line, cursor_down, cursor_up
from modules.variable.definition import Variable


def generate_and_test_one_case(program: str, time_limit: int, variables: dict[str, Variable],
                               override_statements: str, format: list[list[str]]) -> tuple[bool, str, Result]:
    success, test_case = generate_one_case(variables, override_statements, format)

    if not success:
        return False, '', Result()

    return True, test_case, test_one_case(program, test_case, time_limit)


def test_single_with_progress_bar(cases: int, program_1: str, time_limit: float, prefix: str, suffix: str,
                                  verify: bool, variables: dict[str, Variable],
                                  override_statements: str, format: list[list[str]]) -> None:
    python_progress_bar.enable_trapping()
    python_progress_bar.setup_scroll_area()

    pad_length = len(str(cases)) + 1

    progress('Start running tests.')
    print('-' * shutil.get_terminal_size().columns + '\n')

    print(f'Test #{"1".rjust(pad_length, " ")} ...')
    python_progress_bar.draw_progress_bar(0)
    cursor_up()

    with concurrent.futures.ProcessPoolExecutor() as executor:
        try_number = 0
        test_number = 0
        detected_number = 0
        futures = [executor.submit(generate_and_test_one_case, program_1, time_limit,
                                   variables, override_statements, format) for _ in range(cases)]

        for future in concurrent.futures.as_completed(futures):
            try_number += 1
            success, test_case, test_result = future.result()

            if success:
                saved = False
                test_number += 1

                if hasattr(test_result, 'exit_code') and (test_result.exit_code != 0):
                    test_result.result = 'RE'
                elif test_result.time > time_limit:
                    test_result.result = 'TLE'

                if test_result.result != '':
                    saved = True
                    detected_number += 1
                    case_name, result_name = save_case_and_result_single(test_case, detected_number,
                                                                           cases, prefix, suffix, time_limit,
                                                                           program_1, test_result)

                    print('Test #{}: {} --> saved as {} and {}'.format(
                        str(test_number).rjust(pad_length, ' '),
                        colorize(Color[test_result.result], test_result.result.ljust(3, ' ')),
                        code(case_name),
                        code(result_name)
                    ))
                    cursor_down()
                elif not hasattr(test_result, 'stdout'):
                    saved = True
                    detected_number += 1
                    case_name, result_name = save_case_and_result_single(test_case, detected_number,
                                                                           cases, prefix, suffix, time_limit,
                                                                           program_1, test_result)
                    print('Test #{}: Failed to capture the output --> saved as {} and {} (maybe not your fault! just in case.)'.format(
                        str(test_number).rjust(pad_length, ' '),
                        code(case_name),
                        code(result_name)
                    ))
                    cursor_down()

            if try_number == cases:
                python_progress_bar.draw_progress_bar(100)
                clear_current_line()
                print('Test: Done!\n')
            else:
                python_progress_bar.draw_progress_bar(100 * try_number // cases)
                if saved:
                    cursor_up()
                print(f'Test #{str(test_number + 1).rjust(pad_length, " ")}')
                cursor_up()

    print('-' * shutil.get_terminal_size().columns)
    if test_number != cases:
        info(f'Failed to generate {code(cases - test_number)} cases.')

    progress('{} (out of {}) tests run successfully.'.format(
        code(test_number),
        code(cases)
    ))

    if verify and test_number < cases // 2:
        exit_failure()


def test_single_without_progress_bar(cases: int, program_1: str, time_limit: float, prefix: str, suffix: str,
                                     verify: bool, variables: dict[str, Variable],
                                     override_statements: str, format: list[list[str]]) -> None:
    pad_length = len(str(cases)) + 1
    progress('Start running tests.')
    cursor_down()

    with concurrent.futures.ProcessPoolExecutor() as executor:
        test_number = 0
        detected_number = 0
        futures = [executor.submit(generate_and_test_one_case, program_1, time_limit,
                                   variables, override_statements, format) for _ in range(cases)]

        for future in concurrent.futures.as_completed(futures):
            success, test_case, test_result = future.result()

            if success:
                test_number += 1

                if hasattr(test_result, 'exit_code') and (test_result.exit_code != 0):
                    test_result.result = 'RE'
                elif test_result.time > time_limit:
                    test_result.result = 'TLE'

                if test_result.result != '':
                    detected_number += 1
                    case_name, result_name = save_case_and_result_single(test_case, detected_number,
                                                                           cases, prefix, suffix, time_limit,
                                                                           program_1, test_result)

                    print('Test #{}: {} --> saved as {} and {}'.format(
                        str(test_number).rjust(pad_length, ' '),
                        colorize(Color[test_result.result], test_result.result.ljust(3, ' ')),
                        code(case_name),
                        code(result_name)
                    ))
                elif not hasattr(test_result, 'stdout'):
                    detected_number += 1
                    case_name, result_name = save_case_and_result_single(test_case, detected_number,
                                                                           cases, prefix, suffix, time_limit,
                                                                           program_1, test_result)
                    print('Test #{}: Failed to capture the output --> saved as {} and {} (maybe not your fault! just in case.)'.format(
                        str(test_number).rjust(pad_length, ' '),
                        code(case_name),
                        code(result_name)
                    ))

        if detected_number > 0:
            cursor_down()

    if test_number != cases:
        info(f'Failed to generate {code(cases - test_number)} cases.')

    progress('{} (out of {}) tests run successfully.'.format(
        code(test_number),
        code(cases)
    ))

    if verify and test_number < cases // 2:
        exit_failure()
