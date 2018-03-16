#!/usr/bin/env python

from libmc import tarjan

# example graph (undirected)
nodes = [ 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K' ]
edges = [
            ('A', 'B'), ('A', 'E'),
            ('B', 'D'), ('B', 'F'),
            ('C', 'F'),
            ('D', 'A'), ('D', 'H'), ('D', 'I'),
            ('E', 'D'),
            ('F', 'G'), ('F', 'J'),
            ('G', 'C'), ('G', 'K'),
            ('H', 'E'), ('H', 'H'),
            ('I', 'E'), ('I', 'J'),
            ('J', 'G'), ('J', 'K')
        ]

# apply Tarjan's algorithm
scc = tarjan(nodes, edges)

assert scc == [
    ['A', 'B', 'D', 'E', 'H', 'I'],
    ['C', 'F', 'G', 'J'],
    ['K']
]
