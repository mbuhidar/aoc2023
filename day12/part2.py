from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def calculate_positions(record: str, clues: list[int]) -> dict[int, int]:
    """
    Calculate the positions based on the given record and clues.

    Args:
        record (str): The record string.
        clues (list[int]): The list of clues.

    Returns:
        dict: The positions dictionary.
    """
    positions = {0: 1}
    for i, contiguous in enumerate(clues):
        new_positions: dict[int, int] = {}
        for k, v in positions.items():
            new_positions = update_positions(
                record,
                clues,
                i,
                contiguous,
                k,
                v,
                new_positions,
            )
        positions = new_positions
    return positions


def update_positions(
        record: str,
        clues: list[int],
        i: int,
        contiguous: int,
        k: int,
        v: int,
        new_positions: dict[int, int],
) -> dict[int, int]:
    """
    Update the positions dictionary based on the given parameters.

    Args:
        record (str): The record string.
        clues (list[int]): The list of clues.
        i (int): The index of the current clue.
        contiguous (int): The number of contiguous positions.
        k (int): The current position.
        v (int): The current value.
        new_positions (dict): The dictionary of positions.

    Returns:
        dict: The updated positions dictionary.
    """
    for n in range(k, len(record) - sum(clues[i + 1:]) + len(clues[i + 1:])):
        if (
            n + contiguous - 1 < len(record) and '.'
            not in record[n: n + contiguous]
        ):
            if ((i == len(clues) - 1 and '#' not in record[n + contiguous:])
                or (
                    i < len(clues) - 1 and n + contiguous < len(record)
                    and record[n + contiguous] != '#'
            )):

                new_positions[n + contiguous + 1] = (
                    new_positions.get(n + contiguous + 1, 0) + v
                )
        if record[n] == '#':
            break
    return new_positions


def compute(s: str) -> int:
    """
    Compute the sum of positions based on the given input string.

    Args:
        s (str): The input string containing records and clues.

    Returns:
        int: The sum of positions.

    """
    lines = s.splitlines()

    count = 0
    for line in lines:
        record, clue_str = line.split(' ')
        record = [(record + '?') * 5][0][:-1]
        clues = [int(x) for x in clue_str.split(',')] * 5
        positions = calculate_positions(record, clues)
        count += sum(positions.values())

    return count


INPUT_S = """\
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""
EXPECTED = 525152


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    ((INPUT_S, EXPECTED),),
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
