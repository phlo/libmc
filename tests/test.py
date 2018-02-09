#!/usr/bin/env python

from itertools import product

from libmc import *

def expect (result, expectation, msg=None):
    try:
        assert result == expectation
    except AssertionError:
        print("=" * 80)
        if msg is not None:
            print(msg)
            print("=" * 80)
        print("got:      " + str(result))
        print("expected: " + str(expectation))
        print("=" * 80)
        raise

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

expect(L.isComplete(), True, "LTS.isComplete")
expect(L.isDeterministic(), True, "LTS.isDeterministic")

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

expect(F.isComplete(), True, "FA.isComplete")
expect(F.isDeterministic(), True, "FA.isDeterministic")

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

expect(L.isComplete(), True, "LTS.isComplete")
expect(L.isDeterministic(), False, "LTS.isDeterministic")

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

expect(F.isComplete(), True, "FA.isComplete")
expect(F.isDeterministic(), False, "FA.isDeterministic")

# not complete but deterministic
L = LTS (
    S = [1, 2],
    I = [1],
    Σ = ['a', 'b'],
    T = [] # no transition
)

expect(L.isComplete(), False, "LTS.isComplete")
expect(L.isDeterministic(), True, "LTS.isDeterministic")

F = FA (
    S = [1, 2],
    I = [1],
    Σ = ['a', 'b'],
    T = [(1, 'a', 2)], # only one transition
    F = [2]
)

F.toDot()

expect(F.isComplete(), False, "FA.isComplete")
expect(F.isDeterministic(), True, "FA.isDeterministic")

# not complete and not deterministic
L = LTS (
    S = [1, 2],
    I = [1, 2], # more than one initial state
    Σ = ['a', 'b'],
    T = [] # no transition
)

expect(L.isComplete(), False, "LTS.isComplete")
expect(L.isDeterministic(), False, "LTS.isDeterministic")

F = FA (
    S = [1, 2],
    I = [1, 2], # more than one initial state
    Σ = ['a', 'b'],
    T = [
            (1, 'a', 2),
            (1, 'b', 2),
            # no transitions for state 2
        ],
    F = [2]
)

expect(F.isComplete(), False, "FA.isComplete")
expect(F.isDeterministic(), False, "FA.isDeterministic")

################################################################################
# product, complement and power automta
#
# example presented in assignment 1 - exercise 1
################################################################################

Σ = ['a', 'b']

I_EX1 = FA (
    S = ['1', '2', '3', '4'],
    I = ['1'],
    Σ = Σ,
    T = [
            ('1', 'b', '2'),
            ('2', 'b', '3'),
            ('2', 'b', '4'),
            ('3', 'a', '1'),
            ('3', 'b', '3'),
            ('4', 'b', '3')
        ],
    F = ['4']
)

S_EX1 = FA (
    S = ['A', 'B', 'C', 'D'],
    I = ['A'],
    Σ = Σ,
    T = [
            ('A', 'a', 'C'),
            ('A', 'a', 'D'),
            ('A', 'b', 'A'),
            ('A', 'b', 'B'),
            ('B', 'a', 'D'),
            ('B', 'b', 'C'),
            ('C', 'a', 'C'),
            ('C', 'a', 'D'),
            ('D', 'b', 'A')
        ],
    F = ['B']
)

# product
P = I_EX1.product(S_EX1, True)

expect(
    P.S,
    [
        ('1', 'A'), ('1', 'B'), ('1', 'C'), ('1', 'D'),
        ('2', 'A'), ('2', 'B'), ('2', 'C'), ('2', 'D'),
        ('3', 'A'), ('3', 'B'), ('3', 'C'), ('3', 'D'),
        ('4', 'A'), ('4', 'B'), ('4', 'C'), ('4', 'D')
    ],
    "FA.product: states"
)
expect(P.I, [('1', 'A')], "FA.product: initial states")
expect(P.Σ, I_EX1.Σ, "FA.product: alphabet")
expect(
    P.T,
    [
        (('1', 'A'), 'b', ('2', 'A')),
        (('1', 'A'), 'b', ('2', 'B')),
        (('1', 'B'), 'b', ('2', 'C')),
        (('1', 'D'), 'b', ('2', 'A')),
        (('2', 'A'), 'b', ('3', 'A')),
        (('2', 'A'), 'b', ('3', 'B')),
        (('2', 'A'), 'b', ('4', 'A')),
        (('2', 'A'), 'b', ('4', 'B')),
        (('2', 'B'), 'b', ('3', 'C')),
        (('2', 'B'), 'b', ('4', 'C')),
        (('2', 'D'), 'b', ('3', 'A')),
        (('2', 'D'), 'b', ('4', 'A')),
        (('3', 'A'), 'a', ('1', 'C')),
        (('3', 'A'), 'a', ('1', 'D')),
        (('3', 'A'), 'b', ('3', 'A')),
        (('3', 'A'), 'b', ('3', 'B')),
        (('3', 'B'), 'a', ('1', 'D')),
        (('3', 'B'), 'b', ('3', 'C')),
        (('3', 'C'), 'a', ('1', 'C')),
        (('3', 'C'), 'a', ('1', 'D')),
        (('3', 'D'), 'b', ('3', 'A')),
        (('4', 'A'), 'b', ('3', 'A')),
        (('4', 'A'), 'b', ('3', 'B')),
        (('4', 'B'), 'b', ('3', 'C')),
        (('4', 'D'), 'b', ('3', 'A'))
    ],
    "FA.product: transitions"
)
expect(P.F, [('4', 'B')], "FA.product: final states")

