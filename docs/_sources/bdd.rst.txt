:github_url: https://github.com/phlo/libmc

************************
Binary Decision Diagrams
************************

:class:`libmc.BDD` offers a class for generating binary decision diagrams.

Constants
=========

The two constant nodes representing ``True`` and ``False`` can be accessed
through the static class methods :func:`~libmc.BDD.true` and
:func:`~libmc.BDD.false` respectively.

.. literalinclude:: ../../examples/bdd.py
  :lines: 6-7

Variables
=========

Variable nodes are defined by having an index greater or equal to zero.

.. literalinclude:: ../../examples/bdd.py
  :lines: 10-11

Since they have to be unique, a repeated call to the constructor using the same
index will return a reference to the specific node instead of allocating a new
one.

.. literalinclude:: ../../examples/bdd.py
  :lines: 13-14

Operators
=========

Operations are carried out using the logical connectives ``~``, ``|``, ``&``
and ``^``

.. literalinclude:: ../../examples/bdd.py
  :lines: 17-20

Visualization
=============

The :func:`~libmc.BDD.toDot` method can be used generate the `DOT`_ language
string for a given :class:`~libmc.BDD`:

.. literalinclude:: ../../examples/bdd.py
  :lines: 37

Write it to a file:

.. literalinclude:: ../../examples/bdd.py
  :lines: 39-40

Generate a PDF:

.. literalinclude:: ../../examples/bdd.py
  :lines: 42-44

Enjoy :)

.. graphviz:: img/bdd_xnor.dot

.. _DOT: https://www.graphviz.org
