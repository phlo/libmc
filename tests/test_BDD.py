import unittest

from libmc import BDD

class TestBDD (unittest.TestCase):

    def test_invert (self):
        self.assertEqual(
            ~BDD.false(),
            BDD.true()
        )

        self.assertEqual(
            ~BDD.true(),
            BDD.false()
        )

        self.assertEqual(
            str(~BDD(0)),
            "BDD(0, True, [BDD(-1, False), BDD(-1, True)])"
        )

    def test_and (self):
        self.assertEqual(
            BDD.false() & BDD.false(),
            BDD.false()
        )

        self.assertEqual(
            BDD.false() & BDD.true(),
            BDD.false()
        )

        self.assertEqual(
            BDD.true() & BDD.false(),
            BDD.false()
        )

        self.assertEqual(
            BDD.true() & BDD.true(),
            BDD.true()
        )

        self.assertEqual(
            BDD(0) & BDD(1),
            BDD(1, False, [
                BDD(-1, False),
                BDD(0, False, [BDD(-1, False), BDD(-1, True)])
            ])
        )

    def test_or (self):
        self.assertEqual(
            BDD.false() | BDD.false(),
            BDD.false()
        )

        self.assertEqual(
            BDD.false() | BDD.true(),
            BDD.true()
        )

        self.assertEqual(
            BDD.true() | BDD.false(),
            BDD.true()
        )

        self.assertEqual(
            BDD.true() | BDD.true(),
            BDD.true()
        )

        self.assertEqual(
            BDD(0) | BDD(1),
            BDD(1, False, [
                BDD(0, False, [BDD(-1, False), BDD(-1, True)]),
                BDD(-1, True)
            ])
        )

    def test_xor (self):
        self.assertEqual(
            BDD.false() ^ BDD.false(),
            BDD.false()
        )

        self.assertEqual(
            BDD.false() ^ BDD.true(),
            BDD.true()
        )

        self.assertEqual(
            BDD.true() ^ BDD.false(),
            BDD.true()
        )

        self.assertEqual(
            BDD.true() ^ BDD.true(),
            BDD.false()
        )

        self.assertEqual(
            BDD(0) ^ BDD(1),
            BDD(1, False, [
                BDD(0, False, [BDD(-1, False), BDD(-1, True)]),
                BDD(0, True, [BDD(-1, False), BDD(-1, True)])
            ])
        )
