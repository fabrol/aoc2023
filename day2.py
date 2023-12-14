from collections import defaultdict
from typing import Counter, List, Tuple
import logging
import sys
import re
import math

rxs = [re.compile("(\d+) red"), re.compile("(\d+) green"), re.compile("(\d+) blue")]

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


def read_input(filename):
    with open(filename, "r") as f:
        lines = [l.strip() for l in f.readlines()]
        return lines


def is_valid(counts: List[int]):
    if counts[0] > 12:
        return False
    if counts[1] > 13:
        return False
    if counts[2] > 14:
        return False
    return True


def run_part_a(lines: List[str]):
    total = 0
    for idx, l in enumerate(lines):
        _, rest_s = l.split(":")
        grabs = rest_s.split(";")
        valid = True
        for grab in grabs:
            matches = [rx.findall(grab) for rx in rxs]
            counts = [int(m[0]) if len(m) else 0 for m in matches]
            valid &= is_valid(counts)
        if valid:
            total += idx + 1
    return total


def run_part_b(lines):
    total = 0
    for idx, l in enumerate(lines):
        mins = [None, None, None]
        _, rest_s = l.split(":")
        grabs = rest_s.split(";")
        for grab in grabs:
            matches = [rx.findall(grab) for rx in rxs]
            counts = [int(m[0]) if len(m) else 0 for m in matches]
            for idx, (m, c) in enumerate(zip(mins, counts)):
                mins[idx] = c if m is None else max(m, c)
        total += math.prod(mins)
    return total


def test_part_a():
    expected = 8
    actual = run_part_a(read_input("test2.in"))

    assert actual == expected, f"{actual} and we wanted {expected}"


def test_part_b():
    expected = 2286
    actual = run_part_b(read_input("test2.in"))

    assert actual == expected, f"{actual} and we wanted {expected}"


test_part_a()
print(f"Part A: {run_part_a(read_input('day2.in'))}")

test_part_b()
print(f"Part B: {run_part_b(read_input('day2.in'))}")
