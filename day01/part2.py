from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    sum = 0
    lines = s.splitlines()

    num_hash = {"one": "o1e", "two": "t2o", "three": "th3ee", "four": "f4ur",
                "five": "f5ve", "six": "s6x", "seven": "se7en",
                "eight": "ei8ht", "nine": "n9ne"}

    for line in lines:
        for key, value in num_hash.items():
            line = line.replace(key, value)
        numbers = [num for num in line if num.isdigit()]

        if len(numbers) == 0:
            continue
        else:
            line_sum = int(str(numbers[0]) + str(numbers[-1]))
            sum += line_sum

    return sum

INPUT_S = '''
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
1
'''
EXPECTED = 292


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
