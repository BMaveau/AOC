from functools import reduce
from aoc.data import load_data


test_inp = """3-5
10-14
16-20
12-18

1
5
8
11
17
32
"""

data = load_data(False, test_inp, 5, grouped_lines=True)

def get_fresh(id_range):
    start, end = id_range.split("-")
    return int(start), int(end)

def is_fresh(id, id_ranges):
    return any(start <= id <= end for start, end in id_ranges)



id_ranges = [get_fresh(id_range) for id_range in data[0]]
cnt = 0
for str_id in data[1]:
    if is_fresh(int(str_id), id_ranges):
        cnt += 1
print(cnt)

reduced_ranges = []
id_ranges = sorted(id_ranges, key=lambda id_range: id_range[0])
for start, end in id_ranges:
    for i, (ex_start, ex_end) in enumerate(reduced_ranges):
        adapted = False
        if ex_start <= start <= ex_end and end >= ex_end:
            reduced_ranges[i][1] = end
            adapted = True
        if ex_start <= end <= ex_end and start <= ex_start:
            reduced_ranges[i][0] = start
            adapted = True
        if ex_start <= start and end <= ex_end:
            adapted = True
        if adapted:
            break
    else:
        reduced_ranges.append([start,end])

print(reduce(lambda acc, val: acc + val[1] - val[0] +1, reduced_ranges, 0))
