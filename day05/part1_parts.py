from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def sources_to_destinations(
    sources: list[int],
    source_to_dest_map: list[list[int]],
) -> list[int]:
    destinations = []
    for source in sources:
        for source_to_dest in source_to_dest_map:
            if source in range(
                source_to_dest[1], source_to_dest[1] +
                source_to_dest[2],
            ):
                destination = source_to_dest[0] + source - source_to_dest[1]
                break
            else:
                destination = source
        destinations.append(destination)

    return destinations


def compute(s: str) -> int:
    parts = s.split('\n\n')

    seed_part, *other = parts

    seeds = [int(seed) for seed in seed_part.split()[1:]]

    seed_to_soil = [[int(x) for x in line.split(' ')]
                    for line in other[0].split('\n')[1:]]
    soil_to_fertilizer = [[int(x) for x in line.split(' ')]
                          for line in other[1].split('\n')[1:]]
    fertilizer_to_water = [[int(x) for x in line.split()]
                           for line in other[2].split('\n')[1:]]
    water_to_light = [[int(x) for x in line.split()]
                      for line in other[3].split('\n')[1:]]
    light_to_temperature = [[int(x) for x in line.split()]
                            for line in other[4].split('\n')[1:]]
    temperature_to_humidity = [[int(x) for x in line.split()]
                               for line in other[5].split('\n')[1:]]
    humidity_to_location = [[int(x) for x in line.split()]
                            for line in other[6].split('\n')[1:]]

    soils = sources_to_destinations(seeds, seed_to_soil)
    fertilizers = sources_to_destinations(soils, soil_to_fertilizer)
    waters = sources_to_destinations(fertilizers, fertilizer_to_water)
    lights = sources_to_destinations(waters, water_to_light)
    temperatures = sources_to_destinations(lights, light_to_temperature)
    humidities = sources_to_destinations(temperatures, temperature_to_humidity)
    locations = sources_to_destinations(humidities, humidity_to_location)

    return min(locations)


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
EXPECTED = 35


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
