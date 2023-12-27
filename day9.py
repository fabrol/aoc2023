from collections import defaultdict
from typing import Counter, List, Tuple
import logging
import sys
import numpy as np

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


def read_input(filename):
    with open(filename, "r") as f:
        lines = [l.strip() for l in f.readlines()]
        return lines


def run_part_a(lines):
    result = 0
    for line in lines:
        seq = np.array([int(x) for x in line.strip().split(" ")])
        seqs = [seq]
        while seq.any():
            delta = np.diff(seq)
            seqs.append(delta)
            seq = delta.copy()
        seqs = list(reversed(seqs))
        assert seqs[0][-1] == 0
        seqs[0] = np.append(seqs[0], 0)
        for idx in range(1, len(seqs)):
            seqs[idx] = np.append(seqs[idx], seqs[idx][-1] + seqs[idx - 1][-1])
        result += seqs[-1][-1]
    return result


def run_part_b(lines):
    result = 0
    for line in lines:
        seq = np.array([int(x) for x in line.strip().split(" ")])
        seqs = [seq]
        while seq.any():
            delta = np.diff(seq)
            seqs.append(delta)
            seq = delta.copy()
        seqs = list(reversed(seqs))
        assert seqs[0][-1] == 0
        assert seqs[0][0] == 0

        seqs[0] = np.append(seqs[0], [0, 0])
        for idx in range(1, len(seqs)):
            seqs[idx] = np.append(seqs[idx], seqs[idx][-1] + seqs[idx - 1][-1])
            seqs[idx] = np.append(seqs[idx][0] - seqs[idx - 1][0], seqs[idx])
        result += seqs[-1][0]
    return result


def test_part_a():
    expected = 114
    actual = run_part_a(read_input("test9.in"))

    assert actual == expected, f"{actual} and we wanted {expected}"


def test_part_b():
    expected = 2
    actual = run_part_b(read_input("test9.in"))

    assert actual == expected, f"{actual} and we wanted {expected}"


test_part_a()
print(f"Part A: {run_part_a(read_input('day9.in'))}")

test_part_b()
print(f"Part B: {run_part_b(read_input('day9.in'))}")
