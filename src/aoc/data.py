import math as m
from collections import defaultdict
from collections.abc import Callable, MutableMapping
from dataclasses import dataclass
from itertools import batched
from pathlib import Path
from typing import Literal, overload


@overload
def load_data(
    test: bool,
    test_data: str,
    day: int,
    lines: Literal[True] = ...,
    is_2d: Literal[False] = ...,
    grouped_lines: Literal[False] = ...,
) -> list[str]: ...


@overload
def load_data(
    test: bool,
    test_data: str,
    day: int,
    lines: Literal[False] = ...,
    is_2d: Literal[True] = ...,
    grouped_lines: Literal[False] = ...,
) -> "DataMatrix": ...


@overload
def load_data(
    test: bool,
    test_data: str,
    day: int,
    lines: Literal[False] = ...,
    is_2d: Literal[False] = ...,
    grouped_lines: Literal[True] = ...,
) -> list[list[str]]: ...


def load_data(test, test_data, day, lines=False, is_2d=False, grouped_lines=False):
    if test:
        ret = test_data
    else:
        ret = Path(f"./input{day}").read_text()
    if ret[-1] == "\n":
        ret = ret[:-1]
    if lines:
        return ret.split("\n")
    if is_2d:
        return DataMatrix(ret)
    if grouped_lines:
        return [r.split("\n") for r in ret.split("\n\n")]
    return ret


@dataclass(frozen=True)
class Pos:
    x: int
    y: int

    def __post_init__(self):
        object.__setattr__(self, "x", int(self.x))
        object.__setattr__(self, "y", int(self.y))

    def __add__(self, o: "Pos | int"):
        if isinstance(o, int):
            o = Pos(o, o)
        return Pos(self.x + o.x, self.y + o.y)

    def __sub__(self, o: "Pos | int"):
        if isinstance(o, int):
            o = Pos(o, o)
        return Pos(self.x - o.x, self.y - o.y)

    def __getitem__(self, idx):
        if idx == 0 or idx == "x":
            return self.x
        if idx == 1 or idx == "y":
            return self.y

    def __mul__(self, o: int):
        return Pos(self.x * o, self.y * o)

    def __rmul__(self, o: int):
        return self.__mul__(o)

    def __mod__(self, o: "int | Pos | DataMatrix"):
        if isinstance(o, Pos):
            size_x, size_y = o.x, o.y
        elif isinstance(o, DataMatrix):
            size_x, size_y = o.size_x, o.size_y
        else:
            size_x = o
            size_y = o
        return Pos(self.x % size_x, self.y % size_y)

    def __neg__(self):
        return -1 * self

    def __len__(self):
        return 2

    def dist(self, o: "Pos"):
        return abs(self.x - o.x) + abs(self.y - o.y)

    def tuple(self):
        return (self.x, self.y)


