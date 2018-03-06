from weakref import WeakValueDictionary

class BDD:
    """
    Binary Decision Diagram (p149).

    Attributes:
        idx (int): node index
        sign (bool): the node's sign
        child (list(BDD, BDD)): the node's *else* and *then* successors

    Note:
        Operations are carried out using the logical connectives ``~``, ``|``,
        ``&`` and ``^``.
    """
    __unique__ = WeakValueDictionary()

    __id__ = lambda idx, sign, child: \
        hash((idx, sign, id(child[0]), id(child[1]))) \
        if child is not None else \
            1 if sign else 0

    def __hash__ (self):
        return BDD.__id__(self.idx, self.sign, self.child)

    def __new__ (BDD, *args):
        def new_bdd (idx, sign, child):
            node = BDD.__id__(idx, sign, child)
            if node not in BDD.__unique__:
                bdd = object.__new__(BDD)
                bdd.idx = idx
                bdd.sign = sign
                bdd.child = child
                BDD.__unique__[node] = bdd

            bdd = BDD.__unique__[node]
            return BDD.__unique__[node]

        idx = args[0]
        sign = args[1] if len(args) > 1 else False
        child = \
            None if idx < 0 \
            else \
                args[2] if len(args) > 2 and args[2] is not None \
                else [ BDD.false(), BDD.true() ]

        if child is not None:
            if child[0] == child[1]:
                return child[0]

            if BDD.__id__(idx, not sign, child) not in BDD.__unique__:
                sign = child[0].sign
                if sign:
                    child[0] = ~child[0]
                    child[1] = ~child[1]

        return new_bdd(idx, sign, child)

    def __repr__ (self):
        if self.isConstant():
            return "BDD({}, {})".format(self.idx, self.sign)
        else:
            return "BDD({}, {}, {})".format(self.idx, self.sign, self.child)

    @classmethod
    def __top_idx__ (BDD, *args):
        return max([ bdd.idx for bdd in args ])

    def __cofactor__ (self, pos, idx):
        if self.isConstant():
            return self

        sign = self.sign
        if sign:
            self = ~self

        res = self.child[pos] if self.idx == idx else self

        return ~res if sign else res

    @classmethod
    def __cofactor2__ (BDD, a, b):

        idx = BDD.__top_idx__(a, b)

        c = [
                [ a.__cofactor__(0, idx), a.__cofactor__(1, idx) ],
                [ b.__cofactor__(0, idx), b.__cofactor__(1, idx) ]
            ]

        return (idx, c)

    @classmethod
    def __apply__ (BDD, op, a, b):
        if a.isConstant() and b.isConstant():
            return BDD.true() if op(bool(a), bool(b)) else BDD.false()

        idx, c = BDD.__cofactor2__(a, b)
        bdd = BDD(
            idx,
            False,
            [
                BDD.__apply__(op, c[0][0], c[1][0]),
                BDD.__apply__(op, c[0][1], c[1][1])
            ]
        )

        return bdd

    def __bool__ (self): return self.sign

    def __invert__ (self):
        if self.isConstant():
            return BDD.false() if self else BDD.true()

        return BDD(self.idx, not self.sign, self.child)

    def __and__ (self, other):
        return BDD.__apply__(bool.__and__, self, other)

    def __or__ (self, other):
        return BDD.__apply__(bool.__or__, self, other)

    def __xor__ (self, other):
        return BDD.__apply__(bool.__xor__, self, other)

    def __eq__ (self, other):
        return hash(self) == hash(other)

    def __neq__ (self, other):
        return not self == other

    __true__ = None

    @classmethod
    def true (BDD):
        """Boolean constant ``True``."""
        if BDD.__true__ is None:
            BDD.__true__ = BDD(-1, True)
        return BDD.__true__

    __false__ = None

    @classmethod
    def false (BDD):
        """Boolean constant ``False``."""
        if BDD.__false__ is None:
            BDD.__false__ = BDD(-1, False)
        return BDD.__false__

    def isConstant (self):
        """Returns ``True`` for constant nodes."""
        return self.idx < 0

    def toDot (self):
        """
        Returns a graphical representation of the BDD (using `Graphviz
        <https://www.graphviz.org/>`_).

        Returns:
            string: dot language representation
        """
        declared = set()

        def declare (bdd, node):
            if node in declared:
                return ""
            declared.add(node)
            if bdd.isConstant():
                return "\t\"{}\" [shape=box]\n".format(node)
            else:
                return "\t\"{}\" [label=\"@{}\"{}]\n".format(
                    node,
                    bdd.idx,
                    "" if bdd.sign else ",color=red"
                )

        def bdd2dot (bdd):
            edge = "\t\"{}\" -- \"{}\" {}\n"
            node = hash(bdd)
            dot = declare(bdd, node)
            if bdd.isConstant():
                return dot

            for child in bdd.child:
                childNode = hash(child)
                dot += declare(child, childNode)
                dot += edge.format(
                    node,
                    childNode,
                    "" if child == bdd.child[1] else "[style=dashed,color=red]"
                )
                dot += bdd2dot(child)

            return dot

        return "graph BDD {\n" + bdd2dot(self) + "}\n"
