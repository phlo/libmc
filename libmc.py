""" Provides collection of tools for KV Model Checking."""

from functools import reduce
from itertools import chain, combinations, product

__author__  = "Florian Schroegendorfer"
__email__   = "florian.schroegendorfer@phlo.at"
__license__ = "GPLv3"
__version__ = "2017.3"

def powerset (s):
    """
    Returns the powerset of s.
    """
    return \
        [
            list(subset)
            for subset in chain.from_iterable(
                combinations(s, r)
                for r in range(len(s) + 1)
            )
        ]

def intersect (l1, l2):
    """
    Returns the intersection of two lists.
    """
    return [ x for x in l1 if x in l2 ]

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

            def enque (successor): stack.append(successor)

            def cache (successor): S.add(successor)

            def cached (successor): return successor in S

            def successors (current):
                for t in [ t for t in transitions if t[0] == current ]:
                    T.append(t)
                    yield t[2]

            dfs(stack, enque, cache, cached, successors)

            S |= set(I)

        return LTS(S, I, Σ, T)

    def power (self):
        """Create power LTS."""
        S = powerset(self.S)
        I = [ self.I ]
        Σ = self.Σ
        T = [
                (s1, a, sorted(set(s2)))
                for s1 in S
                for a in Σ
                for s2 in
                [[ _s for (s, _a, _s) in self.T if s in s1 and _a == a ]]
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

        def enque (successor):
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

        dfs(stack, enque, cache, cached, successors)

        return traces

class FA (LTS):
    """
    Finite Automata (p18).

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

    def toDot (self, highlight = []):
        """
        Return Graphviz dot language string.

        Args:
            highlight (list of transitions - optional): highlight a given path

        Returns:
            string: .dot file tweaked for dot2tex
        """
        return fa2dot(self.S, self.I, self.Σ, self.T, self.F, highlight)

    def product (self, other, full=False):
        """Create product automaton (p20)."""
        lts = super(FA, self).product(other, full)
        F = list(product(self.F, other.F))

        return FA(lts.S, lts.I, lts.Σ, lts.T, F)

################################################################################
    # TODO remove
    #  @staticmethod
    #  def product (*lts):
        #  assert(all(Σ == lts[0].Σ for Σ in lts[1:]))
#
        #  S = list(product(*[ A.S for A in lts ]))
        #  I = list(product(*[ A.I for A in lts ]))
        #  Σ = lts[0].Σ
        #  T = []
        #  #  T = [
                #  #  (s, a, (t1[2], t2[2]))
                #  #  for s in S
                #  #  for a in Σ
                #  #  for t1 in self.T if t1[0] == s[0] and t1[1] == a
                #  #  for t2 in other.T if t2[0] == s[1] and t2[1] == a
            #  #  ]
        #  #  T = [
                #  #  (s, a, xxx)
                #  #  for s in S
                #  #  for a in Σ
                #  #  for
#
        #  return LTS(S, I, Σ, T)

    def power (self):
        """Create power automaton (p22)."""
        lts = super(FA, self).power()
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

    def conforms (self, other, **kwargs):
        """
        Conformance test (p24).

        * L(self) ⊆ L(other)
        * L(self) ∩ L(other) = 0
        * self × C(P(other)) contains no reachable final state (implemented)

        Args:
            other (FA): the other FA to conform to

        Returns:
            bool: True if this FA conforms to the other
        """
        A = self.product(other.power().complement(), **kwargs);

        traces = list(filter(lambda x: x == True, [ A.trace(f) for f in A.F ]))

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

def maximumSimulation (A1, A2, R0, τ = []):
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
    def isReachable(traces, a):
        """Returns True if a trace of the form τ*a exists."""
        return any(
                all(t[1] in τ for t in trace[:-1]) and trace[-1][1] == a
                for trace in traces
        )

    # refine simulation relation
    R1 = \
        {
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

    # return relation if fixpoint is reached else recurse
    return R1 if R1 == R0 else maximumSimulation(A1, A2, R1, τ)

def maximumBisimulation (A1, A2, R0, τ = []):
    """
    Constructs the maximum bisimulation relation A1 ≈ A2 (p43).

    Can also be used to minimize a deterministic automaton by constructing
    the state equivalence relation using::

        maximumSimulation(A, A, (A.FxA.F)∪((A.S\A.F)x(A.S\A.F)))

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
    return \
        maximumSimulation(
            A2,
            A1,
            { (s, t) for (t, s) in maximumSimulation(A1, A2, R0, τ) },
            τ
        )

def asynchronousComposition (*lts, partialOrderReduction = None):
    """
    Args:
        *lts:
        partialOrderReduction (optional): local expansion function
            ``f: list(index) -> index``
    """
    S = set(product(*[ l.I for l in lts]))
    I = sorted(S)
    Σ = sorted(set.union(*[ set(l.Σ) for l in lts]))
    T = set()

    # number of components in the asynchronous composition
    numComponents = len(lts)

    # global symbols
    #  Γ = {
            #  a
            #  for l in lts
            #  for a in l.Σ
            #  if not [ _l for _l in lts if _l != l and a not in _l.Σ ]
        #  }
    Γ = set.intersection(*[ set(l.Σ) for l in lts ])

    #  print(Γ)

    # local symbols
    #  Λ = [
            #  [
                #  a
                #  for a in l.Σ
                #  if not [ _l for _l in lts if _l != l and a in _l.Σ ]
            #  ]
            #  for l in lts
        #  ]
    Λ = [ set(l.Σ) - Γ for l in lts ]

    #  print(Λ)

    # initialize dfs stack
    stack = list(I)

    # on-the-fly generation of reachable states (dfs)
    def enque (successor): stack.append(successor[2])

    def cache (successor):
        S.add(successor[2])
        T.add(successor)

    def cached (successor): return successor in T

    def successors (fromState):
        # local states
        local = [
                    i
                    for i in range(numComponents)
                    if all(
                        a in Λ[i]
                        for (s, a, t) in lts[i].T
                        if s == fromState[i]
                    )
                ]

        #  print("state = " + str(fromState))
        #  print("local = " + str(local))

        # list of components to expand
        expandComponents = \
            range(numComponents) if not local else \
            partialOrderReduction(local) if partialOrderReduction else \
            local

        # dictionary containing successors per symbol and component state
        _successors = {}

        for i in expandComponents:
            for (s, a, t) in [ t for t in lts[i].T if t[0] == fromState[i] ]:
                _successors.setdefault(a, {}).setdefault(i, []).append(t)

        # build expansion
        expansion = [
                        (fromState, a, toState)
                        for a in _successors
                        for toState in
                            product(*[
                                _successors[a].setdefault(i, [fromState[i]])
                                for i in range(numComponents)
                            ])
                    ]

        #  print("successors   = " + str(_successors))
        #  print("expansion    = " + str(sorted(expansion)))

        return expansion

    dfs(stack, enque, cache, cached, successors)

    return LTS(sorted(S), I, Σ, sorted(T))

def __bfs_dfs_aux__ (stack, enque, deque, cache, cached, successors, op):
    while stack:
        current = deque(stack)

        for successor in successors(current):
            if not cached(successor):
                cache(successor)
                enque(successor)

        if op: op(current)

def bfs (stack, enque, cache, cached, successors, op=None):
    deque = lambda s: s.pop(0)

    __bfs_dfs_aux__(stack, enque, deque, cache, cached, successors, op)

def dfs (stack, enque, cache, cached, successors, op=None):
    deque = lambda s: s.pop()

    __bfs_dfs_aux__(stack, enque, deque, cache, cached, successors, op)

def formatState (s):
    """Prettify a state's string representation for printing."""
    return str(s).replace("'", "").replace("[", "\{").replace("]", "\}")

def printRelation(relation, A, B):
    """Pretty print relation table in markdown format."""
    def formatPair(s, t): return \
        "(" + \
        formatState(s) + \
        ", " + \
        formatState(t) + \
        ")"

    # determine header column width (bold)
    headerWidth = max(
        max(len(str(s)) + 4 for s in A), max(len(str(t)) + 4 for t in B)
    )

    # determine content column width
    colWidth = max(len(formatPair(s, t)) for s in A for t in B)

    # set column width to the maximum
    if headerWidth > colWidth:
        colWidth = headerWidth

    # print header
    print("| " + "".ljust(colWidth) + " | " + " | ".join(
            ("**" + formatState(s) + "**").ljust(colWidth)
            for s in B
        ) + " |"
    )

    # print separator
    print("| " + " | ".join(
            "-" * colWidth
            for i in range(len(B) + 1)
        ) + " |"
    )

    # print table
    for s in A:
        print(
            "| " + ("**" + formatState(s) + "**").ljust(colWidth) + " | " +
            " | ".join(
                formatPair(s, t).ljust(colWidth)
                if (s, t) in relation else "".ljust(colWidth)
                for t in B
            ) + " |"
        )

def fa2dot (S, I, Σ, T, F, highlight = []):
    """
    Returns graphical representation of given automaton (using Graphviz).

    Args:
        S: set of states
        I: set of initial states I ⊆ S
        Σ: input alphabet
        T: transition relation T ⊆ SxΣxS
        F: set of final states F ⊆ S
        highlight (list of transitions - optional): highlight a given path

    Returns:
        string: .dot file tweaked for dot2tex
    """
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
