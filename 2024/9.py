from itertools import zip_longest
import aoc

test = "2333133121414131402"

data = aoc.load_data(True, test, 9, False, False)
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

# Part 2

data = aoc.load_data(False, test, 9, False, False)
data = [int(d) for d in data]
files = [[i] * d for i, d in enumerate(data[::2])]
empty = [[-1] * d for d in data[1::2]]

i = len(files) - 1
while i > 0:
    for idx, e in enumerate(empty):
        if len(files[i]) <= len(e) and idx < i:
            break
    else:
        i -= 1
        continue

    empty.insert(idx, [])
    empty[idx + 1] = empty[idx + 1][: len(empty[idx + 1]) - len(files[i])]
    files.insert(idx + 1, files[i])
    if i + 1 < len(empty):
        empty[i] += empty[i + 1] + [-1] * len(files[i + 1])
        del empty[i + 1]
    del files[i + 1]


data = sum([f + e for f, e in zip(files, empty)], [])
print(sum(i * (f if f > 0 else 0) for i, f in enumerate(data)))
