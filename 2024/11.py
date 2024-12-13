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
for i in range(75):
    ndata = blink(ndata)
    print(i, len(ndata))
