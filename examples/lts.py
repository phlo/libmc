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

################################################################################

import utils

fname = "/tmp/milner-deterministic.pdf"
print("milner-deterministic")
print("=" * 80)
print(G.toDot())
with open("/tmp/milner-deterministic.dot", 'w') as f:
    f.write(G.toDot())
#  utils.dot2pdf(G.toDot(), fname, template="examples/dot2tex-template.tex")
utils.dot2pdf(G.toDot(), fname)
utils.pdf2png(fname)

fname = "/tmp/milner-deterministic-milkyway.pdf"
utils.dot2pdf(G.toDot(G.trace(4)), fname, template="examples/dot2tex-template.tex")
utils.pdf2png(fname)

fname = "/tmp/milner-nondeterministic.pdf"
utils.dot2pdf(B.toDot(), fname, template="examples/dot2tex-template.tex")
utils.pdf2png(fname)

fname = "/tmp/milner-nondeterministic-milkyway.pdf"
utils.dot2pdf(B.toDot(B.trace(9)), fname, template="examples/dot2tex-template.tex")
utils.pdf2png(fname)

fname = "/tmp/milner-product.pdf"
utils.dot2pdf(GB.toDot(), fname, template="examples/dot2tex-template.tex")
utils.pdf2png(fname)

fname = "/tmp/milner-power.pdf"
utils.dot2pdf(G.power().toDot(), fname, template="examples/dot2tex-template.tex")
utils.pdf2png(fname)