# complement
C = I_EX1.complement()

expect(C.S, I_EX1.S, "FA.complement: states")
expect(C.I, I_EX1.I, "FA.complement: initial states")
expect(C.Σ, I_EX1.Σ, "FA.complement: alphabet")
expect(C.T, I_EX1.T, "FA.complement: transitions")
expect(C.F, ['1', '2', '3'], "FA.complement: final states")

# power
P = S_EX1.power()

expect(
    P.S,
    [
        (),
        ('A',),
        ('B',),
        ('C',),
        ('D',),
        ('A', 'B'),
        ('A', 'C'),
        ('A', 'D'),
        ('B', 'C'),
        ('B', 'D'),
        ('C', 'D'),
        ('A', 'B', 'C'),
        ('A', 'B', 'D'),
        ('A', 'C', 'D'),
        ('B', 'C', 'D'),
        ('A', 'B', 'C', 'D')
    ],
    "FA.power: states"
)

expect(P.Σ, S_EX1.Σ, "FA.power: alphabet")

expect(
    P.T,
    [
        ((), 'a', ()),
        ((), 'b', ()),
        (('A',), 'a', ('C', 'D')),
        (('A',), 'b', ('A', 'B')),
        (('B',), 'a', ('D',)),
        (('B',), 'b', ('C',)),
        (('C',), 'a', ('C', 'D')),
        (('C',), 'b', ()),
        (('D',), 'a', ()),
        (('D',), 'b', ('A',)),
        (('A', 'B'), 'a', ('C', 'D')),
        (('A', 'B'), 'b', ('A', 'B', 'C')),
        (('A', 'C'), 'a', ('C', 'D')),
        (('A', 'C'), 'b', ('A', 'B')),
        (('A', 'D'), 'a', ('C', 'D')),
        (('A', 'D'), 'b', ('A', 'B')),
        (('B', 'C'), 'a', ('C', 'D')),
        (('B', 'C'), 'b', ('C',)),
        (('B', 'D'), 'a', ('D',)),
        (('B', 'D'), 'b', ('A', 'C')),
        (('C', 'D'), 'a', ('C', 'D')),
        (('C', 'D'), 'b', ('A',)),
        (('A', 'B', 'C'), 'a', ('C', 'D')),
        (('A', 'B', 'C'), 'b', ('A', 'B', 'C')),
        (('A', 'B', 'D'), 'a', ('C', 'D')),
        (('A', 'B', 'D'), 'b', ('A', 'B', 'C')),
        (('A', 'C', 'D'), 'a', ('C', 'D')),
        (('A', 'C', 'D'), 'b', ('A', 'B')),
        (('B', 'C', 'D'), 'a', ('C', 'D')),
        (('B', 'C', 'D'), 'b', ('A', 'C')),
        (('A', 'B', 'C', 'D'), 'a', ('C', 'D')),
        (('A', 'B', 'C', 'D'), 'b', ('A', 'B', 'C'))
    ],
    "FA.power: transitions"
)

expect(
    P.F,
    [
        ('B',),
        ('A', 'B'),
        ('B', 'C'),
        ('B', 'D'),
        ('A', 'B', 'C'),
        ('A', 'B', 'D'),
        ('B', 'C', 'D'),
        ('A', 'B', 'C', 'D')
    ],
    "FA.power: final states"
)

################################################################################
# acceptance
################################################################################

# (a|b)*abb
F = FA (
    S = [1, 2, 3, 4],
    I = [1],
    Σ = ['a', 'b'],
    T = [
            (1, 'a', 1),
            (1, 'b', 1),
            (1, 'a', 2),
            (2, 'b', 3),
            (3, 'b', 4)
        ],
    F = [4]
)

expect(F.accepts("abb"), True, "FA.accepts")
expect(F.accepts("aabb"), True, "FA.accepts")
expect(F.accepts("ab"), False, "FA.accepts")

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

expect(
    L.trace(3),
    [[(1, 'b', 2), (2, 'b', 3)], [(1, 'a', 2), (2, 'b', 3)]],
    "LTS.traces"
)
expect(
    L.trace(3, [2]),
    [[(2, 'b', 3)], [(2, 'a', 2), (2, 'b', 3)]],
    "LTS.traces"
)

################################################################################
# conformance
#
# example presented in assignment 1 - exercise 1
################################################################################

[ conforms, ICPS, traces ] = I_EX1.conforms(S_EX1, full=True)

