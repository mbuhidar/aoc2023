from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

RED = 12
BLUE = 14
GREEN = 13


def compute(s: str) -> int:

    power_total = 0

    lines = s.splitlines()
    for line in lines:

        red_count = 0
        blue_count = 0
        green_count = 0

        line_split: list[str] = line.split(
            ':', 1,
        )[1].strip().replace(';', ',').split(',')
        line_splits: list[list[str]] = [item.split() for item in line_split]

        for item in line_splits:
            if item[1] == 'red':
                if int(item[0]) > red_count:
                    red_count = int(item[0])
            elif item[1] == 'blue':
                if int(item[0]) > blue_count:
                    blue_count = int(item[0])
            elif item[1] == 'green':
                if int(item[0]) > green_count:
                    green_count = int(item[0])
        power_total += red_count * blue_count * green_count

    return power_total


INPUT_S = '''\
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
'''
EXPECTED = 2286


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
