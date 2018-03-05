:github_url: https://github.com/phlo/libmc

************
Boole Parser
************

The :class:`libmc.Boole` class can be used to evaluate and convert propositional
formulae given in the Boole format, introduced by the SAT solver frontend
`limboole <http://fmv.jku.at/limboole>`_.

Format
======

The Boole format has the following syntax in BNF:

.. productionlist:: Boole
  expr : `iff`
  iff : `implies` { "<->" `implies` }
  implies : `or` [ "->" `or` | "<-" `or` ]
  or : `and` { "|" `and` }
  and : `not` { "&" `not` }
  not : `basic` | "!" `not`
  basic : `var` | "(" `expr` ")"

Where :token:`var` is a string over letters, digits and the following
characters::

  - _ . [ ] $ @

.. Note::
  The last character of :token:`var` should be different from ``-``!

Parsing
=======

Parsing a Boole formula is done by creating a :class:`libmc.Boole` object:

..
.. .. literalinclude:: ../../examples/boole.py
   .. :lines: 6-7,15-16,24

.. literalinclude:: ../../examples/boole.py
   :lines: 6

.. literalinclude:: ../../examples/boole.py
   :lines: 15

.. literalinclude:: ../../examples/boole.py
   :lines: 24

Evaluation
==========

:func:`~libmc.Boole.evaluate` is used to evaluate a propositional formula
under a given assignment and :func:`~libmc.Boole.truthTable` to generate it's
truth table:

.. literalinclude:: ../../examples/boole.py
   :lines: 8-13

.. literalinclude:: ../../examples/boole.py
   :lines: 17-22

.. literalinclude:: ../../examples/boole.py
   :lines: 26-33

Conversion
==========

:class:`libmc.Boole` also offers methods for converting a propositional
formula into other representations.

To AIG
------

Convert a Boole formula to an AIG with :func:`~libmc.Boole.toAIG`:

.. literalinclude:: ../../examples/boole.py
   :lines: 43-48

.. literalinclude:: ../../examples/boole.py
   :lines: 50-55

.. literalinclude:: ../../examples/boole.py
   :lines: 57-65

To BDD
------

Convert a Boole formula to a BDD with :func:`~libmc.Boole.toBDD`:

.. literalinclude:: ../../examples/boole.py
   :lines: 36

.. literalinclude:: ../../examples/boole.py
   :lines: 38

.. literalinclude:: ../../examples/boole.py
   :lines: 40
