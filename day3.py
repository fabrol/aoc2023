from collections import defaultdict
import re
from typing import Counter, List, Tuple, Match
import logging
import sys

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


def read_input(filename):
    with open(filename, "r") as f:
        lines = [l.strip() for l in f.readlines()]
        return lines


nums = re.compile("(\d+)")

OFFSETS_ = [
    (0, 1),
    (1, 1),
    (1, 0),
    (1, -1),
    (0, -1),
    (-1, -1),
    (-1, 0),
    (-1, 1),
]


def get_neighbor_indices(x, y, graph):
    y_lim = len(graph)
    x_lim = len(graph[0])
    ret_idx = []
    for off in OFFSETS_:
        x_new = x + off[0]
        y_new = y + off[1]
        if x_new < 0 or x_new >= x_lim or y_new < 0 or y_new >= y_lim:
            continue
        else:
            ret_idx.append((x_new, y_new))
    return ret_idx


def is_part(row_i, col_i, grid):
    indices = get_neighbor_indices(row_i, col_i, grid)
    symbols = [grid[i[0]][i[1]] for i in indices]
    is_part = [not (s.isdigit() or s == ".") for s in symbols]
    # print(indices, symbols, is_part)
    return any(is_part)


def run_part_a(lines):
    total = 0
    grid = [list(l) for l in lines]
    for row_i, row in enumerate(lines):
        for m in nums.finditer(row):
            # print(m.start(), m.end(), int(m.group()))
            for col_i in range(m.start(), m.end()):
                if is_part(row_i, col_i, grid):
                    total += int(m.group())
                    # print(f"Adding {m.group()}")
                    break

    return total


GEARS = defaultdict(list)


def check_gear(row_i, col_i, grid, part_num):
    global GEARS
    indices = get_neighbor_indices(row_i, col_i, grid)
    symbols = [grid[i[0]][i[1]] for i in indices]
    for idx, s in enumerate(symbols):
        if s == "*":
            GEARS[indices[idx]].append(part_num)
            return True

    return False


def run_part_b(lines):
    global GEARS
    GEARS.clear()
    grid = [list(l) for l in lines]
    for row_i, row in enumerate(lines):
        for m in nums.finditer(row):
            # print(m.start(), m.end(), int(m.group()))
            for col_i in range(m.start(), m.end()):
                if check_gear(row_i, col_i, grid, int(m.group())):
                    # print(f"Adding {m.group()}")
                    break

    total = 0
    for k, v in GEARS.items():
        if len(v) == 2:
            total += v[0] * v[1]
    return total


def test_part_a():
    expected = 4361
    actual = run_part_a(read_input("test3.in"))

    assert actual == expected, f"{actual} and we wanted {expected}"


def test_part_b():
    expected = 467835
    actual = run_part_b(read_input("test3.in"))

    assert actual == expected, f"{actual} and we wanted {expected}"


test_part_a()
print(f"Part A: {run_part_a(read_input('day3.in'))}")

test_part_b()
print(f"Part B: {run_part_b(read_input('day3.in'))}")
