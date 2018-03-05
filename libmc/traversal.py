def __bfs_dfs_aux__ (stack, successors, **kwargs):
    # parse keyword arguments
    enqueue = kwargs.setdefault("enqueue", lambda x: stack.append(x))
    dequeue = kwargs["dequeue"]

    if "cache" in kwargs:
        if "cached" not in kwargs:
            raise ValueError("missing 'cached' argument")
        cache = kwargs["cache"]
        cached = kwargs["cached"]
    else:
        if "cached" in kwargs:
            raise ValueError("missing 'cache' argument")
        __cache = set(stack)
        cache = lambda x: __cache.add(x)
        cached = lambda x: x in __cache

    if "quit" in kwargs:
        quit = kwargs["quit"]
    else:
        quit = None

    # perform bfs/dfs
    while stack:
        current = dequeue(stack)

        for successor in successors(current):
            if not cached(successor):
                cache(successor)
                enqueue(successor)

        if quit is not None and quit(current): return

def bfs (queue, successors, **kwargs):
    """
    Generic breadth-first search.

    .. code-block:: python

        while queue:
            current = dequeue(queue)

            for successor in successors(current):
                if not cached(successor):
                    cache(successor)
                    enqueue(successor)

            if quit is not None and quit(current): return

    Perform BFS on any given problem by defining:

    * the search queue's initial state
    * a function returning the successors to a given object
    * (optional) a function for enqueuing objects
    * (optional) a function for adding objects to the cache
    * (optional) a function checking if a given object has been cached already
    * (optional) a function for stopping the search

    Args:
        queue (list): initial state of the search queue
        successors (function): function ``f: object -> list(object)`` returning
            the list of successors to a given object

    Keyword Args:
        enqueue (function): a function ``f: object -> None`` adding objects to the
            search queue
        cache (function): a function ``f: object -> None`` adding a given object
            to the cache (requires **cached**)
        cached (function): a function ``f: object -> bool`` checking if a given
            object has been cached already (requires **cache**)
        quit (function): a function ``f: object -> bool`` returning ``True`` if
            the search should stop with the given object
    """
    kwargs["dequeue"] = lambda s: s.pop(0)

    __bfs_dfs_aux__(queue, successors, **kwargs)

def dfs (stack, successors, **kwargs):
    """
    Generic depth-first search.

    .. code-block:: python

        while stack:
            current = dequeue(stack)

            for successor in successors(current):
                if not cached(successor):
                    cache(successor)
                    enqueue(successor)

            if quit is not None and quit(current): return

    Perform DFS on any given problem by defining:

    * the search queue's initial state
    * a function returning the successors to a given object
    * (optional) a function for enqueuing objects
    * (optional) a function for adding objects to the cache
    * (optional) a function checking if a given object has been cached already
    * (optional) a function for stopping the search

    Args:
        queue (list): initial state of the search queue
        successors (function): function ``f: object -> list(object)`` returning
            the list of successors to a given object

    Keyword Args:
        enqueue (function): a function ``f: object -> None`` adding objects to
            the search queue
        cache (function): a function ``f: object -> None`` adding a given object
            to the cache (requires **cached**)
        cached (function): a function ``f: object -> bool`` checking if a given
            object has been cached already (requires **cache**)
        quit (function): a function ``f: object -> bool`` returning ``True`` if
            the search should stop with the given object
    """
    kwargs["dequeue"] = lambda s: s.pop()

    __bfs_dfs_aux__(stack, successors, **kwargs)
