from aoc import load_data
from aoc.helpers import cache_results

test = "125 17"
data = load_data(False, test, 11).split(" ")

print(data)


def blink(data):
    n_res = []
    for i in data:
        if i == "0":
            n_res.append("1")
        elif len(i) % 2 == 0:
            idx = len(i) // 2
            a = i[:idx]
            b = i[idx:].lstrip("0")
            if b == "":
                b = "0"
            n_res.extend([a, b])
        else:
            n_res.append(str(int(i) * 2024))
    return n_res


ndata = data
for i in range(25):
    ndata = blink(ndata)
    print(i, len(ndata))


# Part 2


@cache_results
def blink_one(number, n):
    if n == 1:
        if number == "0":
            return 1
        elif len(number) % 2 == 0:
            return 2
        else:
            return 1
    elif number == "0":
        return blink_one("1", n - 1)
    elif len(number) % 2 == 0:
        idx = len(number) // 2
        a = number[:idx]
        b = number[idx:].lstrip("0")
        if b == "":
            b = "0"
        return blink_one(a, n - 1) + blink_one(b, n - 1)
    else:
        return blink_one(str(int(number) * 2024), n - 1)


print(sum(blink_one(d, 75) for d in data))
