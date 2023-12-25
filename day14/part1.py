from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()
    lines_list = []

    for line in lines:
        lines_list.append(list(line))

    total_load = 0
    done_flag = False
    platform_height = len(lines_list)

    while done_flag is False:
        done_flag = True
        total_load = 0
        for i, line_list in enumerate(lines_list):
            total_load += line_list.count('O') * (platform_height - i)
            if i == 0:
                continue
            for j, char in enumerate(line_list):
                if char == 'O' and lines_list[i-1][j] not in ('O', '#'):
                    lines_list[i-1][j] = 'O'
                    lines_list[i][j] = '.'
                    done_flag = False

    return total_load


INPUT_S = '''\
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
'''
EXPECTED = 136


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
