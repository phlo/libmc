import unittest

from itertools import product

from libmc import LTS, maximumSimulation, maximumBisimulation

class TestSimulation (unittest.TestCase):

    ############################################################################
    # strong simulation
    #
    # example presented in the lecture
    ############################################################################
    def test_strong_simulation (self):
        Σ = ['p', 'd', 'm']

        A_VO = LTS (
            S = [1, 2, 3, 4],
            I = [1],
            Σ = Σ,
            T = [
                    (1, 'p', 2),
                    (2, 'd', 3),
                    (2, 'm', 4)
                ]
        )

        B_VO = LTS (
            S = [5, 6, 7, 8, 9],
            I = [5],
            Σ = Σ,
            T = [
                    (5, 'p', 6),
                    (5, 'p', 7),
                    (6, 'd', 8),
                    (7, 'm', 9)
                ]
        )

        # full simulation relation
        simulation = \
            maximumSimulation(A_VO, A_VO, set(product(A_VO.S, A_VO.S))) | \
            maximumSimulation(A_VO, B_VO, set(product(A_VO.S, B_VO.S))) | \
            maximumSimulation(B_VO, A_VO, set(product(B_VO.S, A_VO.S))) | \
            maximumSimulation(B_VO, B_VO, set(product(B_VO.S, B_VO.S)))

        try:
            self.assertEqual(
                simulation,
                {
                    (1, 1),
                            (2, 2),
                    (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9),
                    (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9),
                    (5, 1),                         (5, 5),
                            (6, 2),                         (6, 6),
                                    (7, 2),                         (7, 7),
                    (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8), (8, 9),
                    (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (9, 7), (9, 8), (9, 9)
                },
                "maximumSimulation: simulation relation"
            )
        except AssertionError:
            print("=" * 80)
            printRelation(simulation, A_VO.S + B_VO.S, A_VO.S + B_VO.S)
            print("=" * 80)
            raise

        # A.simulate(B)
        simulates = A_VO.simulates(B_VO)
        simulation = maximumSimulation(B_VO, A_VO, set(product(B_VO.S, A_VO.S)))

        try:
            self.assertEqual(simulates, True, "maximumSimulation: simulates")
            self.assertEqual(
                simulation,
                {
                    (5, 1),
                    (6, 2),
                    (7, 2),
                    (8, 1), (8, 2), (8, 3), (8, 4),
                    (9, 1), (9, 2), (9, 3), (9, 4)
                },
                "maximumSimulation: simulation relation"
            )
        except AssertionError:
            print("=" * 80)
            printRelation(simulation, B_VO.S, A_VO.S)
            print("=" * 80)
            raise

        # B.simulate(A)
        simulates = B_VO.simulates(A_VO)
        simulation = maximumSimulation(A_VO, B_VO, set(product(A_VO.S, B_VO.S)))

        try:
            self.assertEqual(simulates, False, "maximumSimulation: simulates")
            self.assertEqual(
                simulation,
                {
                    (3, 5), (3, 6), (3, 7), (3, 8), (3, 9),
                    (4, 5), (4, 6), (4, 7), (4, 8), (4, 9)
                },
                "maximumSimulation: simulation relation"
            )
        except AssertionError:
            print("=" * 80)
            printRelation(simulation, A_VO.S, B_VO.S)
            print("=" * 80)
            raise

    ############################################################################
    # weak simulation
    #
    # example presented in assignment 2 - exercise 1
    ############################################################################
    def test_weak_simulation (self):
        Σ = ['a', 'b', 'τ']

        A_EX2 = LTS (
            S = [1, 2, 3],
            I = [1],
            Σ = Σ,
            T = [
                    (1, 'b', 3),
                    (1, 'τ', 2),
                    (2, 'a', 3),
                    (3, 'τ', 1)
                ]
        )

        B_EX2 = LTS (
            S = [4, 5],
            I = [4],
            Σ = Σ,
            T = [
                    (4, 'a', 4),
                    (4, 'b', 5),
                    (5, 'a', 4),
                    (5, 'τ', 4)
                ]
        )

        τ = ['τ']

        # full simulation relation
        simulation = \
            maximumSimulation(A_EX2, A_EX2, set(product(A_EX2.S, A_EX2.S)), τ) | \
            maximumSimulation(A_EX2, B_EX2, set(product(A_EX2.S, B_EX2.S)), τ) | \
            maximumSimulation(B_EX2, A_EX2, set(product(B_EX2.S, A_EX2.S)), τ) | \
            maximumSimulation(B_EX2, B_EX2, set(product(B_EX2.S, B_EX2.S)), τ)

        try:
            self.assertEqual(
                simulation,
                {
                    (1, 1),         (1, 3), (1, 4), (1, 5),
                    (2, 1), (2, 2), (2, 3), (2, 4), (2, 5),
                    (3, 1),         (3, 3), (3, 4), (3, 5),
                    (4, 1),         (4, 3), (4, 4), (4, 5),
                    (5, 1),         (5, 3), (5, 4), (5, 5)
                },
                "maximumSimulation (weak): simulation relation"
            )
        except AssertionError:
            print("=" * 80)
            printRelation(simulation, A_EX2.S + B_EX2.S, A_EX2.S + B_EX2.S)
            print("=" * 80)
            raise

        # A.simulate(B)
        simulates = A_EX2.simulates(B_EX2, τ)
        simulation = maximumSimulation(B_EX2, A_EX2, set(product(B_EX2.S, A_EX2.S)), τ)

        try:
            self.assertEqual(simulates, True, "maximumSimulation (weak): simulates")
            self.assertEqual(
                simulation,
                {(4, 1), (4, 3), (5, 1), (5, 3)},
                "maximumSimulation (weak): simulation relation"
            )
        except AssertionError:
            print("=" * 80)
            printRelation(simulation, B_EX2.S, A_EX2.S)
            print("=" * 80)
            raise

        # B.simulate(A)
        simulates = B_EX2.simulates(A_EX2, τ)
        simulation = maximumSimulation(A_EX2, B_EX2, set(product(A_EX2.S, B_EX2.S)), τ)

        try:
            self.assertEqual(simulates, True, "maximumSimulation (weak): simulates")
            self.assertEqual(
                simulation,
                {
                    (1, 4), (1, 5), (2, 4), (2, 5), (3, 4), (3, 5)
                },
                "maximumSimulation (weak): simulation relation"
            )
        except AssertionError:
            print("=" * 80)
            printRelation(simulation, A_EX2.S + B_EX2.S, A_EX2.S + B_EX2.S)
            print("=" * 80)
            raise

    ############################################################################
    # bisimulation
    #
    # example presented in assignment 2 - exercise 3
    ############################################################################
    def test_bisimulation_EX (self):
        Σ = ['a', 'b']

        A1_EX2 = LTS (
            S = [1, 2, 3],
            I = [1],
            Σ = Σ,
            T = [
                    (1, 'a', 2),
                    (1, 'a', 3),
                    (2, 'a', 1),
                    (3, 'b', 1)
                ]
        )

        A2_EX2 = LTS (
            S = [4, 5],
            I = [4],
            Σ = Σ,
            T = [
                    (4, 'a', 4),
                    (4, 'a', 5),
                    (5, 'b', 4)
                ]
        )

        simulates = A1_EX2.bisimulates(A2_EX2)
        simulation = \
            maximumBisimulation(A1_EX2, A1_EX2, set(product(A1_EX2.S, A1_EX2.S))) | \
            maximumBisimulation(A1_EX2, A2_EX2, set(product(A1_EX2.S, A2_EX2.S))) | \
            maximumBisimulation(A2_EX2, A1_EX2, set(product(A2_EX2.S, A1_EX2.S))) | \
            maximumBisimulation(A2_EX2, A2_EX2, set(product(A2_EX2.S, A2_EX2.S)))

        try:
            self.assertEqual(simulates, False, "maximumBisimulation: simulates")
            self.assertEqual(
                simulation,
                {
                (1, 1),
                        (2, 2),
                                (3, 3),
                                        (4, 4),
                                                (5, 5)
                },
                "maximumBisimulation: simulation relation"
            )
        except AssertionError:
            print("=" * 80)
            printRelation(simulation, A1_EX2.S + A2_EX2.S, A1_EX2.S + A2_EX2.S)
            print("=" * 80)
            raise

    # example presented in the lecture
    def test_bisimulation_VO (self):
        Σ = ['p', 'd', 'm']

        A_VO = LTS (
            S = [1, 2, 3, 4],
            I = [1],
            Σ = Σ,
            T = [
                    (1, 'p', 2),
                    (2, 'd', 3),
                    (2, 'm', 4)
                ]
        )

        B_VO = LTS (
            S = [5, 6, 7, 8, 9],
            I = [5],
            Σ = Σ,
            T = [
                    (5, 'p', 6),
                    (5, 'p', 7),
                    (6, 'd', 8),
                    (7, 'm', 9)
                ]
        )

        simulates = A_VO.bisimulates(B_VO)
        simulation = \
            maximumBisimulation(A_VO, A_VO, set(product(A_VO.S, A_VO.S))) | \
            maximumBisimulation(A_VO, B_VO, set(product(A_VO.S, B_VO.S))) | \
            maximumBisimulation(B_VO, A_VO, set(product(B_VO.S, A_VO.S))) | \
            maximumBisimulation(B_VO, B_VO, set(product(B_VO.S, B_VO.S)))

        try:
            self.assertEqual(simulates, False, "maximumBisimulation: simulates")
            self.assertEqual(
                simulation,
                {
                    (1, 1),
                            (2, 2),
                                    (3, 3), (3, 4),                         (3, 8), (3, 9),
                                    (4, 3), (4, 4),                         (4, 8), (4, 9),
                                                    (5, 5),
                                                            (6, 6),
                                                                    (7, 7),
                                    (8, 3), (8, 4),                         (8, 8), (8, 9),
                                    (9, 3), (9, 4),                         (9, 8), (9, 9)
                },
                "maximumBisimulation: simulation relation"
            )
        except AssertionError:
            print("=" * 80)
            printRelation(simulation, A_VO.S + B_VO.S, A_VO.S + B_VO.S)
            print("=" * 80)
            raise
