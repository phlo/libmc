""" Provides collection of tools for KV Model Checking."""

import re
from functools import reduce
from itertools import chain, combinations, product

__author__  = "Florian Schroegendorfer"
__email__   = "florian.schroegendorfer@phlo.at"
__license__ = "GPLv3"
__version__ = "2017.1"

# powerset of s
def powerset (s):
    return [ list(subset) for subset in chain.from_iterable(
            combinations(s, r) for r in range(len(s) + 1)) ]

# intersection of lists
def intersect (l1, l2):
    return [ x for x in l1 if x in l2 ]

# labelled transition system (p31)
class LTS:

    def __init__ (self, S, I, Σ, T):
        self.S = S
        self.I = I
        self.Σ = Σ
        self.T = T

    # tries to compute a trace from an initial to the target state (DFS)
    # returns an empty list iff target is unreachable
    def trace (self, target):
        stack = [ (s, [s], []) for s in self.I ]
        while stack:
            (node, path, trace) = stack.pop()
            for t in [ t for t in self.T if t[0] == node and t[2] not in path ]:
                if t[2] == target:
                    return trace + [t]
                else:
                    stack.append((t[2], path + [t[2]], trace + [t]))
        return []

# finite automata (p18)
class FA (LTS):

    def __init__ (self, S, I, Σ, T, F):
        super(FA, self).__init__(S, I, Σ, T)
        self.F = F

    def toDot (self, highlight=[]):
        return fa2dot(self.S, self.I, self.Σ, self.T, self.F, highlight)

    def toLatex (self):
        return fa2dot2texi(self.S, self.I, self.Σ, self.T, self.F)

    # True iff automaton is complete (p21)
    def isComplete (self):
        return len(self.I) > 0 and \
            reduce(lambda x, y: x and y,
                map(lambda x: len(x) > 0,
                    [
                        [ t for t in self.T if t[0] == s and t[1] == a ]
                        for s in self.S
                        for a in self.Σ
                    ]))

    # True iff automaton is deterministic (p21)
    def isDeterministic (self):
        return len(self.I) <= 1 and \
            reduce(lambda x, y: x and y,
                map(lambda x: len(x) <= 1,
                    [
                        [ t for t in self.T if t[0] == s and t[1] == a ]
                        for s in self.S
                        for a in self.Σ
                    ]))

    # create product automaton (p20)
    def product (self, other):
        S = list(product(self.S, other.S))
        I = list(product(self.I, other.I))
        Σ = self.Σ
        T = [
                (s, a, (t1[2], t2[2]))
                for s in S
                for a in Σ
                for t1 in self.T if t1[0] == s[0] and t1[1] == a
                for t2 in other.T if t2[0] == s[1] and t2[1] == a
            ]
        F = list(product(self.F, other.F))

        return FA(S, I, Σ, T, F)

    # create power automaton (p22)
    def power (self):
        S = powerset(self.S)
        I = [ self.I ]
        Σ = self.Σ
        T = [
                (s1, a, sorted(list(set(s2))))
                for s1 in S
                for a in Σ
                for s2 in [[ t[2] for t in self.T if t[0] in s1 and t[1] == a ]]
            ]
        F = [ s for s in S if intersect(self.F, s) ]

        return FA(S, I, Σ, T, F)

    # create complement automaton (p23)
    def complement (self):
        S = self.S
        I = self.I
        Σ = self.Σ
        T = self.T
        F = [ s for s in S if s not in self.F ]

        return FA(S, I, Σ, T, F)

    # conformance test (p24):
    # * L(self) ⊆ L(other)
    # * iff L(self) ∩ L(other) = 0
    # * iff self × C(P(other)) contains no reachable final state (implemented)
    def conforms (self, other):

        A = self.product(other.power().complement());

        traces = list(filter(lambda x: x == True, [ A.trace(f) for f in A.F ]))

        return [ not traces, A, traces ]

# prettify states for printing
def formatState (s):
    return str(s).replace("'", "").replace("[", "\{").replace("]", "\}")

# returns graphical representation of given automaton (LaTex - pure TikZ)
def fa2tex (S, I, Σ, T, F):
    tex = """\
% requires following LaTex preamble:
% \\usepackage{pgf}
% \\usepackage{tikz}
% \\usetikzlibrary{arrows,automata}
\\begin{tikzpicture}[shorten >=1pt,node distance=2cm,auto,initial text=]

"""
    # generate nodes
    tex += "  % manual positioning required!\n"
    for s in S:
        tex += "  {:<26}{:<28}{};\n".format(
            "\\node[state" + \
                (",initial" if s in I else ",accepting" if s in F else "") + \
                "]",
            "({})".format(s),
            "{{${}$}}".format(formatState(s)))

    tex += "\n"

    # generate paths
    for t in T:
        tex += "  {:<10}{:<6}{:<20}{:<14}{:<6}{};\n".format(
            "\\path[->]",
            "({})".format(t[0]),
            "edge",
            "node",
            "{{${}$}}".format(t[1]),
            "({})".format(t[2]))

    tex += "\\end{tikzpicture}"
    return tex

# returns graphical representation of given automaton (using GraphViz)
# * generated .dot file tweaked for dot2tex
# * optional: highlight a given path (list of transitions)
def fa2dot (S, I, Σ, T, F, highlight=[]):
    tex = """\
digraph FSM {
  node [style="state"]
  edge [lblstyle="auto"]
"""
    # generate states
    for s in S:
        style = []
        if s in I: style.append("initial")
        if s in F: style.append("accepting")
        if [ t for t in highlight if s == t[0] or s == t[2] ]:
            style.append("draw=red")

        tex += "  \"{}\"{};\n".format(
                formatState(s),
                " [style=\"state," + ','.join(style) + "\"]" if style else "")

    # generate transitions
    for t in T:
        tex += "  \"{}\" -> \"{}\" [label=\"{}\"{}];\n".format(
                formatState(t[0]),
                formatState(t[2]),
                t[1],
                ",style=\"draw=red\"" if t in highlight else "")

    tex += "}"
    return tex

# returns graphical representation of given automaton (LaTex - using dot2texi)
def fa2dot2texi (S, I, Σ, T, F):
    tex = """\
% requires following LaTex preamble:
% \\usepackage{pgf}
% \\usepackage{tikz}
% \\usepackage{dot2texi}
% \\usetikzlibrary{arrows,shapes,automata}

\\begin{tikzpicture}[>=latex',scale=1]
  \\begin{dot2tex}[dot,tikz,mathmode,codeonly,styleonly]
"""
    tex += re.sub("^", "  ", fa2dot(S, I, Σ, T, F), 0, re.MULTILINE)
    tex += """
  \\end{dot2tex}
\\end{tikzpicture}\
"""
    return tex
