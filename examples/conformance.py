#!/usr/bin/env python

from libmc import FA

# common alphabet
Σ = ['a', 'b']

################################################################################
# implementation conforms to specification
################################################################################

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
# implementation does not conform to specification
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

# I does not conform to S
conforms, ICPS, traces = I.conforms(S)

assert not conforms
assert traces
