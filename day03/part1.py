from __future__ import annotations

import argparse
import os.path
import re

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    '''Count the sum of all numbers that are adjacent to a symbol in the grid'''
    # build set of all symbols
    symbols = set()
    for char in s:
        if char not in '0123456789.\n':
            symbols.add(char)

    # build map of coords for symbols
    symbol_coords = support.parse_coords_hash(s, symbols)

    # calculate sum of all part numbers adjacent to symbols 
    pn_count = 0

    for y, line in enumerate(s.splitlines()):
        # find each number in the line with starting position
        for match in re.finditer(r'\d+', line):
            number = match.group()
            start_pos = match.start()
            # check if any of the adjacent coords are in the symbol coords
            found = False
            for x, char in enumerate(number):
                adjacent_coords = support.adjacent_8(x+start_pos, y)
                for adjacent_coord in adjacent_coords:
                    if adjacent_coord in symbol_coords:
                        pn = int(number)
                        pn_count += pn
                        found = True
                        break 
                if found:
                    break
        
    return pn_count


INPUT_S = '''\
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
'''
EXPECTED = 4361


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
