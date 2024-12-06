from collections import deque
from os import access
from pathlib import Path
from re import findall, finditer
from dataclasses import dataclass
from itertools import accumulate, compress, batched

# data = Path.open("./input6").read()
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

size_x = data.index("\n")
data = data.replace("\n", "")


def rotate_dir(dir):
    if dir == -size_x:
        return 1
    if dir == 1:
        return size_x
    if dir == size_x:
        return -1
    return -size_x


def proceed(map, pos, dir, length):
    new_pos = pos + dir
    if new_pos > len(map) or new_pos < 0:
        return None
    if dir == -1 and new_pos % size_x == size_x - 1:
        return None
    if dir == 1 and new_pos % size_x == 0:
        return None

    if map[new_pos] != "#":
        return new_pos, dir, length + 1
    else:
        return pos, rotate_dir(dir), 0


start = data.index("^")
dir = -size_x
passed_pos = {start}

while (ret := proceed(data, start, dir)) is not None:
    passed_pos.add(ret[0])
    start = ret[0]
    dir = ret[1]

print(len(passed_pos))

data = list(data)
for i in passed_pos:
    data[i] = "X"

print("\n".join("".join(l) for l in batched("".join(data), size_x)))
# print("\n".join("".join(batched(txt, size_x))))


# Part 2
def check_obstacle(data, pos, dir, length):
    ndir = rotate_dir(dir)


start = data.index("^")
dir = -size_x
length = 0

while (ret := proceed(data, start, dir)) is not None:
    start, dir, length = ret
