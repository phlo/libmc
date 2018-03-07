#!/usr/bin/env python

from libmc import FA

# (un)?sat
F = FA(
    S = [1, 2, 3, 4, 5, 6],
    I = [1],
    Σ = ['u', 'n', 's', 'a', 't'],
    T = [
            (1, 's', 4),
            (1, 'u', 2),
            (2, 'n', 3),
            (3, 's', 4),
            (4, 'a', 5),
            (5, 't', 6)
        ],
    F = [6]
)

# completeness
assert not F.isComplete()

# determinism
assert F.isDeterministic()

# acceptance
assert F.accepts("sat")
assert F.accepts("unsat")
assert not F.accepts("santa")

# complement
C = F.complement()

assert C.S == F.S
assert C.I == F.I
assert C.Σ == F.Σ
assert C.T == F.T
assert C.F == [1, 2, 3, 4, 5]

################################################################################
#  import utils
#
#  fname = "/tmp/fa.pdf"
#  utils.dot2pdf(F.toDot(), fname)
#  utils.pdf2png(fname)
