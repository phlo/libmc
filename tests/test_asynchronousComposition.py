import unittest

from libmc import asynchronousComposition, LTS

class TestAsynchronousComposition (unittest.TestCase):

    def setUp (self):
        self.maxDiff = None

    # simple example presented in the lecture (p89)
    def test_VO (self):
        A = LTS (
            S = [1, 2, 3, 4],
            I = [1],
            Σ = ['a', 'b', 'c', 's'],
            T = [
                    (1, 'a', 2),
                    (2, 'b', 3),
                    (3, 'c', 4),
                    (4, 's', 1)
                ]
            )

        B = LTS (
            S = [5, 6, 7, 8],
            I = [5],
            Σ = ['d', 'e', 'f', 's'],
            T = [
                    (5, 'd', 6),
                    (6, 'e', 7),
                    (7, 'f', 8),
                    (8, 's', 5),
                ]
            )

        composition = asynchronousComposition(A, B)

        self.assertEqual(
            composition.S,
            [
                (1, 5), (1, 6), (1, 7), (1, 8),
                (2, 5), (2, 6), (2, 7), (2, 8),
                (3, 5), (3, 6), (3, 7), (3, 8),
                (4, 5), (4, 6), (4, 7), (4, 8)
            ],
            "asynchronousComposition: states"
        )
        self.assertEqual(
            composition.I,
            [(1, 5)],
            "asynchronousComposition: initial states"
        )
        self.assertEqual(
            composition.Σ,
            ['a', 'b', 'c', 'd', 'e', 'f', 's'],
            "asynchronousComposition: alphabet"
        )
        self.assertEqual(
            composition.T,
            [
                ((1, 5), 'a', (2, 5)), ((1, 5), 'd', (1, 6)),
                ((1, 6), 'a', (2, 6)), ((1, 6), 'e', (1, 7)),
                ((1, 7), 'a', (2, 7)), ((1, 7), 'f', (1, 8)),
                ((1, 8), 'a', (2, 8)), ((2, 5), 'b', (3, 5)),
                ((2, 5), 'd', (2, 6)), ((2, 6), 'b', (3, 6)),
                ((2, 6), 'e', (2, 7)), ((2, 7), 'b', (3, 7)),
                ((2, 7), 'f', (2, 8)), ((2, 8), 'b', (3, 8)),
                ((3, 5), 'c', (4, 5)), ((3, 5), 'd', (3, 6)),
                ((3, 6), 'c', (4, 6)), ((3, 6), 'e', (3, 7)),
                ((3, 7), 'c', (4, 7)), ((3, 7), 'f', (3, 8)),
                ((3, 8), 'c', (4, 8)), ((4, 5), 'd', (4, 6)),
                ((4, 6), 'e', (4, 7)), ((4, 7), 'f', (4, 8)),
                ((4, 8), 's', (1, 5))
            ],
            "asynchronousComposition: transitions"
        )

        # with partial order reduction
        composition = asynchronousComposition(A, B, partialOrderReduction = lambda x: [x[-1]])

        self.assertEqual(
            composition.S,
            [(1, 5), (1, 6), (1, 7), (1, 8), (2, 8), (3, 8), (4, 8)],
            "partialOrderReduction: states"
        )
        self.assertEqual(
            composition.I,
            [(1, 5)],
            "partialOrderReduction: initial states"
        )
        self.assertEqual(
            composition.Σ,
            ['a', 'b', 'c', 'd', 'e', 'f', 's'],
            "partialOrderReduction: alphabet"
        )
        self.assertEqual(
            composition.T,
            [
                ((1, 5), 'd', (1, 6)), ((1, 6), 'e', (1, 7)), ((1, 7), 'f', (1, 8)),
                ((1, 8), 'a', (2, 8)), ((2, 8), 'b', (3, 8)), ((3, 8), 'c', (4, 8)),
                ((4, 8), 's', (1, 5))
            ],
            "partialOrderReduction: transitions"
        )

    # assignment 3 - exercise 1
    def test_AS3_EX1 (self):
        A = LTS (
            S = [1, 2, 3, 4],
            I = [1],
            Σ = ['a', 't', 's'],
            T = [
                    (1, 'a', 2),
                    (2, 't', 3),
                    (3, 'a', 4),
                    (4, 's', 4)
                ]
            )

        B = LTS (
            S = [1, 2, 3],
            I = [1],
            Σ = ['b', 't', 's'],
            T = [
                    (1, 'b', 2),
                    (2, 't', 2),
                    (2, 'b', 3),
                    (3, 's', 1),
                ]
            )

        composition = asynchronousComposition(A, B)

        self.assertEqual(
            composition.S,
            [
                (1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3),
                (3, 2), (3, 3), (4, 1), (4, 2), (4, 3)
            ],
            "asynchronousComposition: states"
        )
        self.assertEqual(
            composition.I,
            [(1, 1)],
            "asynchronousComposition: initial states"
        )
        self.assertEqual(
            composition.Σ,
            ['a', 'b', 's', 't'],
            "asynchronousComposition: alphabet"
        )
        self.assertEqual(
            composition.T,
            [
                ((1, 1), 'a', (2, 1)), ((1, 1), 'b', (1, 2)),
                ((1, 2), 'a', (2, 2)), ((1, 2), 'b', (1, 3)),
                ((1, 3), 'a', (2, 3)), ((2, 1), 'b', (2, 2)),
                ((2, 2), 'b', (2, 3)), ((2, 2), 't', (3, 2)),
                ((3, 2), 'a', (4, 2)), ((3, 2), 'b', (3, 3)),
                ((3, 3), 'a', (4, 3)), ((4, 1), 'b', (4, 2)),
                ((4, 2), 'b', (4, 3)), ((4, 3), 's', (4, 1))
            ],
            "asynchronousComposition: transitions"
        )

    # assignment 3 - exercise 2
    def test_AS3_EX2 (self):
        A = LTS (
            S = [1, 2, 3, 4],
            I = [1],
            Σ = ['a', 't', 's'],
            T = [
                    (1, 't', 1),
                    (1, 'a', 2),
                    (2, 'a', 3),
                    (3, 's', 4),
                    (4, 'a', 4)
                ]
            )

        B = LTS (
            S = ['A', 'B', 'C', 'D'],
            I = ['A'],
            Σ = ['b', 's'],
            T = [
                    ('A', 'b', 'B'),
                    ('B', 's', 'C'),
                    ('C', 'b', 'D'),
                    ('D', 'b', 'C')
                ]
            )

        C = LTS (
            S = [5, 6, 7],
            I = [5],
            Σ = ['c', 't'],
            T = [
                    (5, 'c', 6),
                    (6, 'c', 7),
                    (6, 't', 6)
                ]
            )

        # checker automaton
        D = LTS (
            S = ['X', 'Y', 'Z'],
            I = ['X'],
            Σ = ['a', 'b', 'c', 's', 't'],
            T = [
                    ('X', 'a', 'X'),
                    ('X', 'b', 'X'),
                    ('X', 'c', 'X'),
                    ('X', 't', 'Y'),
                    ('Y', 'a', 'Y'),
                    ('Y', 'b', 'Y'),
                    ('Y', 'c', 'Y'),
                    ('Y', 's', 'Z'),
                    ('Z', 'a', 'Z'),
                    ('Z', 'b', 'Z'),
                    ('Z', 'c', 'Z')
                ]
            )

        composition = asynchronousComposition(
                A,
                B,
                C,
                partialOrderReduction = lambda x: [x[-1]]
        )

        self.assertEqual(
            composition.S,
            [
                (1, 'A', 5), (1, 'A', 6), (1, 'B', 6), (1, 'B', 7),
                (2, 'B', 6), (2, 'B', 7), (3, 'B', 6), (3, 'B', 7),
                (4, 'C', 6), (4, 'C', 7), (4, 'D', 6), (4, 'D', 7)
            ],
            "partialOrderReduction: states"
        )
        self.assertEqual(
            composition.I,
            [(1, 'A', 5)],
            "partialOrderReduction: initial states"
        )
        self.assertEqual(
            composition.Σ,
            ['a', 'b', 'c', 's', 't'],
            "partialOrderReduction: alphabet"
        )
        self.assertEqual(
            composition.T,
            [
                ((1, 'A', 5), 'c', (1, 'A', 6)),
                ((1, 'A', 6), 'b', (1, 'B', 6)),
                ((1, 'B', 6), 'a', (2, 'B', 6)),
                ((1, 'B', 6), 'c', (1, 'B', 7)),
                ((1, 'B', 6), 't', (1, 'B', 6)),
                ((1, 'B', 7), 'a', (2, 'B', 7)),
                ((2, 'B', 6), 'a', (3, 'B', 6)),
                ((2, 'B', 7), 'a', (3, 'B', 7)),
                ((3, 'B', 6), 'c', (3, 'B', 7)),
                ((3, 'B', 6), 's', (4, 'C', 6)),
                ((3, 'B', 7), 's', (4, 'C', 7)),
                ((4, 'C', 6), 'b', (4, 'D', 6)),
                ((4, 'C', 7), 'b', (4, 'D', 7)),
                ((4, 'D', 6), 'a', (4, 'D', 6)),
                ((4, 'D', 6), 'b', (4, 'C', 6)),
                ((4, 'D', 6), 'c', (4, 'D', 7)),
                ((4, 'D', 7), 'a', (4, 'D', 7)),
                ((4, 'D', 7), 'b', (4, 'C', 7))
            ],
            "partialOrderReduction: transitions"
        )
