from __future__ import annotations

import sys
import traceback

from modules.command.commands.impl.definition import Result
from modules.utility.exit_failure import exit_failure
from modules.utility.printer import error


def case_file_name(case_number: int, max: int, prefix: str, suffix: str) -> str:
    return prefix + str(case_number).rjust(len(str(max)), '0') + suffix


def verdict_file_name(case_number: int, max: int, prefix: str, suffix: str) -> str:
    return prefix + 'verdict_' + str(case_number).rjust(len(str(max)), '0') + suffix


def save_case(test_case: str, case_number: int, max: int, prefix: str, suffix: str) -> str:
    try:
        with open(case_file_name(case_number, max, prefix, suffix), mode='w') as f:
            f.write(test_case)
    except:
        error('Failed to save the test case.')
        print(traceback.format_exc(), file=sys.stderr)
        exit_failure()


def shorten(s: str, l: int = 2000) -> str:
    return s if (len(s) <= l) else f'{s[:l]} ... ({len(s) - l} characters have been ommited)'


def save_case_and_verdict_single(test_case: str, case_number: int, max: int, prefix: str, suffix: str,
                                 time_limit: float, program_1: str, result_1: Result) -> tuple[str, str]:
    case_name = case_file_name(case_number, max, prefix, suffix)
    verdict_name = verdict_file_name(case_number, max, prefix, suffix)

    try:
        with open(case_name, mode='w') as f:
            f.write(test_case)

        with open(verdict_name, mode='w') as f:
            f.write('[File name]\n{}\n\n[{}]{}\n'.format(
                case_name,
                program_1,
                '' if (result_1.verdict == '') else f'\nverdict: {result_1.verdict}',
            ))
            if hasattr(result_1, 'exit_code'):
                f.write(f'exit code: {result_1.exit_code}\n')
            if hasattr(result_1, 'time') and (result_1.time < time_limit):
                f.write(f'exec time: {round(result_1.time * 1000)} ms\n')
            f.write('\n')
            if hasattr(result_1, 'stdout'):
                f.write(f'stdout:\n{shorten(result_1.stdout)}\n')
            if hasattr(result_1, 'stderr'):
                f.write(f'stderr:\n{shorten(result_1.stderr)}\n')
    except:
        error('Failed to save the test case.')
        print(traceback.format_exc(), file=sys.stderr)
        exit_failure()

    return case_name, verdict_name


def save_case_and_verdict_double(test_case: str, case_number: int, max: int, prefix: str, suffix: str,
                                 time_limit: float, program_1: str, result_1: Result,
                                 program_2: str, result_2: Result) -> tuple[str, str]:
    case_name = case_file_name(case_number, max, prefix, suffix)
    verdict_name = verdict_file_name(case_number, max, prefix, suffix)

    try:
        with open(case_name, mode='w') as f:
            f.write(test_case)

        with open(verdict_name, mode='w') as f:
            f.write('[File name]\n{}\n\n[{}]{}\n'.format(
                case_name,
                program_1,
                '' if (result_1.verdict == '') else f'\nverdict: {result_1.verdict}',
            ))
            if hasattr(result_1, 'exit_code'):
                f.write(f'exit code: {result_1.exit_code}\n')
            if hasattr(result_1, 'time') and (result_1.time < time_limit):
                f.write(f'exec time: {round(result_1.time * 1000)} ms\n')
            f.write('\n')
            if hasattr(result_1, 'stdout'):
                f.write(f'stdout:\n{shorten(result_1.stdout)}\n')
            if hasattr(result_1, 'stderr'):
                f.write(f'stderr:\n{shorten(result_1.stderr)}\n')
            f.write('[{}]{}\n'.format(
                program_2,
                '' if (result_2.verdict == '') else f'\nverdict: {result_2.verdict}',
            ))
            if hasattr(result_2, 'exit_code'):
                f.write(f'exit code: {result_2.exit_code}\n')
            if hasattr(result_2, 'time') and (result_2.time < time_limit):
                f.write(f'exec time: {round(result_2.time * 1000)} ms\n')
            f.write('\n')
            if hasattr(result_2, 'stdout'):
                f.write(f'stdout:\n{shorten(result_2.stdout)}\n')
            if hasattr(result_2, 'stderr'):
                f.write(f'stderr:\n{shorten(result_2.stderr)}\n')
    except:
        error('Failed to save the test case.')
        print(traceback.format_exc(), file=sys.stderr)
        exit_failure()

    return case_name, verdict_name
