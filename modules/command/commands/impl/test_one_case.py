from __future__ import annotations

import subprocess
import time

from modules.command.commands.impl.definition import Result


def test_one_case(program: str, test_case: str, time_limit: float) -> Result:
    result = Result()

    try:
        start = time.time()
        status = subprocess.run(program, shell=True, input=test_case, timeout=time_limit,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        result.time = time.time() - start
        result.stdout = status.stdout
        result.stderr = status.stderr
        result.exit_code = status.returncode
    except subprocess.TimeoutExpired:
        result.time = time_limit + 100

    return result