expect(conforms, True, "FA.conforms: conforms")

expect(
    ICPS.S,
    [
        ('1', ()),
        ('1', ('A',)),
        ('1', ('B',)),
        ('1', ('C',)),
        ('1', ('D',)),
        ('1', ('A', 'B')),
        ('1', ('A', 'C')),
        ('1', ('A', 'D')),
        ('1', ('B', 'C')),
        ('1', ('B', 'D')),
        ('1', ('C', 'D')),
        ('1', ('A', 'B', 'C')),
        ('1', ('A', 'B', 'D')),
        ('1', ('A', 'C', 'D')),
        ('1', ('B', 'C', 'D')),
        ('1', ('A', 'B', 'C', 'D')),
        ('2', ()),
        ('2', ('A',)),
        ('2', ('B',)),
        ('2', ('C',)),
        ('2', ('D',)),
        ('2', ('A', 'B')),
        ('2', ('A', 'C')),
        ('2', ('A', 'D')),
        ('2', ('B', 'C')),
        ('2', ('B', 'D')),
        ('2', ('C', 'D')),
        ('2', ('A', 'B', 'C')),
        ('2', ('A', 'B', 'D')),
        ('2', ('A', 'C', 'D')),
        ('2', ('B', 'C', 'D')),
        ('2', ('A', 'B', 'C', 'D')),
        ('3', ()),
        ('3', ('A',)),
        ('3', ('B',)),
        ('3', ('C',)),
        ('3', ('D',)),
        ('3', ('A', 'B')),
        ('3', ('A', 'C')),
        ('3', ('A', 'D')),
        ('3', ('B', 'C')),
        ('3', ('B', 'D')),
        ('3', ('C', 'D')),
        ('3', ('A', 'B', 'C')),
        ('3', ('A', 'B', 'D')),
        ('3', ('A', 'C', 'D')),
        ('3', ('B', 'C', 'D')),
        ('3', ('A', 'B', 'C', 'D')),
        ('4', ()),
        ('4', ('A',)),
        ('4', ('B',)),
        ('4', ('C',)),
        ('4', ('D',)),
        ('4', ('A', 'B')),
        ('4', ('A', 'C')),
        ('4', ('A', 'D')),
        ('4', ('B', 'C')),
        ('4', ('B', 'D')),
        ('4', ('C', 'D')),
        ('4', ('A', 'B', 'C')),
        ('4', ('A', 'B', 'D')),
        ('4', ('A', 'C', 'D')),
        ('4', ('B', 'C', 'D')),
        ('4', ('A', 'B', 'C', 'D'))
    ],
    "FA.conforms: states"
)

expect(ICPS.Σ, I_EX1.Σ, "FA.conforms: alphabet")

