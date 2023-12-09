from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()

    lr_instructions = lines[0]

    nodes = {}
    for line in lines[2:]:
        node = line.split('=')
        node_id = node[0].strip()
        node_coords = node[1].strip().strip('()').split(', ')
        nodes[node_id] = node_coords

    prior_node = nodes['AAA']
    goal = False
    step_count = 0

    while goal is False:
        for direction in lr_instructions:
            if direction == 'L':
                if prior_node[0] == 'ZZZ':
                    goal = True
                prior_node = nodes[prior_node[0]]
                step_count += 1
            elif direction == 'R':
                if prior_node[1] == 'ZZZ':
                    goal = True
                prior_node = nodes[prior_node[1]]
                step_count += 1

    return step_count


INPUT_S = '''\
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
'''
EXPECTED = 2


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
