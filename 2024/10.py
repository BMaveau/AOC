import aoc
from aoc.data import DataMatrix

test = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""

data: DataMatrix = aoc.load_data(False, test, 10, is_2d=True)

start = aoc.Pos(0, 0)

cnt = 0
pdir = [aoc.Dir(-1, 0), aoc.Dir(1, 0), aoc.Dir(0, -1), aoc.Dir(0, 1)]
for th in data.find_iter("0", start):
    print(th)
    pos = {th}
    for i in "123456789":
        n_pos = set()
        for p in pos:
            for d in pdir:
                if (res := p + d) in data and data[res] == i:
                    n_pos.add(res)
        pos = n_pos
    cnt += len(n_pos)

print(cnt)
