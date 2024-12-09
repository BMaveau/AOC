from collections import deque
from os import access, stat
from pathlib import Path
from re import findall, finditer
from dataclasses import dataclass
from itertools import accumulate, compress, batched
from aoc import load_data
from aoc.data import DataMatrix, Dir, Pos

data = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""

data = load_data(False, data, "6", is_2d=True)


def proceed(map: DataMatrix, pos: Pos, dir: Dir):
    new_pos = pos + dir
    if new_pos not in map:
        return None

    if map[new_pos] != "#":
        return new_pos, dir
    else:
        return pos, dir.rotate()


start = data.index("^")
dir = Dir(0, -1)
passed_pos = {start}

while (ret := proceed(data, start, dir)) is not None:
    passed_pos.add(ret[0])
    start = ret[0]
    dir = ret[1]

print(len(passed_pos))
print(data.replace(passed_pos, "X"))

# Part 2


def check_in_loop(data: DataMatrix):
    start = data.index("^")
    if start is None:
        return 0
    dir = Dir(0, -1)
    passed = set()

    while (ret := proceed(data, start, dir)) is not None:
        if ret in passed:
            return 1
        passed.add(ret)
        start = ret[0]
        dir = ret[1]
    return 0


cnt = 0
for i in passed_pos:
    copy = data.replace([i], "#")

    cnt += check_in_loop(copy)
print(cnt)


def check_feasible(data: DataMatrix, pos: Pos, dir: Dir, length: int):
    if data.index(pos + dir) == ".":
        next_pos = data.find("#", pos, dir.rotate())
        if next_pos is None:
            return False
        y = next_pos.dist(pos)
        corner_a = next_pos - dir.rotate()
        corner_b = corner_a - dir * (length + 1)
        if data[corner_b] != "#":
            return False
        corner_c = pos - dir * length - dir.rotate(clock=False)
        if data[corner_c] != "#":
            return False
