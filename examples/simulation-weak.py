#!/usr/bin/env python

from itertools import product

from libmc import LTS, maximumSimulation

# example automata
A1 = LTS(
    S = [1, 2, 3],
    I = [1],
    Σ = ['a', 'b', 'τ'],
    T = [
            (1, 'b', 3),
            (1, 'τ', 2),
            (2, 'a', 3),
            (3, 'τ', 1)
        ]
)

A2 = LTS(
    S = [4, 5],
    I = [4],
    Σ = ['a', 'b', 'τ'],
    T = [
            (4, 'a', 4),
            (4, 'b', 5),
            (5, 'a', 4),
            (5, 'τ', 4)
        ]
)

# internal event
τ = ['τ']

# full simulation relation
simulation = \
    maximumSimulation(A1, A1, set(product(A1.S, A1.S)), τ) | \
    maximumSimulation(A1, A2, set(product(A1.S, A2.S)), τ) | \
    maximumSimulation(A2, A1, set(product(A2.S, A1.S)), τ) | \
    maximumSimulation(A2, A2, set(product(A2.S, A2.S)), τ)

assert simulation == {
    (1, 1),         (1, 3), (1, 4), (1, 5),
    (2, 1), (2, 2), (2, 3), (2, 4), (2, 5),
    (3, 1),         (3, 3), (3, 4), (3, 5),
    (4, 1),         (4, 3), (4, 4), (4, 5),
    (5, 1),         (5, 3), (5, 4), (5, 5)
}

# A1 simulates A2?
simulates = A1.simulates(A2, τ)
simulation = maximumSimulation(A2, A1, set(product(A2.S, A1.S)), τ)

assert simulates
assert simulation == {(4, 1), (4, 3), (5, 1), (5, 3)}

# A2 simulates A1?
simulates = A2.simulates(A1, τ)
simulation = maximumSimulation(A1, A2, set(product(A1.S, A2.S)), τ)

assert simulates
assert simulation == {(1, 4), (1, 5), (2, 4), (2, 5), (3, 4), (3, 5)}
