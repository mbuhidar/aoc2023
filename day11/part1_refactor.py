from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()

    # Find the columns with a '#' in them
    unique_used_columns = {
        i for line in lines for i, char in enumerate(line)
        if char == '#'
    }

    # Expand each line to duplicate columns with no '#' in them
    expanded_lines = [
        ''.join(
            char if i in unique_used_columns else
            char + '.' for i, char in enumerate(line)
        )
        for line in lines
    ]

    # Duplicate the lines with no '#' in them
    expanded_universe = [
        line for line in expanded_lines
        for _ in range(2 if '#' not in line else 1)
    ]

    # Write the expanded universe to a file
    with open('output.txt', 'w', encoding='utf-8') as f:
        f.writelines(line + '\n' for line in expanded_universe)

    # Create dictionary of count and coordinates for each '#' in the
    # expanded universe
    galaxy_num = 1
    galaxy_map = {
        (galaxy_num := galaxy_num + 1): (i, j)
        for i, line in enumerate(expanded_universe)
        for j, char in enumerate(line) if char == '#'
    }

    # Find the distance between each '#' and every other '#'
    distance = sum(
        abs(v[0] - v2[0]) + abs(v[1] - v2[1])
        for k, v in galaxy_map.items() for
        k2, v2 in galaxy_map.items() if k < k2
    )

    return distance


INPUT_S = '''\
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....

'''
EXPECTED = 374


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
