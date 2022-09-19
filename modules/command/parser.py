from __future__ import annotations

import argparse

from modules.utility.colorizer import code


def parse_command_line_argument() -> argparse.Namespace:
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, epilog='''
example:
  {} {}
    Generate 1000 test cases in the test_case directory from fmt.txt.

  {} {}
    Generate 2000 test cases from vars.txt
    and give them as input to ./a.out and ./naive.out to run tests.
    '''.format(
        code('%(prog)s'),
        code('gen -i fmt.txt -p test_case/ -c 1000'),
        code('%(prog)s'),
        code('test ./a.out ./naive.out --input vars.txt --cases 2000')
    ))

    subparsers = parser.add_subparsers(dest='subcommand', required=True)

    parser_gen = subparsers.add_parser(
        'gen', help='Generate test cases.'
    )
    parser_gen.add_argument('-c', '--cases', required=True, type=int, metavar='#cases',
                            help='The number of test cases to generate.')
    parser_gen.add_argument('-i', '--input', required=False, type=str, default='', metavar='filename',
                            help='The name of the file that specifies the format of the test case following this.\n'
                            'if ommited, the input is read from standard input.')
    parser_gen.add_argument('-p', '--prefix', required=False, type=str, default='', metavar='prefix',
                            help='Prefix of the name of test cases to be saved.')
    parser_gen.add_argument('-s', '--suffix', required=False, type=str, default='', metavar='suffix',
                            help='Suffix of the name of test cases to be saved.\n'
                            'By default, test cases are saved with sequentially numbered names starting with 1.\n'
                            'You can prefix and / or suffix to their names by specifying these options.')
    parser_gen.add_argument('-n', '--no-progress-bar', action='store_true', required=False, default=False,
                            help='If specified, the progress bar output will be suppressed.\n'
                            'This option takes no additional arguments.')
    parser_gen.add_argument('--verify', required=False, default=False, action='store_true', help=argparse.SUPPRESS)

    parser_test = subparsers.add_parser(
        'test', help='Generate test cases and feed them to provided program(s) as inputs to run tests.'
    )
    parser_test.add_argument('programs', nargs='+', type=str, metavar='program_1 [program_2]', help='program(s) to test')
    parser_test.add_argument('-c', '--cases', required=True, type=int, metavar='#cases',
                             help='The number of test cases to generate.')
    parser_test.add_argument('-i', '--input', required=False, type=str, default='', metavar='filename',
                             help='The name of the file that specifies the format of the test case following this.\n'
                             'if ommited, the input is read from standard input.')
    parser_test.add_argument('-p', '--prefix', required=False, type=str, default='', metavar='prefix',
                             help='Prefix of the name of test cases to be saved.')
    parser_test.add_argument('-s', '--suffix', required=False, type=str, default='', metavar='suffix',
                             help='Suffix of the name of test cases to be saved.\n'
                             'By default, test cases are saved with sequentially numbered names starting with 1.\n'
                             'You can prefix and/or suffix to their names by specifying these options.')
    parser_test.add_argument('-t', '--time-limit', required=False, type=float, default=2., metavar='time_in_sec',
                             help='The maximum execution time of each test in seconds.\n'
                             'If ommited, the maximum execution time of each test will be 2 seconds.')
    parser_test.add_argument('-n', '--no-progress-bar', action='store_true', required=False, default=False,
                             help='If specified, the progress bar output will be suppressed.\n'
                             'This option takes no additional arguments.')
    parser_test.add_argument('--verify', required=False, default=False, action='store_true', help=argparse.SUPPRESS)

    return parser.parse_args()
