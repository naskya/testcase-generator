import sys

from modules.utility.colorizer import Color, colorize


def info(msg: str) -> None:
    print(f'    {colorize(Color.INFO, "Info:")}', msg, file=sys.stderr)


def hint(msg: str) -> None:
    print(f'    {colorize(Color.HINT, "Hint:")}', msg, file=sys.stderr)


def progress(msg: str) -> None:
    print('Progress:', msg, file=sys.stderr)


def warning(msg: str) -> None:
    print(f' {colorize(Color.WARNING, "Warning:")}', msg, file=sys.stderr)


def error(msg: str) -> None:
    print(f'   {colorize(Color.ERROR, "Error:")}', msg, file=sys.stderr)


def prompt() -> None:
    print(colorize(Color.PROMPT, '>>> '), end='', flush=True)


def progress_bar(done: int, total: int, length: int) -> None:
    print(f'  {done*100//total:3}% [', end='')
    for i in range(length):
        print(colorize(Color.DONE, '#') if (i <= done*length//total) else '.', end='')
    print(']', end='\r')
