import re

class Boole:

    class Expr:
        def __init__ (self, *args):
            self.args = args

        def __str__ (self):
            def op ():
                return BooleParser.patterns[self.__class__].replace('\\', '')

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

    class UnaryExpr (Expr): pass
    class BinaryExpr (Expr): pass

    class Iff (BinaryExpr): pass
    class Implies (BinaryExpr): pass
    class Or (BinaryExpr): pass
    class And (BinaryExpr): pass
    class Not (UnaryExpr): pass
    class Var (Expr): pass

    def __init__ (self, formula):
        self.formula = formula

    def __str__ (self):
        return self.formula.__str__()

class BooleParser:

    from collections import OrderedDict

    patterns = OrderedDict([
        (Boole.Iff        , r"<->"),
        (Boole.Implies    , r"->"),
        (Boole.Or         , r"\|"),
        (Boole.And        , r"&"),
        (Boole.Not        , r"!"),
        (Boole.Var        , r"[a-zA-Z0-9-_\.\[\]\$\@]+(?!-)"),
        ("("             , r"\("),
        (")"             , r"\)"),
        ("skip"          , r"\s+")
    ])
    #  patterns = {
        #  Boole.Iff        : r"<->",
        #  Boole.Implies    : r"->",
        #  Boole.Or         : r"\|",
        #  Boole.And        : r"&",
        #  Boole.Not        : r"!",
        #  Boole.Var        : r"[a-zA-Z0-9-_\.\[\]\$\@]+(?!-)",
        #  "("             : r"\(",
        #  ")"             : r"\)",
        #  "skip"          : r"\s+"
    #  }

    __lexicon__ = None

    #  __lexicon__ = [
        #  ( patterns[Boole.Iff],       createToken(Boole.Iff) ),
        #  ( patterns[Boole.Implies],   createToken(Boole.Implies) ),
        #  ( patterns[Boole.Or],        createToken(Boole.Or) ),
        #  ( patterns[Boole.And],       createToken(Boole.And) ),
        #  ( patterns[Boole.Not],       createToken(Boole.Not) ),
        #  ( patterns[Boole.Var],       createToken(Boole.Var) ),
        #  ( patterns["("],            createToken("(") ),
        #  ( patterns[")"],            createToken(")") ),
        #  ( patterns["skip"],         None)
    #  ]

    #  __lexicon__ = [
        #  ( r'<->', createToken(Boole.Iff)),
        #  ( r'->', createToken(Boole.Implies)),
        #  ( r'\|', createToken(Boole.Or)),
        #  ( r'&', createToken(Boole.And)),
        #  ( r'!', createToken(Boole.Not)),
        #  ( r'[a-zA-Z0-9-_\.\[\]\$\@]+(?!-)', createToken(Boole.Var)),
        #  ( r'\(', createToken("(")),
        #  ( r'\)', createToken(")")),
        #  ( r'\s+', None)
    #  ]
