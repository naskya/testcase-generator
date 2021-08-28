import os
import shutil
import subprocess
import sys
import tempfile


def main() -> None:
    temp_dir = os.path.join(tempfile.gettempdir(), 'testcase-generator')
    os.mkdir(temp_dir)

    cases = 10
    test_command = f'python3 main.py test "python3 {os.path.join("verify", "impl", "exit_failure.py")}" --cases {cases} ' \
                   f'--input {os.path.join("verify", "impl", "in.txt")} ' \
                   f'--prefix {temp_dir}{os.sep} --no-progress-bar --verify'

    print(f'$ {test_command}\n', file=sys.stderr)
    subprocess.run(test_command, shell=True).check_returncode()

    pad_length = len(str(cases))

    assert len(os.listdir(temp_dir)) == (cases * 2)

    for i in range(1, cases + 1):
        assert str(i).rjust(pad_length, '0') in os.listdir(temp_dir)
        assert 'verdict_' + str(i).rjust(pad_length, '0') in os.listdir(temp_dir)

    shutil.rmtree(temp_dir)


if __name__ == '__main__':
    main()
