from itertools import zip_longest
import aoc

test = "2333133121414131402"

data = aoc.load_data(False, test, 9, False, False)
data = [int(d) for d in data]


data = sum(
    [
        [i] * d + [-1] * e
        for i, (d, e) in enumerate(zip_longest(data[::2], data[1::2], fillvalue=0))
    ],
    [],
)

for l in range(len(data) - 1, -1, -1):
    i = data.index(-1)
    if i > l:
        break
    data[i] = data[l]
    data[l] = -1

print(sum(i * (f if f > 0 else 0) for i, f in enumerate(data)))
