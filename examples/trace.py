#!/usr/bin/env python

from libmc import LTS

# deterministic version of Milner's vending machine
G = LTS(
    S = [1, 2, 3, 4],
    I = [1],
    Σ = ['p', 'd', 'm'],
    T = [
            (1, 'p', 2),
            (2, 'd', 3),
            (2, 'm', 4),
        ]
)

# find the way to milk chocolate
traces = G.trace(4)

assert traces == [[(1, 'p', 2), (2, 'm', 4)]]
