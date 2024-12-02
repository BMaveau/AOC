from pathlib import Path
from re import match

data = Path.open("./input1a").readlines()
# data = """3   4
# 4   3
# 2   5
# 1   3
# 3   9
# 3   3""".split(
#     "\n"
# )

# Part 1
data_a = [[int(x) for x in match(r"([0-9]+)\s+([0-9]+)", d).groups()] for d in data]

data_a = list(zip(*data_a))
data_a = [sorted(d) for d in data_a]
data_a = [abs(x - y) for x, y in zip(*data_a)]
print(data_a)
print(sum(data_a))

# Part 2
data_b = [[int(x) for x in match(r"([0-9]+)\s+([0-9]+)", d).groups()] for d in data]
data_b = list(zip(*data_b))
data_b = [x * data_b[1].count(x) for x in data_b[0]]
print(sum(data_b))
