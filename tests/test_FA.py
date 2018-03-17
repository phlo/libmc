import unittest

from libmc import FA

class TestFA (unittest.TestCase):

    def setUp (self):
        self.maxDiff = None

    # FA I presented in assignment 1 - exercise 1
    I_EX1 = FA (
        S = [1, 2, 3, 4],
        I = [1],
        Σ = ['a', 'b'],
        T = [
                (1, 'b', 2),
                (2, 'b', 3),
                (2, 'b', 4),
                (3, 'a', 1),
                (3, 'b', 3),
                (4, 'b', 3)
            ],
        F = [4]
    )

    # FA S presented in assignment 1 - exercise 1
    S_EX1 = FA (
        S = ['A', 'B', 'C', 'D'],
        I = ['A'],
        Σ = ['a', 'b'],
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

    ############################################################################
    # completeness and determinism
    ############################################################################

    # complete and deterministic
    def test_complete_and_deterministic (self):
        F = FA (
            S = [1, 2],
            I = [1],
            Σ = ['a', 'b'],
            T = [
                    (1, 'a', 2),
                    (1, 'b', 2),
                    (2, 'a', 2),
                    (2, 'b', 2)
                ],
            F = [2]
        )

        self.assertEqual(F.isComplete(), True, "FA.isComplete")
        self.assertEqual(F.isDeterministic(), True, "FA.isDeterministic")

    # complete but not deterministic
    def test_complete_and_not_deterministic (self):
        F = FA (
            S = [1, 2],
            I = [1],
            Σ = ['a', 'b'],
            T = [
                    (1, 'a', 2),
                    (1, 'b', 2),
                    (2, 'a', 2), # non deterministic transition
                    (2, 'a', 2),
                    (2, 'b', 2)
                ],
            F = [2]
        )

        self.assertEqual(F.isComplete(), True, "FA.isComplete")
        self.assertEqual(F.isDeterministic(), False, "FA.isDeterministic")

    # not complete but deterministic
    def test_not_complete_and_deterministic (self):
        F = FA (
            S = [1, 2],
            I = [1],
            Σ = ['a', 'b'],
            T = [(1, 'a', 2)], # only one transition
            F = [2]
        )

        self.assertEqual(F.isComplete(), False, "FA.isComplete")
        self.assertEqual(F.isDeterministic(), True, "FA.isDeterministic")

    # not complete and not deterministic
    def test_not_complete_and_not_deterministic (self):
        F = FA (
            S = [1, 2],
            I = [1, 2], # more than one initial state
            Σ = ['a', 'b'],
            T = [
                    (1, 'a', 2),
                    (1, 'b', 2),
                    # no transitions for state 2
                ],
            F = [2]
        )

        self.assertEqual(F.isComplete(), False, "FA.isComplete")
        self.assertEqual(F.isDeterministic(), False, "FA.isDeterministic")

    ############################################################################
    # product
    #
    # example presented in assignment 1 - exercise 1
    ############################################################################
    def test_product (self):
        P = self.I_EX1.product(self.S_EX1)

        self.assertEqual(
            P.S,
            [
                (1, 'A'),
                (1, 'C'),
                (1, 'D'),
                (2, 'A'),
                (2, 'B'),
                (3, 'A'),
                (3, 'B'),
                (3, 'C'),
                (4, 'A'),
                (4, 'B'),
                (4, 'C'),
            ],
            "FA.product: states"
        )
        self.assertEqual(P.I, [(1, 'A')], "FA.product: initial states")
        self.assertEqual(P.Σ, self.I_EX1.Σ, "FA.product: alphabet")
        self.assertEqual(
            P.T,
            [
                ((1, 'A'), 'b', (2, 'A')),
                ((1, 'A'), 'b', (2, 'B')),
                ((1, 'D'), 'b', (2, 'A')),
                ((2, 'A'), 'b', (3, 'A')),
                ((2, 'A'), 'b', (3, 'B')),
                ((2, 'A'), 'b', (4, 'A')),
                ((2, 'A'), 'b', (4, 'B')),
                ((2, 'B'), 'b', (3, 'C')),
                ((2, 'B'), 'b', (4, 'C')),
                ((3, 'A'), 'a', (1, 'C')),
                ((3, 'A'), 'a', (1, 'D')),
                ((3, 'A'), 'b', (3, 'A')),
                ((3, 'A'), 'b', (3, 'B')),
                ((3, 'B'), 'a', (1, 'D')),
                ((3, 'B'), 'b', (3, 'C')),
                ((3, 'C'), 'a', (1, 'C')),
                ((3, 'C'), 'a', (1, 'D')),
                ((4, 'A'), 'b', (3, 'A')),
                ((4, 'A'), 'b', (3, 'B')),
                ((4, 'B'), 'b', (3, 'C')),
            ],
            "FA.product: transitions"
        )
        self.assertEqual(P.F, [(4, 'B')], "FA.product: final states")

    def test_product_full (self):
        P = self.I_EX1.product(self.S_EX1, True)

        self.assertEqual(
            P.S,
            [
                (1, 'A'), (1, 'B'), (1, 'C'), (1, 'D'),
                (2, 'A'), (2, 'B'), (2, 'C'), (2, 'D'),
                (3, 'A'), (3, 'B'), (3, 'C'), (3, 'D'),
                (4, 'A'), (4, 'B'), (4, 'C'), (4, 'D')
            ],
            "FA.product: states"
        )
        self.assertEqual(P.I, [(1, 'A')], "FA.product: initial states")
        self.assertEqual(P.Σ, self.I_EX1.Σ, "FA.product: alphabet")
        self.assertEqual(
            P.T,
            [
                ((1, 'A'), 'b', (2, 'A')),
                ((1, 'A'), 'b', (2, 'B')),
                ((1, 'B'), 'b', (2, 'C')),
                ((1, 'D'), 'b', (2, 'A')),
                ((2, 'A'), 'b', (3, 'A')),
                ((2, 'A'), 'b', (3, 'B')),
                ((2, 'A'), 'b', (4, 'A')),
                ((2, 'A'), 'b', (4, 'B')),
                ((2, 'B'), 'b', (3, 'C')),
                ((2, 'B'), 'b', (4, 'C')),
                ((2, 'D'), 'b', (3, 'A')),
                ((2, 'D'), 'b', (4, 'A')),
                ((3, 'A'), 'a', (1, 'C')),
                ((3, 'A'), 'a', (1, 'D')),
                ((3, 'A'), 'b', (3, 'A')),
                ((3, 'A'), 'b', (3, 'B')),
                ((3, 'B'), 'a', (1, 'D')),
                ((3, 'B'), 'b', (3, 'C')),
                ((3, 'C'), 'a', (1, 'C')),
                ((3, 'C'), 'a', (1, 'D')),
                ((3, 'D'), 'b', (3, 'A')),
                ((4, 'A'), 'b', (3, 'A')),
                ((4, 'A'), 'b', (3, 'B')),
                ((4, 'B'), 'b', (3, 'C')),
                ((4, 'D'), 'b', (3, 'A'))
            ],
            "FA.product: transitions"
        )
        self.assertEqual(P.F, [(4, 'B')], "FA.product: final states")

    ############################################################################
    # complement
    #
    # example presented in assignment 1 - exercise 1
    ############################################################################
    def test_complement (self):
        C = self.I_EX1.complement()

        self.assertEqual(C.S, self.I_EX1.S, "FA.complement: states")
        self.assertEqual(C.I, self.I_EX1.I, "FA.complement: initial states")
        self.assertEqual(C.Σ, self.I_EX1.Σ, "FA.complement: alphabet")
        self.assertEqual(C.T, self.I_EX1.T, "FA.complement: transitions")
        self.assertEqual(C.F, [1, 2, 3], "FA.complement: final states")

    ############################################################################
    # power
    #
    # example presented in assignment 1 - exercise 1
    ############################################################################
    def test_power (self):
        P = self.S_EX1.power()

        self.assertTrue(P.isComplete(), "FA.power: isComplete")
        self.assertTrue(P.isDeterministic(), "FA.power: isDeterministic")

        self.assertEqual(
            P.S,
            [
                ['A'],
                ['A', 'B'],
                ['A', 'B', 'C'],
                ['C', 'D'],
            ],
            "FA.power: states"
        )

        self.assertEqual(P.Σ, self.S_EX1.Σ, "FA.power: alphabet")

        self.assertEqual(
            P.T,
            [
                (['A'], 'a', ['C', 'D']),
                (['A'], 'b', ['A', 'B']),
                (['A', 'B'], 'a', ['C', 'D']),
                (['A', 'B'], 'b', ['A', 'B', 'C']),
                (['A', 'B', 'C'], 'a', ['C', 'D']),
                (['A', 'B', 'C'], 'b', ['A', 'B', 'C']),
                (['C', 'D'], 'a', ['C', 'D']),
                (['C', 'D'], 'b', ['A']),
            ],
            "FA.power: transitions"
        )

        self.assertEqual(
            P.F,
            [
                ['A', 'B'],
                ['A', 'B', 'C'],
            ],
            "FA.power: final states"
        )

    def test_power_full (self):
        P = self.S_EX1.power(True)

        self.assertTrue(P.isComplete(), "FA.power: isComplete")
        self.assertTrue(P.isDeterministic(), "FA.power: isDeterministic")

        self.assertEqual(
            P.S,
            [
                [],
                ['A',],
                ['B',],
                ['C',],
                ['D',],
                ['A', 'B'],
                ['A', 'C'],
                ['A', 'D'],
                ['B', 'C'],
                ['B', 'D'],
                ['C', 'D'],
                ['A', 'B', 'C'],
                ['A', 'B', 'D'],
                ['A', 'C', 'D'],
                ['B', 'C', 'D'],
                ['A', 'B', 'C', 'D']
            ],
            "FA.power: states"
        )

        self.assertEqual(P.Σ, self.S_EX1.Σ, "FA.power: alphabet")

        self.assertEqual(
            P.T,
            [
                ([], 'a', []),
                ([], 'b', []),
                (['A'], 'a', ['C', 'D']),
                (['A'], 'b', ['A', 'B']),
                (['B'], 'a', ['D']),
                (['B'], 'b', ['C']),
                (['C'], 'a', ['C', 'D']),
                (['C'], 'b', []),
                (['D'], 'a', []),
                (['D'], 'b', ['A']),
                (['A', 'B'], 'a', ['C', 'D']),
                (['A', 'B'], 'b', ['A', 'B', 'C']),
                (['A', 'C'], 'a', ['C', 'D']),
                (['A', 'C'], 'b', ['A', 'B']),
                (['A', 'D'], 'a', ['C', 'D']),
                (['A', 'D'], 'b', ['A', 'B']),
                (['B', 'C'], 'a', ['C', 'D']),
                (['B', 'C'], 'b', ['C']),
                (['B', 'D'], 'a', ['D']),
                (['B', 'D'], 'b', ['A', 'C']),
                (['C', 'D'], 'a', ['C', 'D']),
                (['C', 'D'], 'b', ['A']),
                (['A', 'B', 'C'], 'a', ['C', 'D']),
                (['A', 'B', 'C'], 'b', ['A', 'B', 'C']),
                (['A', 'B', 'D'], 'a', ['C', 'D']),
                (['A', 'B', 'D'], 'b', ['A', 'B', 'C']),
                (['A', 'C', 'D'], 'a', ['C', 'D']),
                (['A', 'C', 'D'], 'b', ['A', 'B']),
                (['B', 'C', 'D'], 'a', ['C', 'D']),
                (['B', 'C', 'D'], 'b', ['A', 'C']),
                (['A', 'B', 'C', 'D'], 'a', ['C', 'D']),
                (['A', 'B', 'C', 'D'], 'b', ['A', 'B', 'C'])
            ],
            "FA.power: transitions"
        )

        self.assertEqual(
            P.F,
            [
                ['B'],
                ['A', 'B'],
                ['B', 'C'],
                ['B', 'D'],
                ['A', 'B', 'C'],
                ['A', 'B', 'D'],
                ['B', 'C', 'D'],
                ['A', 'B', 'C', 'D']
            ],
            "FA.power: final states"
        )

    ############################################################################
    # acceptance
    ############################################################################
    def test_acceptance (self):
        # (a|b)*abb
        F = FA (
            S = [1, 2, 3, 4],
            I = [1],
            Σ = ['a', 'b'],
            T = [
                    (1, 'a', 1),
                    (1, 'b', 1),
                    (1, 'a', 2),
                    (2, 'b', 3),
                    (3, 'b', 4)
                ],
            F = [4]
        )

        self.assertEqual(F.accepts("abb"), True, "FA.accepts")
        self.assertEqual(F.accepts("aabb"), True, "FA.accepts")
        self.assertEqual(F.accepts("ab"), False, "FA.accepts")

    ############################################################################
    # conformance
    #
    # example presented in assignment 1 - exercise 1
    ############################################################################
    def test_conformance_false (self):
        I = FA(
            S = [1, 2, 3],
            I = [1],
            Σ = ['a', 'b'],
            T = [
                (1, 'a', 2),
                (1, 'b', 3),
            ],
            F = [3]
        )

        S = FA(
            S = ['A', 'B', 'C'],
            I = ['A'],
            Σ = ['a', 'b'],
            T = [
                ('A', 'b', 'B'),
                ('B', 'a', 'C'),
            ],
            F = ['C']
        )

        [ conforms, ICPS, traces ] = I.conforms(S)

        self.assertEqual(conforms, False, "FA.conforms: conforms")

        self.assertEqual(
            ICPS.S,
            [(1, ['A']), (2, []), (3, ['B'])],
            "FA.conforms: states"
        )

        self.assertEqual(ICPS.Σ, self.I_EX1.Σ, "FA.conforms: alphabet")

        self.assertEqual(
            ICPS.T,
            [((1, ['A']), 'a', (2, [])), ((1, ['A']), 'b', (3, ['B']))],
            "FA.conforms: transitions"
        )

        self.assertEqual(
            ICPS.F,
            [(3, ['B'])],
            "FA.conforms: final states"
        )

        self.assertEqual(
            traces,
            [[((1, ['A']), 'b', (3, ['B']))]],
            "FA.conforms: traces"
        )

    def test_conformance (self):
        [ conforms, ICPS, traces ] = self.I_EX1.conforms(self.S_EX1)

        self.assertEqual(conforms, True, "FA.conforms: conforms")

        self.assertEqual(
            ICPS.S,
            [
                (1, ['A']),
                (1, ['C', 'D']),
                (2, ['A']),
                (2, ['A', 'B']),
                (3, ['A', 'B']),
                (3, ['A', 'B', 'C']),
                (4, ['A', 'B']),
                (4, ['A', 'B', 'C'])
            ],
            "FA.conforms: states"
        )

        self.assertEqual(ICPS.Σ, self.I_EX1.Σ, "FA.conforms: alphabet")

        self.assertEqual(
            ICPS.T,
            [
                ((1, ['A',]), 'b', (2, ['A', 'B'])),
                ((1, ['C', 'D']), 'b', (2, ['A'])),
                ((2, ['A']), 'b', (3, ['A', 'B'])),
                ((2, ['A']), 'b', (4, ['A', 'B'])),
                ((2, ['A', 'B']), 'b', (3, ['A', 'B', 'C'])),
                ((2, ['A', 'B']), 'b', (4, ['A', 'B', 'C'])),
                ((3, ['A', 'B']), 'a', (1, ['C', 'D'])),
                ((3, ['A', 'B']), 'b', (3, ['A', 'B', 'C'])),
                ((3, ['A', 'B', 'C']), 'a', (1, ['C', 'D'])),
                ((3, ['A', 'B', 'C']), 'b', (3, ['A', 'B', 'C'])),
                ((4, ['A', 'B']), 'b', (3, ['A', 'B', 'C'])),
                ((4, ['A', 'B', 'C']), 'b', (3, ['A', 'B', 'C'])),
            ],
            "FA.conforms: transitions"
        )

        self.assertEqual(ICPS.F, [], "FA.conforms: final states")

        self.assertEqual(traces, [], "FA.conforms: traces")

    def test_conformance_full (self):
        [ conforms, ICPS, traces ] = self.I_EX1.conforms(self.S_EX1, full=True)

        self.assertEqual(conforms, True, "FA.conforms: conforms")

        self.assertEqual(
            ICPS.S,
            [
                (1, []),
                (1, ['A']),
                (1, ['A', 'B']),
                (1, ['A', 'B', 'C']),
                (1, ['A', 'B', 'C', 'D']),
                (1, ['A', 'B', 'D']),
                (1, ['A', 'C']),
                (1, ['A', 'C', 'D']),
                (1, ['A', 'D']),
                (1, ['B']),
                (1, ['B', 'C']),
                (1, ['B', 'C', 'D']),
                (1, ['B', 'D']),
                (1, ['C']),
                (1, ['C', 'D']),
                (1, ['D']),
                (2, []),
                (2, ['A']),
                (2, ['A', 'B']),
                (2, ['A', 'B', 'C']),
                (2, ['A', 'B', 'C', 'D']),
                (2, ['A', 'B', 'D']),
                (2, ['A', 'C']),
                (2, ['A', 'C', 'D']),
                (2, ['A', 'D']),
                (2, ['B']),
                (2, ['B', 'C']),
                (2, ['B', 'C', 'D']),
                (2, ['B', 'D']),
                (2, ['C']),
                (2, ['C', 'D']),
                (2, ['D']),
                (3, []),
                (3, ['A']),
                (3, ['A', 'B']),
                (3, ['A', 'B', 'C']),
                (3, ['A', 'B', 'C', 'D']),
                (3, ['A', 'B', 'D']),
                (3, ['A', 'C']),
                (3, ['A', 'C', 'D']),
                (3, ['A', 'D']),
                (3, ['B']),
                (3, ['B', 'C']),
                (3, ['B', 'C', 'D']),
                (3, ['B', 'D']),
                (3, ['C']),
                (3, ['C', 'D']),
                (3, ['D']),
                (4, []),
                (4, ['A']),
                (4, ['A', 'B']),
                (4, ['A', 'B', 'C']),
                (4, ['A', 'B', 'C', 'D']),
                (4, ['A', 'B', 'D']),
                (4, ['A', 'C']),
                (4, ['A', 'C', 'D']),
                (4, ['A', 'D']),
                (4, ['B']),
                (4, ['B', 'C']),
                (4, ['B', 'C', 'D']),
                (4, ['B', 'D']),
                (4, ['C']),
                (4, ['C', 'D']),
                (4, ['D']),
            ],
            "FA.conforms: states"
        )

        self.assertEqual(ICPS.Σ, self.I_EX1.Σ, "FA.conforms: alphabet")

        self.assertEqual(
            ICPS.T,
            [
                ((1, []), 'b', (2, [])),
                ((1, ['A']), 'b', (2, ['A', 'B'])),
                ((1, ['A', 'B']), 'b', (2, ['A', 'B', 'C'])),
                ((1, ['A', 'B', 'C']), 'b', (2, ['A', 'B', 'C'])),
                ((1, ['A', 'B', 'C', 'D']), 'b', (2, ['A', 'B', 'C'])),
                ((1, ['A', 'B', 'D']), 'b', (2, ['A', 'B', 'C'])),
                ((1, ['A', 'C']), 'b', (2, ['A', 'B'])),
                ((1, ['A', 'C', 'D']), 'b', (2, ['A', 'B'])),
                ((1, ['A', 'D']), 'b', (2, ['A', 'B'])),
                ((1, ['B']), 'b', (2, ['C'])),
                ((1, ['B', 'C']), 'b', (2, ['C'])),
                ((1, ['B', 'C', 'D']), 'b', (2, ['A', 'C'])),
                ((1, ['B', 'D']), 'b', (2, ['A', 'C'])),
                ((1, ['C']), 'b', (2, [])),
                ((1, ['C', 'D']), 'b', (2, ['A'])),
                ((1, ['D']), 'b', (2, ['A'])),
                ((2, []), 'b', (3, [])),
                ((2, []), 'b', (4, [])),
                ((2, ['A']), 'b', (3, [ 'A', 'B' ])),
                ((2, ['A']), 'b', (4, ['A', 'B'])),
                ((2, ['A', 'B']), 'b', (3, ['A', 'B', 'C'])),
                ((2, ['A', 'B']), 'b', (4, ['A', 'B', 'C'])),
                ((2, ['A', 'B', 'C']), 'b', (3, ['A', 'B', 'C'])),
                ((2, ['A', 'B', 'C']), 'b', (4, ['A', 'B', 'C'])),
                ((2, ['A', 'B', 'C', 'D']), 'b', (3, ['A', 'B', 'C'])),
                ((2, ['A', 'B', 'C', 'D']), 'b', (4, ['A', 'B', 'C'])),
                ((2, ['A', 'B', 'D']), 'b', (3, ['A', 'B', 'C'])),
                ((2, ['A', 'B', 'D']), 'b', (4, ['A', 'B', 'C'])),
                ((2, ['A', 'C']), 'b', (3, ['A', 'B'])),
                ((2, ['A', 'C']), 'b', (4, ['A', 'B'])),
                ((2, ['A', 'C', 'D']), 'b', (3, ['A', 'B'])),
                ((2, ['A', 'C', 'D']), 'b', (4, ['A', 'B'])),
                ((2, ['A', 'D']), 'b', (3, ['A', 'B'])),
                ((2, ['A', 'D']), 'b', (4, ['A', 'B'])),
                ((2, ['B']), 'b', (3, ['C'])),
                ((2, ['B']), 'b', (4, ['C'])),
                ((2, ['B', 'C']), 'b', (3, ['C'])),
                ((2, ['B', 'C']), 'b', (4, ['C'])),
                ((2, ['B', 'C', 'D']), 'b', (3, ['A', 'C'])),
                ((2, ['B', 'C', 'D']), 'b', (4, ['A', 'C'])),
                ((2, ['B', 'D']), 'b', (3, ['A', 'C'])),
                ((2, ['B', 'D']), 'b', (4, ['A', 'C'])),
                ((2, ['C']), 'b', (3, [])),
                ((2, ['C']), 'b', (4, [])),
                ((2, ['C', 'D']), 'b', (3, ['A'])),
                ((2, ['C', 'D']), 'b', (4, ['A'])),
                ((2, ['D']), 'b', (3, ['A'])),
                ((2, ['D']), 'b', (4, ['A'])),
                ((3, []), 'a', (1, [])),
                ((3, []), 'b', (3, [])),
                ((3, ['A']), 'a', (1, ['C', 'D'])),
                ((3, ['A']), 'b', (3, ['A', 'B'])),
                ((3, ['A', 'B']), 'a', (1, ['C', 'D'])),
                ((3, ['A', 'B']), 'b', (3, ['A', 'B', 'C'])),
                ((3, ['A', 'B', 'C']), 'a', (1, ['C', 'D'])),
                ((3, ['A', 'B', 'C']), 'b', (3, ['A', 'B', 'C'])),
                ((3, ['A', 'B', 'C', 'D']), 'a', (1, ['C', 'D'])),
                ((3, ['A', 'B', 'C', 'D']), 'b', (3, ['A', 'B', 'C'])),
                ((3, ['A', 'B', 'D']), 'a', (1, ['C', 'D'])),
                ((3, ['A', 'B', 'D']), 'b', (3, ['A', 'B', 'C'])),
                ((3, ['A', 'C']), 'a', (1, ['C', 'D'])),
                ((3, ['A', 'C']), 'b', (3, ['A', 'B'])),
                ((3, ['A', 'C', 'D']), 'a', (1, ['C', 'D'])),
                ((3, ['A', 'C', 'D']), 'b', (3, ['A', 'B'])),
                ((3, ['A', 'D']), 'a', (1, ['C', 'D'])),
                ((3, ['A', 'D']), 'b', (3, ['A', 'B'])),
                ((3, ['B']), 'a', (1, ['D'])),
                ((3, ['B']), 'b', (3, ['C'])),
                ((3, ['B', 'C']), 'a', (1, ['C', 'D'])),
                ((3, ['B', 'C']), 'b', (3, ['C'])),
                ((3, ['B', 'C', 'D']), 'a', (1, ['C', 'D'])),
                ((3, ['B', 'C', 'D']), 'b', (3, ['A', 'C'])),
                ((3, ['B', 'D']), 'a', (1, ['D'])),
                ((3, ['B', 'D']), 'b', (3, ['A', 'C'])),
                ((3, ['C']), 'a', (1, ['C', 'D'])),
                ((3, ['C']), 'b', (3, [])),
                ((3, ['C', 'D']), 'a', (1, ['C', 'D'])),
                ((3, ['C', 'D']), 'b', (3, ['A'])),
                ((3, ['D']), 'a', (1, [])),
                ((3, ['D']), 'b', (3, ['A'])),
                ((4, []), 'b', (3, [])),
                ((4, ['A']), 'b', (3, ['A', 'B'])),
                ((4, ['A', 'B']), 'b', (3, ['A', 'B', 'C'])),
                ((4, ['A', 'B', 'C']), 'b', (3, ['A', 'B', 'C'])),
                ((4, ['A', 'B', 'C', 'D']), 'b', (3, ['A', 'B', 'C'])),
                ((4, ['A', 'B', 'D']), 'b', (3, ['A', 'B', 'C'])),
                ((4, ['A', 'C']), 'b', (3, ['A', 'B'])),
                ((4, ['A', 'C', 'D']), 'b', (3, ['A', 'B'])),
                ((4, ['A', 'D']), 'b', (3, ['A', 'B'])),
                ((4, ['B']), 'b', (3, ['C'])),
                ((4, ['B', 'C']), 'b', (3, ['C'])),
                ((4, ['B', 'C', 'D']), 'b', (3, ['A', 'C'])),
                ((4, ['B', 'D']), 'b', (3, ['A', 'C'])),
                ((4, ['C']), 'b', (3, [])),
                ((4, ['C', 'D']), 'b', (3, ['A'])),
                ((4, ['D']), 'b', (3, ['A'])),
            ],
            "FA.conforms: transitions"
        )

        self.assertEqual(
            ICPS.F,
            [
                (4, []),
                (4, ['A']),
                (4, ['A', 'C']),
                (4, ['A', 'C', 'D']),
                (4, ['A', 'D']),
                (4, ['C']),
                (4, ['C', 'D']),
                (4, ['D'])
            ],
            "FA.conforms: final states"
        )

        self.assertEqual(traces, [], "FA.conforms: traces")

    ############################################################################
    # minimization
    #
    # example presented in assignment 2 - exercise 2
    ############################################################################
    def test_minimize (self):
        F = FA (
            S = ['A', 'B', 'C', 'D', 'E', 'F'],
            I = ['A'],
            Σ = [0, 1],
            T = [
                    ('A', 0, 'B'),
                    ('A', 1, 'E'),
                    ('B', 0, 'A'),
                    ('B', 1, 'C'),
                    ('C', 0, 'A'),
                    ('C', 1, 'C'),
                    ('D', 0, 'F'),
                    ('D', 1, 'C'),
                    ('E', 0, 'D'),
                    ('E', 1, 'E'),
                    ('F', 0, 'A'),
                    ('F', 1, 'E')
                ],
            F = ['B', 'F']
        )

        F = F.minimize()

        self.assertEqual(
            F.S,
            [('A', 'D'), ('B', 'F'), ('C', 'E')],
            "minimize: states"
        )
        self.assertEqual(
            F.I,
            [('A', 'D')],
            "minimize: initial states"
        )
        self.assertEqual(
            F.T,
            [
                (('A', 'D'), 0, ('B', 'F')),
                (('A', 'D'), 1, ('C', 'E')),
                (('B', 'F'), 0, ('A', 'D')),
                (('B', 'F'), 1, ('C', 'E')),
                (('C', 'E'), 0, ('A', 'D')),
                (('C', 'E'), 1, ('C', 'E'))
            ],
            "minimize: transitions"
        )
        self.assertEqual(
            F.F,
            [('B', 'F')],
            "minimize: final states"
        )
