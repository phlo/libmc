:github_url: https://github.com/phlo/libmc

*********************
Reachability Analysis
*********************

:mod:`libmc` offers generic graph search methods, central to explicit model
checking.

BFS and DFS
===========

:func:`libmc.bfs` and :func:`libmc.dfs` implement a generic way to perform graph
search.

.. , using the following skeleton:
..
.. .. code-block:: python
..
  .. while stack:
    .. current = dequeue(stack)
..
    .. for successor in successors(current):
        .. if not cached(successor):
            .. cache(successor)
            .. enqueue(successor)
..
    .. if quit is not None and quit(current): return

Consider this example graph:

.. literalinclude:: ../../examples/bfs_dfs.py
  :lines: 10-25

To perform breadth-first and depth-first search, some key components have to be
defined:

* a search node to keep track of the current path by storing a pointer to the
  parent node

  .. literalinclude:: ../../examples/bfs_dfs.py
    :lines: 32-35

* a mandatory ``successors()`` function, generating the set of successors to the
  given node

  .. literalinclude:: ../../examples/bfs_dfs.py
    :lines: 42-44

* an optional ``cache()`` function, adding a node's id to the cache

  .. literalinclude:: ../../examples/bfs_dfs.py
    :lines: 38

* an optional ``cached()`` function, checking if a given node's id has been
  cached already

  .. literalinclude:: ../../examples/bfs_dfs.py
    :lines: 40

* an optional ``quit()`` function, returning ``True`` iff the target has been
  found

  .. literalinclude:: ../../examples/bfs_dfs.py
    :lines: 46-54

To simplify repeated initialization of the global variables ``Cache``, ``Stack``
and ``numVisited``, the following function is defined:

.. literalinclude:: ../../examples/bfs_dfs.py
   :lines: 57-62

Finally, the function generating the trace in ``quit()`` is given below:

.. literalinclude:: ../../examples/bfs_dfs.py
   :lines: 65-71

A search on the example graph can now be performed by using the previously
defined complements.

.. topic:: Breadth-First Search

  .. literalinclude:: ../../examples/bfs_dfs.py
     :lines: 91-100

.. topic:: Depth-First Search

  .. literalinclude:: ../../examples/bfs_dfs.py
     :lines: 79-88

Tarjan's Algorithm
==================

Tarjan's algorithm is implemented in :func:`libmc.tarjan` and can be used to
find strongly connected components in a graph:

.. literalinclude:: ../../examples/tarjan.py
  :lines: 3-
