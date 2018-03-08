#!/usr/bin/env python

from libmc import FA

# deterministic example automaton
F = FA (
    S = ['A', 'B', 'C', 'D', 'E', 'F'],
    I = ['A'],
    Σ = [0, 1],
    T = [
            ('A', 0, 'B'),
            ('A', 1, 'E'),
            ('B', 0, 'A'),
            ('B', 1, 'C'),
            ('C', 0, 'A'),
            ('C', 1, 'C'),
            ('D', 0, 'F'),
            ('D', 1, 'C'),
            ('E', 0, 'D'),
            ('E', 1, 'E'),
            ('F', 0, 'A'),
            ('F', 1, 'E')
        ],
    F = ['B', 'F']
)

assert F.isDeterministic()

# minimization
minF = F.minimize()

assert minF.S == [('A', 'D'), ('B', 'F'), ('C', 'E')]
assert minF.I == [('A', 'D')]
assert minF.Σ == F.Σ
assert minF.T == [
    (('A', 'D'), 0, ('B', 'F')),
    (('A', 'D'), 1, ('C', 'E')),
    (('B', 'F'), 0, ('A', 'D')),
    (('B', 'F'), 1, ('C', 'E')),
    (('C', 'E'), 0, ('A', 'D')),
    (('C', 'E'), 1, ('C', 'E'))
]
assert minF.F == [('B', 'F')]
