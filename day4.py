from collections import defaultdict
from typing import Counter, List, Tuple
import logging
import sys
import re

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

nums = re.compile("(\d+)")


def read_input(filename):
    with open(filename, "r") as f:
        lines = [l.strip() for l in f.readlines()]
        return lines


def run_part_a(lines):
    total = 0
    for idx, l in enumerate(lines):
        winners, ours = l.split(":")[1].split("|")
        winners = set(nums.findall(winners))
        ours = set(nums.findall(ours))

        wins = len(ours.intersection(winners))
        total += 2 ** (wins - 1) if wins else 0
        # print(winners, ours, wins, total)
    return total


def run_part_b(lines):
    card_counts = defaultdict(int)
    card_points = {}

    for idx, l in enumerate(lines):
        winners, ours = l.split(":")[1].split("|")
        winners = set(nums.findall(winners))
        ours = set(nums.findall(ours))

        wins = len(ours.intersection(winners))
        card_counts[idx] += 1
        my_count = card_counts[idx]
        for i in range(1, wins + 1):
            card_counts[idx + i] += my_count
        print(wins, card_counts)

    return sum(card_counts.values())


def test_part_a():
    expected = 13
    actual = run_part_a(read_input("test4.in"))

    assert actual == expected, f"{actual} and we wanted {expected}"


def test_part_b():
    expected = 30
    actual = run_part_b(read_input("test4.in"))

    assert actual == expected, f"{actual} and we wanted {expected}"


test_part_a()
print(f"Part A: {run_part_a(read_input('day4.in'))}")

test_part_b()
print(f"Part B: {run_part_b(read_input('day4.in'))}")
