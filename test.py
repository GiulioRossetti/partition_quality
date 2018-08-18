import networkx as nx

g = nx.Graph()
f = open("/home/rossetti/git/CNA_Python_Book/data/book1.csv")
for l in f:
    l = l.rstrip().split(",")
    w = int(l[2])
    if w > 10:
        g.add_edge(l[0], l[1], weight=int(l[2]))


import community as louvain
from collections import defaultdict

import pquality

coms = louvain.best_partition(g)

# Reshaping the results to make them in the same format of the other CD algorithms
coms_to_node = defaultdict(list)
for n, c in coms.items():
    coms_to_node[c].append(n)

coms_louvain = [tuple(c) for c in coms_to_node.values()]
coms_louvain

results = pquality.pquality_summary(g, coms_louvain)
results['Indexes']

print(results)