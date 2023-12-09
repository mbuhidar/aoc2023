from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def secondary_sort(type_list: list[list[str]], i: int) -> list[list[str]]:
    relative_strength = [
        'A', 'K', 'Q', 'J', 'T',
        '9', '8', '7', '6', '5', '4', '3', '2',
    ]
    if i < 0:
        return type_list

    type_list_sorted = []
    for card_strength in relative_strength:
        for hand in type_list:
            if hand[0][i] in card_strength:
                type_list_sorted.append(hand)

    return secondary_sort(type_list_sorted, i-1)


def compute(s: str) -> int:
    lines = s.splitlines()

    # hand types
    five_of_a_kind = []
    four_of_a_kind = []
    full_house = []
    three_of_a_kind = []
    two_pairs = []
    one_pair = []
    high_card = []

    for line in lines:
        hands_bids = list(line.split(' '))

        char_used = []
        hand_counts = []

        for char in hands_bids[0]:
            if char in char_used:
                continue
            char_used.append(char)
            hand_counts.append(str(hands_bids[0].count(char)))

        if '5' in hand_counts:
            five_of_a_kind.append(hands_bids)
        elif '4' in hand_counts:
            four_of_a_kind.append(hands_bids)
        elif '3' in hand_counts:
            if '2' in hand_counts:
                full_house.append(hands_bids)
            else:
                three_of_a_kind.append(hands_bids)
        elif hand_counts.count('2') == 2:
            two_pairs.append(hands_bids)
        elif hand_counts.count('2') == 1:
            one_pair.append(hands_bids)
        else:
            high_card.append(hands_bids)

    entire_sort = []

    five_of_a_kind = secondary_sort(five_of_a_kind, 4)
    entire_sort.extend(five_of_a_kind)
    four_of_a_kind = secondary_sort(four_of_a_kind, 4)
    entire_sort.extend(four_of_a_kind)
    full_house = secondary_sort(full_house, 4)
    entire_sort.extend(full_house)
    three_of_a_kind = secondary_sort(three_of_a_kind, 4)
    entire_sort.extend(three_of_a_kind)
    two_pairs = secondary_sort(two_pairs, 4)
    entire_sort.extend(two_pairs)
    one_pair = secondary_sort(one_pair, 4)
    entire_sort.extend(one_pair)
    high_card = secondary_sort(high_card, 4)
    entire_sort.extend(high_card)

    entire_sort.reverse()

    total = 0
    for rank, hands_bids in enumerate(entire_sort):
        total = total + int(hands_bids[1]) * (rank + 1)

    return total


INPUT_S = '''\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
'''
EXPECTED = 6440


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
