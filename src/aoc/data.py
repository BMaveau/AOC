from dataclasses import dataclass
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


@dataclass
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


@dataclass
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

    def __init__(self, data):
        self.size_x = data.index("\n")
        self.data = data.replace("\n", "")

    def __getitem__(self, idx):
        if isinstance(idx, Pos):
            pos_x = idx[0]
            pos_y = idx[1]
            idx = pos_x + pos_y * self.size_x
        if isinstance(idx, str):
            pos = self.data.index(idx)
            return Pos(x=pos % self.size_x, y=pos // self.size_x)
        return self.data[idx]

    def __contains__(self, pos):
        if not isinstance(pos, int):
            return -1 < pos < len(self.data)
