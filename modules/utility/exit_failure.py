import sys
import typing

import colorama


def exit_failure() -> typing.NoReturn:
    colorama.deinit()
    sys.exit(1)
