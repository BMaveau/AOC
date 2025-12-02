from aoc.data import load_data


test_inp = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"

inp = load_data(False, test_inp, 2).split(',')
def create_range(i):
    start, end = i.split('-')
    return range(int(start), int(end)+1)

def create_pattern(pat, n):
    return pat * n

def has_pattern(id):
    id_str = str(id)
    for i in range(1, len(id_str)// 2 + 1):
        if len(id_str) % i != 0:
            continue
        if id_str[:i] * (len(id_str) // i) == id_str:
            return id
    return 0

sum(map(has_pattern, (id  for i in inp for id in create_range(i))))
