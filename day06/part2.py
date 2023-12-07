from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()
    times = [time for time in lines[0].split()[1:]]
    distances = [distance for distance in lines[1].split()[1:]]

    time_str = ''
    for time in times:
        time_str += time
    total_time = int(time_str)

    dist_str = ''
    for dist in distances:
        dist_str += dist
    total_dist = int(dist_str)

    wins = 0
    for i in range(total_time):
        travel_distance = (total_time - i) * i
        if travel_distance > total_dist:
            wins += 1

    return wins


INPUT_S = '''\
Time:      7  15   30
Distance:  9  40  200
'''
EXPECTED = 71503


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
