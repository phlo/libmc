from functools import reduce
from itertools import chain, combinations, product

from .printing import fa2dot, fa2tex
from .traversal import dfs

def powerset (s):
    """Returns the powerset of s."""
    return [
        list(subset)
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
        return "LTS(" + \
            str(self.S) + ", " + \
            str(self.I) + ", " + \
            str(self.Σ) + ", " + \
            str(self.T) + \
        ")"

    def toDot (self, highlight=[]):
        """
        Return LTS as `Graphviz <https://www.graphviz.org/>`_ dot language
        string.

        Args:
            highlight (list of transition lists - optional): highlight the
                given paths

        Returns:
            string: .dot file tweaked for dot2tex
        """
        return fa2dot(self.S, self.I, self.Σ, self.T, [], highlight)

    def toTex (self, highlight=[]):
        """
        Return LTS as TikZ based LaTeX figure (tikzpicture).

        Args:
            highlight (list of transition lists - optional): highlight the
                given paths

        Returns:
            string: .tex file (tikzpicture)

        Note:
            Requires manual positioning!
        """
        return fa2tex(self.S, self.I, self.Σ, self.T, [], highlight)

    def isComplete (self):
        """Completeness (p21): True if LTS is complete."""
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
        """Determinism (p21): True if LTS is deterministic."""
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

    @classmethod
    def _generateReachable (cls, initial, transitions):
        S = []
        T = []

        stack = list(initial)

        def cache (succ): S.append(succ)

        def cached (succ): return succ in S

        def successors (cur):
            for t in filter(lambda t: t[0] == cur and t not in T, transitions):
                T.append(t)
                yield t[2]

        dfs(stack, successors, cache=cache, cached=cached)

        S.extend(s for s in initial if s not in S)

        return (sorted(S), sorted(T))

    def product (self, other, full=False):
        """
        Create product automaton (p20).

        Args:
            other (LTS): another LTS
            full (bool - optional): create full automaton if True, else
                only reachable states are included (default)
        """
        S = sorted(product(self.S, other.S))
        I = sorted(product(self.I, other.I))
        T = [
                (s, a, (t1, t2))
                for s in S
                for a in self.Σ
                for (s1, a1, t1) in self.T if s1 == s[0] and a1 == a
                for (s2, a2, t2) in other.T if s2 == s[1] and a2 == a
            ]

        if not full:
            S, T = self._generateReachable(I, T)

        return LTS(S, I, self.Σ, T)

    def power (self, full=False):
        """
        Create power automaton (p22).

        Args:
            full (bool - optional): create full automaton if True, else
                only reachable states are included (default)
        """
        S = powerset(self.S)
        I = [ self.I ]
        T = [
                (s1, a, sorted(s2))
                for s1 in S
                for a in self.Σ
                for s2 in
                [{ t for (s, _a, t) in self.T if s in s1 and _a == a }]
            ]

        if not full:
            S, T = self._generateReachable(I, T)

        return LTS(S, I, self.Σ, T)

    def simulates (self, other, τ=[]):
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

    def bisimulates (self, other, τ=[]):
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
            list: all paths (list of transitions) to the target or an empty
            list if it is unreachable
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
            node, path, trace = current
            return [
                t for t in self.T
                if t[0] == node and t[2] not in path[1:]
            ]

        dfs(stack, successors, enqueue=enqueue, cache=cache, cached=cached)

        return traces

def maximumSimulation (A1, A2, R0, τ=[]):
    """
    Constructs the maximum simulation relation A1 ≲ A2 (p36).

    To get the *full* maximum simulation between two LTS A1 and A2 build
    the union of all possible permutations::

        fullSimulationRelation =
            maximumSimulation(A1, A1, set(product(A1.S, A1.S))) |
            maximumSimulation(A1, A2, set(product(A1.S, A2.S))) |
            maximumSimulation(A2, A1, set(product(A2.S, A1.S))) |
            maximumSimulation(A2, A2, set(product(A2.S, A2.S)))

    Args:
        A1 (LTS): some LTS
        A2 (LTS): another LTS
        R0 (set): the starting relation, e.g. A1.SxA2.S
        τ (optional): set of unobservable internal events

    Returns:
        set: A1 ≲ A2 ⊆ R0 - the maximum simulation relation
    """
    def isReachable (traces, a):
        """Returns True if a trace of the form τ*a exists."""
        return any(
            all(t[1] in τ for t in trace[:-1]) and trace[-1][1] == a
            for trace in traces
        )

    # refine simulation relation
    R = {
            (s, t)
            for (s, t) in R0
            # ∀ a ∈ Σ, s' ∈ S [ s -a> s' ]
            if all(
                # ∃ t' ∈ S [ t -a> t' ∧ s' ≲ t' ]
                any(
                    # s' ≲ t'
                    (_s, _t) in R0
                    # { t' ∈ S | t -a> t' }
                    for _t in A2.S
                    if isReachable(A2.trace(_t, [t]), a)
                )
                # { (a, s') ∈ ΣxS | s -a> s' }
                for (a, _s) in
                {
                    (a, _s)
                    for a in set(A1.Σ) - set(τ)
                    for _s in A1.S
                    if isReachable(A1.trace(_s, [s]), a)
                }
            )
        }

    # return relation if fixpoint is reached else recurs
    return R if R == R0 else maximumSimulation(A1, A2, R, τ)

def maximumBisimulation (A1, A2, R0, τ=[]):
    """
    Constructs the maximum bisimulation relation A1 ≈ A2 (p43).

    Can also be used to minimize a deterministic automaton by constructing
    the state equivalence relation using::

        maximumBisimulation(A, A, (A.FxA.F)∪((A.S\A.F)x(A.S\A.F)))

    To get the *full* maximum bisimulation between two LTS A1 and A2 build
    the union of all possible permutations::

        fullSimulationRelation =
            maximumBisimulation(A1, A1, set(product(A1.S, A1.S))) |
            maximumBisimulation(A1, A2, set(product(A1.S, A2.S))) |
            maximumBisimulation(A2, A1, set(product(A2.S, A1.S))) |
            maximumBisimulation(A2, A2, set(product(A2.S, A2.S)))

    Args:
        A1 (LTS): some LTS
        A2 (LTS): another LTS
        R0 (set): the starting relation, e.g. A1.SxA2.S
        τ (optional): set of unobservable internal events

    Returns:
        set: A1 ≈ A2 ⊆ R0 - the maximum simulation relation
    """
    return maximumSimulation(
        A2,
        A1,
        { (s, t) for (t, s) in maximumSimulation(A1, A2, R0, τ) },
        τ
    )

def asynchronousComposition (*lts, partialOrderReduction=None):
    """
    Asynchronous composition of two or more LTS through interleaving (p84).

    * performs on-the-fly generation of reachable states
    * Partial Order Reduction can be applied by supplying a function
      **partialOrderReduction**, selecting the components to expand

    Args:
        *lts (variable argument list(LTS)): list of LTS to interleave

    Keyword Args:
        partialOrderReduction (optional): function ``f: list(index) ->
            list(index)`` selecting the local components to expand
    """
    S = set(product(*[ l.I for l in lts ]))
    I = sorted(S)
    Σ = { a for l in lts for a in l.Σ }
    T = []

    # set of component indices
    components = range(len(lts))

    # local symbols
    Λ = [
            {
                a
                for a in l.Σ
                if all(a not in _l.Σ for _l in lts if _l is not l)
            }
            for l in lts
        ]

    # map of symbols to the set of components knowing that symbol
    Ψ = { a: { i for i in components if a in lts[i].Σ } for a in Σ }

    # initialize dfs stack
    stack = [ (i, [i]) for i in I ]

    # current path during dfs (to detect back edges)
    path = None

    # on-the-fly generation of reachable states (dfs)
    def enqueue (successor): stack.append((successor, path + [successor]))

    def cache (successor): S.add(successor)

    def cached (successor): return successor in S

    def successors (current):
        nonlocal path
        fromState, path = current

        # dictionary containing successors per symbol and component
        nextStates = {}
        for i in components:
            for (s, a, t) in [ t for t in lts[i].T if t[0] == fromState[i] ]:
                nextStates.setdefault(a, {}).setdefault(i, []).append(t)

        # generates all successors of a given symbol
        def toStates (a):
            return product(*[
                nextStates[a].get(i, [fromState[i]]) for i in components
            ])

        # perform partial order reduction
        if partialOrderReduction:

            # indices of local components
            local = [
                i for i in components
                if
                    # component i has a successor
                    any(i in nextStates[a] for a in nextStates)
                    and
                    # all transitions of component i are local
                    all(
                        a in Λ[i]
                        for a in nextStates
                        if i in nextStates[a]
                    )
            ]

            # current state is local
            if local:

                # select component for partial expansion
                local = partialOrderReduction(local)

                # fully expand cycles with only partial expansion
                expandCycle = any(
                    any(s in path for s in toStates(a))
                    for i in local
                    for a in Λ[i]
                    if a in nextStates
                )

                # partial expansion - remove successors of skipped components
                if not expandCycle:
                    for a in nextStates:
                        for i in filter(lambda x: x not in local, components):
                            if i in nextStates[a]:
                                del nextStates[a][i]

        # build expansion
        transitions = [
            (fromState, a, toState)
            for a in sorted(nextStates.keys(), reverse=True)
            if Ψ[a] == nextStates[a].keys()
            for toState in toStates(a)
        ]

        # add transitions
        T.extend(transitions)

        # return expansion
        return [ t for _, _, t in transitions ]

    dfs(stack, successors, enqueue=enqueue, cache=cache, cached=cached)

    return LTS(sorted(S), I, sorted(Σ), sorted(T))
