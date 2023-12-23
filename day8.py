from collections import defaultdict
import math
from typing import Counter, List, Tuple
import logging
import sys
import re

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


def read_input(filename):
    with open(filename, "r") as f:
        lines = [l.strip() for l in f.readlines()]
        return lines


def run_part_a(lines):
    steps = lines[0]

    nodes = {}
    node_r = re.compile(r"(\w+) = \((\w+), (\w+)\)")
    for line in lines[2:]:
        source, left, right = node_r.findall(line)[0]
        nodes[source] = [left, right]

    curr = "AAA"
    idx = 0
    count = 0
    while curr != "ZZZ":
        count += 1
        step = steps[idx]
        if step == "L":
            curr = nodes[curr][0]
        else:
            curr = nodes[curr][1]

        idx += 1
        idx %= len(steps)

    return count


def run_part_b(lines):
    steps = lines[0]

    nodes = {}
    node_r = re.compile(r"(\w+) = \((\w+), (\w+)\)")
    curr = []
    for line in lines[2:]:
        source, left, right = node_r.findall(line)[0]
        nodes[source] = [left, right]
        if source.endswith("A"):
            curr.append(source)

    idx = 0
    count = 0

    found = [None] * len(curr)

    def is_done(positions):
        endswithZ = [p.endswith("Z") for p in positions]
        if any(endswithZ):
            for idx in range(len(curr)):
                if endswithZ[idx]:
                    if not found[idx]:
                        found[idx] = count
            print(f"hit a Z {positions} at {idx} overall {count}")
        if all(found):
            return True
        return False

    while not is_done(curr):
        count += 1
        step = steps[idx]
        if step == "L":
            curr = [nodes[c][0] for c in curr]
        else:
            curr = [nodes[c][1] for c in curr]

        idx += 1
        idx %= len(steps)

    return math.lcm(*found)

    return count


def test_part_a():
    expected = 6
    actual = run_part_a(read_input("test8.in"))

    assert actual == expected, f"{actual} and we wanted {expected}"


def test_part_b():
    expected = 6
    actual = run_part_b(read_input("test8b.in"))

    assert actual == expected, f"{actual} and we wanted {expected}"


test_part_a()
print(f"Part A: {run_part_a(read_input('day8.in'))}")

test_part_b()
print(f"Part B: {run_part_b(read_input('day8.in'))}")