#
    def __init__ (self, fileName):
        self.file = fileName
        self.tokens = None

        self.formula = None

        if self.__lexicon__ is None:
            self.__lexicon__ = [
                (v, createToken(k))
                for k, v in self.patterns.items()
            ]

        def getToken (rule):
            return lambda scanner, token: (rule, token)

        #  patterns = {
            #  Boole.Iff        : r"<->",
            #  Boole.Implies    : r"->",
            #  Boole.Or         : r"\|",
            #  Boole.And        : r"&",
            #  Boole.Not        : r"!",
            #  Boole.Var        : r"[a-zA-Z0-9-_\.\[\]\$\@]+(?!-)",
            #  "("             : r"\(",
            #  ")"             : r"\)"
        #  }

        #  self.__lexicon__ = [
            #  #  ( r'<->', self._iff),
            #  #  ( r'->', self._implies),
            #  #  ( r'\|', self._or),
            #  #  ( r'&', self._and),
            #  #  ( r'!', self._not),
            #  #  ( r'[a-zA-Z0-9-_\.\[\]\$\@]+(?!-)', self._var),
            #  #  ( r'\(', self._open),
            #  #  ( r'\)', self._close),
            #  #  ( r'\s+', None)
            #  #  ( r'<->', Boole.Iff),
            #  #  ( r'->', Boole.Implies),
            #  #  ( r'\|', Boole.Or),
            #  #  ( r'&', Boole.And),
            #  #  ( r'!', Boole.Not),
            #  #  ( r'[a-zA-Z0-9-_\.\[\]\$\@]+(?!-)', Boole.Var),
            #  #  ( r'\(', self._open),
            #  #  ( r'\)', self._close),
            #  #  ( r'\s+', None)
            #  #
            #  ( r'<->', getToken(Boole.Iff.__name__)),
            #  ( r'->', getToken(Boole.Implies.__name__)),
            #  ( r'\|', getToken(Boole.Or.__name__)),
            #  ( r'&', getToken(Boole.And.__name__)),
            #  ( r'!', getToken(Boole.Not.__name__)),
            #  ( r'[a-zA-Z0-9-_\.\[\]\$\@]+(?!-)', getToken(Boole.Var.__name__)),
            #  ( r'\(', getToken("(")),
            #  ( r'\)', getToken(")")),
            #  ( r'\s+', None)
        #  ]

    def _parseBinary (self, cls, op):
        print(cls.__name__)
        lhs = op()

        if self.token[0] == cls.__name__:
            self.scan()
            return cls(lhs, op())
        else:
            return lhs

    def _expr (self):
        self.scan()
        return self._iff()

    def _iff (self):
        return self._parseBinary(Boole.Iff, self._implies)

    def _implies (self):
        #  return self._parseBinary("implies", Boole.Implies, self._or)
        return self._parseBinary(Boole.Implies, self._or)

    def _or (self):
        #  return self._parseBinary("or", Boole.Or, self._and)
        return self._parseBinary(Boole.Or, self._and)

    def _and (self):
        #  return self._parseBinary("and", Boole.And, self._not)
        return self._parseBinary(Boole.And, self._not)

    def _not (self):
        print(Boole.Not.__name__)
        if self.token[0] == Boole.Not.__name__:
            self.scan()
            return Boole.Not(self._basic())
        else:
            return self._basic()

    def _basic (self):
        print("basic")
        if self.token[0] == "(":
            expr = self._expr()
            self.check(")")
            return expr
        else:
            print("var: " + self.token[1])
            var = self.token[1]
            self.scan()
            return Boole.Var(var)

    def tokenize (self):
        scanner = re.Scanner(self.__lexicon__)

        with open(self.file) as f:
            content = f.read()

        tokens, remaining = scanner.scan(content)

        for t in tokens:
            yield t

        yield ("eof")

    def scan (self):
        if self.tokens is None:
            self.tokens = self.tokenize()

        self.token = next(self.tokens)
        #  token.parser = self

        if self.token[0] == "eof":
        #  if isinstance(token, self.EOF):
            self.tokens = None

        print("scan: " + self.token[0])

    def check (self, expected):
        if self.token[0] == expected:
            self.scan()
        else:
            raise SyntaxError("{} expected, got {}".format(expected, self.token[0]))

    def parse (self):
        import pdb; pdb.set_trace()

        if self.formula is None:
            self.formula = Boole(self._expr())

        print(self.formula)
        return self.formula

#  def boole2str (expr):
    #  def op ():
        #  return BooleParser.patterns[expr.__class__].replace('\\', '')
#
    #  def group (arg):
        #  if isinstance(arg, Boole.Var) or isinstance(arg, Boole.Not):
            #  return "{}".format(arg)
        #  else:
            #  return "({})".format(arg)
#
    #  if isinstance(expr, Boole.UnaryExpr):
        #  return op() + group(expr.args[0])
    #  elif isinstance(expr, Boole.BinaryExpr):
        #  return (" " + op() + " ").join(group(expr) for expr in expr.args)
    #  else:
        #  return expr.args[0]

def createToken (rule):
    if not isinstance(rule, str):
        rule = rule.__name__

    return None if rule == "skip" else lambda scanner, token: (rule, token)
