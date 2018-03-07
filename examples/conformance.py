#!/usr/bin/env python

from libmc import FA

Σ = ['a', 'b']

# automaton modelling the implementation
I = FA(
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

# automaton modelling the specification
S = FA(
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

# I conforms to S
conforms, ICPS, traces = I.conforms(S)

assert conforms
assert not traces

################################################################################
import utils

fname = "/tmp/conforms-I.pdf"
utils.dot2pdf(I.toDot(), fname)
utils.pdf2png(fname)

fname = "/tmp/conforms-S.pdf"
utils.dot2pdf(S.toDot(), fname)
utils.pdf2png(fname)

fname = "/tmp/conforms-product.pdf"
utils.dot2pdf(I.product(S).toDot(), fname)
utils.pdf2png(fname)

fname = "/tmp/conforms-power.pdf"
utils.dot2pdf(S.power().toDot(), fname)
utils.pdf2png(fname)

fname = "/tmp/conforms-complement.pdf"
utils.dot2pdf(S.power().complement().toDot(), fname)
utils.pdf2png(fname)

fname = "/tmp/conforms-true.pdf"
utils.dot2pdf(ICPS.toDot(), fname)
utils.pdf2png(fname)
################################################################################

# automaton modelling the implementation
I = FA(
    S = [1, 2, 3],
    I = [1],
    Σ = ['a', 'b'],
    T = [
        (1, 'a', 2),
        (1, 'b', 3),
    ],
    F = [2]
)

# automaton modelling the specification
S = FA(
    S = ['A', 'B', 'C'],
    I = ['A'],
    Σ = ['a', 'b'],
    T = [
        ('A', 'a', 'B'),
        ('A', 'b', 'C'),
    ],
    F = ['C']
)

# I doesn't conform to S
conforms, ICPS, traces = I.conforms(S)

assert not conforms
assert traces

fname = "/tmp/conforms-a.pdf"
utils.dot2pdf(I.toDot(), fname)
utils.pdf2png(fname)

fname = "/tmp/conforms-b.pdf"
utils.dot2pdf(S.toDot(), fname)
utils.pdf2png(fname)

fname = "/tmp/conforms-false.pdf"
utils.dot2pdf(ICPS.toDot(traces[0]), fname)
utils.pdf2png(fname)

# visualize non-conforming path
#  with open("/tmp/ICPS.dot", "w") as f:
    #  f.write(ICPS.toDot(traces[0]))
