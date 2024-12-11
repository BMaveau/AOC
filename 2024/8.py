import aoc
from aoc.data import Pos

data = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""

data = aoc.load_data(False, data, 8, is_2d=True)

freq = set(data.data) - {"."}

res = set()
for f in freq:
    pos = Pos(0, 0)
    for fa in data.find_iter(f, pos):
        for fb in data.find_iter(f, fa):
            dist = fa - fb
            if fa + dist in data:
                res.add(fa + dist)
            if fb - dist in data:
                res.add(fb - dist)


print(len(res))


# Part 2

res = set()
for f in freq:
    pos = Pos(0, 0)
    for fa in data.find_iter(f, pos):
        for fb in data.find_iter(f, fa):
            dist = aoc.Dir.from_pos(fa - fb)
            res.add(fa)
            an = fa
            while (an := an + dist) in data:
                res.add(an)
            an = fa
            while (an := an - dist) in data:
                res.add(an)

print(len(res))
