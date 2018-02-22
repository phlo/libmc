from re import Scanner
from itertools import product, zip_longest
from collections import OrderedDict
from collections.abc import Sequence

from .bdd import BDD

class Boole:

    class Expr:
        def __init__ (self, *args):
            self.args = args

        def __str__ (self):
            def op ():
                return BooleParser.patterns[type(self)].replace("\\", "")

            def group (arg):
                return (
                    "{}"
                    if isinstance(arg, Boole.Var) or isinstance(arg, Boole.Not)
                    else
                    "({})"
                ).format(arg)

            if isinstance(self, Boole.UnaryExpr):
                return op() + group(self.args[0])
            elif isinstance(self, Boole.BinaryExpr):
                return (" " + op() + " ").join(group(arg) for arg in self.args)
            else:
                return self.args[0]

        def __repr__ (self):
            return "Boole(\"{}\")".format(str(self))

    class UnaryExpr (Expr): pass
    class BinaryExpr (Expr):
        def evaluate (self, assignments):
            return (self.args[0].evaluate(assignments),
                    self.args[1].evaluate(assignments))

        def toBDD (self, variables):
            return (self.args[0].toBDD(variables),
                    self.args[1].toBDD(variables))

        def toAIG (self, aag, numAnd, isOutput):
            lhs = self.args[0].toAIG(aag)
            rhs = self.args[1].toAIG(aag)

            lit = aag["output"]

            if not isOutput:
                lit += (aag["ands"] + 1) * 2

            ands = lit + (aag["ands"] + 1) * 2 if isOutput else lit
            ands = [ ands + i * 2 for i in range(0, numAnd - 1) ]

            aag["ands"] += numAnd

            return tuple([ lhs, rhs, lit ] + ands)

    class Var (Expr):
        def evaluate (self, assignments):
            return assignments[self.args[0]]

        def toBDD (self, variables):
            return variables[self.args[0]]

        def toAIG (self, aag, isOutput=False):
            return aag["inputs"][self.args[0]]

    class Iff (BinaryExpr):
        def evaluate (self, assignments):
            a, b = super().evaluate(assignments)
            return not a ^ b

        def toBDD (self, variables):
            a, b = super().toBDD(variables)
            return ~(a ^ b)

        def toAIG (self, aag, isOutput=False):
            """
            x <-> y ... (x & y) | (!x & !y) ... !(!(x & y) & !(!x & !y))
            """
            lhs, rhs, lit, litL, litR = super().toAIG(aag, 3, isOutput)

            lit ^= 1
            litL ^= 1
            litR ^= 1

            aag["literals"][litL] = "{} {}".format(lhs, rhs)
            aag["literals"][litR] = "{} {}".format(lhs ^ 1, rhs ^ 1)
            aag["literals"][lit] = "{} {}".format(litL, litR)

            return lit

    class Implies (BinaryExpr):
        def evaluate (self, assignments):
            a, b = super().evaluate(assignments)
            return (not a) | b

        def toBDD (self, variables):
            a, b = super().toBDD(variables)
            return ~a | b

        def toAIG (self, aag, isOutput=False):
            """
            x -> y  ... !x | y ... !(x & !y)
            """
            lhs, rhs, lit = super().toAIG(aag, 1, isOutput)

            lit ^= 1

            aag["literals"][lit] = "{} {}".format(lhs, rhs ^ 1)

            return lit

    class ImpliedBy (BinaryExpr):
        def evaluate (self, assignments):
            a, b = super().evaluate(assignments)
            return a | (not b)

        def toBDD (self, variables):
            a, b = super().toBDD(variables)
            return a | ~b

        def toAIG (self, aag, isOutput=False):
            """
            x <- y  ... x | !y ... !(!x & y)
            """
            lhs, rhs, lit = super().toAIG(aag, 1, isOutput)

            lit ^= 1

            aag["literals"][lit] = "{} {}".format(lhs ^ 1, rhs)

            return lit

    class Or (BinaryExpr):
        def evaluate (self, assignments):
            a, b = super().evaluate(assignments)
            return a | b

        def toBDD (self, variables):
            a, b = super().toBDD(variables)
            return a | b

        def toAIG (self, aag, isOutput=False):
            """
            x | y   ... !(!x & !y)
            """
            lhs, rhs, lit = super().toAIG(aag, 1, isOutput)

            lit ^= 1

            aag["literals"][lit] = "{} {}".format(lhs ^ 1, rhs ^ 1)

            return lit

    class And (BinaryExpr):
        def evaluate (self, assignments):
            a, b = super().evaluate(assignments)
            return a & b

        def toBDD (self, variables):
            a, b = super().toBDD(variables)
            return a & b

        def toAIG (self, aag, isOutput=False):
            lhs, rhs, lit = super().toAIG(aag, 1, isOutput)

            aag["literals"][lit] = "{} {}".format(lhs, rhs)

            return lit

    class Not (UnaryExpr):
        def evaluate (self, assignments):
            return not self.args[0].evaluate(assignments)

        def toBDD (self, variables):
            return self.args[0].toBDD(variables).__invert__()

        def toAIG (self, aag, isOutput=False):
            return self.args[0].toAIG(aag, isOutput) ^ 1

    def __init__ (self, formula):
        self.formula, self.variables = BooleParser(formula).parse()

    def __str__ (self):
        return self.formula.__str__()

    def __repr__ (self):
        return self.formula.__repr__()

    def evaluate (self, assignments):
        if isinstance(assignments, Sequence):
            assignments = dict(zip_longest(self.variables, assignments))

        return self.formula.evaluate(assignments)

    def truthTable (self):
        return [
            (values, self.evaluate(values))
            for values in
            product([False, True], repeat=len(self.variables))
        ]

    def toBDD (self):
        return self.formula.toBDD({
            self.variables[i]: BDD(i) for i in range(len(self.variables))
        })

    def toAIG (self):
        """
        x <-> y ... (x & y) | (!x & !y) ... !(!(x & y) & !(!x & !y))
        x -> y  ... !x | y ... !(x & !y)
        x <- y  ... x | !y ... !(!x & y)
        x | y   ... !(!x & !y)
        """
        lit = 2
        inputs = {}
        for v in self.variables:
            inputs[v] = lit
            lit += 2

        aag = {
            "inputs" : inputs,
            "output" : lit,
            "ands" : 0,
            "literals" : {}
        }

        self.formula.toAIG(aag, True)

        header = "aag {} {} 0 1 {}\n".format(
            lit - 1 + aag["ands"],
            lit - 2,
            aag["ands"]
        )

        #  import pdb; pdb.set_trace()

        #  print(self.formula.toAIG(aag, True))
        #  print(aag)

        return \
            "aag {} {} 0 1 {}\n".format(
                lit // 2 + aag["ands"],
                (lit - 2) // 2,
                aag["ands"]
            ) + \
            "\n".join(str(i) for i in range(2, aag["output"], 2)) + \
            "\n" + \
            str(lit if lit in aag["literals"] else lit ^ 1) + \
            "\n" + \
            "\n".join(
                "{} {}".format(l - 1 if l % 2 else l, aag["literals"][l])
                for l in sorted(aag["literals"].keys())
            ) + "\n"

