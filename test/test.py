#!/usr/bin/env python

from itertools import product

from libmc import FA
from libmc import LTS
from libmc import maximumSimulation
from libmc import maximumBisimulation
from libmc import printRelation

################################################################################
# completeness and determinism
################################################################################

# complete and deterministic
L = LTS (
    S = [1, 2],
    I = [1],
    Σ = ['a', 'b'],
    T = [
            (1, 'a', 2),
            (1, 'b', 2),
            (2, 'a', 2),
            (2, 'b', 2)
        ]
)

assert L.isComplete()
assert L.isDeterministic()

F = FA (
    S = [1, 2],
    I = [1],
    Σ = ['a', 'b'],
    T = [
            (1, 'a', 2),
            (1, 'b', 2),
            (2, 'a', 2),
            (2, 'b', 2)
        ],
    F = [2]
)

assert F.isComplete()
assert F.isDeterministic()

# complete but not deterministic
L = LTS (
    S = [1, 2],
    I = [1],
    Σ = ['a', 'b'],
    T = [
            (1, 'a', 2),
            (1, 'b', 2),
            (2, 'a', 1),
            (2, 'a', 2), # non deterministic transition
            (2, 'b', 2)
        ]
)

assert L.isComplete()
assert not L.isDeterministic()

F = FA (
    S = [1, 2],
    I = [1],
    Σ = ['a', 'b'],
    T = [
            (1, 'a', 2),
            (1, 'b', 2),
            (2, 'a', 2), # non deterministic transition
            (2, 'a', 2),
            (2, 'b', 2)
        ],
    F = [2]
)

assert F.isComplete()
assert not F.isDeterministic()

# not complete but deterministic
L = LTS (
    S = [1, 2],
    I = [1],
    Σ = ['a', 'b'],
    T = [] # no transition
)

assert not L.isComplete()
assert L.isDeterministic()

F = FA (
    S = [1, 2],
    I = [1],
    Σ = ['a', 'b'],
    T = [(1, 'a', 2)], # only one transition
    F = [2]
)

assert not F.isComplete()
assert F.isDeterministic()

# not complete and not deterministic
L = LTS (
    S = [1, 2],
    I = [1, 2], # more than one initial state
    Σ = ['a', 'b'],
    T = [] # no transition
)

assert not L.isComplete()
assert not L.isDeterministic()

F = FA (
    S = [1, 2],
    I = [1],
    Σ = ['a', 'b'],
    T = [
            (1, 'a', 2),
            (1, 'b', 2)
            # no transitions for state 2
        ],
    F = [2]
)

assert not F.isComplete()
assert F.isDeterministic()

################################################################################
# accepts
################################################################################
#
#  # (a|b)*abb
#  F = FA (
    #  S = [1, 2, 3, 4],
    #  I = [1],
    #  Σ = ['a', 'b'],
    #  T = [
            #  (1, 'a', 1),
            #  (1, 'b', 1),
            #  (1, 'a', 2),
            #  (2, 'b', 3),
            #  (3, 'b', 4)
        #  ],
    #  F = [4]
#  )
#
#  x = F.accepts("abb")
#  import pdb; pdb.set_trace()
#  x = F.accepts("aabb")
#  x = F.accepts("ab")

################################################################################
# traces
################################################################################

L = LTS (
    S = [1, 2, 3],
    I = [1],
    Σ = ['a', 'b'],
    T = [
            (1, 'a', 2),
            (1, 'b', 2),
            (2, 'a', 2),
            (2, 'b', 3)
        ]
)

assert L.trace(3) == [[(1, 'b', 2), (2, 'b', 3)], [(1, 'a', 2), (2, 'b', 3)]]
assert L.trace(3, [2]) == [[(2, 'b', 3)]]

################################################################################
# simulations
#
# example presented in the lecture
################################################################################

Σ = ['p', 'd', 'm']

A = LTS (
    S = [1, 2, 3, 4],
    I = [1],
    Σ = Σ,
    T = [
            (1, 'p', 2),
            (2, 'd', 3),
            (2, 'm', 4)
        ]
)

B = LTS (
    S = [5, 6, 7, 8, 9],
    I = [5],
    Σ = Σ,
    T = [
            (5, 'p', 6),
            (5, 'p', 7),
            (6, 'd', 8),
            (7, 'm', 9)
        ]
)

