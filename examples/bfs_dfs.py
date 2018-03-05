#!/usr/bin/env python

from libmc import bfs
from libmc import dfs

################################################################################
# example graph
################################################################################

# initial states
I = [1, 2]

# transitions
T = {
        1:  [2, 4],
        2:  [5, 6],
        3:  [7],
        4:  [3, 7],
        5:  [9],
        6:  [7, 8],
        7:  [3, 4],
        8:  [5, 8],
        9:  [10],
        10: [7]
    }

################################################################################
# define search components
################################################################################

# search node
class Node:
    def __init__ (self, ID, parent=None):
        self.id = ID
        self.parent = parent

# DFS/BFS functions required by libmc
def cache (successor): Cache.add(successor.id)

def cached (successor): return successor.id in Cache

def successors (current):
    for successor in sorted(T[current.id]):
        yield Node(successor, current)

def quit(current):
    global numVisited
    numVisited = numVisited + 1

    if current.id == target:
        buildTrace(current)
        return True
    else:
        return False

# common initializations
def initialize ():
    return (
        [ Node(i) for i in I ], # Stack
        set(I),                 # Cache
        0                       # numVisited
    )

# trace generator
def buildTrace (node):
    global trace
    trace = []
    while True:
        trace = [ node.id ] + trace
        node = node.parent
        if node is None: break

################################################################################
# search target = 7
################################################################################
target = 7

# DFS
(Stack, Cache, numVisited) = initialize()

dfs(Stack, successors,
    cache=cache,
    cached=cached,
    quit=quit
)

assert numVisited == 4
assert trace == [ 2, 6, 7 ]

# BFS
(Stack, Cache, numVisited) = initialize()

bfs(Stack, successors,
    cache=cache,
    cached=cached,
    quit=quit
)

assert numVisited == 7
assert trace == [ 1, 4, 7 ]

################################################################################
# search target = 5
################################################################################
target = 5

# DFS
(Stack, Cache, numVisited) = initialize()

dfs(Stack, successors,
    cache=cache,
    cached=cached,
    quit=quit
)

assert numVisited == 7
assert trace == [ 2, 5 ]

# BFS
(Stack, Cache, numVisited) = initialize()

bfs(Stack, successors,
    cache=cache,
    cached=cached,
    quit=quit
)


assert numVisited == 4
assert trace == [ 2, 5 ]
