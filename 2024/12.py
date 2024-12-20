import aoc
from aoc.data import DataMatrix, Dir, Pos
from collections import deque

test = """AAAA
BBCD
BBCC
EEEC
"""

data: DataMatrix = aoc.load_data(False, test, 12, is_2d=True)

parsed_regions = set()


def find_region(pos: Pos):
    pdir = [aoc.Dir(-1, 0), aoc.Dir(1, 0), aoc.Dir(0, -1), aoc.Dir(0, 1)]
    to_check = deque()
    to_check.append(pos)
    symbol = data[pos]
    area = 0
    border = 0
    parsed = set()
    while len(to_check) != 0:
        area += 1
        n = to_check.pop()
        for d in pdir:
            if n + d in data:
                if data[n + d] == symbol:
                    if n + d not in parsed and n + d not in to_check:
                        to_check.append(n + d)
                else:
                    border += 1
            else:
                border += 1
        parsed.add(n)
    return area, border, parsed


gl_parsed = set()
cnt = 0
for i in data:
    if i not in gl_parsed:
        area, border, parsed = find_region(i)
        cnt += area * border
    gl_parsed.update(parsed)
print(cnt)


def find_region_b(pos: Pos):
    pdir = [aoc.Dir(-1, 0), aoc.Dir(1, 0), aoc.Dir(0, -1), aoc.Dir(0, 1)]
    to_check = deque()
    to_check.append(pos)
    symbol = data[pos]
    area = 0
    border = 0
    parsed = set()
    borders = {p: [] for p in pdir}
    while len(to_check) != 0:
        area += 1
        n = to_check.pop()
        for d in pdir:
            if n + d in data:
                if data[n + d] == symbol:
                    if n + d not in parsed and n + d not in to_check:
                        to_check.append(n + d)
                else:
                    borders[d.rotate()].append(n)
            else:
                borders[d.rotate()].append(n)
                border += 1
        parsed.add(n)
    return area, parsed, borders


def parse_borders(borders: dict[Dir, list[Pos]]):
    sides = 0
    for d, lp in borders.items():
        while len(lp) != 0:
            p = lp[0]
            i = 1
            while p + d * i in lp:
                lp.remove(p + d * i)
                i += 1
            i = 1
            while p - d * i in lp:
                lp.remove(p - d * i)
                i += 1
            lp.remove(p)
            sides += 1
    return sides


gl_parsed = set()
cnt = 0
for i in data:
    if i not in gl_parsed:
        area, parsed, borders = find_region_b(i)
        sides = parse_borders(borders)
        cnt += area * sides
    gl_parsed.update(parsed)
print(cnt)
