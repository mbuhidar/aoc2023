from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

EXPANSION_FACTOR = 1000000


def compute(s: str) -> int:

    lines = s.splitlines()
    unique_used_columns = set()
    used_columns = []
    expanded_lines = []
    expanded_universe = []

    # Find the columns with a '#' in them
    for line in lines:
        for i, char in enumerate(line):
            if char == '#':
                used_columns.append(i)
        unique_used_columns = set(used_columns)

    # Expand each line to duplicate columns with no '#' in them
    for line in lines:
        expanded_line = ''
        for i, char in enumerate(line):
            expanded_line += char
            if i not in unique_used_columns:
                expanded_line = expanded_line[:-1] + 'm'
        expanded_lines.append(expanded_line)

    # Duplicate the lines with no '#' in them
    for line in expanded_lines:
        expanded_universe.append(line)
        if '#' not in line:
            line = line.replace('.', 'm')
            expanded_universe[-1] = line

    # Write the expanded universe to a file
    with open('output_pt2.txt', 'w', encoding='utf-8') as f:
        for line in expanded_universe:
            f.write(line + '\n')

    # Create dictionary of count and coordinates for each '#' in the
    # expanded universe
    galaxy_map = {}
    galaxy_num = 1
    row_add = 0
    col_add = 0
    y = 0

    for i, line in enumerate(expanded_universe):
        if line.count('m') == len(line):
            row_add += EXPANSION_FACTOR - 1
            y = i + row_add
            continue
        y = i + row_add
        col_add = 0
        x = 0
        for j, char in enumerate(line):
            if char == 'm':
                col_add += EXPANSION_FACTOR - 1
            x = j + col_add
            if char == '#':
                galaxy_map[galaxy_num] = (x, y)
                galaxy_num += 1

    # Find the distance between each '#' and every other '#'
    distance = 0
    for k, v in galaxy_map.items():
        for k2, v2 in galaxy_map.items():
            if k < k2:
                distance += abs(v[0] - v2[0]) + abs(v[1] - v2[1])

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
EXPECTED = 8410


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
