.. toctree::
   :hidden:
   :glob:
   :maxdepth: 2
   :caption: Contents:

   libmc API <libmc>


Overview
========

.. contents:: Contents
   :local:

----

:mod:`libmc` is a python module providing a collection of tools for KV Model Checkin and implements the following concepts presented in the lecture.


Completeness and Determinism
----------------------------

.. autosummary::
   libmc.LTS.isComplete
   libmc.LTS.isDeterministic


Product Automata and Sub-Set Construction
-----------------------------------------

.. autosummary::
   libmc.LTS.product
   libmc.LTS.power


Labelled Transition Systems
---------------------------

.. autosummary::
   libmc.LTS


Simulation and Bisimulation
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autosummary::
  libmc.LTS.simulates
  libmc.maximumSimulation
  libmc.LTS.bisimulates
  libmc.maximumBisimulation


Finite Automata
---------------

.. autosummary::
   libmc.FA


Acceptance
^^^^^^^^^^

.. autosummary::
   libmc.FA.accepts


Complement
^^^^^^^^^^

.. autosummary::
   libmc.FA.complement


Conformance
^^^^^^^^^^^

.. autosummary::
   libmc.FA.conforms


Minimization
^^^^^^^^^^^^

.. autosummary::
   libmc.FA.minimize


API Index
---------

See :ref:`genindex` for a list of module members.
