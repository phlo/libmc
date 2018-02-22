import unittest

from libmc import BDD, Boole

class TestBoole (unittest.TestCase):

    def test_iff (self):
        self.assertEqual(
            Boole("a <-> b").truthTable(),
            [
                ((False, False), True),
                ((False, True), False),
                ((True, False), False),
                ((True, True), True)
            ]
        )

    def test_implies (self):
        self.assertEqual(
            Boole("a -> b").truthTable(),
            [
                ((False, False), True),
                ((False, True), True),
                ((True, False), False),
                ((True, True), True)
            ]
        )

    def test_impliedBy (self):
        self.assertEqual(
            Boole("a <- b").truthTable(),
            [
                ((False, False), True),
                ((False, True), False),
                ((True, False), True),
                ((True, True), True)
            ]
        )

    def test_or (self):
        self.assertEqual(
            Boole("a | b").truthTable(),
            [
                ((False, False), False),
                ((False, True), True),
                ((True, False), True),
                ((True, True), True)
            ]
        )

    def test_and (self):
        self.assertEqual(
            Boole("a & b").truthTable(),
            [
                ((False, False), False),
                ((False, True), False),
                ((True, False), False),
                ((True, True), True)
            ]
        )

    def test_not (self):
        self.assertEqual(
            Boole("!a").truthTable(),
            [
                ((False,), True),
                ((True,), False)
            ]
        )

    def test_precedence (self):
        self.assertTrue(
            all(
                line[1]
                for line in
                Boole("a & b | c -> d <-> (((a & b) | c) -> d)").truthTable()
            )
        )

    def test_toBDD (self):
        self.assertEqual(Boole("a & !a").toBDD(), BDD.false())
        self.assertEqual(Boole("a | !a").toBDD(), BDD.true())
        self.assertEqual(Boole("a <-> b").toBDD(), ~(BDD(0) ^ BDD(1)))
        self.assertEqual(
            Boole("((a | b) & (!a | !(c & !d))) <-> !(!(a | b) | !(!a | !(c & !d)))").toBDD(),
            BDD.true()
        )
        self.assertEqual(
            Boole("(!(a | b) -> !c) & !a & !b & c").toBDD(),
            BDD.false()
        )

    def test_toAIG (self):
        self.assertEqual(
            Boole("a & b").toAIG(),
            (
                "aag 4 2 0 1 1\n"
                "2\n"
                "4\n"
                "6\n"
                "6 2 4\n"
            )
        )

        self.assertEqual(
            Boole("a | b").toAIG(),
            (
                "aag 4 2 0 1 1\n"
                "2\n"
                "4\n"
                "7\n"
                "6 3 5\n"
            )
        )

        self.assertEqual(
            Boole("a & !a").toAIG(),
            (
                "aag 3 1 0 1 1\n"
                "2\n"
                "4\n"
                "4 2 3\n"
            )
        )

        self.assertEqual(
            Boole("a | !a").toAIG(),
            (
                "aag 3 1 0 1 1\n"
                "2\n"
                "5\n"
                "4 3 2\n"
            )
        )

        self.assertEqual(
            Boole("(a <-> b)").toAIG(),
            (
                "aag 6 2 0 1 3\n"
                "2\n"
                "4\n"
                "7\n"
                "6 9 11\n"
                "8 2 4\n"
                "10 3 5\n"
            )
        )

        self.assertEqual(
            Boole("((a | b) & (!a | !(c & !d))) <-> !(!(a | b) | !(!a | !(c & !d)))").toAIG(),
            (
                "aag 16 4 0 1 11\n"
                "2\n"
                "4\n"
                "6\n"
                "8\n"
                "11\n"
                "10 29 31\n"
                "12 3 5\n"
                "14 6 9\n"
                "16 2 14\n"
                "18 13 17\n"
                "20 3 5\n"
                "22 6 9\n"
                "24 2 22\n"
                "26 21 25\n"
                "28 18 26\n"
                "30 19 27\n"
            )
        )

        self.assertEqual(
            Boole("(!(a | b) -> !c) & !a & !b & c").toAIG(),
            (
                "aag 9 3 0 1 5\n"
                "2\n"
                "4\n"
                "6\n"
                "8\n"
                "8 13 16\n"
                "10 3 5\n"
                "12 10 6\n"
                "14 5 6\n"
                "16 3 14\n"
            )
        )
