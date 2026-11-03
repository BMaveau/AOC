from collections import deque

import numpy as np
from aoc.data import DOWN, SE, SW, DataMatrix, Pos, load_data

test_inp = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
"""

# Start at the bottom
# Move up
# if diagonal up is ^, put +1 on that cell


def find_trajectory(world, other_worlds):
    (start_y, data) = world
    for y in range(start_y, data.size_y - 1):
        for x in range(data.size_x):
            if data[x, y] != "|":
                continue
            if data[x, y + 1] == "^":
                other_worlds.append((y + 1, data.replace([(x + 1, y + 1)], "|")))
                data[x - 1, y + 1] = "|"
                continue
            data[x, y + 1] = "|"
    return world


def parse_world(data: DataMatrix):
    beams = np.zeros((data.size_x, data.size_y))
    beams[data.index("|").tuple()] = 1
    while pos := data.index("|"):
        parse_beam(data, beams, pos)
        data[pos] = "."

    print(beams)
    print(sum(beams[:, -1]))


def parse_beam(data: DataMatrix, beams, pos: Pos):
    own_worlds = beams[pos.tuple()]
    if pos + DOWN not in data:
        return
    if data[pos + DOWN] == "." or data[pos + DOWN] == "|":
        beams[(pos + DOWN).tuple()] += own_worlds
        data[pos + DOWN] = "|"
    elif data[pos + DOWN] == "^":
        if pos + SW in data:
            beams[(pos + SW).tuple()] += own_worlds
            data[pos + SW] = "|"
        if pos + SE in data:
            beams[(pos + SE).tuple()] += own_worlds
            data[pos + SE] = "|"
    else:
        print("Unknown symbol")


data = load_data(False, test_inp, 7, is_2d=True)
data.replace([data.index("S")], "|", inplace=True)
parse_world(data)

# worlds = deque()
# worlds.append((0, data))

# cnt = 0
# while len(worlds):
#     world = find_trajectory(worlds.pop(), worlds)
#     cnt += 1
# print(cnt)
