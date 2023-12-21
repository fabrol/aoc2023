from collections import defaultdict
from enum import Enum, IntEnum
from typing import Counter, List, Tuple
import logging
import sys
import functools
import pprint

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


def read_input(filename):
    with open(filename, "r") as f:
        lines = [l.strip() for l in f.readlines()]
        return lines


CARDS_ = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
CARDS = list(reversed(CARDS_))

CARDS_B = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]
CARDS_B = list(reversed(CARDS_B))


@functools.total_ordering
class CARD:
    def __init__(self, name, alt=False) -> None:
        self.name = name
        if alt:
            self.val = CARDS_B.index(self.name)
        else:
            self.val = CARDS.index(self.name)

    def __eq__(self, __value: object) -> bool:
        return self.val == __value.val

    def __lt__(self, other):
        return self.val < other.val

    def __repr__(self) -> str:
        return self.name


class Hands(IntEnum):
    HIGH_C = (1,)
    ONE_P = (2,)
    TWO_P = (3,)
    THREE = (4,)
    FULL_H = (5,)
    FOUR = (6,)
    FIVE = (7,)


def eval_hand_j(hand):
    counts = Counter(hand).most_common()
    for c in counts:
        if c[0] == "J":
            count_j = c
            to_remove = c
    counts.remove(to_remove)
    print(counts, count_j)
    raw_counts = [x[1] for x in counts]

    if 5 in raw_counts:
        hand_type = Hands.FIVE
    elif 4 in raw_counts:
        hand_type = Hands.FIVE
    elif 3 in raw_counts and 2 in raw_counts:
        hand_type = Hands.FULL_H
    elif 3 in raw_counts:
        if count_j[1] == 2:
            hand_type = Hands.FIVE
        elif count_j[1] == 1:
            hand_type = Hands.FOUR
        else:
            hand_type = Hands.THREE
    elif raw_counts.count(2) == 2:
        if count_j[1] == 1:
            # T T J K K
            hand_type = Hands.FULL_H
        else:
            hand_type = Hands.TWO_P
    elif raw_counts.count(2) == 1:
        if count_j[1] == 3:
            hand_type = Hands.FIVE
        elif count_j[1] == 2:
            hand_type = Hands.FOUR
        elif count_j[1] == 1:
            hand_type = Hands.THREE
        else:
            hand_type = Hands.ONE_P
    else:
        if count_j[1] == 5:
            hand_type = Hands.FIVE
        elif count_j[1] == 4:
            hand_type = Hands.FIVE
        elif count_j[1] == 3:
            hand_type = Hands.FOUR
        elif count_j[1] == 2:
            hand_type = Hands.THREE
        elif count_j[1] == 1:
            hand_type = Hands.ONE_P
        else:
            hand_type = Hands.HIGH_C

    return hand_type


def test_eval_hand_j():
    assert eval_hand_j("KTJJT") == Hands.FOUR
    assert eval_hand_j("T55J5") == Hands.FOUR
    assert eval_hand_j("QQQJA") == Hands.FOUR


test_eval_hand_j()


def eval_hand(hand):
    counts = Counter(hand).most_common()
    raw_counts = [x[1] for x in counts]

    if 5 in raw_counts:
        hand_type = Hands.FIVE
    elif 4 in raw_counts:
        hand_type = Hands.FOUR
    elif 3 in raw_counts and 2 in raw_counts:
        hand_type = Hands.FULL_H
    elif 3 in raw_counts:
        hand_type = Hands.THREE
    elif raw_counts.count(2) == 2:
        hand_type = Hands.TWO_P
    elif raw_counts.count(2) == 1:
        hand_type = Hands.ONE_P
    else:
        hand_type = Hands.HIGH_C

    return hand_type


def run_part_a(lines):
    hands = []
    for play in lines:
        hand, bid = play.split(" ")
        hand_type = eval_hand(hand)
        hand_o = [CARD(x) for x in hand]
        hands.append((hand_type, hand_o, bid))

    hands.sort(key=lambda x: (x[0], x[1]))
    pprint.pprint(hands)
    res = 0
    for idx, hand in enumerate(hands, start=1):
        res += int(hand[2]) * idx
    return res


def run_part_b(lines):
    hands = []
    for play in lines:
        hand, bid = play.split(" ")
        if "J" in hand:
            hand_type = eval_hand_j(hand)
        else:
            hand_type = eval_hand(hand)
        hand_o = [CARD(x, alt=True) for x in hand]
        hands.append((hand_type, hand_o, bid))

    hands.sort(key=lambda x: (x[0], x[1]))
    pprint.pprint(hands)
    res = 0
    for idx, hand in enumerate(hands, start=1):
        res += int(hand[2]) * idx
    return res


def test_part_a():
    expected = 6440
    actual = run_part_a(read_input("test7.in"))

    assert actual == expected, f"{actual} and we wanted {expected}"


def test_part_b():
    expected = 5905
    actual = run_part_b(read_input("test7.in"))

    assert actual == expected, f"{actual} and we wanted {expected}"


"""
test_part_a()
print(f"Part A: {run_part_a(read_input('day7.in'))}")
"""
test_part_b()
print(f"Part B: {run_part_b(read_input('day7.in'))}")
