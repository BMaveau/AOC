from itertools import combinations

from aoc.data import load_data

test_input = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""


def area(c1, c2):
    return (abs(c2[1] - c1[1]) + 1) * (abs(c2[0] - c1[0]) + 1)


data = load_data(False, test_input, 9, lines=True)
corners = [[int(n) for n in l.split(",")] for l in data]
areas = [area(c1, c2) for c1, c2 in combinations(corners, 2)]
print(max(areas))
