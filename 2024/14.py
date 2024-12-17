from collections import defaultdict
import aoc
import re

from aoc.data import DataMatrix, Dir, Pos

test = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""

data = aoc.load_data(False, test, 14, lines=True)

robots = [
    re.match(r"p=([0-9]+),([0-9]+) v=(-?[0-9]+),(-?[0-9]+)", d).groups() for d in data
]

pos, dirs = zip(*[(Pos(r[0], r[1]), Dir(r[2], r[3])) for r in robots])

size_x = 101
size_y = 103
bath = DataMatrix(["."] * size_x * size_y, size_x, size_y)

npos = [(p + 100 * d) % bath for p, d in zip(pos, dirs)]

res = [0, 0, 0, 0]
for p in npos:
    if p.x < size_x // 2 and p.y < size_y // 2:
        res[0] += 1
    if p.x > size_x // 2 and p.y < size_y // 2:
        res[1] += 1
    if p.x < size_x // 2 and p.y > size_y // 2:
        res[2] += 1
    if p.x > size_x // 2 and p.y > size_y // 2:
        res[3] += 1

print(res[0] * res[1] * res[2] * res[3])

# part 2

for i in range(10000):
    npos = [(p + i * d) % bath for p, d in zip(pos, dirs)]
    if len(set(npos)) == 500:
        print(bath.replace(npos, "r"))
        print(i)
        break
