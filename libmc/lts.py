from functools import reduce
from itertools import chain, combinations, product

from .bfs_dfs import dfs
from .maximumSimulation import maximumSimulation
from .maximumBisimulation import maximumBisimulation
from .printing import fa2dot

def powerset (s):
    """
    Returns the powerset of s.
    """
    return \
        [
            tuple(subset)
            for subset in chain.from_iterable(
                combinations(s, r)
                for r in range(len(s) + 1)
            )
        ]

class LTS:
    """
    Labelled Transition System (p31).

    Attributes:
        S: set of states
        I: set of initial states I ⊆ S
        Σ: input alphabet
        T: transition relation T ⊆ SxΣxS
    """
    def __init__ (self, S, I, Σ, T):
        self.S = S
        self.I = I
        self.Σ = Σ
        self.T = T

    def __repr__ (self):
        return \
            "LTS(" + \
            str(self.S) + ", " + \
            str(self.I) + ", " + \
            str(self.Σ) + ", " + \
            str(self.T) + \
            ")"

    def toDot (self, highlight = []):
        """
        Return LTS as Graphviz dot language string.

        Args:
            highlight (list of transitions - optional): highlight a given path

        Returns:
            string: .dot file tweaked for dot2tex
        """
        return fa2dot(self.S, self.I, self.Σ, self.T, [], highlight)

    def isComplete (self):
        """
        Completeness (p21): True if LTS is complete.
        """
        return len(self.I) > 0 and \
            reduce(lambda x, y: x and y,
                map(lambda x: len(x) > 0,
                    [
                        [ t for t in self.T if t[0] == s and t[1] == a ]
                        for s in self.S
                        for a in self.Σ
                    ]
                )
            )

    def isDeterministic (self):
        """
        Determinism (p21): True if LTS is deterministic.
        """
        return len(self.I) <= 1 and \
            reduce(lambda x, y: x and y,
                map(lambda x: len(x) <= 1,
                    [
                        [ t for t in self.T if t[0] == s and t[1] == a ]
                        for s in self.S
                        for a in self.Σ
                    ]
                )
            )

    def product (self, other, full=False):
        """
        Create product LTS.

        Args:
            other (LTS): another LTS
            full (bool - optional): create full product automaton if True, else
                only reachable states are included (default)
        """
        S = set() if not full else list(product(self.S, other.S))
        I = sorted(product(self.I, other.I))
        Σ = self.Σ
        T = [] if not full else \
            [
                (s, a, (t1[2], t2[2]))
                for s in S
                for a in Σ
                for t1 in self.T if t1[0] == s[0] and t1[1] == a
                for t2 in other.T if t2[0] == s[1] and t2[1] == a
            ]

        # reachability analysis
        if not full:
            transitions = \
                [
                    (s, a, (t1[2], t2[2]))
                    for s in list(product(self.S, other.S))
                    for a in Σ
                    for t1 in self.T if t1[0] == s[0] and t1[1] == a
                    for t2 in other.T if t2[0] == s[1] and t2[1] == a
                ]

            stack = list(I)

            def cache (successor): S.add(successor)

            def cached (successor): return successor in S

            def successors (current):
                for t in [ t for t in transitions if t[0] == current ]:
                    T.append(t)
                    yield t[2]

            dfs(stack, successors, cache=cache, cached=cached)

            S |= set(I)

        return LTS(S, I, Σ, T)

    def power (self):
        """Create power LTS."""
        S = powerset(self.S)
        I = [ tuple(self.I) ]
        Σ = self.Σ
        T = [
                (s1, a, tuple(sorted(s2)))
                for s1 in S
                for a in Σ
                for s2 in
                [{ _s for (s, _a, _s) in self.T if s in s1 and _a == a }]
            ]

        return LTS(S, I, Σ, T)

    def simulates (self, other, τ = []):
        """
        Simulation of LTS (p39).

        ∀ s ∊ other.I, ∃ t ∊ self.I [ s ≤ t ]

        Args:
            other (LTS): another LTS
            τ (optional): set of unobservable internal events

        Returns:
            bool: True if this LTS simulates the other
        """
        R0 = set(product(other.S, self.S))

        return all(
            any(
                (s1, s2) in maximumSimulation(other, self, R0, τ)
                for s2 in self.I
            )
            for s1 in other.I
        )

    def bisimulates (self, other, τ = []):
        """
        Bisimulation of LTS (p43).

        ∀ s ∊ self.I, ∃ t ∊ other.I [ s ≈ t ]

        Args:
            other (LTS): another LTS
            τ (optional): set of unobservable internal events

        Returns:
            bool: True if this LTS bisimulates the other
        """
        R0 = set(product(other.S, self.S))

        return all(
            any(
                (s1, s2) in maximumBisimulation(other, self, R0, τ)
                for s2 in self.I
            )
            for s1 in other.I
        )

    def trace (self, target, sources=None):
        """
        Tries to compute all traces to the target state (DFS).

        If no source states are given, the set of initial states is used.

        Args:
            target: target state
            sources (optional): set of initial states

        Returns:
            list: the trace or an empty list if target is unreachable
        """
        if sources is None: sources = self.I

        stack = [ (s, [s], []) for s in sources ]
        traces = []

        # state components used in DFS
        node = None
        path = None
        trace = None

        def enqueue (successor):
            stack.append(
                (successor[2], path + [successor[2]], trace + [successor])
            )

        def cache (successor): pass

        def cached (successor):
            if successor[2] == target:
                traces.append(trace + [successor])
                return True

            return False

        def successors (current):
            nonlocal node, path, trace
            (node, path, trace) = current
            return [
                t for t in self.T
                if t[0] == node and t[2] not in path[1:]
            ]

        dfs(stack, successors, enqueue=enqueue, cache=cache, cached=cached)

        return traces
