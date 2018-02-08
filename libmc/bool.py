import re

class Bool:
    class Expr: pass

class BoolParser:

    class Rule:
        def __init__ (self, *args): pass
        #  @classmethod
        #  def parse (cls): pass

    class Expr (Rule):
        @classmethod
        def parse (cls, parser):
            self.child = BoolParser.Iff.parse(parser)

    class Iff (Rule):
        @classmethod
        def parse (cls, parser):
            lhs = BoolParser.Implies.parse(parser)

            token = parser.scan()

            if isinstance(token, BoolParser.Iff):
                rhs = BoolParser.Implies.parse(parser)
                self.child = ( lhs, rhs )
                return self
            elif not isinstance(token, BoolParser.EOF):
                raise SyntaxError("EOF expected, got {}".format(token))
            else:
                return lhs


    class Implies (Rule):
        @classmethod
        def parse (cls, parser):
            pass

    class Or (Rule): pass

    class And (Rule): pass

    class Not (Rule): pass

    class Var (Rule):
        def __init__ (self, *args):
            super().__init__(*args)
            self.name = args[1]

    class Basic (Rule): pass

    class Open (Rule): pass

    class Close (Rule): pass

    class EOF (Rule): pass

    __lexicon__ = [
        ( r'<->', Iff),
        ( r'->', Implies),
        ( r'\|', Or),
        ( r'&', And),
        ( r'!', Not),
        ( r'[a-zA-Z0-9-_\.\[\]\$\@]+(?!-)', Var),
        ( r'\(', Open),
        ( r'\)', Close),
        ( r'\s+', None)
    ]

    def __init__ (self, fileName):
        self.file = fileName
        self.tokens = None
        self.symbol = None
        self.nextSymbol = None

        self.formula = Bool()

    #  def _expr (self):
        #  pass
#
    #  def _iff (self):
        #  pass
#
    #  def _implies (self):
        #  pass
#
    #  def _or (self):
        #  pass
#
    #  def _and (self):
        #  pass
#
    #  def _not (self):
        #  pass
#
    #  def _basic (self):
        #  pass

    def tokenize (self):
        scanner = re.Scanner(self.__lexicon__)

        with open(self.file) as f:
            content = f.read()

        tokens, remaining = scanner.scan(content)

        for t in tokens:
            yield t

        yield self.EOF()

    def scan (self):
        if self.tokens is None:
            self.tokens = self.tokenize()

        token = next(self.tokens)
        token.parser = self

        if isinstance(token, self.EOF):
            self.tokens = None

        self.symbol = token

        return token

    def check (self, expected):
        if self.symbol == expected:
            return self.scan()

        raise SyntaxError("{} expected, got {}".format(expected, self.symbol))

    def parse (self):
        #  import pdb; pdb.set_trace()
        #  t = self.scan()
        #  print(self.scan())
        #  print(self.scan())
        #  print(self.scan())
        #  print(self.scan())
        #  print(self.scan())
        #  print(self.scan())
        #  print(self.scan())
        #  print(self.scan())
        #  print(self.scan())
        #  print(self.scan())
        #  print(self.scan())

        import pdb; pdb.set_trace()

        self.Expr.parse(self)

        pass

        #  for token in self.tokenize():
            #  print(token)

