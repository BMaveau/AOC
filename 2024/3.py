from pathlib import Path
from re import findall

data = Path.open("./input3").read()
# data = """xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"""

# Part 1
sum([int(x) * int(y) for (x, y) in findall(r"mul\(([0-9]+),([0-9]+)\)", data)])

# Part 2

data = data.split("don't()")
data = "".join([data[0]] + ["".join(d.split("do()")[1:]) for d in data[1:]])

sum([int(x) * int(y) for (x, y) in findall(r"mul\(([0-9]+),([0-9]+)\)", data)])
