from numpy import array
import aoc
import numpy as np

data = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""

data = aoc.load_data(False, data, "7", True)

rows = [r.split(": ") for r in data]
rows = [(int(r[0]), np.array([int(x) for x in r[1].split(" ")])) for r in rows]


def ret_feasible(res, lhs, rhs):
    ret = lhs + rhs
    ret = ret[ret <= res]

    ret_p = lhs * rhs
    ret_p = ret_p[ret_p <= res]

    ret_c = lhs * (10 ** np.ceil(np.log10(rhs + 1))) + rhs
    ret_c = ret_c[ret_c <= res]

    res = np.hstack((ret, ret_p, ret_c))
    return res


def check_row(row):
    res, numbers = row
    n = numbers[0]
    for nn in numbers[1:]:
        n = ret_feasible(res, n, nn)
    return res if any(n == res) else 0


print(sum(check_row(r) for r in rows))
