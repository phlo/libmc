from itertools import product

from .analysis import dfs
from .LTS import LTS

def asynchronousComposition (*lts, partialOrderReduction=None):
    """
    Asynchronous composition of LTS through interleaving (p84).

    * performs on-the-fly generation of reachable states
    * Partial Order Reduction can be applied by supplying a function
      **partialOrderReduction**, selecting the component to expand

    Args:
        *lts (variable argument list(LTS)): list of LTS to interleave
        partialOrderReduction (optional): function ``f: list(index) -> index``
            selecting the local component to expand
    """
    S = set(product(*[ l.I for l in lts ]))
    I = sorted(S)
    Σ = set.union(*[ set(l.Σ) for l in lts ])
    T = set()

    # set of component indices
    components = range(len(lts))

    # local symbols
    Λ = [
            {
                a
                for a in l.Σ
                if all(a not in _l.Σ for _l in lts if _l != l)
            }
            for l in lts
        ]

    # map of symbols to the set of components knowing that symbol
    Ψ = { a: { i for i in components if a in lts[i].Σ } for a in Σ }

    # initialize dfs stack
    stack = list(I)

    # on-the-fly generation of reachable states (dfs)
    def enqueue (successor): stack.append(successor[2])

    def cache (successor):
        S.add(successor[2])
        T.add(successor)

    def cached (successor): return successor in T

    def successors (fromState):
        # dictionary containing successors per symbol and component state
        nextStates = {}

        for i in components:
            for (s, a, t) in [ t for t in lts[i].T if t[0] == fromState[i] ]:
                nextStates.setdefault(a, {}).setdefault(i, []).append(t)

        # perform partial order reduction
        if partialOrderReduction:

            # index of components with local states
            local = [
                        i
                        for i in components
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

            # partial expansion
            if local:
                local = partialOrderReduction(local)

                # unset successors of skipped components
                for a in nextStates:
                    for i in { i for i in components if i not in local }:
                        if i in nextStates[a]:
                            del nextStates[a][i]

        # build expansion
        expansion = [
                        (fromState, a, toState)
                        for a in nextStates
                        if Ψ[a] == nextStates[a].keys()
                        for toState in
                            product(*[
                                nextStates[a].setdefault(i, [fromState[i]])
                                for i in components
                            ])
                    ]

        return expansion

    dfs(stack, successors, enqueue=enqueue, cache=cache, cached=cached)

    return LTS(sorted(S), I, sorted(Σ), sorted(T))
