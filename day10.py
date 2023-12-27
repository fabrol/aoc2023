from collections import defaultdict
from typing import Counter, List, Tuple
import logging
import sys
import itertools

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


def read_input(filename):
    with open(filename, "r") as f:
        lines = [l.strip() for l in f.readlines()]
        return lines


OFFSETS_ = [
    (0, 1),
    (1, 0),
    (0, -1),
    (-1, 0),
]


class Position:
    def __init__(self, r, c) -> None:
        self.r = r
        self.c = c

    def __sub__(self, other):
        return Position(self.r - other.r, self.c - other.c)

    def __add__(self, other):
        return Position(self.r + other.r, self.c + other.c)

    def __repr__(self) -> str:
        return f"({self.r}, {self.c})"

    def __eq__(self, __value: object) -> bool:
        return self.r == __value.r and self.c == __value.c

    def __hash__(self) -> int:
        return hash((self.r, self.c))


def get_interesting_neighs(p: Position, graph):
    r_lim = len(graph)
    c_lim = len(graph[0])
    ret_idx = []
    for off in OFFSETS_:
        c_new = p.c + off[0]
        r_new = p.r + off[1]
        if c_new < 0 or c_new >= c_lim or r_new < 0 or r_new >= r_lim:
            continue
        else:
            char = graph[r_new][c_new]
            if char != ".":
                delta: Position = Position(r_new, c_new) - p
                # Check validity based on where you're going
                if char == "|":
                    if delta.c != 0:
                        continue
                elif char == "-":
                    if delta.r != 0:
                        continue
                elif char == "L":
                    if delta.c == 1 or delta.r == -1:
                        continue
                elif char == "7":
                    if delta.c == -1 or delta.r == 1:
                        continue
                elif char == "F":
                    if delta.c == 1 or delta.r == 1:
                        continue
                elif char == "J":
                    if delta.c == -1 or delta.r == -1:
                        continue
                else:
                    raise (f"WTF got {char}")

                ret_idx.append(Position(r_new, c_new))
    return ret_idx


def next_direction(position: Position, from_position: Position, grid):
    char = grid[position.r][position.c]
    delta = position - from_position
    if char == "|" or char == "-":
        new_pos = position + delta
    elif char == "L" or char == "7":
        new_pos = Position(position.r + delta.c, position.c + delta.r)
    elif char == "F" or char == "J":
        new_pos = Position(position.r - delta.c, position.c - delta.r)
    else:
        raise (f"WTF got {char}")
    return new_pos


def print_graph(positions: [Position], grid):
    for p in positions:
        print(f"{p}: {grid[p.r][p.c]}", end=", ")
    print()


def get_loop_length(s_loc: Position, grid):
    # Start a depth first on any direction until you come back to S
    nebs = get_interesting_neighs(s_loc, grid)
    print(s_loc)
    assert len(nebs) == 2

    # Figure out what S would be
    s_sub = None
    nebs_delta = nebs[1] - nebs[0]
    if nebs_delta.r == 0:
        s_sub = "-"
    elif nebs_delta.c == 0:
        s_sub = "|"
    elif nebs_delta.r * nebs_delta.c == -1:
        ns = sorted(nebs, key=lambda n: n.c)
        if ns[1].c > s_loc.c:
            s_sub = "F"
        else:
            s_sub = "J"
    else:
        ns = sorted(nebs, key=lambda n: n.c)
        if ns[1].c > s_loc.c:
            s_sub = "L"
        else:
            s_sub = "7"
    logging.debug(f"With {nebs}, S -> {s_sub}")

    loop = set([s_loc])
    steps = 0
    curr: [Position] = nebs
    prev: [Position] = [s_loc, s_loc]
    loop.update(curr)
    while curr[0] != curr[1]:
        next = [
            next_direction(curr[0], prev[0], grid),
            next_direction(curr[1], prev[1], grid),
        ]
        prev = curr
        curr = next
        loop.update(curr)
        steps += 1
    return loop, steps + 1, s_sub


def run_part_a(lines):
    grid = [list(l) for l in lines]
    s_loc = None  # (r,c)
    for idx, row in enumerate(grid):
        try:
            c = row.index("S")
            s_loc = Position(idx, c)
        except ValueError:
            pass

    _, steps, _ = get_loop_length(s_loc, grid)
    return steps


def run_part_b(lines):
    grid = [list(l) for l in lines]
    s_loc = None  # (r,c)
    for idx, row in enumerate(grid):
        try:
            c = row.index("S")
            s_loc = Position(idx, c)
        except ValueError:
            pass

    loop, _, s_sub = get_loop_length(s_loc, grid)
    grid[s_loc.r][s_loc.c] = s_sub

    # March down the grid one row at a time and mark every point as in or out
    in_loop = set()
    for row_i, row in enumerate(grid):
        intersections = 0
        line_start = None

        for col_i in range(len(row)):
            p = Position(row_i, col_i)
            val = grid[row_i][col_i]

            if p not in loop:
                if intersections % 2 != 0:
                    in_loop.add(p)
                    logging.debug(f"Adding {p} with inter: {intersections}")
            else:
                if val == "|":
                    intersections += 1
                elif val == "-":
                    assert line_start, f"At {p} {val}"
                elif val == "F" or val == "L":
                    assert not line_start, f"At {p} {val}"
                    line_start = val
                elif val == "J":
                    assert line_start, f"At {p} {val}"
                    if line_start == "F":
                        intersections += 1
                    line_start = None
                elif val == "7":
                    assert line_start, f"At {p} {val}"
                    if line_start == "L":
                        intersections += 1
                    line_start = None

    logging.debug(str(in_loop))

    return len(in_loop)


def test_part_a():
    expected = 8
    actual = run_part_a(read_input("test10.in"))

    assert actual == expected, f"{actual} and we wanted {expected}"


def test_part_b():
    expected = 4
    actual = run_part_b(read_input("test10b.in"))
    assert actual == expected, f"{actual} and we wanted {expected}"

    logging.debug("Starting 10b2")
    expected = 8
    actual = run_part_b(read_input("test10b2.in"))
    assert actual == expected, f"{actual} and we wanted {expected}"

    logging.debug("Starting 10b1")
    expected = 10
    actual = run_part_b(read_input("test10b1.in"))
    assert actual == expected, f"{actual} and we wanted {expected}"


test_part_a()
print(f"Part A: {run_part_a(read_input('day10.in'))}")

test_part_b()
print(f"Part B: {run_part_b(read_input('day10.in'))}")

"""
F, L, - -> you're on the line
J, 7 -> you're leaving the line
| -> always a crossing

Have to hit an F or L or S first from left
if F--J cross, F--7 no cross
if L--7 cross, L--J no cross
"""
