from typing import List

file = open("./day5.in").read().strip().split("\n\n")

seeds = [int(x) for x in file[0].replace("seeds: ", "").split(" ")]

# Map format: [[destination_range_start, source_range_start, range_length], ...]
maps = [
    [[int(y) for y in x.split(" ")] for x in file[i].splitlines()[1::]]
    for i in range(1, 8)
]


def x_to_y(step: int, m: List[List[int]]) -> int:
    for destination_range_start, source_range_start, range_length in m:
        if step >= source_range_start and step < source_range_start + range_length:
            step = destination_range_start + (step - source_range_start)
            break

    return step


r = float("inf")

for seed in seeds:
    print(f"{seed}: ", end=", ")
    for m in maps:
        seed = x_to_y(seed, m)
        print(f"{seed} ", end=", ")
    print()
    r = min(r, seed)

print(r)

"""
Seed: 549922357: Location: 86825267
549922357->2599525823->1853542877->378899042->2048586407->2139045340->3786533001->86825267

549922357: 549922357 , 2145280521: , 734811734: , 842454433: , 374993723: , 392296326: , 3510499789: , 
"""
