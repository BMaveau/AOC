from itertools import tee

from aoc.data import load_data
from aoc.helpers import cache_results

def find_pos(l, el):
    return [i for i, x in enumerate(l) if x == el]

@cache_results
def find_largest_joltage(bank: tuple[int, ...], n):
    if len(bank) == n:
        return int(''.join(str(i) for i in bank))
    if n == 1:
        return max(bank)
    digit = max(bank)
    indexes = []
    while digit > 0:
        indexes = [idx for idx in find_pos(bank, digit) if idx +n <= len(bank)]
        if len(indexes):
            break
        digit -= 1
    return digit * 10 ** (n-1) + max(find_largest_joltage(bank[i+1:], n-1) for i in indexes)

test_inp = """987654321111111
811111111111119
234234234234278
818181911112111"""

inp = load_data(False, test_inp, 3, True)
inp = map(lambda bank: tuple(int(b) for b in bank), inp)

inp_a, inp_b = tee(inp)
print(sum(map(lambda i: find_largest_joltage(i, 2), inp_a)))
print(sum(map(lambda i: find_largest_joltage(i, 12), inp_b)))


    
