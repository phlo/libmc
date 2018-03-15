import unittest

from libmc import tarjan

class TestTarjan (unittest.TestCase):

    # example from lecture slides (p108)
    #
    # SCC
    # * [1]
    # * [2]
    # * [3, 7, 8]
    # * [4]
    # * [5]
    # * [6] lasso
    # * [9]
    # * [10, 11, 12]
    def test_1 (self):
        states = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        edges = \
            [
                (1, 3),
                (1, 4),
                (2, 4),
                (2, 5),
                (2, 6),
                (3, 7), (7, 8), (8, 3), # scc
                (4, 8),
                (4, 9),
                (5, 9),
                (5, 10),
                (6, 6), # scc
                (8, 12),
                (9, 8),
                (9, 10),
                (10, 6),
                (10, 12), (12, 11), (11, 10), # scc
                (11, 6)
            ]

        self.assertEqual(
            tarjan(states, edges),
            [[1], [2], [3, 7, 8], [4], [5], [6], [9], [10, 11, 12]]
        )

    # example from wikipedia
    #
    # SCC
    # * [1, 2, 3]
    # * [4, 5]
    # * [6, 7]
    # * [8]
    def test_2 (self):
        states = [1, 2, 3, 4, 5, 6, 7, 8]
        edges = \
            [
                (1, 2), (2, 3), (3, 1), # scc
                (4, 2), (4, 3),
                (4, 5), (5, 4), # scc
                (5, 6),
                (6, 3),
                (6, 7), (7, 6), # scc
                (8, 5),
                (8, 7),
                (8, 8) # scc
            ]

        self.assertEqual(
            tarjan(states, edges),
            [[1, 2, 3], [4, 5], [6, 7], [8]]
        )

    # assignment 3 - exercise 4
    def test_3 (self):
        states = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']
        edges = \
            [
                ('A', 'B'), ('A', 'E'),
                ('B', 'D'), ('B', 'F'),
                ('C', 'F'),
                ('D', 'A'), ('D', 'H'), ('D', 'I'),
                ('E', 'D'),
                ('F', 'G'), ('F', 'J'),
                ('G', 'C'), ('G', 'K'),
                ('H', 'E'), ('H', 'H'),
                ('I', 'E'), ('I', 'J'),
                ('J', 'G'), ('J', 'K')
            ]

        self.assertEqual(
            tarjan(states, edges),
            [['A', 'B', 'D', 'E', 'H', 'I'], ['C', 'F', 'G', 'J'], ['K']]
        )
