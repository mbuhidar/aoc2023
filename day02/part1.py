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

    game_total = 0

    lines = s.splitlines()
    for idx, line in enumerate(lines):

        game_id = idx + 1
        game_total += game_id

        line = line.split(':', 1)[1].strip().replace(';', ',').split(',')
        line = [item.split() for item in line]
        print(game_id)
        print(line)

        for item in line:
            if item[1] == 'red':
                if int(item[0]) > RED:
                    game_total -= game_id
                    break
            elif item[1] == 'blue':
                if int(item[0]) > BLUE:
                    game_total -= game_id
                    break
            elif item[1] == 'green':
                if int(item[0]) > GREEN:
                    game_total -= game_id
                    break

    return game_total


INPUT_S = '''\
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
'''
EXPECTED = 8


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
