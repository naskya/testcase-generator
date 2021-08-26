from __future__ import annotations

import concurrent.futures
import os
import shutil
import signal

import psutil

from modules.case.saver import save_case
from modules.command.commands.impl.generate_one_case import generate_one_case
from modules.command.definition import Command
from modules.utility.colorizer import Color, colorize
from modules.utility.printer import progress, progress_bar
from modules.variable.definition import VariableType


def gen_with_progress_bar(command: Command, variables: dict[str, VariableType],
                          override_statements: str, format: list[list[str]]) -> None:
    pad_length = len(str(command.cases)) + 1

    progress('Start generating test cases.')
    print('-' * shutil.get_terminal_size().columns + '\n')
    print(f'Generating test case #{"1".rjust(pad_length, " ")}')

    with concurrent.futures.ProcessPoolExecutor() as executor:
        test_number = 0
        futures = [executor.submit(generate_one_case, variables, override_statements, format)
                   for _ in range(command.cases * 2)]

        for future in concurrent.futures.as_completed(futures):
            test_number += 1

            save_case(future.result(), test_number, command.cases, command.prefix, command.suffix)

            # show progress
            print(f'\033[AGenerating test case #{str(test_number + 1).rjust(pad_length, " ")}')
            progress_bar(test_number, command.cases, 50)

            if test_number == command.cases:
                print(f'\033[AGenerating test case: Done!\033[K\n\n')
                executor.shutdown(wait=False)

                try:
                    parent = psutil.Process(os.getpid())
                    for process in parent.children(recursive=True):
                        process.send_signal(signal.SIGKILL)
                except psutil.NoSuchProcess:
                    pass

                break

    print('-' * shutil.get_terminal_size().columns)
    progress('{} (out of {}) cases have been generated successfully.'.format(
        colorize(Color.CODE, test_number),
        colorize(Color.CODE, command.cases)
    ))


def gen_without_progress_bar(command: Command, variables: dict[str, VariableType],
                             override_statements: str, format: list[list[str]]) -> None:
    progress('Start generating test cases.')

    with concurrent.futures.ProcessPoolExecutor() as executor:
        test_number = 0
        futures = [executor.submit(generate_one_case, variables, override_statements, format) for _ in range(command.cases * 2)]

        for future in concurrent.futures.as_completed(futures):
            test_number += 1

            save_case(future.result(), test_number, command.cases, command.prefix, command.suffix)

            if test_number == command.cases:
                executor.shutdown(wait=False)

                try:
                    parent = psutil.Process(os.getpid())
                    for process in parent.children(recursive=True):
                        process.send_signal(signal.SIGKILL)
                except psutil.NoSuchProcess:
                    pass

                break

    progress('{} (out of {}) cases have been generated successfully.'.format(
        colorize(Color.CODE, test_number),
        colorize(Color.CODE, command.cases)
    ))
