#!/usr/bin/env python

from itertools import product

from libmc import LTS, maximumSimulation

# deterministic version of Milner's vending machine
G = LTS (
    S = [1, 2, 3, 4],
    I = [1],
    Σ = ['p', 'd', 'm'],
    T = [
            (1, 'p', 2),
            (2, 'd', 3),
            (2, 'm', 4)
        ]
)

# nondeterministic version of Milner's vending machine
B = LTS (
    S = [5, 6, 7, 8, 9],
    I = [5],
    Σ = ['p', 'd', 'm'],
    T = [
            (5, 'p', 6),
            (5, 'p', 7),
            (6, 'd', 8),
            (7, 'm', 9)
        ]
)

# full simulation relation
simulation = \
    maximumSimulation(G, G, set(product(G.S, G.S))) | \
    maximumSimulation(G, B, set(product(G.S, B.S))) | \
    maximumSimulation(B, G, set(product(B.S, G.S))) | \
    maximumSimulation(B, B, set(product(B.S, B.S)))

assert simulation == {
    (1, 1),
            (2, 2),
    (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9),
    (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9),
    (5, 1),                         (5, 5),
            (6, 2),                         (6, 6),
            (7, 2),                                 (7, 7),
    (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8), (8, 9),
    (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (9, 7), (9, 8), (9, 9)
}

# G.simulate(B)
simulates = G.simulates(B)
simulation = maximumSimulation(B, G, set(product(B.S, G.S)))

assert simulates
assert simulation == {
    (5, 1),
            (6, 2),
            (7, 2),
    (8, 1), (8, 2), (8, 3), (8, 4),
    (9, 1), (9, 2), (9, 3), (9, 4)
}

# B.simulate(G)
simulates = B.simulates(G)
simulation = maximumSimulation(G, B, set(product(G.S, B.S)))

assert not simulates
assert simulation == {
    (3, 5), (3, 6), (3, 7), (3, 8), (3, 9),
    (4, 5), (4, 6), (4, 7), (4, 8), (4, 9)
}