# A.simulate(B)
simulates = A.simulates(B)
simulation = maximumSimulation(B, A, set(product(B.S, A.S)))
try:
    assert simulates and simulation == {
        (5, 1),
        (6, 2),
        (7, 2),
        (8, 1), (8, 2), (8, 3), (8, 4),
        (9, 1), (9, 2), (9, 3), (9, 4)
    }
except AssertionError:
    print("=" * 80)
    printRelation(simulation, B.S, A.S)
    print("=" * 80)
    raise

# B.simulate(A)
simulates = B.simulates(A)
simulation = maximumSimulation(A, B, set(product(A.S, B.S)))
try:
    assert not simulates and simulation == {
        (3, 5), (3, 6), (3, 7), (3, 8), (3, 9),
        (4, 5), (4, 6), (4, 7), (4, 8), (4, 9)
    }
except AssertionError:
    print("=" * 80)
    printRelation(simulation, B.S, A.S)
    print("=" * 80)
    raise

# full simulation relation
simulation = \
    maximumSimulation(A, A, set(product(A.S, A.S))) | \
    maximumSimulation(A, B, set(product(A.S, B.S))) | \
    maximumSimulation(B, A, set(product(B.S, A.S))) | \
    maximumSimulation(B, B, set(product(B.S, B.S)))
try:
    assert simulation == {
        (3, 5), (3, 6), (3, 7), (3, 8), (3, 9),
        (4, 5), (4, 6), (4, 7), (4, 8), (4, 9),
        (1, 1),
                (2, 2),
        (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9),
        (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9),
        (5, 1),                      (5, 5),
                (6, 2),                      (6, 6),
                (7, 2),                             (7, 7),
        (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8), (8, 9),
        (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (9, 7), (9, 8), (9, 9)
    }
except AssertionError:
    print("=" * 80)
    printRelation(simulation, A.S + B.S, A.S + B.S)
    print("=" * 80)
    raise

################################################################################
# bisimulations
################################################################################

Σ = ['a', 'b']

A1 = LTS (
    S = [1, 2, 3],
    I = [1],
    Σ = Σ,
    T = [
            (1, 'a', 2),
            (1, 'a', 3),
            (2, 'a', 1),
            (3, 'b', 1)
        ]
)

A2 = LTS (
    S = [4, 5],
    I = [4],
    Σ = Σ,
    T = [
            (4, 'a', 4),
            (4, 'a', 5),
            (5, 'b', 4)
        ]
)

simulates = A1.bisimulates(A2)
simulation = \
    maximumBisimulation(A1, A1, set(product(A1.S, A1.S))) | \
    maximumBisimulation(A1, A2, set(product(A1.S, A2.S))) | \
    maximumBisimulation(A2, A1, set(product(A2.S, A1.S))) | \
    maximumBisimulation(A2, A2, set(product(A2.S, A2.S)))
try:
    assert not simulates and simulation == \
    {
    (1, 1),
            (2, 2),
                    (3, 3),
                            (4, 4),
                                    (5, 5)
    }
except AssertionError:
    print("=" * 80)
    printRelation(simulation, A1.S + A2.S, A1.S + A2.S)
    print("=" * 80)
    raise

simulates = A.bisimulates(B)
simulation = \
    maximumBisimulation(A, A, set(product(A.S, A.S))) | \
    maximumBisimulation(A, B, set(product(A.S, B.S))) | \
    maximumBisimulation(B, A, set(product(B.S, A.S))) | \
    maximumBisimulation(B, B, set(product(B.S, B.S)))
try:
    assert not simulates and simulation == \
    {
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
except AssertionError:
    print("=" * 80)
    printRelation(simulation, A.S + B.S, A.S + B.S)
    print("=" * 80)
    raise

################################################################################
# deterministic finite automata minimization
################################################################################

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

F = F.minimize()

assert F.S == ['A', 'B', 'C']
assert F.I == ['A']
assert F.Σ == F.Σ
assert F.T == \
    [
        ('A', 0, 'B'),
        ('A', 1, 'C'),
        ('B', 0, 'A'),
        ('B', 1, 'C'),
        ('C', 0, 'A'),
        ('C', 1, 'C')
    ]
