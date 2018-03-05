#!/usr/bin/env python

from libmc import BDD, Boole

# evaluation
contradiction = Boole("a & !a")

assert not contradiction.evaluate({ 'a': True })
assert not contradiction.evaluate({ 'a': False })
assert contradiction.truthTable() == [
    ((False,), False),
    ((True,), False)
]

tautology = Boole("a | !a")

assert tautology.evaluate({ 'a': True })
assert tautology.evaluate({ 'a': False })
assert tautology.truthTable() == [
    ((False,), True),
    ((True,), True)
]

equivalence = Boole("a <-> b")

assert equivalence.evaluate({ 'a': True, 'b': True })
assert not equivalence.evaluate({ 'a': True, 'b': False })
assert equivalence.truthTable() == [
    ((False, False), True),
    ((False, True), False),
    ((True, False), False),
    ((True, True), True)
]

# convert to BDD
assert contradiction.toBDD() is BDD.false()

assert tautology.toBDD() is BDD.true()

assert equivalence.toBDD() is ~(BDD(0) ^ BDD(1))

# convert to AIG
assert contradiction.toAIG() == """\
aag 3 1 0 1 1
2
4
4 2 3
"""

assert tautology.toAIG() == """\
aag 3 1 0 1 1
2
5
4 3 2
"""

assert equivalence.toAIG() == """\
aag 6 2 0 1 3
2
4
7
6 9 11
8 2 4
10 3 5
"""
