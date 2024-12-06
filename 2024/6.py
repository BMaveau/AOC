from collections import deque
from os import access
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

data = load_data(True, data, "6", is_2d=True)


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
