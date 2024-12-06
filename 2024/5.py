from collections import deque
from os import access
from pathlib import Path
from re import findall, finditer
from dataclasses import dataclass
from itertools import accumulate, compress, batched

data = Path.open("./input5").read()
# data = """47|53
# 97|13
# 97|61
# 97|47
# 75|29
# 61|13
# 75|53
# 29|13
# 97|29
# 53|29
# 61|53
# 97|53
# 61|29
# 47|13
# 75|47
# 97|75
# 47|61
# 75|61
# 47|29
# 75|13
# 53|13

# 75,47,61,53,29
# 97,61,53,29,13
# 75,29,13
# 75,97,47,61,53
# 61,13,29
# 97,13,75,29,47"""

rules, pages = data.split("\n\n")

rules = findall(r"([0-9]+)\|([0-9]+)", rules)
rules = [(int(n[0]), int(n[1])) for n in rules]

pages = pages.split("\n")
pages = [[int(n) for n in p.split(",")] for p in pages]


def get_rel_rules(pages):
    for r in rules:
        if r[0] in pages and r[1] in pages:
            yield r


def check_correct(pages):
    for i, p in enumerate(pages):
        for q in pages[i + 1 :]:
            for r in get_rel_rules(pages):
                if p == r[1] and q == r[0]:
                    return False
    return True


def _correct(pages):
    for i, p in enumerate(pages):
        for j, q in enumerate(pages[i + 1 :]):
            for r in get_rel_rules(pages):
                if p == r[1] and q == r[0]:
                    pages[i], pages[i + j + 1] = q, p
                    return pages
    return None


def correct_pages(pages):
    while (ret := _correct(pages)) is not None:
        pages = ret
    return pages


correct = [p for p in pages if check_correct(p)]
print(sum([p[len(p) // 2] for p in correct]))

incorrect = [p for p in pages if not check_correct(p)]
corrected = [correct_pages(p) for p in incorrect]
print(sum([p[len(p) // 2] for p in corrected]))
