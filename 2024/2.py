from pathlib import Path
from re import match

data = Path.open("./input2").readlines()
# data = """7 6 4 2 1
# 1 2 7 8 9
# 9 7 6 2 1
# 1 3 2 4 5
# 8 6 4 4 1
# 1 3 6 7 9""".split(
#     "\n"
# )


def diff(a):
    return [x - y for x, y in zip(a[1:], a)]


# Part 1


def check_a(a):
    res = all(0 < abs(x) < 4 for x in a) and (
        all(x < 0 for x in a) or all(x > 0 for x in a)
    )
    return res


data_a = [diff([int(x) for x in d.split(" ")]) for d in data]
print(sum(check_a(a) for a in data_a))


# part 2


def check_b_new(b):
    res = check_a(diff(b))
    res |= any([check_a(diff(b[:idx] + b[idx + 1 :])) for idx in range(len(b))])
    return res


def append_or_ignore(b, idx):
    # return b[:idx] + b[idx + 1 :]
    if idx == len(b) - 1:
        return b[:-1]
    if idx == 0:
        return b[1:]
    return b[:idx] + [b[idx] + b[idx + 1]] + b[idx + 2 :]


def check_b(b):
    # Check the 0 difference levels
    # Remove this 0 value from the list and check if still ok
    # No need to adapt any value, as 0 indicates no change
    #
    # Check those where 1 value is wrong sign
    #
    # Check those where 1 value is too big
    res = check_a(b)
    try:
        idx = b.index(0)
        res |= check_a(b[0:idx] + b[idx + 1 :])
    except ValueError:
        pass

    if (sum(all_neg := [x < 0 for x in b])) == 1 or sum(all_neg) == len(b) - 1:
        idx = all_neg.index(True) if sum(all_neg) == 1 else all_neg.index(False)
        res |= check_a(append_or_ignore(b, idx))

    if sum(size := [abs(x) > 3 for x in b]) == 1:
        idx = size.index(True)
        res |= check_a(append_or_ignore(b, idx))

    return res


data_b = [[int(x) for x in d.split(" ")] for d in data]
data_b_old = [check_b(diff(x)) for x in data_b]
data_b = [check_b_new(x) for x in data_b]

for i, (x, y) in enumerate(zip(data_b, data_b_old)):
    if x != y:
        print(i)


print(sum(data_b))
# print(sum(check_b(a) for a in data_a))

# 540
# 564
# 551
# 558
