from itertools import product

from .lts import LTS, maximumBisimulation
from .printing import fa2dot

def intersect (l1, l2):
    """
    Returns the intersection of two lists.
    """
    return [ x for x in l1 if x in l2 ]

class FA (LTS):
    """
    Finite Automaton (p18).

    Attributes:
        S: set of states
        I: set of initial states I ⊆ S
        Σ: input alphabet
        T: transition relation T ⊆ SxΣxS
        F: set of final states F ⊆ S
    """
    def __init__ (self, S, I, Σ, T, F):
        super(FA, self).__init__(S, I, Σ, T)
        self.F = F

    def __repr__ (self):
        return \
            "FA(" + \
            str(self.S) + ", " + \
            str(self.I) + ", " + \
            str(self.Σ) + ", " + \
            str(self.T) + ", " + \
            str(self.F) + \
            ")"

    def toDot (self, highlight=[]):
        """
        Return `Graphviz <https://www.graphviz.org/>`_ dot language string.

        Args:
            highlight (list of transitions - optional): highlight a given path

        Returns:
            string: .dot file tweaked for dot2tex
        """
        return fa2dot(self.S, self.I, self.Σ, self.T, self.F, highlight)

    def product (self, other, full=False):
        """
        Create product automaton (p20).

        Args:
            other (FA): another FA
            full (bool - optional): create full product automaton if True, else
                only reachable states are included (default)
        """
        lts = super(FA, self).product(other, full)
        F = sorted(set(lts.S) & set(product(self.F, other.F)))

        return FA(lts.S, lts.I, lts.Σ, lts.T, F)

    def power (self, full=False):
        """
        Create power automaton (p22).

        Args:
            full (bool - optional): create full product automaton if True, else
                only reachable states are included (default)
        """
        lts = super(FA, self).power(full)
        F = [ s for s in lts.S if intersect(self.F, s) ]

        return FA(lts.S, lts.I, lts.Σ, lts.T, F)

    def complement (self):
        """Create complement automaton (p23)."""
        S = self.S
        I = self.I
        Σ = self.Σ
        T = self.T
        F = [ s for s in S if s not in self.F ]

        return FA(S, I, Σ, T, F)

    def accepts (self, word):
        """
        Test acceptance of a given word.

        Args:
            word (list): the word to check

        Returns:
            bool: True if the word is accepted by the automaton
        """
        def _accepts (state, word):
            if not word:
                return True if state in self.F else False
            else:
                return any(
                    _accepts(_s, word[1:])
                    for (s, a, _s) in self.T
                    if s == state and a == word[0]
                )

        return any(_accepts(i, word) for i in self.I)

    def conforms (self, other, full=False):
        """
        Conformance test (p24).

        * L(self) ⊆ L(other)
        * L(self) ∩ L(other) = 0
        * self × C(P(other)) contains no reachable final state (implemented)

        Args:
            other (FA): the other FA to conform to

        Returns:
            (bool, FA, list): a triple containing:

            * the result of the conformance test
            * the generated checker automaton self × C(P(other))
            * all traces from initial to final states
        """
        A = self.product(other.power(full).complement(), full);

        traces = [ t for f in A.F for t in A.trace(f) if t ]

        return ( not traces, A, traces )

    def minimize (self):
        """
        Minimization of Deterministic Finite Automata (p44).
        """
        notFinal = set(self.S) - set(self.F)

        bisimulation = \
            {
                (a, b)
                for (a, b) in
                    maximumBisimulation(
                        self,
                        self,
                        set(product(self.F, self.F)) | \
                        set(product(notFinal, notFinal))
                    )
                if self.S.index(a) < self.S.index(b)
            }

        redundantStates = { b for (a, b) in bisimulation }

        S = [
                tuple([s] + [ b for (a, b) in bisimulation if a == s ])
                for s in self.S if s not in redundantStates
            ]
        I = [ s for s in S if any(i in s for i in self.I) ]
        T = [
                (s, a, t)
                for s in S
                for t in S
                for a in self.Σ
                if any(
                    (_s, a, _t) in self.T
                    for _s in s if _s not in redundantStates
                    for _t in t if _t
                )
            ]
        F = [ s for s in S if any(f in s for f in self.F) ]

        return FA(S, I, self.Σ, T, F)
