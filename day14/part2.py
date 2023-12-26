from __future__ import annotations

import argparse
import copy
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def tilt_north(lines_list: list[list[str]]) -> list[list[str]]:
    done_flag = False
    while done_flag is False:
        done_flag = True
        for i, line_list in enumerate(lines_list):
            if i == 0:
                continue
            for j, char in enumerate(line_list):
                if char == 'O' and lines_list[i-1][j] not in ('O', '#'):
                    lines_list[i-1][j] = 'O'
                    lines_list[i][j] = '.'
                    done_flag = False
    return lines_list


def tilt_west(lines_list: list[list[str]]) -> list[list[str]]:
    done_flag = False
    while done_flag is False:
        done_flag = True
        for line_list in lines_list:
            for j, char in enumerate(line_list):
                if j == 0:
                    continue
                if char == 'O' and line_list[j - 1] not in ('O', '#'):
                    line_list[j - 1] = 'O'
                    line_list[j] = '.'
                    done_flag = False
    return lines_list


def ew_flip(lines_list: list[list[str]]) -> list[list[str]]:
    for line_list in lines_list:
        line_list.reverse()
    return lines_list


def ns_flip(lines_list: list[list[str]]) -> list[list[str]]:
    lines_list.reverse()
    return lines_list


def tilt_cycle(lines_list: list[list[str]]) -> list[list[str]]:
    lines_list = tilt_north(lines_list)
    lines_list = tilt_west(lines_list)
    lines_list = ns_flip(tilt_north(ns_flip(lines_list)))
    lines_list = ew_flip(tilt_west(ew_flip(lines_list)))
    return lines_list


def compute(s: str) -> int:
    lines = s.splitlines()
    lines_list: list[list[str]] = []

    for line in lines:
        lines_list.append(list(line))

    # find the repeating cycle count
    prior_lines_lists: list[list[str]] = []
    i = 0
    while True:
        i += 1
        lines_list = tilt_cycle(lines_list)
        if lines_list in prior_lines_lists:
            cycle_count = i
            break
        prior_lines_lists.append(copy.deepcopy(lines_list))

    # run through tilt cycles and calculate total load on north platform
    total_load = 0
    for _ in range(cycle_count + 1000000000 % cycle_count - 1):
        lines_list = tilt_cycle(lines_list)
        platform_height = len(lines_list)
        total_load = 0
        for j, line_list in enumerate(lines_list):
            total_load += line_list.count('O') * (platform_height - j)

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
EXPECTED = 64


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