@dataclass(frozen=True)
class Dir(Pos):
    @classmethod
    def from_pos(cls, pos: Pos):
        c = m.gcd(pos.x, pos.y)
        return Dir(pos.x // c, pos.y // c)

    def rotate(self, clock: bool = True) -> "Dir":
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


UP = Dir(0, -1)
DOWN = Dir(0, 1)
LEFT = Dir(-1, 0)
RIGHT = Dir(1, 0)
NE = UP + RIGHT
SE = DOWN + RIGHT
SW = DOWN + LEFT
NW = UP + LEFT


class DataMatrix(MutableMapping):
    def __init__(self, data, size_x: int | None = None, size_y: int | None = None):
        self.size_x = data.index("\n") if size_x is None else size_x
        self.size_y = data.count("\n") + 1 if size_y is None else size_y
        if isinstance(data, str):
            self.data = list(data.replace("\n", ""))
        else:
            self.data = data[:]

    def __len__(self) -> int:
        return self.size_x * self.size_y

    def __delitem__(self, key, /) -> None:
        raise NotImplementedError

    def __getitem__(self, idx):
        if isinstance(idx, Pos):
            pos_x = idx[0]
            pos_y = idx[1]
            _idx = pos_x + pos_y * self.size_x
        elif isinstance(idx, tuple):
            return self.get_item_range(*idx)
        else:
            _idx = idx
        if _idx < 0 or _idx >= len(self.data):
            print(idx, _idx, self.size_x, self.size_y, len(self.data))
            raise KeyError()

        return self.data[_idx]

    def get_item_range(self, range_x, range_y):
        if isinstance(range_x, Pos):
            return self[range_x.x, range_y]
        if isinstance(range_y, Pos):
            return self[range_x, range_y.y]
        if isinstance(range_x, slice):
            res = []
            for idx_x in list(range(self.size_x))[range_x]:
                res += list(self[idx_x, range_y])
            return res
        if isinstance(range_y, slice):
            res = []
            for idx_y in list(range(self.size_y))[range_y]:
                res += list(self[range_x, idx_y])
            return res

        return self[Pos(range_x, range_y)]

    def __setitem__(self, idx, o):
        if isinstance(idx, (Pos, tuple)):
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

    def find(self, symbol, pos, dir) -> None | Pos:
        new_pos = pos + dir
        while new_pos != symbol:
            new_pos += dir
            if new_pos not in self:
                return None
        return new_pos

    def find_iter(self, symbol: str, pos: Pos):
        _pos = pos.x + pos.y * self.size_x
        try:
            while True:
                _pos = self.data.index(symbol, _pos + 1)
                yield Pos(_pos % self.size_x, _pos // self.size_x)
        except ValueError:
            pass

    def advance_util(self, spos: Pos, dir: Dir, pred):
        p = spos
        while pred(p):
            p += dir
        return p

    def __contains__(self, pos):
        if isinstance(pos, int):
            return -1 < pos < len(self.data)
        return (-1 < pos.x < self.size_x) and (-1 < pos.y < self.size_y)

    def __repr__(self):
        return "\n".join("".join(l) for l in batched("".join(self.data), self.size_x))

    def __iter__(self):
        for y in range(self.size_y):
            for x in range(self.size_x):
                yield Pos(x, y)

    def replace(self, repl, symbol, inplace: bool = False) -> "DataMatrix":
        if not inplace:
            copy = DataMatrix(self.data, self.size_x, self.size_y)
        else:
            copy = self
        for i in repl:
            copy[i] = symbol
        return copy

    def orthogonal_neighbors(self, pos: Pos) -> list[Pos]:
        directions = [UP, RIGHT, DOWN, LEFT]
        if pos.x == 0:
            directions.remove(LEFT)
        if pos.x == self.size_x - 1:
            directions.remove(RIGHT)
        if pos.y == 0:
            directions.remove(UP)
        if pos.y == self.size_y - 1:
            directions.remove(DOWN)
        return [pos + d for d in directions]

    def diagonal_neighbours(self, pos: Pos) -> list[Pos]:
        directions = {NE, SE, SW, NW}
        if pos.x == 0:
            directions.discard(NW)
            directions.discard(SW)
        if pos.x == self.size_x - 1:
            directions.discard(NE)
            directions.discard(SE)
        if pos.y == 0:
            directions.discard(NE)
            directions.discard(NW)
        if pos.y == self.size_y - 1:
            directions.discard(SE)
            directions.discard(SW)
        return [pos + d for d in directions]

    def neighbors(self, pos) -> list[Pos]:
        neighbors = self.orthogonal_neighbors(pos) + self.diagonal_neighbours(pos)
        if len(neighbors) not in [3, 5, 8]:
            breakpoint()
        return neighbors

    def find_path_dijkstra(
        self,
        start: Pos,
        goal: Pos,
        cost: Callable[["DataMatrix", Pos, Pos], int],
        wall="#",
    ):
        passed_steps: dict[Pos, int] = defaultdict(default_factory=1000000000000)
        passed_steps[start] = 0
        while True:
            el = min(passed_steps.items(), key=lambda k: k[1])
            if el == goal:
                break
            # Get el neighbours
            # Determine cost of going to neighbour from el
            #

            res = cost(self, el)
            for r in res:
                passed_steps[r[0]] = min(r[1])

    # def find_path_astar(
    #     self, start, goal, wall="#", cost=lambda _: 1, ecost=lambda __: 1
    # ):
    #     to_parse = [([start], ecost([start]))]
    #     pdir = [UP, RIGHT, DOWN, LEFT]

    #     while len(to_parse) != 0:
    #         el = min(to_parse, key=lambda k: k[1])
    #         p, pcost = el


#         to_parse.remove(el)
#         for d in pdir:
#             if p[-1] + d not in p and p[-1] + d in self and self[p[-1] + d] != wall:
#                 npath = p + [p[-1] + d]
#                 npath = (npath, pcost + cost(npath) + ecost(npath))
#                 to_parse.append(npath)
#                 if p[-1] + d == goal:
#                     return npath[0], pcost + cost(npath[0])
