from collections import defaultdict
from types import FunctionType
from typing import Counter, List, Set, Tuple
import logging
import sys
import numpy as np

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


def get_neighbor_indices(r, c, graph):
    r_lim = len(graph)
    c_lim = len(graph[0])
    ret_idx = []
    for off in OFFSETS_:
        c_new = c + off[0]
        r_new = r + off[1]
        if c_new < 0 or c_new >= c_lim or r_new < 0 or r_new >= r_lim:
            continue
        else:
            ret_idx.append((r_new, c_new))
    return ret_idx


def flip_grid(grid):
    grid_new = [[r[c] for r in grid] for c in range(len(grid[0]))]
    return grid_new


def find_all_shortest_paths(grid, source, targets: Set, get_distance):
    print(f"Starting search from {source} with {targets}")
    targets_copy = targets.copy()
    frontier = [source]
    distance = {}
    distance[source] = 0

    while len(frontier) and len(targets):
        curr = frontier.pop(0)
        if curr in targets:
            targets.remove(curr)
        for neb in get_neighbor_indices(curr[0], curr[1], grid):
            if neb not in distance:
                distance[neb] = get_distance(neb, curr) + distance[curr]
                frontier.append(neb)

    results = {}
    for target in targets_copy:
        print(f"{target} : {distance[target]}")
        results[target] = distance[target]

    return results


def find_all_stars_shortest(lines, expansion):
    grid = [list(l) for l in lines]

    # Find rows,cols to duplicate
    grid_row_dupl = set()
    for row_i, row in enumerate(grid):
        if not "#" in row:
            grid_row_dupl.add(row_i)
    grid_col_dupl = set()
    for row_i, row in enumerate(flip_grid(grid)):
        if not "#" in row:
            grid_col_dupl.add(row_i)

    #  Even though expansion is downwards, this needs to be aware of coming from or going into
    # a row with expansion
    def step_distance(source, to):
        delta_r = to[0] - source[0]
        delta_c = to[1] - source[1]

        if to[0] in grid_row_dupl and delta_r != 0:
            return expansion
        elif to[1] in grid_col_dupl and delta_c != 0:
            return expansion
        else:
            return 1

    # Find all star locations
    stars = set()
    for row_i, row in enumerate(grid):
        if "#" in row:
            stars.update([(row_i, col_i) for col_i, v in enumerate(row) if v == "#"])
    print(stars)

    # All pairs shortest path -> only once per pair
    pairs_to_dist = {}  # tuple (sorted(a,b)) -> dist
    for star in stars:
        rest = stars.difference([star])
        to_target = set()
        for target in rest:
            if tuple(sorted([target, star])) not in pairs_to_dist:
                to_target.add(target)

        results = find_all_shortest_paths(grid, star, to_target, step_distance)
        for target in results:
            pairs_to_dist[tuple(sorted([target, star]))] = results[target]

    print(pairs_to_dist)
    return sum(pairs_to_dist.values())


def run_part_a(lines):
    return find_all_stars_shortest(lines, 2)


def run_part_b(lines, expansion=10**6):
    return find_all_stars_shortest(lines, expansion)


def test_part_a():
    expected = 374
    actual = run_part_b(read_input("test11.in"), expansion=2)

    assert actual == expected, f"{actual} and we wanted {expected}"


def test_part_b():
    expected = 1030
    actual = run_part_b(read_input("test11.in"), expansion=10)
    assert actual == expected, f"{actual} and we wanted {expected}"

    expected = 8410
    actual = run_part_b(read_input("test11.in"), expansion=100)
    assert actual == expected, f"{actual} and we wanted {expected}"


test_part_a()
print(f"Part A: {run_part_a(read_input('day11.in'))}")

test_part_b()
print(f"Part B: {run_part_b(read_input('day11.in'))}")
