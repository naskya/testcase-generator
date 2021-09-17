from __future__ import annotations

import sys
import traceback

from modules.utility.exit_failure import exit_failure
from modules.utility.printer import error


def override_all(override_statements: str, generated_values: list[list]) -> None:
    try:
        exec(override_statements, locals())
    except:
        error('Failed to override values.')
        print(traceback.format_exc(), file=sys.stderr)
        exit_failure()
