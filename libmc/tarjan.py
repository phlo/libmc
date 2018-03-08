from math import inf

def tarjan (nodes, edges):
    """
    Tarjan's Algorithm (p110).

    Find strongly connected components in a directed graph.

    Args:
        nodes (iterable): set of nodes
        edges (iterable): set of edges (pairs of nodes)

    Returns:
        list: set of strongly connected components (list of nodes)
    """
    # depth first search index (DFSI)
    dfsi = { s: 0 for s in nodes }

    # min. reachable DFSI through back edges (MRDFSI)
    mrdfsi = { s: inf for s in nodes }

    # auxiliary stack
    stack = []

    # smallest index of all reachable nodes (SCC index)
    i = 0

    # map of strongly connected components: root node -> SCC (list of nodes)
    scc = {}

    # compute a node's DFSI and MRDFSI recursively
    def tarjan_aux (node, i, stack):

        # return if the node's DFSI is already known
        if dfsi[node] != 0: return i

        # increment the index
        i = i + 1

        # set the node's DFSI and MRDFSI
        dfsi[node] = i
        mrdfsi[node] = i

        # push newly reached node on the auxiliary stack
        stack.append(node)

        # find children
        children = [ t for (s, t) in edges if s == node ]

        # compute DFSI and MRDFSI of all child nodes
        for child in children:
            i = tarjan_aux(child, i, stack)

        # minimize MRDFSI over the MRDFSI of each node and it's direct children
        for child in children:
            mrdfsi[node] = min(mrdfsi[node], mrdfsi[child])

        # return index if it's not a root node
        if dfsi[node] != mrdfsi[node]:
            return i

        # generate the node's SCC
        child = None
        while child != node:
            child = stack.pop()

            scc.setdefault(node, []).append(child)

            mrdfsi[child] = inf

        return i

    # compute each node's DFSI and MRDFSI
    for node in nodes:
        i = tarjan_aux(node, i, stack)

    # return the list of strongly connected components
    return [
        sorted(scc[node])
        for node in nodes
        if
            node in scc
            and
            (
                len(scc[node]) > 1
                or
                (node, node) in edges
            )
    ]
