import unittest

from libmc import LTS

class TestLTS (unittest.TestCase):

    ############################################################################
    # completeness and determinism
    ############################################################################

    # complete and deterministic
    def test_complete_and_deterministic (self):
        L = LTS (
            S = [1, 2],
            I = [1],
            Σ = ['a', 'b'],
            T = [
                    (1, 'a', 2),
                    (1, 'b', 2),
                    (2, 'a', 2),
                    (2, 'b', 2)
                ]
        )

        self.assertEqual(L.isComplete(), True, "LTS.isComplete")
        self.assertEqual(L.isDeterministic(), True, "LTS.isDeterministic")

    # complete but not deterministic
    def test_complete_and_not_deterministic (self):
        L = LTS (
            S = [1, 2],
            I = [1],
            Σ = ['a', 'b'],
            T = [
                    (1, 'a', 2),
                    (1, 'b', 2),
                    (2, 'a', 1),
                    (2, 'a', 2), # non deterministic transition
                    (2, 'b', 2)
                ]
        )

        self.assertEqual(L.isComplete(), True, "LTS.isComplete")
        self.assertEqual(L.isDeterministic(), False, "LTS.isDeterministic")

    # not complete but deterministic
    def test_not_complete_and_deterministic (self):
        L = LTS (
            S = [1, 2],
            I = [1],
            Σ = ['a', 'b'],
            T = [] # no transition
        )

        self.assertEqual(L.isComplete(), False, "LTS.isComplete")
        self.assertEqual(L.isDeterministic(), True, "LTS.isDeterministic")

    # not complete and not deterministic
    def test_not_complete_and_not_deterministic (self):
        L = LTS (
            S = [1, 2],
            I = [1, 2], # more than one initial state
            Σ = ['a', 'b'],
            T = [] # no transition
        )

        self.assertEqual(L.isComplete(), False, "LTS.isComplete")
        self.assertEqual(L.isDeterministic(), False, "LTS.isDeterministic")

    ############################################################################
    # traces
    ############################################################################
    def test_traces (self):
        L = LTS (
            S = [1, 2, 3],
            I = [1],
            Σ = ['a', 'b'],
            T = [
                    (1, 'a', 2),
                    (1, 'b', 2),
                    (2, 'a', 2),
                    (2, 'b', 3)
                ]
        )

        self.assertEqual(
            L.trace(3),
            [[(1, 'b', 2), (2, 'b', 3)], [(1, 'a', 2), (2, 'b', 3)]],
            "LTS.traces"
        )
        self.assertEqual(
            L.trace(3, [2]),
            [[(2, 'b', 3)], [(2, 'a', 2), (2, 'b', 3)]],
            "LTS.traces"
        )
