#!/usr/bin/env python

from libmc import FA

F = FA(
    S = [1, 2, 3],
    I = [1],
    Σ = ['a', 'b'],
    T = [
            (1, 'a', 2),
            (2, 'b', 3),
        ],
    F = [3]
)

C = F.complement()

assert C.S == F.S
assert C.I == F.I
assert C.Σ == F.Σ
assert C.T == F.T
assert C.F == [1, 2]
