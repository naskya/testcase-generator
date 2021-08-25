from __future__ import annotations

import enum
import io
import typing


class Feature(enum.Enum):
    GENERATE = 0
    TEST_SINGLE = 1
    TEST_DOUBLE = 2


class Command:
    feature: Feature
    # programs to test
    program_1: str
    program_2: str
    # input file
    source: typing.TextIO | io.TextIOWrapper
    # output file name
    prefix: str
    suffix: str
    # number of test cases to generate
    cases: int
    # time limit in seconds
    time_limit: float
    # show progress bar?
    show_progress: bool


# default settings
default_prefix = ''
default_suffix = ''
default_cases_for_gen = 1
default_cases_for_test = 2000
default_time_limit = 2.0
default_show_progress = True
