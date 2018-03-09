:github_url: https://github.com/phlo/libmc

*********************
Reachability Analysis
*********************

:mod:`libmc` also offers graph search methods, central to explicit model
checking.

BFS and DFS
===========

:func:`libmc.bfs` and :func:`libmc.dfs` implement a generic way to perform graph
search.

Consider this example graph:

.. literalinclude:: ../../examples/bfs_dfs.py
  :lines: 9-24

To perform breadth-first and depth-first search, some key components have to be
defined:

* a search node to keep track of the current path by storing a pointer to the
  parent node

  .. literalinclude:: ../../examples/bfs_dfs.py
    :lines: 31-34

* a mandatory ``successors()`` function, generating the set of successors to the
  given node

  .. literalinclude:: ../../examples/bfs_dfs.py
    :lines: 41-43

* an optional ``cache()`` function, adding a node's id to the cache

  .. literalinclude:: ../../examples/bfs_dfs.py
    :lines: 37

* an optional ``cached()`` function, checking if a given node's id has been
  cached already

  .. literalinclude:: ../../examples/bfs_dfs.py
    :lines: 39

* an optional ``quit()`` function, returning ``True`` iff the target has been
  found

  .. literalinclude:: ../../examples/bfs_dfs.py
    :lines: 45-53

To simplify repeated initialization of the global variables ``Cache``, ``Stack``
and ``numVisited``, the following function is defined:

.. literalinclude:: ../../examples/bfs_dfs.py
  :lines: 56-61

Finally, the function generating the trace in ``quit()`` is given below:

.. literalinclude:: ../../examples/bfs_dfs.py
  :lines: 64-70

A search on the example graph can now be performed by using the previously
defined components.

.. literalinclude:: ../../examples/bfs_dfs.py
  :lines: 75

.. topic:: Breadth-First Search

  .. literalinclude:: ../../examples/bfs_dfs.py
    :lines: 86

  .. literalinclude:: ../../examples/bfs_dfs.py
    :lines: 88

  .. literalinclude:: ../../examples/bfs_dfs.py
    :lines: 90-91

.. topic:: Depth-First Search

  .. literalinclude:: ../../examples/bfs_dfs.py
    :lines: 78

  .. literalinclude:: ../../examples/bfs_dfs.py
    :lines: 80

  .. literalinclude:: ../../examples/bfs_dfs.py
    :lines: 82-83

Tarjan's Algorithm
==================

Tarjan's algorithm is implemented in :func:`libmc.tarjan` and can be used to
find strongly connected components in a graph:

.. literalinclude:: ../../examples/tarjan.py
  :lines: 5-18

.. literalinclude:: ../../examples/tarjan.py
  :lines: 21

.. literalinclude:: ../../examples/tarjan.py
  :lines: 23-26
