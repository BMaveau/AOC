from functools import reduce
from itertools import zip_longest
from operator import mul, add
import re
from aoc.data import Pos, load_data


test_inp = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """

data =  load_data(False, test_inp, 6, lines=True)

factors = []
for line in data[:-1]:
    factors.append([int(f) for f in re.findall("[0-9]+", line)])

factors = zip(*factors)

operation = [add if opr == '+' else mul for opr in  re.findall("[*+]", data[-1])]
result = [reduce(opr, operands) for opr, operands in zip(operation, factors)]
print(sum(result))


data =  load_data(False, test_inp, 6, is_2d=True)

opr_cols = []
for pos in data.find_iter('*', Pos(0, 0)):
    opr_cols.append(pos)
for pos in data.find_iter('+', Pos(0, 0)):
    opr_cols.append(pos)
opr_cols.sort(key=lambda pos: pos[0])

cnt = 0
for pos_start, pos_next in zip_longest(opr_cols, opr_cols[1:], fillvalue=Pos(data.size_x+1, 0)):
    factors = [int(''.join(data[i, :-1])) for i in range(pos_next.x - 2, pos_start.x-1, -1)]
    cnt += reduce(add if data[pos_start] == '+' else mul, factors)
print(cnt)

