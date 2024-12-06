from dataclasses import dataclass
from itertools import batched
from pathlib import Path


def load_data(test, test_data, day, lines=False, is_2d=False):
    if test:
        ret = test_data
    else:
        ret = Path.open(f"./input{day}").read()
    if lines:
        ret.split("")
    if lines:
        return ret.split("\n")
    if is_2d:
        return DataMatrix(ret)
    return ret


@dataclass(frozen=True)
class Pos:
    x: int
    y: int

    def __add__(self, o: "Pos"):
        return Pos(self.x + o.x, self.y + o.y)

    def __getitem__(self, idx):
        if idx == 0 or idx == "x":
            return self.x
        if idx == 1 or idx == "y":
            return self.y

    def __mul__(self, o: int):
        return Pos(self.x * o, self.y * o)


@dataclass(frozen=True)
class Dir(Pos):

    def rotate(self, clock: bool = True):
        ret = None
        if self.y == -1:
            ret = Dir(1, 0)
        elif self.x == 1:
            ret = Dir(0, 1)
        elif self.y == 1:
            ret = Dir(-1, 0)
        else:
            ret = Dir(0, -1)
        return ret if clock else ret * -1


class DataMatrix:

    def __init__(self, data, size_x: int | None = None, size_y: int | None = None):
        self.size_x = data.index("\n") if size_x is None else size_x
        self.size_y = data.count("\n") + 1 if size_y is None else size_y
        if isinstance(data, str):
            self.data = list(data.replace("\n", ""))
        else:
            self.data = data

    def __getitem__(self, idx):
        if isinstance(idx, Pos):
            pos_x = idx[0]
            pos_y = idx[1]
            idx = pos_x + pos_y * self.size_x
        return self.data[idx]

    def __setitem__(self, idx, o):
        if isinstance(idx, Pos):
            pos_x = idx[0]
            pos_y = idx[1]
            idx = pos_x + pos_y * self.size_x
        self.data[idx] = o

    def index(self, o) -> None | Pos:
        try:
            pos = self.data.index(o)
        except:
            return None
        return Pos(pos % self.size_x, pos // self.size_x)

    def __contains__(self, pos):
        if isinstance(pos, int):
            return -1 < pos < len(self.data)
        return (-1 < pos.x < self.size_x) and (-1 < pos.y < self.size_y)

    def __repr__(self):
        return "\n".join("".join(l) for l in batched("".join(self.data), self.size_x))

    def replace(self, repl, symbol) -> "DataMatrix":
        copy = DataMatrix(self.data, self.size_x, self.size_y)
        for i in repl:
            copy[i] = symbol
        return copy
