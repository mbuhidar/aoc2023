from __future__ import annotations

import argparse
import os.path
import re

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    boxes: dict[int, dict[str, int]] = {}

    for token in s.split(','):
        # parse token into lens label, operation, and focal length
        lens_label = ''.join(re.findall('[a-zA-Z]', token))  # Find all letters
        # Find all non-alphanumeric characters
        operation = re.findall(r'\W', token)
        focal_length = int(
            ''.join(re.findall(r'\d', token)),
        ) if re.findall(r'\d', token) else 0

        # find box number from lens label using hashing algorithm
        box_number = 0
        current_value = 0
        for char in lens_label:
            current_value = (current_value + ord(char)) * 17 % 256
        box_number += current_value

        # create dictionary of dictionaries for boxes and lenses
        if operation[0] == '=':
            if box_number not in boxes:
                boxes[box_number] = {}
            boxes[box_number][lens_label] = focal_length
        elif operation[0] == '-':
            if box_number not in boxes:
                continue
            if lens_label in boxes[box_number]:
                del boxes[box_number][lens_label]

    # calculate total focusing power
    total_focusing_power = 0
    for k, v in boxes.items():
        for i, v2 in enumerate(v.values()):
            focusing_power = (k + 1) * (i + 1) * v2
            total_focusing_power += focusing_power

    return total_focusing_power


INPUT_S = '''\
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
'''
EXPECTED = 145  # 247933


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
