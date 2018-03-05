#!/usr/bin/env python

from libmc import FA

# nondeterministic version of Milner's vending machine
B = FA(
    S = [1, 2, 3, 4, 5],
    I = [1],
    Σ = ['p', 'd', 'm'],
    T = [
            (1, 'p', 2),
            (1, 'p', 3),
            (2, 'd', 4),
            (3, 'm', 5),
        ],
    F = [4, 5]
)

assert not B.isComplete()
assert not B.isDeterministic()

# power automaton
P = B.power()

assert P.isComplete()
assert P.isDeterministic()

assert P.S == [(), (1,), (2, 3), (4,), (5,)]
assert P.I == [(1,)]
assert P.Σ == ['p', 'd', 'm']
assert P.T == [
    ((), 'd', ()),
    ((), 'm', ()),
    ((), 'p', ()),
    ((1,), 'd', ()),
    ((1,), 'm', ()),
    ((1,), 'p', (2, 3)),
    ((2, 3), 'd', (4,)),
    ((2, 3), 'm', (5,)),
    ((2, 3), 'p', ()),
    ((4,), 'd', ()),
    ((4,), 'm', ()),
    ((4,), 'p', ()),
    ((5,), 'd', ()),
    ((5,), 'm', ()),
    ((5,), 'p', ())
]
assert P.F == [(4,), (5,)]

################################################################################

import utils

fname = "/tmp/milner-fa-nondeterministic.pdf"
utils.dot2pdf(B.toDot(), fname)
utils.pdf2png(fname)

fname = "/tmp/milner-fa-power.pdf"
utils.dot2pdf(P.toDot(), fname)
utils.pdf2png(fname)
