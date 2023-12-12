from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def layers(readings: list[list[int]]) -> list[list[int]]:

    if all(value == 0 for value in readings[-1]):
        return readings

    next_layer = [
        int(readings[-1][i + 1]) - int(readings[-1][i])
        for i in range(len(readings[-1]) - 1)
    ]
    readings.append(next_layer)
    return layers(readings)


def compute(s: str) -> int:
    lines = s.splitlines()

    sum_of_next_values = 0

    for line in lines:
        readings = [[int(reading) for reading in line.split(' ')]]
        tree = layers(readings)
        tree = tree[::-1]
        appended_lines = []
        appended_line = []

        for i in range(len(tree) - 1):
            tree[i + 1].append(tree[i][-1] + tree[i + 1][-1])
        appended_lines.append(tree[-1])
        appended_line = list(appended_lines[-1])

        sum_of_next_values = sum_of_next_values + appended_line[-1]

    return sum_of_next_values


INPUT_S = '''\
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
'''
EXPECTED = 114


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
