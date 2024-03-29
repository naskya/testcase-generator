import fnmatch
import os
import shutil
import subprocess
import sys
import tempfile
import time


def main() -> None:
    cases = 100
    temp_dir = os.path.join(tempfile.gettempdir(), 'testcase-generator')
    checker_dir = os.path.join('verify', 'checker')
    os.mkdir(temp_dir)

    for dirpath, _, filenames in os.walk('samples'):
        for filename in filenames:
            if not filename.endswith('.txt'):
                print(f'{os.path.join(dirpath, filename)} does not end with \'.txt\'.')
                sys.exit(1)

            test_command = 'python3 main.py test ' \
                           f'"python3 {os.path.join(checker_dir, os.path.join(dirpath, filename)[8:-4])}.py" ' \
                           f'"python3 {os.path.join("verify", "impl", "exit_success.py")}" ' \
                           f'--prefix {temp_dir}{os.sep} --suffix .in ' \
                           f'--input {os.path.join(dirpath, filename)} --cases {cases} --no-progress-bar --verify'

            print(f'Start testing {os.path.join(dirpath, filename)}.', file=sys.stderr)
            print(f'$ {test_command}\n', file=sys.stderr)

            started = time.time()
            subprocess.run(test_command, shell=True).check_returncode()
            diff = time.time() - started

            assert len(fnmatch.filter(os.listdir(temp_dir), '*.in')) == 0

            print(f'\nOK (exec time: {round(diff * 1000)} ms)', file=sys.stderr)
            print('Note: testcase-generator uses multiprocessing, so the tests', file=sys.stderr)
            print('      should run much faster than this on your computer.', file=sys.stderr)
            print('-' * 75, file=sys.stderr)

    shutil.rmtree(temp_dir)


if __name__ == '__main__':
    main()
