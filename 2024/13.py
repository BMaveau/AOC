import aoc
import re
import numpy as np

test = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""

data = aoc.load_data(False, test, 13, grouped_lines=True)


def get_game(game):
    a_x, b_x = re.findall(r"X\+([0-9]+)", "".join(game))
    a_y, b_y = re.findall(r"Y\+([0-9]+)", "".join(game))
    x = re.findall(r"X=([0-9]+), Y=([0-9]+)", game[2])
    return (a_x, a_y), (b_x, b_y), x[0]


def solve_game(game, part_b=0):
    # n * Ax + m * Bx = x
    # n * Ay + m * By = y
    # g > 100 * Ag + 100 By -> quit
    # A * (n;m) = (x;y)

    A = np.array([game[0], game[1]], dtype=float).T
    B = part_b + np.array(game[2], dtype=float)
    x = np.linalg.solve(A, B)
    if all(abs(np.round(x) - x) < 1e-3) and all(0 <= x):
        return x @ [3, 1]
    else:
        return 0


games = [get_game(d) for d in data]
print(sum([solve_game(g) for g in games]))
print(sum([solve_game(g, 10000000000000) for g in games]))
