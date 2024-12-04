from collections import deque
from os import access
from pathlib import Path
from re import findall, finditer
from dataclasses import dataclass
from itertools import accumulate, compress, batched

data = Path.open("./input4").read()
# data = """MMMSXXMASM
# MSAMXMSMSA
# AMXSXMAAMM
# MSAMASMSMX
# XMASAMXAMM
# XXAMMXXAMA
# SMSMSASXSS
# SAXAMASAAA
# MAMMMXMMMM
# MXMXAXMASX
# """

size_x = data.index("\n")
data = data.replace("\n", "")


@dataclass
class Search:
    x: int = -1
    m: int = -1
    a: int = -1
    s: int = -1

    @classmethod
    def _search_all(cls, letter, pos):
        res = []
        if pos > size_x:
            if data[pos - size_x] == letter:
                yield pos - size_x
            if pos % size_x > 0 and data[pos - size_x - 1] == letter:
                yield pos - size_x - 1
            if pos % size_x < size_x - 1 and data[pos - size_x + 1] == letter:
                yield pos - size_x + 1
        if data[pos] == letter:
            yield pos
        if pos % size_x > 0 and data[pos - 1] == letter:
            yield pos - 1
        if pos % size_x < size_x - 1 and data[pos + 1] == letter:
            yield pos + 1
        if pos + size_x < len(data):
            if data[pos + size_x] == letter:
                yield pos - size_x
            if pos % size_x > 0 and data[pos + size_x - 1] == letter:
                yield pos + size_x - 1
            if pos % size_x < size_x - 1 and data[pos + size_x + 1] == letter:
                yield pos + size_x + 1

    def search(self):
        if self.m == -1:
            next_letter = "m"
            pos = self.x
            fpos = [pos for pos in self._search(next_letter, pos)]

        if self.m == -1:
            return [Search(x=self.x, m=p) for p in fpos]
        elif self.a == -1:
            return [Search(x=self.x, m=self.m, a=p) for p in fpos]
        else:
            return [Search(x=self.x, m=self.m, a=self.a, s=p) for p in fpos]


def gen_dir(pos_x):
    steps = [-size_x, size_x]
    if pos_x % size_x > 2:
        steps += [-size_x - 1, -1, size_x - 1]
    if pos_x % size_x < size_x - 3:
        steps += [-size_x + 1, 1, size_x + 1]

    for step in steps:
        pos = [pos_x] + [step for _ in range(3)]
        pos = list(accumulate(pos))
        if all(p > 0 for p in pos) and all(p < len(data) for p in pos):
            yield "".join([data[p] for p in pos]), pos


cnt = 0
res = []
for pos_x in [m.start() for m in finditer("X", data)]:
    for text, pos in gen_dir(pos_x):
        if text == "XMAS":
            cnt += 1
            res.extend(pos)
print(cnt)
# txt = []
# for i, c in enumerate(data):
#     if i in res:
#         txt += [c]
#     else:
#         txt += ["."]

# print("\n".join("".join(l) for l in batched("".join(txt), size_x)))
# print(cnt)

# print("\n".join("".join(batched(txt, size_x))))


# Part 2
def gen_dir_2(pos_x):
    if pos_x % size_x == 0:
        return ([], [])
    if pos_x % size_x == size_x - 1:
        return ([], [])
    if pos_x < size_x:
        return ([], [])
    if pos_x + size_x > len(data):
        return ([], [])

    return [data[pos_x - size_x - 1], data[pos_x + size_x + 1]], [
        data[pos_x - size_x + 1],
        data[pos_x + size_x - 1],
    ]


cnt = 0
for pos_x in [m.start() for m in finditer("A", data)]:
    text_1, text_2 = gen_dir_2(pos_x)
    if ("M" in text_1 and "S" in text_1) and ("M" in text_2 and "S" in text_2):
        cnt += 1

print(cnt)
