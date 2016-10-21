import networkx as nx
import numpy as np

__author__ = "Giulio Rossetti"
__contact__ = "giulio.rossetti@isti.cnr.it"


def median(lst):
    return np.median(np.array(lst))


def community_modularity(coms, g):
    if type(g) != nx.Graph:
        raise TypeError("Bad graph type, use only non directed graph")

    inc = dict([])
    deg = dict([])
    links = g.size(weight='weight')
    if links == 0:
        raise ValueError("A graph without link has an undefined modularity")

    for node in g:
        try:
            com = coms[node]
            deg[com] = deg.get(com, 0.) + g.degree(node, weight='weight')
            for neighbor, dt in g[node].items():
                weight = dt.get("weight", 1)
                if coms[neighbor] == com:
                    if neighbor == node:
                        inc[com] = inc.get(com, 0.) + float(weight)
                    else:
                        inc[com] = inc.get(com, 0.) + float(weight) / 2.
        except:
            pass

    res = 0.
    for com in set(coms.values()):
        res += (inc.get(com, 0.) / links) - (deg.get(com, 0.) / (2.*links))**2
    return res


def read_graph(filename):
    f = open(filename)
    g = nx.Graph()
    f.next()
    for l in f:
        l = l.split(";")
        g.add_edge(l[0], l[1])
    return g


def read_communities(filename):
    f = open(filename)
    cms = []
    for l in f:
        l = l.rstrip().split(",")
        cms .append(l)
    return cms


def internal_edge_density(coms):
    ms = len(coms.edges())
    ns = len(coms.nodes())
    try:
        internal_density = float(ms) / float(ns * (ns - 1)) / 2
    except:
        return 0
    return internal_density


def average_internal_degree(coms):
    ms = len(coms.edges())
    ns = len(coms.nodes())
    try:
        avg_id = float(2*ms) / ns
    except:
        return 0
    return avg_id


def fraction_over_median_degree(coms):
    ns = len(community.nodes())
    degs = coms.degree()
    med = median(degs.values())
    above_med = len([d for d in degs if d > med])
    try:
        ratio = float(above_med) / ns
    except:
        return 0
    return ratio


def expansion(g, coms):
    ns = len(coms.nodes())
    edges_outside = 0
    for n in coms.nodes():
        neighbors = g.neighbors(n)
        for n1 in neighbors:
            if n1 not in coms:
                edges_outside += 1
    try:
        return float(edges_outside) / ns
    except:
        return 0


def cut_ratio(g, coms):
    ns = len(coms.nodes())
    edges_outside = 0
    for n in coms.nodes():
        neighbors = g.neighbors(n)
        for n1 in neighbors:
            if n1 not in coms:
                edges_outside += 1
    try:
        ratio = float(edges_outside) / (ns * (len(g.nodes()) - ns))
    except:
        return 0
    return ratio


def conductance(g, coms):
    ms = len(coms.edges())
    edges_outside = 0
    for n in coms.nodes():
        neighbors = g.neighbors(n)
        for n1 in neighbors:
            if n1 not in coms:
                edges_outside += 1
    try:
        ratio = float(edges_outside) / ((2 * ms) + edges_outside)
    except:
        return 0
    return ratio


def normalized_cut(g, coms):
    ms = len(coms.edges())
    edges_outside = 0
    for n in coms.nodes():
        neighbors = g.neighbors(n)
        for n1 in neighbors:
            if n1 not in coms:
                edges_outside += 1
    try:
        ratio = (float(edges_outside) / ((2 * ms) + edges_outside)) + \
            float(edges_outside) / (2 * (len(g.edges()) - ms) + edges_outside)
    except:
        return 0

    return ratio


def modularity(g, coms):
    part = {}
    ids = 0
    for c in coms:
        for n in c:
            part[n] = ids
        ids += 1

    mod = community_modularity(part, g)
    return mod


if __name__ == "__main__":
    import argparse

    print "-------------------------------------"
    print "         Partition Quality           "
    print "-------------------------------------"
    print "Author: ", __author__
    print "Email:  ", __contact__
    print "------------------------------------\n"

    parser = argparse.ArgumentParser()

    parser.add_argument('graph_file', type=str, help='network file (edge list format)')
    parser.add_argument('community_file', type=str, help='community file')

    args = parser.parse_args()

    graph = read_graph(args.graph_file)
    partition = read_communities(args.community_file)

    n_cut, ied, aid, fomd, ex, cr, cond = [], [], [], [], [], [], []

    for cs in partition:
        if len(cs) > 1:
            community = graph.subgraph(cs)
            n_cut.append(normalized_cut(graph, community))
            ied.append(internal_edge_density(community))
            aid.append(average_internal_degree(community))
            fomd.append(fraction_over_median_degree(community))
            ex.append(expansion(graph, community))
            cr.append(cut_ratio(graph, community))
            cond.append(conductance(graph, community))
        
    print "Measure: min/max/avg/std"
    print "Normalized Cut: %f/%f/%f/%f" % (min(n_cut), max(n_cut), np.mean(n_cut), np.std(n_cut))
    print "Internal Edge Density: %f/%f/%f/%f" % (min(ied), max(ied), np.mean(ied), np.std(ied))
    print "Average Internal Degree: %f/%f/%f/%f" % (min(aid), max(aid), np.mean(aid), np.std(aid))
    print "Fraction over median degree: %f/%f/%f/%f" % (min(fomd), max(fomd), np.mean(fomd), np.std(fomd))
    print "Expansion: %f/%f/%f/%f" % (min(ex), max(ex), np.mean(ex), np.std(ex))
    print "Cut Ratio: %f/%f/%f/%f" % (min(cr), max(cr), np.mean(cr), np.std(cr))
    print "Conductance: %f/%f/%f/%f" % (min(cond), max(cond), np.mean(cond), np.std(cond))
    print ""
    print "Modularity (no overlap): %f" % modularity(graph, partition)

