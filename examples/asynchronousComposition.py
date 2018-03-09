#!/usr/bin/env python

from libmc import LTS, asynchronousComposition

# example automata
A1 = LTS(
    S = [1, 2, 3, 4],
    I = [1],
    Σ = ['a', 'b', 'c', 's'],
    T = [
            (1, 'a', 2),
            (2, 'b', 3),
            (3, 'c', 4),
            (4, 's', 1)
        ]
    )

A2 = LTS(
    S = [5, 6, 7, 8],
    I = [5],
    Σ = ['d', 'e', 'f', 's'],
    T = [
            (5, 'd', 6),
            (6, 'e', 7),
            (7, 'f', 8),
            (8, 's', 5),
        ]
    )

# generate the asynchronous composition through interleaving
composition = asynchronousComposition(A1, A2)

assert composition.S == [
    (1, 5), (1, 6), (1, 7), (1, 8),
    (2, 5), (2, 6), (2, 7), (2, 8),
    (3, 5), (3, 6), (3, 7), (3, 8),
    (4, 5), (4, 6), (4, 7), (4, 8)
]
assert composition.I == [(1, 5)]
assert composition.Σ == ['a', 'b', 'c', 'd', 'e', 'f', 's']
assert composition.T == [
    ((1, 5), 'a', (2, 5)), ((1, 5), 'd', (1, 6)),
    ((1, 6), 'a', (2, 6)), ((1, 6), 'e', (1, 7)),
    ((1, 7), 'a', (2, 7)), ((1, 7), 'f', (1, 8)),
    ((1, 8), 'a', (2, 8)), ((2, 5), 'b', (3, 5)),
    ((2, 5), 'd', (2, 6)), ((2, 6), 'b', (3, 6)),
    ((2, 6), 'e', (2, 7)), ((2, 7), 'b', (3, 7)),
    ((2, 7), 'f', (2, 8)), ((2, 8), 'b', (3, 8)),
    ((3, 5), 'c', (4, 5)), ((3, 5), 'd', (3, 6)),
    ((3, 6), 'c', (4, 6)), ((3, 6), 'e', (3, 7)),
    ((3, 7), 'c', (4, 7)), ((3, 7), 'f', (3, 8)),
    ((3, 8), 'c', (4, 8)), ((4, 5), 'd', (4, 6)),
    ((4, 6), 'e', (4, 7)), ((4, 7), 'f', (4, 8)),
    ((4, 8), 's', (1, 5))
]

# with partial order reduction, expanding the rightmost component
composition = asynchronousComposition(A1, A2, partialOrderReduction = lambda x: [x[-1]])

assert composition.S == [(1, 5), (1, 6), (1, 7), (1, 8), (2, 8), (3, 8), (4, 8)]
assert composition.I == [(1, 5)]
assert composition.Σ == ['a', 'b', 'c', 'd', 'e', 'f', 's']
assert composition.T == [
    ((1, 5), 'd', (1, 6)),
    ((1, 6), 'e', (1, 7)),
    ((1, 7), 'f', (1, 8)),
    ((1, 8), 'a', (2, 8)),
    ((2, 8), 'b', (3, 8)),
    ((3, 8), 'c', (4, 8)),
    ((4, 8), 's', (1, 5))
]
