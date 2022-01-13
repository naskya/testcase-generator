import enum

import colorama


class Color(enum.Enum):
    # color used in message
    ERROR = colorama.Fore.RED
    WARNING = colorama.Fore.YELLOW
    INFO = colorama.Fore.BLUE
    HINT = colorama.Fore.CYAN
    CODE = colorama.Fore.GREEN
    PROMPT = colorama.Fore.MAGENTA
    DONE = colorama.Fore.GREEN

    # color used in judge result
    WA = colorama.Fore.RED
    TLE = colorama.Fore.YELLOW
    RE = colorama.Fore.YELLOW

    RESET = colorama.Fore.RESET


def colorize(color: Color, msg) -> str:
    return f'{color.value}{msg}{Color.RESET.value}'


def code(msg) -> str:
    return colorize(Color.CODE, msg)
