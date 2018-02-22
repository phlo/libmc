import unittest

from libmc import Boole

class TestBooleParser (unittest.TestCase):

    def test_well_formed (self):
        wffs = [
            "a",
            "a & !a",
            "a | !a",
            "a <-> b",
            "((a | b) & (!a | !(c & !d))) <-> !(!(a | b) | !(!a | !(c & !d)))",
            "(!(a | b) -> !c) & (!a & (!b & c))",
        ]

        for wff in wffs:
            with self.subTest(wff=wff):
                self.assertEqual(str(Boole(wff)), wff)

    def test_malformed (self):
        mffs = [
            "",
            "()",
            "a b",
            "a & b |",
            "a && b",
            "a <--> b",
            "(&|<-!-><->)",
        ]

        for mff in mffs:
            with self.subTest(mff=mff):
                with self.assertRaises(SyntaxError) as ex:
                    Boole(mff)

    def test_variable_name (self):
        name = "f[o]o@b.a.r$"

        self.assertEqual(name, Boole(name).variables[0])

        with self.assertRaises(SyntaxError):
            Boole(name + '-')
