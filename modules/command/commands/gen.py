from __future__ import annotations

import concurrent.futures
import os
import shutil
import signal

import psutil
import python_progress_bar

from modules.case.saver import save_case
from modules.command.commands.impl.generate_one_case import generate_one_case
from modules.utility.colorizer import code
from modules.utility.exit_failure import exit_failure
from modules.utility.printer import info, progress
from modules.utility.terminal import clear_current_line, cursor_down, cursor_up
from modules.variable.definition import Variable


def gen_with_progress_bar(cases: int, prefix: str, suffix: str, verify: bool, variables: dict[str, Variable],
                          override_statements: str, format: list[list[str]]) -> None:
    python_progress_bar.enable_trapping()
    python_progress_bar.setup_scroll_area()

    pad_length = len(str(cases)) + 1

    progress('Start generating test cases.')
    print('-' * shutil.get_terminal_size().columns + '\n')
    print(f'Generate #{"1".rjust(pad_length, " ")} ...')

    with concurrent.futures.ProcessPoolExecutor() as executor:
        test_number = 0

        futures = [executor.submit(generate_one_case, variables, override_statements, format)
                   for _ in range(cases * 2)]

        for future in concurrent.futures.as_completed(futures):
            success, result = future.result()

            if not success:
                continue

            test_number += 1

            save_case(result, test_number, cases, prefix, suffix)

            # show progress
            cursor_up()
            print(f'Generate #{str(test_number + 1).rjust(pad_length, " ")} ...')
            python_progress_bar.draw_progress_bar(100 * test_number // cases)

            if test_number == cases:
                cursor_up()
                clear_current_line()
                print('Generate: Done!')
                python_progress_bar.destroy_scroll_area()
                executor.shutdown(wait=False)

                try:
                    parent = psutil.Process(os.getpid())
                    for process in parent.children(recursive=True):
                        process.send_signal(signal.SIGKILL)
                except psutil.NoSuchProcess:
                    pass

                break

    print('-' * shutil.get_terminal_size().columns)
    if test_number != cases:
        info(f'Failed to generate {cases - test_number} cases.')

    progress('{} (out of {}) cases have been generated successfully.'.format(
        code(test_number),
        code(cases)
    ))

    if verify and test_number < cases // 2:
        exit_failure()


def gen_without_progress_bar(cases: int, prefix: str, suffix: str, verify: bool, variables: dict[str, Variable],
                             override_statements: str, format: list[list[str]]) -> None:
    progress('Start generating test cases.')

    with concurrent.futures.ProcessPoolExecutor() as executor:
        test_number = 0
        futures = [executor.submit(generate_one_case, variables, override_statements, format) for _ in range(cases * 2)]

        for future in concurrent.futures.as_completed(futures):
            success, result = future.result()

            if not success:
                continue

            test_number += 1

            save_case(result, test_number, cases, prefix, suffix)

            if test_number == cases:
                executor.shutdown(wait=False)

                try:
                    parent = psutil.Process(os.getpid())
                    for process in parent.children(recursive=True):
                        process.send_signal(signal.SIGKILL)
                except psutil.NoSuchProcess:
                    pass

                break

    if test_number != cases:
        info(f'Failed to generate {cases - test_number} cases.')

    progress('{} (out of {}) cases have been generated successfully.'.format(
        code(test_number),
        code(cases)
    ))

    if verify and test_number < cases // 2:
        exit_failure()
