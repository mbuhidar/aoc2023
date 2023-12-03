from __future__ import annotations

import argparse
import os.path
import re

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    '''Count the product of all numbers that share adjacency with one other
     number to a * symbol in a grid'''
    # build map of coords for symbol *
    map_symbol = set('*')
    map_of_symbol_coords = support.parse_coords_hash(s, map_symbol)

    # calculate sum of all gear ratios (products of two, and only two, numbers
    # adjacent to the * symbol)
    sum_of_gear_ratios = 0

    # list for coord clouds surrounding all numbers
    number_coord_clouds = []

    for y, line in enumerate(s.splitlines()):
        # find each number in the line with starting position
        for match in re.finditer(r'\d+', line):
            number = match.group()
            start_pos = match.start()

            # build a coordinate cloud around the number
            number_cloud = [] 
            for x in range(len(number)):
                adjacent_coords = support.adjacent_8(x+start_pos, y)
                for adjacent_coord in adjacent_coords:
                    number_cloud.append(adjacent_coord)
            number_coord_clouds.append([number, number_cloud])

    # for each *, check count of adjacent numbers for qty 2
    for gear_coord in map_of_symbol_coords:
        gear_nums_list = []
        for item in number_coord_clouds:
            number = item[0]
            cloud = item[1]
            if gear_coord in cloud:
                gear_nums_list.append(number)
        if len(gear_nums_list) == 2:
            sum_of_gear_ratios += int(gear_nums_list[0]) * int(gear_nums_list[1])

    return sum_of_gear_ratios


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
EXPECTED = 467835


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
