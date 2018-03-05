#!/usr/bin/env python

from libmc import BDD

# constants
true  = BDD.true()
false = BDD.false()

# variables
a = BDD(0)
b = BDD(1)

assert a is BDD(0)
assert b is BDD(1)

# operators
~a
a & b
a | b
a ^ b

# contradiction
assert a & ~a == BDD.false()

# tautology
assert a | ~a == BDD.true()

# De Morgan
assert ~(a & b) == ~a | ~b

# equivalence (xnor): a ⇔ b
~(a ^ b)
assert ~(true ^ true) == true
assert ~(true ^ false) == false

# visualization
dot = (~(a ^ b)).toDot()

with open("xnor.dot", 'w') as f:
    f.write(dot)

with open("xnor.pdf", 'w') as f:
    import subprocess
    subprocess.run(["dot", "-Tpdf", "xnor.dot"], stdout=f)
