#!/usr/bin/env python

from itertools import product

from libmc import LTS, maximumBisimulation

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
    maximumBisimulation(G, G, set(product(G.S, G.S))) | \
    maximumBisimulation(G, B, set(product(G.S, B.S))) | \
    maximumBisimulation(B, G, set(product(B.S, G.S))) | \
    maximumBisimulation(B, B, set(product(B.S, B.S)))

# does G bisimulate B
simulates = G.bisimulates(B)

assert not simulates
assert simulation == {
    (1, 1),
            (2, 2),
                    (3, 3), (3, 4),                         (3, 8), (3, 9),
                    (4, 3), (4, 4),                         (4, 8), (4, 9),
                                    (5, 5),
                                            (6, 6),
                                                    (7, 7),
                    (8, 3), (8, 4),                         (8, 8), (8, 9),
                    (9, 3), (9, 4),                         (9, 8), (9, 9)
}