class BooleParser:

    scanner = None

    # must be ordered
    patterns = OrderedDict([
        (Boole.Iff          , r"<->"),
        (Boole.Implies      , r"->"),
        (Boole.ImpliedBy    , r"<-"),
        (Boole.Or           , r"\|"),
        (Boole.And          , r"&"),
        (Boole.Not          , r"!"),
        (Boole.Var          , r"[\w\-\.\[\]\$\@]*[\w\.\[\]\$\@]"),
        ("("                , r"\("),
        (")"                , r"\)"),
        ("skip"             , r"\s+")
    ])

    def __init__ (self, formula):
        self.formula = formula
        self.variables = set()
        self.tokens = None

    def _parseBinary (self, cls, op, repetitive=False):
        lhs = op()

        if self.token[0] == cls.__name__:
            self.scan()
            return cls(
                lhs,
                self._parseBinary(cls, op, repetitive) if repetitive else op()
            )
        else:
            return lhs

    def _expr (self):
        self.scan()
        return self._iff()

    def _iff (self):
        return self._parseBinary(Boole.Iff, self._implies, True)

    def _implies (self):
        return self._parseBinary(Boole.Implies, self._impliedBy)

    def _impliedBy (self):
        return self._parseBinary(Boole.ImpliedBy, self._or)

    def _or (self):
        return self._parseBinary(Boole.Or, self._and, True)

    def _and (self):
        return self._parseBinary(Boole.And, self._not, True)

    def _not (self):
        if self.token[0] == Boole.Not.__name__:
            self.scan()
            return Boole.Not(self._basic())
        else:
            return self._basic()

    def _basic (self):
        if self.token[0] == "(":
            expr = self._expr()
            self.check(")")
            return expr
        else:
            var = self.token
            self.check(Boole.Var.__name__)
            self.variables.add(var[1])
            return Boole.Var(var[1])

    def tokenize (self):
        if self.scanner is None:
            def createToken (rule):
                if not isinstance(rule, str):
                    rule = rule.__name__
                return lambda scanner, token: (rule, token)

            self.scanner = Scanner([
                (v, None if k == "skip" else createToken(k))
                for k, v in self.patterns.items()
            ])

        tokens, remaining = self.scanner.scan(self.formula)
        if remaining:
            raise SyntaxError(
                "{} '{}' followed by '{}'".format(
                    tokens[-1][0].lower(),
                    tokens[-1][-1],
                    remaining
                )
            )

        #  print("tokens = {}".format(tokens))
        #  print("remaining = {}".format(remaining))

        for t in tokens:
            yield t

        yield ("eof",)

    def scan (self):
        if self.tokens is None:
            self.tokens = self.tokenize()

        try:
            self.token = next(self.tokens)
        except StopIteration:
            raise SyntaxError("unexpected EOF")

        if self.token[0] == "eof":
            self.tokens = None

    def check (self, expected):
        if self.token[0] == expected:
            self.scan()
        else:
            raise SyntaxError("{} expected, got {}".format(
                expected,
                self.token[0])
            )

    def parse (self):
        #  import pdb; pdb.set_trace()
        formula = self._expr()
        self.check("eof")
        return (formula, sorted(self.variables))
