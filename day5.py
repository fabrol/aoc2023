from collections import defaultdict
from typing import Counter, List, Tuple
import logging
import sys
import functools

logging.basicConfig(stream=sys.stderr, level=logging.CRITICAL)


def read_input(filename):
    with open(filename, "r") as f:
        lines = [l.strip() for l in f.readlines()]
        return lines


def find_mapping(input_ranges, search) -> int:
    idx = 0
    while idx < len(input_ranges) and search < input_ranges[idx][0][0]:
        idx += 1
    while idx < len(input_ranges) and search >= input_ranges[idx][0][1]:
        idx += 1
    if (
        idx < len(input_ranges)
        and search < input_ranges[idx][0][1]
        and search >= input_ranges[idx][0][0]
    ):
        target = input_ranges[idx][1][0] + (search - input_ranges[idx][0][0])
        return target
    return search


@functools.total_ordering
class Range(object):
    def __init__(self, lower: float, upper: float) -> None:
        self.lower = lower
        self.upper = upper

    def __repr__(self) -> str:
        return f"[{self.lower}, {self.upper})"

    def __eq__(self, __value: object) -> bool:
        return self.lower == __value.lower and self.upper == __value.upper

    def __lt__(self, other):
        return self.lower < other.lower


class Mapping(object):
    def __init__(self, lower, upper, target_lower, target_upper) -> None:
        self.source = Range(lower, upper)
        self.target = Range(target_lower, target_upper)

    def make_default(lower, upper):
        return Mapping(lower, upper, lower, upper)

    def __repr__(self) -> str:
        return f"[{self.source.lower}, {self.source.upper}) -> [{self.target.lower}, {self.target.upper})]"


def list_to_mapping(ranges) -> List[Mapping]:
    return [Mapping(x[0][0], x[0][1], x[1][0], x[1][1]) for x in ranges]


# input: sorted list of pairs of ranges from source to target
def intersect_mappings(
    range_list: List[List[Tuple[float, float]]], target_range: Range
):
    ranges = list_to_mapping(range_list)
    # Fill out the map_ranges to have no gaps
    # Keep going while lower of target is >= upper of range
    # Clipping
    # if target_upper > range_upper:
    #   create a node with [range_upper, target_upper]
    #   map [target_lower, range_upper]
    # else :
    #   map [target_lower, target_upper]

    ranges.insert(0, Mapping.make_default(float("-inf"), ranges[0].source.lower))
    ranges.append(Mapping.make_default(ranges[-1].source.upper, float("inf")))
    new_ranges: List[Mapping] = []
    for idx in range(0, len(ranges) - 1):
        cur = ranges[idx]
        next = ranges[idx + 1]
        new_ranges.append(cur)
        if cur.source.upper < next.source.lower:
            new_ranges.append(Mapping.make_default(cur.source.upper, next.source.lower))
    new_ranges.append(ranges[-1])
    logging.debug(new_ranges)

    results = []
    to_process = [target_range]
    while len(to_process):
        search = to_process.pop()
        logging.debug(f"Processing {search}, with results: {results}")
        idx = 0
        while idx < len(new_ranges) and search.lower >= new_ranges[idx].source.upper:
            idx += 1
        assert idx < len(new_ranges)
        if search.upper > new_ranges[idx].source.upper:
            to_process.append(Range(new_ranges[idx].source.upper, search.upper))
            # map [target_lower, range_upper]
            results.append(
                Range(
                    search.lower
                    if new_ranges[idx].target.lower == float("-inf")
                    else new_ranges[idx].target.lower
                    + (search.lower - new_ranges[idx].source.lower),
                    new_ranges[idx].target.upper,
                )
            )
        else:
            results.append(
                Range(
                    search.lower
                    if new_ranges[idx].target.lower == float("-inf")
                    else new_ranges[idx].target.lower
                    + (search.lower - new_ranges[idx].source.lower),
                    search.upper
                    if new_ranges[idx].target.upper == float("inf")
                    else new_ranges[idx].target.upper
                    - (new_ranges[idx].source.upper - search.upper),
                )
            )

    logging.debug(f"Intersection results: {results}")
    return results


def test_intersect_mapping():
    maps = [
        [(0, 15), (39, 54)],
        [(15, 52), (0, 37)],
        [(52, 54), (37, 39)],
        [(60, 77), (71, 78)],
    ]
    # maps = [[(50, 98), (52, 100)], [(98, 100), (50, 52)]]
    assert intersect_mappings(maps, Range(40, 56)) == [
        Range(25, 37),
        Range(37, 39),
        Range(54, 56),
    ]
    assert intersect_mappings(maps, Range(55, 80)) == [
        Range(55, 60),
        Range(71, 78),
        Range(77, 80),
    ]


