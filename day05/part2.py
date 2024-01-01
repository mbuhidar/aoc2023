from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    seed_ranges, *parts = s.split('\n\n')

    seed_inputs = list(map(int, seed_ranges.split(':')[1].split()))

    seeds = []
    for i in range(0, len(seed_inputs), 2):
        seeds.append((seed_inputs[i], seed_inputs[i] + seed_inputs[i + 1]))

    for part in parts:
        origin_to_dest_map = []
        for line in part.splitlines()[1:]:
            origin_to_dest_map.append(list(map(int, line.split())))

        new_destination = []
        while len(seeds) > 0:
            start, end = seeds.pop()
            for destination, source, range_length in origin_to_dest_map:
                overlap_start = max(start, source)
                overlap_end = min(end, source + range_length)
                if overlap_start < overlap_end:
                    new_destination.append(
                        (
                            overlap_start - source + destination,
                            overlap_end - source + destination,
                        ),
                    )
                    if overlap_start > start:
                        seeds.append((start, overlap_start))
                    if end > overlap_end:
                        seeds.append((overlap_end, end))
                    break
            else:
                new_destination.append((start, end))

        seeds = new_destination

    return min(seeds)[0]  # 69323688


INPUT_S = '''\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
'''
EXPECTED = 46


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
