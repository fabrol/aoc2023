from collections import defaultdict
from typing import Counter, List, Tuple, Dict
import logging
import sys

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


def read_input(filename):
    with open(filename, "r") as f:
        lines = [l.strip() for l in f.readlines()]
        return lines


def run_part_a(lines: List[str]):
    total = 0
    for l in lines:
        result = ""
        for val in l:
            if val.isnumeric():
                result += val
                break
        for val in l[::-1]:
            if val.isnumeric():
                result += val
                break
        total += int(result)
    return total


digits_f = sorted(
    [
        ("one", "1"),
        ("two", "2"),
        ("three", "3"),
        ("four", "4"),
        ("five", "5"),
        ("six", "6"),
        ("seven", "7"),
        ("eight", "8"),
        ("nine", "9"),
    ],
    key=lambda x: len(x[0]),
    reverse=True,
)
digits_r = [(str(x[0][::-1]), x[1]) for x in digits_f]


def find_first_digit(l: str, digits: Dict[str, str]) -> str:
    result = ""
    indices_f = [(d[1], l.find(d[0])) for d in digits if l.find(d[0]) != -1]
    indices_f = sorted(indices_f, key=lambda x: x[1])
    lowest_text = indices_f[0] if len(indices_f) else None

    for idx, val in enumerate(l):
        if val.isnumeric():
            if not lowest_text:
                result += val
                break

            if idx < lowest_text[1]:
                result += val
            else:
                result += lowest_text[0]
            break
    if not len(result):
        result += lowest_text[0]
    return result


def run_part_b(lines: List[str]):
    total = 0
    for l in lines:
        result = ""

        digit_1 = find_first_digit(l, digits_f)
        digit_2 = find_first_digit(l[::-1], digits_r)

        result = digit_1 + digit_2
        total += int(result)
    return total


def test_part_a():
    expected = 142
    actual = run_part_a(read_input("test1.in"))

    assert actual == expected, f"{actual} and we wanted {expected}"


def test_part_b():
    expected = 281
    actual = run_part_b(read_input("test1b.in"))

    assert actual == expected, f"{actual} and we wanted {expected}"


test_part_a()
print(f"Part A: {run_part_a(read_input('day1.in'))}")

test_part_b()
print(f"Part B: {run_part_b(read_input('day1.in'))}")
