from itertools import product
from aoc.data import Dir, Pos, load_data

test_inp = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""

dir = [Dir(x, y) for x, y in product(range(-1, 2),  repeat=2)]
data = load_data(False, test_inp, 4, is_2d=True)
cnt = 0
accesible = [None]
while len(accesible) != 0:
    accesible = []
    for pos in data.find_iter('@', Pos(-1, 0)):
        pos_neighbors = data.neighbors(pos)
        neighbours = [data[p]  for p in pos_neighbors]

        if neighbours.count('@') < 4:
            accesible.append(pos)
    cnt += len(accesible)
    data.replace(accesible, 'x', inplace=True)
print(cnt)



