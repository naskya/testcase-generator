import sys


def cursor_up(lines: int = 1) -> None:
    if lines < 0:
        cursor_down(-lines)
    else:
        sys.stdout.write('\033[A' * lines)


def cursor_down(lines: int = 1) -> None:
    if lines < 0:
        cursor_up(-lines)
    else:
        sys.stdout.write('\n' * lines)


def clear_current_line() -> None:
    sys.stdout.write('\033[K')