expect(
    ICPS.T,
    [
        (('1', ()), 'b', ('2', ())),
        (('1', ('A',)), 'b', ('2', ('A', 'B'))),
        (('1', ('B',)), 'b', ('2', ('C',))),
        (('1', ('C',)), 'b', ('2', ())),
        (('1', ('D',)), 'b', ('2', ('A',))),
        (('1', ('A', 'B')), 'b', ('2', ('A', 'B', 'C'))),
        (('1', ('A', 'C')), 'b', ('2', ('A', 'B'))),
        (('1', ('A', 'D')), 'b', ('2', ('A', 'B'))),
        (('1', ('B', 'C')), 'b', ('2', ('C',))),
        (('1', ('B', 'D')), 'b', ('2', ('A', 'C'))),
        (('1', ('C', 'D')), 'b', ('2', ('A',))),
        (('1', ('A', 'B', 'C')), 'b', ('2', ('A', 'B', 'C'))),
        (('1', ('A', 'B', 'D')), 'b', ('2', ('A', 'B', 'C'))),
        (('1', ('A', 'C', 'D')), 'b', ('2', ('A', 'B'))),
        (('1', ('B', 'C', 'D')), 'b', ('2', ('A', 'C'))),
        (('1', ('A', 'B', 'C', 'D')), 'b', ('2', ('A', 'B', 'C'))),
        (('2', ()), 'b', ('3', ())),
        (('2', ()), 'b', ('4', ())),
        (('2', ('A',)), 'b', ('3', ('A', 'B'))),
        (('2', ('A',)), 'b', ('4', ('A', 'B'))),
        (('2', ('B',)), 'b', ('3', ('C',))),
        (('2', ('B',)), 'b', ('4', ('C',))),
        (('2', ('C',)), 'b', ('3', ())),
        (('2', ('C',)), 'b', ('4', ())),
        (('2', ('D',)), 'b', ('3', ('A',))),
        (('2', ('D',)), 'b', ('4', ('A',))),
        (('2', ('A', 'B')), 'b', ('3', ('A', 'B', 'C'))),
        (('2', ('A', 'B')), 'b', ('4', ('A', 'B', 'C'))),
        (('2', ('A', 'C')), 'b', ('3', ('A', 'B'))),
        (('2', ('A', 'C')), 'b', ('4', ('A', 'B'))),
        (('2', ('A', 'D')), 'b', ('3', ('A', 'B'))),
        (('2', ('A', 'D')), 'b', ('4', ('A', 'B'))),
        (('2', ('B', 'C')), 'b', ('3', ('C',))),
        (('2', ('B', 'C')), 'b', ('4', ('C',))),
        (('2', ('B', 'D')), 'b', ('3', ('A', 'C'))),
        (('2', ('B', 'D')), 'b', ('4', ('A', 'C'))),
        (('2', ('C', 'D')), 'b', ('3', ('A',))),
        (('2', ('C', 'D')), 'b', ('4', ('A',))),
        (('2', ('A', 'B', 'C')), 'b', ('3', ('A', 'B', 'C'))),
        (('2', ('A', 'B', 'C')), 'b', ('4', ('A', 'B', 'C'))),
        (('2', ('A', 'B', 'D')), 'b', ('3', ('A', 'B', 'C'))),
        (('2', ('A', 'B', 'D')), 'b', ('4', ('A', 'B', 'C'))),
        (('2', ('A', 'C', 'D')), 'b', ('3', ('A', 'B'))),
        (('2', ('A', 'C', 'D')), 'b', ('4', ('A', 'B'))),
        (('2', ('B', 'C', 'D')), 'b', ('3', ('A', 'C'))),
        (('2', ('B', 'C', 'D')), 'b', ('4', ('A', 'C'))),
        (('2', ('A', 'B', 'C', 'D')), 'b', ('3', ('A', 'B', 'C'))),
        (('2', ('A', 'B', 'C', 'D')), 'b', ('4', ('A', 'B', 'C'))),
        (('3', ()), 'a', ('1', ())),
        (('3', ()), 'b', ('3', ())),
        (('3', ('A',)), 'a', ('1', ('C', 'D'))),
        (('3', ('A',)), 'b', ('3', ('A', 'B'))),
        (('3', ('B',)), 'a', ('1', ('D',))),
        (('3', ('B',)), 'b', ('3', ('C',))),
        (('3', ('C',)), 'a', ('1', ('C', 'D'))),
        (('3', ('C',)), 'b', ('3', ())),
        (('3', ('D',)), 'a', ('1', ())),
        (('3', ('D',)), 'b', ('3', ('A',))),
        (('3', ('A', 'B')), 'a', ('1', ('C', 'D'))),
        (('3', ('A', 'B')), 'b', ('3', ('A', 'B', 'C'))),
        (('3', ('A', 'C')), 'a', ('1', ('C', 'D'))),
        (('3', ('A', 'C')), 'b', ('3', ('A', 'B'))),
        (('3', ('A', 'D')), 'a', ('1', ('C', 'D'))),
        (('3', ('A', 'D')), 'b', ('3', ('A', 'B'))),
        (('3', ('B', 'C')), 'a', ('1', ('C', 'D'))),
        (('3', ('B', 'C')), 'b', ('3', ('C',))),
        (('3', ('B', 'D')), 'a', ('1', ('D',))),
        (('3', ('B', 'D')), 'b', ('3', ('A', 'C'))),
        (('3', ('C', 'D')), 'a', ('1', ('C', 'D'))),
        (('3', ('C', 'D')), 'b', ('3', ('A',))),
        (('3', ('A', 'B', 'C')), 'a', ('1', ('C', 'D'))),
        (('3', ('A', 'B', 'C')), 'b', ('3', ('A', 'B', 'C'))),
        (('3', ('A', 'B', 'D')), 'a', ('1', ('C', 'D'))),
        (('3', ('A', 'B', 'D')), 'b', ('3', ('A', 'B', 'C'))),
        (('3', ('A', 'C', 'D')), 'a', ('1', ('C', 'D'))),
        (('3', ('A', 'C', 'D')), 'b', ('3', ('A', 'B'))),
        (('3', ('B', 'C', 'D')), 'a', ('1', ('C', 'D'))),
        (('3', ('B', 'C', 'D')), 'b', ('3', ('A', 'C'))),
        (('3', ('A', 'B', 'C', 'D')), 'a', ('1', ('C', 'D'))),
        (('3', ('A', 'B', 'C', 'D')), 'b', ('3', ('A', 'B', 'C'))),
        (('4', ()), 'b', ('3', ())),
        (('4', ('A',)), 'b', ('3', ('A', 'B'))),
        (('4', ('B',)), 'b', ('3', ('C',))),
        (('4', ('C',)), 'b', ('3', ())),
        (('4', ('D',)), 'b', ('3', ('A',))),
        (('4', ('A', 'B')), 'b', ('3', ('A', 'B', 'C'))),
        (('4', ('A', 'C')), 'b', ('3', ('A', 'B'))),
        (('4', ('A', 'D')), 'b', ('3', ('A', 'B'))),
        (('4', ('B', 'C')), 'b', ('3', ('C',))),
        (('4', ('B', 'D')), 'b', ('3', ('A', 'C'))),
        (('4', ('C', 'D')), 'b', ('3', ('A',))),
        (('4', ('A', 'B', 'C')), 'b', ('3', ('A', 'B', 'C'))),
        (('4', ('A', 'B', 'D')), 'b', ('3', ('A', 'B', 'C'))),
        (('4', ('A', 'C', 'D')), 'b', ('3', ('A', 'B'))),
        (('4', ('B', 'C', 'D')), 'b', ('3', ('A', 'C'))),
        (('4', ('A', 'B', 'C', 'D')), 'b', ('3', ('A', 'B', 'C')))
    ],
    "FA.conforms: transitions"
)

