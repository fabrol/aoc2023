from collections import defaultdict
import math
from typing import Counter, List, Tuple
import logging
import sys

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


def read_input(filename):
    with open(filename, "r") as f:
        lines = [l.strip() for l in f.readlines()]
        return lines


def get_int_solutions(b, c):
    # 4c - b**2
    term = abs(4 * c - b**2)
    lower = ((b - math.sqrt(term)) / 2) + 0.01
    upper = ((b + math.sqrt(term))) / 2 - 0.01
    result = math.floor(upper) - math.ceil(lower) + 1
    logging.debug(f"{b}, {c}: {term}, {lower}, {upper}, {result}")
    return result


def test_get_int_solutions():
    assert get_int_solutions(7, 9) == 4
    assert get_int_solutions(15, 40) == 8
    assert get_int_solutions(30, 200) == 9


test_get_int_solutions()


def run_part_a(lines):
    inputs = [(56, 499), (97, 2210), (77, 1097), (93, 1440)]
    solutions = []
    for time, dist in inputs:
        solutions.append(get_int_solutions(time, dist))
    return math.prod(solutions)


def run_part_b(lines):
    return get_int_solutions(56977793, 499221010971440)


print(f"Part A: {run_part_a(None)}")

print(f"Part B: {run_part_b(None)}")
