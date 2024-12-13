from aoc import load_data

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


def blink_one(number, n):
    if (number, n) in blink_one._cached:
        return blink_one._cached[(number, n)]
    res: int = 0
    if n == 1:
        if number == "0":
            res = 1
        elif len(number) % 2 == 0:
            res = 2
        else:
            res = 1
    elif number == "0":
        res = blink_one("1", n - 1)
    elif len(number) % 2 == 0:
        idx = len(number) // 2
        a = number[:idx]
        b = number[idx:].lstrip("0")
        if b == "":
            b = "0"
        res = blink_one(a, n - 1) + blink_one(b, n - 1)
    else:
        res = blink_one(str(int(number) * 2024), n - 1)
    blink_one._cached[(number, n)] = res
    return res


blink_one._cached = {}

print(sum(blink_one(d, 75) for d in data))
