from __future__ import annotations

import io
import re
import sys
import typing

from modules.utility.colorizer import Color, colorize
from modules.utility.printer import info, prompt
from modules.variable.definition import Variable


def parse_format(source: typing.TextIO | io.TextIOWrapper, variables: dict[str, Variable]) -> list[list[str]]:
    comment_pattern = re.compile(r'%%.*$')
    res: list[list[str]] = []

    if (source == sys.stdin) and sys.stdin.isatty():
        prompt()

    for line in source:
        if not line.startswith('%%'):
            line = re.sub(comment_pattern, '', line)

            res.append([])

            for token in line.split():
                if token not in variables:
                    info(f'{colorize(Color.CODE, token)} will be printed as is, since there is no such variable.')

                res[-1].append(token)

        if (source == sys.stdin) and sys.stdin.isatty():
            prompt()

    return res