expect(
    ICPS.F,
    [
        ('4', ()),
        ('4', ('A',)),
        ('4', ('A', 'C')),
        ('4', ('A', 'C', 'D')),
        ('4', ('A', 'D')),
        ('4', ('C',)),
        ('4', ('C', 'D')),
        ('4', ('D',))
    ],
    "FA.conforms: final states"
)

expect(traces, [], "FA.conforms: traces")

################################################################################
# strong simulations
#
# example presented in the lecture
################################################################################

Σ = ['p', 'd', 'm']

A_VO = LTS (
    S = [1, 2, 3, 4],
    I = [1],
    Σ = Σ,
    T = [
            (1, 'p', 2),
            (2, 'd', 3),
            (2, 'm', 4)
        ]
)

B_VO = LTS (
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

# full simulation relation
simulation = \
    maximumSimulation(A_VO, A_VO, set(product(A_VO.S, A_VO.S))) | \
    maximumSimulation(A_VO, B_VO, set(product(A_VO.S, B_VO.S))) | \
    maximumSimulation(B_VO, A_VO, set(product(B_VO.S, A_VO.S))) | \
    maximumSimulation(B_VO, B_VO, set(product(B_VO.S, B_VO.S)))

try:
    expect(
        simulation,
        {
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
        },
        "maximumSimulation: simulation relation"
    )
except AssertionError:
    print("=" * 80)
    printRelation(simulation, A_VO.S + B_VO.S, A_VO.S + B_VO.S)
    print("=" * 80)
    raise

# A.simulate(B)
simulates = A_VO.simulates(B_VO)
simulation = maximumSimulation(B_VO, A_VO, set(product(B_VO.S, A_VO.S)))

try:
    expect(simulates, True, "maximumSimulation: simulates")
    expect(
        simulation,
        {
            (5, 1),
            (6, 2),
            (7, 2),
            (8, 1), (8, 2), (8, 3), (8, 4),
            (9, 1), (9, 2), (9, 3), (9, 4)
        },
        "maximumSimulation: simulation relation"
    )
except AssertionError:
    print("=" * 80)
    printRelation(simulation, B_VO.S, A_VO.S)
    print("=" * 80)
    raise

# B.simulate(A)
simulates = B_VO.simulates(A_VO)
simulation = maximumSimulation(A_VO, B_VO, set(product(A_VO.S, B_VO.S)))

try:
    expect(simulates, False, "maximumSimulation: simulates")
    expect(
        simulation,
        {
            (3, 5), (3, 6), (3, 7), (3, 8), (3, 9),
            (4, 5), (4, 6), (4, 7), (4, 8), (4, 9)
        },
        "maximumSimulation: simulation relation"
    )
except AssertionError:
    print("=" * 80)
    printRelation(simulation, A_VO.S, B_VO.S)
    print("=" * 80)
    raise

################################################################################
# weak simulations
#
# example presented in assignment 2 - exercise 1
################################################################################

Σ = ['a', 'b', 'τ']

A_EX2 = LTS (
    S = [1, 2, 3],
    I = [1],
    Σ = Σ,
    T = [
            (1, 'b', 3),
            (1, 'τ', 2),
            (2, 'a', 3),
            (3, 'τ', 1)
        ]
)

B_EX2 = LTS (
    S = [4, 5],
    I = [4],
    Σ = Σ,
    T = [
            (4, 'a', 4),
            (4, 'b', 5),
            (5, 'a', 4),
            (5, 'τ', 4)
        ]
)

τ = ['τ']

# full simulation relation
simulation = \
    maximumSimulation(A_EX2, A_EX2, set(product(A_EX2.S, A_EX2.S)), τ) | \
    maximumSimulation(A_EX2, B_EX2, set(product(A_EX2.S, B_EX2.S)), τ) | \
    maximumSimulation(B_EX2, A_EX2, set(product(B_EX2.S, A_EX2.S)), τ) | \
    maximumSimulation(B_EX2, B_EX2, set(product(B_EX2.S, B_EX2.S)), τ)

try:
    expect(
        simulation,
        {
            (1, 1),         (1, 3), (1, 4), (1, 5),
            (2, 1), (2, 2), (2, 3), (2, 4), (2, 5),
            (3, 1),         (3, 3), (3, 4), (3, 5),
            (4, 1),         (4, 3), (4, 4), (4, 5),
            (5, 1),         (5, 3), (5, 4), (5, 5)
        },
        "maximumSimulation (weak): simulation relation"
    )
except AssertionError:
    print("=" * 80)
    printRelation(simulation, A_EX2.S + B_EX2.S, A_EX2.S + B_EX2.S)
    print("=" * 80)
    raise

# A.simulate(B)
simulates = A_EX2.simulates(B_EX2, τ)
simulation = maximumSimulation(B_EX2, A_EX2, set(product(B_EX2.S, A_EX2.S)), τ)

try:
    expect(simulates, True, "maximumSimulation (weak): simulates")
    expect(
        simulation,
        {(4, 1), (4, 3), (5, 1), (5, 3)},
        "maximumSimulation (weak): simulation relation"
    )
except AssertionError:
    print("=" * 80)
    printRelation(simulation, B_EX2.S, A_EX2.S)
    print("=" * 80)
    raise

# B.simulate(A)
simulates = B_EX2.simulates(A_EX2, τ)
simulation = maximumSimulation(A_EX2, B_EX2, set(product(A_EX2.S, B_EX2.S)), τ)

try:
    expect(simulates, True, "maximumSimulation (weak): simulates")
    expect(
        simulation,
        {
            (1, 4), (1, 5), (2, 4), (2, 5), (3, 4), (3, 5)
        },
        "maximumSimulation (weak): simulation relation"
    )
except AssertionError:
    print("=" * 80)
    printRelation(simulation, A_EX2.S + B_EX2.S, A_EX2.S + B_EX2.S)
    print("=" * 80)
    raise

################################################################################
# bisimulations
#
# example presented in assignment 2 - exercise 3
################################################################################

Σ = ['a', 'b']

A1_EX2 = LTS (
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

A2_EX2 = LTS (
    S = [4, 5],
    I = [4],
    Σ = Σ,
    T = [
            (4, 'a', 4),
            (4, 'a', 5),
            (5, 'b', 4)
        ]
)

simulates = A1_EX2.bisimulates(A2_EX2)
simulation = \
    maximumBisimulation(A1_EX2, A1_EX2, set(product(A1_EX2.S, A1_EX2.S))) | \
    maximumBisimulation(A1_EX2, A2_EX2, set(product(A1_EX2.S, A2_EX2.S))) | \
    maximumBisimulation(A2_EX2, A1_EX2, set(product(A2_EX2.S, A1_EX2.S))) | \
    maximumBisimulation(A2_EX2, A2_EX2, set(product(A2_EX2.S, A2_EX2.S)))

try:
    expect(simulates, False, "maximumBisimulation: simulates")
    expect(
        simulation,
        {
        (1, 1),
                (2, 2),
                        (3, 3),
                                (4, 4),
                                        (5, 5)
        },
        "maximumBisimulation: simulation relation"
    )
except AssertionError:
    print("=" * 80)
    printRelation(simulation, A1_EX2.S + A2_EX2.S, A1_EX2.S + A2_EX2.S)
    print("=" * 80)
    raise

simulates = A_VO.bisimulates(B_VO)
simulation = \
    maximumBisimulation(A_VO, A_VO, set(product(A_VO.S, A_VO.S))) | \
    maximumBisimulation(A_VO, B_VO, set(product(A_VO.S, B_VO.S))) | \
    maximumBisimulation(B_VO, A_VO, set(product(B_VO.S, A_VO.S))) | \
    maximumBisimulation(B_VO, B_VO, set(product(B_VO.S, B_VO.S)))

try:
    expect(simulates, False, "maximumBisimulation: simulates")
    expect(
        simulation,
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
        },
        "maximumBisimulation: simulation relation"
    )
except AssertionError:
    print("=" * 80)
    printRelation(simulation, A_VO.S + B_VO.S, A_VO.S + B_VO.S)
    print("=" * 80)
    raise

################################################################################
# deterministic finite automata minimization
#
# example presented in assignment 2 - exercise 2
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

expect(F.S, [('A', 'D'), ('B', 'F'), ('C', 'E')], "minimize: states")
expect(F.I, [('A', 'D')], "minimize: initial states")
expect(
    F.T,
    [
        (('A', 'D'), 0, ('B', 'F')),
        (('A', 'D'), 1, ('C', 'E')),
        (('B', 'F'), 0, ('A', 'D')),
        (('B', 'F'), 1, ('C', 'E')),
        (('C', 'E'), 0, ('A', 'D')),
        (('C', 'E'), 1, ('C', 'E'))
    ],
    "minimize: transitions"
)
expect(F.F, [('B', 'F')], "minimize: final states")

################################################################################
# asynchronous composition
################################################################################

# simple example presented in the lecture (p89)
A = LTS (
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

B = LTS (
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

composition = asynchronousComposition(A, B)

expect(
    composition.S,
    [
        (1, 5), (1, 6), (1, 7), (1, 8),
        (2, 5), (2, 6), (2, 7), (2, 8),
        (3, 5), (3, 6), (3, 7), (3, 8),
        (4, 5), (4, 6), (4, 7), (4, 8)
    ],
    "asynchronousComposition: states"
)
expect(
    composition.I,
    [(1, 5)],
    "asynchronousComposition: initial states"
)
expect(
    composition.Σ,
    ['a', 'b', 'c', 'd', 'e', 'f', 's'],
    "asynchronousComposition: alphabet"
)
expect(
    composition.T,
    [
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
    ],
    "asynchronousComposition: transitions"
)

# with partial order reduction
composition = asynchronousComposition(A, B, partialOrderReduction = lambda x: [x[-1]])

expect(
    composition.S,
    [(1, 5), (1, 6), (1, 7), (1, 8), (2, 8), (3, 8), (4, 8)],
    "partialOrderReduction: states"
)
expect(
    composition.I,
    [(1, 5)],
    "partialOrderReduction: initial states"
)
expect(
    composition.Σ,
    ['a', 'b', 'c', 'd', 'e', 'f', 's'],
    "partialOrderReduction: alphabet"
)
expect(
    composition.T,
    [
        ((1, 5), 'd', (1, 6)), ((1, 6), 'e', (1, 7)), ((1, 7), 'f', (1, 8)),
        ((1, 8), 'a', (2, 8)), ((2, 8), 'b', (3, 8)), ((3, 8), 'c', (4, 8)),
        ((4, 8), 's', (1, 5))
    ],
    "partialOrderReduction: transitions"
)

# assignment 3 - exercise 1
A = LTS (
    S = [1, 2, 3, 4],
    I = [1],
    Σ = ['a', 't', 's'],
    T = [
            (1, 'a', 2),
            (2, 't', 3),
            (3, 'a', 4),
            (4, 's', 4)
        ]
    )

B = LTS (
    S = [1, 2, 3],
    I = [1],
    Σ = ['b', 't', 's'],
    T = [
            (1, 'b', 2),
            (2, 't', 2),
            (2, 'b', 3),
            (3, 's', 1),
        ]
    )

composition = asynchronousComposition(A, B)

expect(
    composition.S,
    [
        (1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3),
        (3, 2), (3, 3), (4, 1), (4, 2), (4, 3)
    ],
    "asynchronousComposition: states"
)
expect(
    composition.I,
    [(1, 1)],
    "asynchronousComposition: initial states"
)
expect(
    composition.Σ,
    ['a', 'b', 's', 't'],
    "asynchronousComposition: alphabet"
)
expect(
    composition.T,
    [
        ((1, 1), 'a', (2, 1)), ((1, 1), 'b', (1, 2)),
        ((1, 2), 'a', (2, 2)), ((1, 2), 'b', (1, 3)),
        ((1, 3), 'a', (2, 3)), ((2, 1), 'b', (2, 2)),
        ((2, 2), 'b', (2, 3)), ((2, 2), 't', (3, 2)),
        ((3, 2), 'a', (4, 2)), ((3, 2), 'b', (3, 3)),
        ((3, 3), 'a', (4, 3)), ((4, 1), 'b', (4, 2)),
        ((4, 2), 'b', (4, 3)), ((4, 3), 's', (4, 1))
    ],
    "asynchronousComposition: transitions"
)

# assignment 3 - exercise 2
A = LTS (
    S = [1, 2, 3, 4],
    I = [1],
    Σ = ['a', 't', 's'],
    T = [
            (1, 't', 1),
            (1, 'a', 2),
            (2, 'a', 3),
            (3, 's', 4),
            (4, 'a', 4)
        ]
    )

B = LTS (
    S = ['A', 'B', 'C', 'D'],
    I = ['A'],
    Σ = ['b', 's'],
    T = [
            ('A', 'b', 'B'),
            ('B', 's', 'C'),
            ('C', 'b', 'D'),
            ('D', 'b', 'C')
        ]
    )

C = LTS (
    S = [5, 6, 7],
    I = [5],
    Σ = ['c', 't'],
    T = [
            (5, 'c', 6),
            (6, 'c', 7),
            (6, 't', 6)
        ]
    )

# checker automaton
D = LTS (
    S = ['X', 'Y', 'Z'],
    I = ['X'],
    Σ = ['a', 'b', 'c', 's', 't'],
    T = [
            ('X', 'a', 'X'),
            ('X', 'b', 'X'),
            ('X', 'c', 'X'),
            ('X', 't', 'Y'),
            ('Y', 'a', 'Y'),
            ('Y', 'b', 'Y'),
            ('Y', 'c', 'Y'),
            ('Y', 's', 'Z'),
            ('Z', 'a', 'Z'),
            ('Z', 'b', 'Z'),
            ('Z', 'c', 'Z')
        ]
    )

composition = asynchronousComposition(
        A,
        B,
        C,
        partialOrderReduction = lambda x: [x[-1]]
)

expect(
    composition.S,
    [
        (1, 'A', 5), (1, 'A', 6), (1, 'B', 6), (1, 'B', 7),
        (2, 'B', 6), (2, 'B', 7), (3, 'B', 6), (3, 'B', 7),
        (4, 'C', 6), (4, 'C', 7), (4, 'D', 6), (4, 'D', 7)
    ],
    "partialOrderReduction: states"
)
expect(
    composition.I,
    [(1, 'A', 5)],
    "partialOrderReduction: initial states"
)
expect(
    composition.Σ,
    ['a', 'b', 'c', 's', 't'],
    "partialOrderReduction: alphabet"
)
expect(
    composition.T,
    [
        ((1, 'A', 5), 'c', (1, 'A', 6)), ((1, 'A', 6), 'b', (1, 'B', 6)),
        ((1, 'B', 6), 'a', (2, 'B', 6)), ((1, 'B', 6), 'c', (1, 'B', 7)),
        ((1, 'B', 6), 't', (1, 'B', 6)), ((1, 'B', 7), 'a', (2, 'B', 7)),
        ((2, 'B', 6), 'a', (3, 'B', 6)), ((2, 'B', 7), 'a', (3, 'B', 7)),
        ((3, 'B', 6), 'c', (3, 'B', 7)), ((3, 'B', 6), 's', (4, 'C', 6)),
        ((3, 'B', 7), 's', (4, 'C', 7)), ((4, 'C', 6), 'b', (4, 'D', 6)),
        ((4, 'C', 7), 'b', (4, 'D', 7)), ((4, 'D', 6), 'b', (4, 'C', 6)),
        ((4, 'D', 7), 'b', (4, 'C', 7))
    ],
    "partialOrderReduction: transitions"
)

################################################################################
# tarjan's algorithm
################################################################################

# example from lecture slides (p108)
#
# SCC
# * [3, 7, 8]
# * [6]
# * [10, 11, 12]
states = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
edges = \
    [
        (1, 3),
        (1, 4),
        (2, 4),
        (2, 5),
        (2, 6),
        (3, 7), (7, 8), (8, 3), # scc
        (4, 8),
        (4, 9),
        (5, 9),
        (5, 10),
        (6, 6), # scc
        (8, 12),
        (9, 8),
        (9, 10),
        (10, 6),
        (10, 12), (12, 11), (11, 10), # scc
        (11, 6)
    ]

scc = tarjan(states, edges)

expect(scc, [[3, 7, 8], [6], [10, 11, 12]], "tarjan")

# example from wikipedia
#
# SCC
# * [1, 2, 3]
# * [4, 5]
# * [6, 7]
# * [8]
states = [1, 2, 3, 4, 5, 6, 7, 8]
edges = \
    [
        (1, 2), (2, 3), (3, 1), # scc
        (4, 2), (4, 3),
        (4, 5), (5, 4), # scc
        (5, 6),
        (6, 3),
        (6, 7), (7, 6), # scc
        (8, 5),
        (8, 7),
        (8, 8) # scc
    ]

scc = tarjan(states, edges)

expect(scc, [[1, 2, 3], [4, 5], [6, 7], [8]], "tarjan")

# assignment 3 - exercise 4
states = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']
edges = \
    [
        ('A', 'B'), ('A', 'E'),
        ('B', 'D'), ('B', 'F'),
        ('C', 'F'),
        ('D', 'A'), ('D', 'H'), ('D', 'I'),
        ('E', 'D'),
        ('F', 'G'), ('F', 'J'),
        ('G', 'C'), ('G', 'K'),
        ('H', 'E'), ('H', 'H'),
        ('I', 'E'), ('I', 'J'),
        ('J', 'G'), ('J', 'K')
    ]

scc = tarjan(states, edges)

expect(scc, [['A', 'B', 'D', 'E', 'H', 'I'], ['C', 'F', 'G', 'J']], "tarjan")

################################################################################
# BoolParser
################################################################################

import glob

files = glob.glob("bool/*.bool")

parser = BooleParser("../../../ex4/tests/t4.boole")

parser.parse()

import sys
sys.exit()

################################################################################
# BDD
################################################################################

from subprocess import run

a = BDD(0)
b = BDD(1)
#  c = a & b

#  print(a)
#  print(b)
#  print(a & b)
#  print(~(a & b))
#  print(a | b)
#
#  print(c.toDot())
#  with open("/tmp/a.dot", 'w') as f:
    #  f.write(c.toDot())
#  run(["dot", "-O", "-Tpdf", "/tmp/a.dot"])

#  import pdb; pdb.set_trace()
d = ~(a ^ b);
with open("/tmp/py_xor.dot", 'w') as f:
    f.write(d.toDot())
run(["dot", "-O", "-Tpdf", "/tmp/py_xor.dot"])
#
#  t3 = ~(a ^ b)
#  with open("/tmp/py_t3.dot", 'w') as f:
    #  f.write(t3.toDot())
#  run(["dot", "-O", "-Tpdf", "/tmp/py_t3.dot"])
