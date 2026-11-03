from itertools import combinations
from math import dist, prod

import networkx as nx
from aoc.data import load_data

test_input = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""

data = load_data(False, test_input, 8, lines=True)
pos = [[int(coord) for coord in line.split(",")] for line in data]

distances = {}
for a, b in combinations(enumerate(pos), 2):
    distances[a[0], b[0]] = dist(a[1], b[1])

G = nx.Graph()
G.add_nodes_from(list(range(len(pos))))
distances = sorted(distances.items(), key=lambda it: it[1])
for boxes in distances[:1000]:
    G.add_edge(*boxes[0])

print(
    prod(
        [
            len(x)
            for x in sorted((nx.connected_components(G)), key=len, reverse=True)[:3]
        ]
    )
)


for boxes in distances[1000:]:
    G.add_edge(*boxes[0])
    if nx.is_connected(G):
        pos_a = pos[boxes[0][0]]
        pos_b = pos[boxes[0][1]]
        print(pos_a[0] * pos_b[0])
        break


# Too low
# 1024
# Too high
# 1699502020562777685460341646914339955834466355159657990774338988539904000000000000000000000
