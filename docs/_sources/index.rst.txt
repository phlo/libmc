.. toctree::
   :hidden:
   :glob:
   :maxdepth: 2

   API <libmc>


Overview
========

:mod:`libmc` is a python module providing a collection of tools for `KV Model Checking <http://fmv.jku.at/mc>`_ and implements the following concepts presented in the lecture.


Completeness and Determinism
----------------------------

.. autosummary::
   :nosignatures:

   libmc.LTS.isComplete
   libmc.LTS.isDeterministic


Product Automata and Sub-Set Construction
-----------------------------------------

.. autosummary::
   :nosignatures:

   libmc.FA.product
   libmc.LTS.product
   libmc.FA.power
   libmc.LTS.power


Labelled Transition Systems
---------------------------

.. autosummary::
   :nosignatures:

   libmc.LTS


Asynchronous Composition
^^^^^^^^^^^^^^^^^^^^^^^^

.. autosummary::
   :nosignatures:

   libmc.asynchronousComposition


Simulation and Bisimulation
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autosummary::
   :nosignatures:

   libmc.LTS.simulates
   libmc.maximumSimulation
   libmc.LTS.bisimulates
   libmc.maximumBisimulation


Traces
^^^^^^

.. autosummary::
   :nosignatures:

   libmc.LTS.trace


Finite Automata
---------------

.. autosummary::
   :nosignatures:

   libmc.FA


Acceptance
^^^^^^^^^^

.. autosummary::
   :nosignatures:

   libmc.FA.accepts


Complement
^^^^^^^^^^

.. autosummary::
   :nosignatures:

   libmc.FA.complement


Conformance
^^^^^^^^^^^

.. autosummary::
   :nosignatures:

   libmc.FA.conforms


Minimization
^^^^^^^^^^^^

.. autosummary::
   :nosignatures:

   libmc.FA.minimize


Breadth-First and Depth-First Search
------------------------------------

.. autosummary::
   :nosignatures:

   libmc.bfs
   libmc.dfs


Tarjan's Algorithm
------------------

.. autosummary::
   :nosignatures:

   libmc.tarjan


Graphviz DOT Language String Generation
---------------------------------------

.. autosummary::
   :nosignatures:

   libmc.fa2dot
   libmc.FA.toDot
   libmc.LTS.toDot


API Index
---------

See :ref:`genindex` for a list of module members.