# test_intersect_mapping()


def test_mapping():
    maps = [[(0, 15), (39, 54)], [(15, 52), (0, 37)], [(52, 54), (37, 39)]]
    # maps = [[(50, 98), (52, 100)], [(98, 100), (50, 52)]]
    assert find_mapping(maps, 81) == 81
    assert find_mapping(maps, 14) == 53
    assert find_mapping(maps, 57) == 57
    assert find_mapping(maps, 13) == 52

    maps = [[(18, 25), (88, 95)], [(25, 95), (18, 88)]]
    assert find_mapping(maps, 81) == 74


test_mapping()


def process_input(lines):
    seeds = [int(x) for x in lines[0].split(":")[1].strip().split(" ")]
    map_names = {}
    map_ranges = defaultdict(list)

    idx = 2
    while idx < len(lines):
        source, dest = lines[idx].split(" ")[0].split("-to-")
        map_names[source] = dest
        idx += 1
        while idx < len(lines) and lines[idx] != "":
            dst, src, range = [int(x) for x in lines[idx].split(" ")]
            map_ranges[source].append([(src, src + range), (dst, dst + range)])
            idx += 1
        map_ranges[source].sort(key=lambda x: x[0][0])
        idx += 1

    source = "seed"
    ordering = [source]
    while True:
        dest = map_names[source]
        if dest == "location":
            break
        ordering.append(dest)
        source = dest

    for m in map_ranges.items():
        logging.debug(m)
    logging.debug(map_names)
    logging.debug(ordering)
    return (seeds, map_ranges, map_names, ordering)


def run_part_a(lines):
    seeds, map_ranges, map_names, ordering = process_input(lines)

    min_location = None
    for seed in seeds:
        mapping = seed
        mappings = [mapping]
        for source in ordering:
            # logging.debug(f"From {source}:{mapping}", end=" ")
            mapping = find_mapping(map_ranges[source], mapping)
            mappings.append(mapping)
            # logging.debug(f"to {mapping}")
        logging.debug(f"Seed: {seed}: Location: {mapping}")
        logging.debug("->".join([str(m) for m in mappings]))
        min_location = min(min_location, mapping) if min_location else mapping
    return min_location


def run_part_a_2(lines):
    seeds, map_ranges, map_names, ordering = process_input(lines)
    seed_ranges = [Range(s, s + 1) for s in seeds]
    logging.debug(seed_ranges)

    locations = []
    for range in seed_ranges:
        logging.debug(f"starting search for {range}")
        mappings = [range]
        for source in ordering:
            new_mappings = []
            for mapping in mappings:
                logging.debug(f"Looking at {source} for {mapping}")
                new_mappings.extend(intersect_mappings(map_ranges[source], mapping))
            mappings = new_mappings
        locations.append(mappings)
    results = [item for loc in locations for item in loc]
    logging.debug(min(results))
    return min(results).lower


def run_part_b(lines):
    seeds, map_ranges, map_names, ordering = process_input(lines)

    seed_ranges = []
    a = iter(seeds)
    for seed, delta in zip(a, a):
        seed_ranges.append(Range(seed, seed + delta))
    seed_ranges.sort(key=lambda x: x.lower)

    logging.debug(seed_ranges)
    locations = []
    for range in seed_ranges:
        logging.debug(f"starting search for {range}")
        mappings = [range]
        for source in ordering:
            new_mappings = []
            for mapping in mappings:
                logging.debug(f"Looking at {source} for {mapping}")
                new_mappings.extend(intersect_mappings(map_ranges[source], mapping))
            mappings = new_mappings
        locations.append(mappings)
    results = [item for loc in locations for item in loc]
    logging.debug(min(results))
    return min(results).lower


def test_part_a():
    expected = 35
    actual = run_part_a_2(read_input("test5.in"))

    assert actual == expected, f"{actual} and we wanted {expected}"


def test_part_b():
    expected = 46
    actual = run_part_b(read_input("test5.in"))

    assert actual == expected, f"{actual} and we wanted {expected}"


test_part_a()
print(f"Part A: {run_part_a_2(read_input('day5.in'))}")

test_part_b()
print(f"Part B: {run_part_b(read_input('day5.in'))}")
