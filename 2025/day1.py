from functools import reduce
import itertools
from pathlib import Path

inp = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"""
inp = inp.split("\n")

inp = Path.open("./input1a.txt").readlines()
pr = [(-1 if val[0] == 'L' else 1 ) *  int(val[1:]) for val in inp]

def rotate_knob(prev, rot):
    res = prev[1] + rot
    st = prev[0]
    return (st + abs(res) // 100 + (res <= 0 and prev[1] != 0), res % 100)

# Answer part 1
print(list(map(lambda knob: knob % 100, itertools.accumulate(pr, initial=50))).count(0))
# Answer part 2
(reduce(rotate_knob, pr, (0, 50)))[0]
