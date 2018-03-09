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

# nondeterministic version of Milner's vending machine
B = LTS(
    S = [5, 6, 7, 8, 9],
    I = [5],
    Σ = ['p', 'd', 'm'],
    T = [
            (5, 'p', 6),
            (5, 'p', 7),
            (6, 'd', 8),
            (7, 'm', 9),
        ]
)

# completeness
assert not G.isComplete()
assert not B.isComplete()

# determinism
assert G.isDeterministic()
assert not B.isDeterministic()

# product
GB = G.product(B)

assert GB.S == [(1, 5), (2, 6), (2, 7), (3, 8), (4, 9)]
assert GB.I == [(1, 5)]
assert GB.Σ == ['p', 'd', 'm']
assert GB.T == [
    ((1, 5), 'p', (2, 6)),
    ((1, 5), 'p', (2, 7)),
    ((2, 6), 'd', (3, 8)),
    ((2, 7), 'm', (4, 9))
]

# sub-set construction
P = B.power()

assert P.isComplete()
assert P.isDeterministic()

assert P.S == [[], [5], [6, 7], [8], [9]]
assert P.I == [[5]]
assert P.Σ == B.Σ
assert P.T == [
    ([], 'd', []),
    ([], 'm', []),
    ([], 'p', []),
    ([5], 'd', []),
    ([5], 'm', []),
    ([5], 'p', [6, 7]),
    ([6, 7], 'd', [8]),
    ([6, 7], 'm', [9]),
    ([6, 7], 'p', []),
    ([8], 'd', []),
    ([8], 'm', []),
    ([8], 'p', []),
    ([9], 'd', []),
    ([9], 'm', []),
    ([9], 'p', [])
]

# visualization
dot = G.toDot()
with open("/tmp/milner-deterministic.dot", 'w') as f:
    f.write(dot)

dot = B.toDot()
with open("/tmp/milner-nondeterministic.dot", 'w') as f:
    f.write(dot)

# highlight the way to milk chocolate
dot = G.toDot(G.trace(4))
with open("/tmp/milner-deterministic-milkyway.dot", 'w') as f:
    f.write(dot)

dot = B.toDot(B.trace(9))
with open("/tmp/milner-nondeterministic-milkyway.dot", 'w') as f:
    f.write(dot)
