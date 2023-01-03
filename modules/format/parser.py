from __future__ import annotations

import io
import re
import sys
import typing

from modules.utility.colorizer import code
from modules.utility.printer import info, prompt
from modules.variable.definition import Variable


def parse_format(using_tty: bool, source: typing.TextIO | io.TextIOWrapper, variables: dict[str, Variable]) -> tuple[
    # parsed format
    list[list[str]],
    # raw input
    list[str]
]:
    comment_pattern = re.compile(r'%%.*$')
    res: list[list[str]] = []

    inputs: list[str] = []

    if using_tty:
        prompt()

    for line in source:
        if using_tty:
            inputs.append(line)

        if not line.startswith('%%'):
            line = re.sub(comment_pattern, '', line)

            res.append([])

            for token in line.split():
                if token not in variables:
                    info(f'{code(token)} will be printed as is, since there is no such variable.')

                res[-1].append(token)

        if using_tty:
            prompt()

    return res, inputs
