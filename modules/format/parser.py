from __future__ import annotations

import io
import re
import sys
import typing

from modules.utility.colorizer import Color, colorize
from modules.utility.printer import prompt, warning
from modules.variable.definition import VariableType


def parse_format(source: typing.TextIO | io.TextIOWrapper, variables: dict[str, VariableType]) -> list[list[str]]:
    comment_pattern = re.compile(r'%%.*$')
    res: list[list[str]] = []

    if (source == sys.stdin) and sys.stdin.isatty():
        prompt()

    for line in source:
        line = re.sub(comment_pattern, '', line)

        res.append([])

        for token in line.split():
            if not token in variables:
                warning(f'{colorize(Color.CODE, token)} will be printed as is, since there is no such variable.')

            res[-1].append(token)

        if (source == sys.stdin) and sys.stdin.isatty():
            prompt()

    return res
