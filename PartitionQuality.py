import networkx as nx
import numpy as np
import pandas as pd
from colorama import *
init(autoreset=True)

__author__ = "Giulio Rossetti"
__contact__ = "giulio.rossetti@gmail.com"
__github__ = "https://github.com/GiulioRossetti"


def read_graph(filename):
    f = open(filename)
    g = nx.Graph()
    for l in f:
        l = l.rstrip().split(";")
        g.add_edge(l[0], l[1])
    return g


def read_communities(filename):
    f = open(filename)
    cms = []
    for l in f:
        l = l.rstrip().split(",")
        cms.append(l)
    return cms


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


def internal_edge_density(coms):
    ms = len(coms.edges())
    ns = len(coms.nodes())
    try:
        internal_density = float(ms) / float(ns * (ns - 1)) / 2
    except:
        return 0
    return internal_density


def edges_inside(coms):
    return coms.number_of_edges()


def average_internal_degree(coms):
    ms = len(coms.edges())
    ns = len(coms.nodes())
    try:
        avg_id = float(2*ms) / ns
    except:
        return 0
    return avg_id


def fraction_over_median_degree(coms):
    ns = community.number_of_nodes()
    degs = coms.degree()
    med = median(degs.values())
    above_med = len([d for d in degs.values() if d > med])
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


def __out_degree_fraction(g, coms):
    nds = []
    for n in coms:
        nds.append(g.degree(n) - coms.degree(n))
    return nds


def max_odf(g, coms):
    return max(__out_degree_fraction(g, coms))


def avg_odf(g, coms):
    return float(sum(__out_degree_fraction(g, coms)))/len(coms)


def flake_odf(g, coms):
    df = 0
    for n in coms:
        fr = coms.degree(n) - (g.degree(n) - coms.degree(n))
        if fr < 0:
            df += 1
    return float(df)/len(coms)


def triangle_participation_ratio(coms):
    cls = nx.triangles(coms)
    nc = [n for n in cls if cls[n] > 0]
    return float(len(nc))/len(coms)


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

    print "-----------------------------------------------------------------"
    print Fore.GREEN + "                         Partition Quality"
    print "-----------------------------------------------------------------"
    print "Author: " + Fore.RED + __author__
    print "Email:  " + Fore.RED + __contact__
    print "GitHub: " + Fore.RED + __github__
    print "-----------------------------------------------------------------\n"



    parser = argparse.ArgumentParser()

    parser.add_argument('graph_file', type=str, help='network file (edge list format)')
    parser.add_argument('community_file', type=str, help='community file')

    args = parser.parse_args()

    graph = read_graph(args.graph_file)
    partition = read_communities(args.community_file)
    n_cut, ied, aid, fomd, ex, cr, cond, nedges, modf, aodf, flake, tpr = [], [], [], [], [], [], [], [], [], [], [], []

    for cs in partition:
        if len(cs) > 1:
            community = graph.subgraph(cs)

            n_cut.append(normalized_cut(graph, community))
            ied.append(internal_edge_density(community))
            aid.append(average_internal_degree(community))
            fomd.append(fraction_over_median_degree(community))
            ex.append(expansion(graph, community))
            cr.append(cut_ratio(graph, community))
            nedges.append(edges_inside(community))
            cond.append(conductance(graph, community))
            modf.append(max_odf(graph, community))
            aodf.append(avg_odf(graph, community))
            flake.append(flake_odf(graph, community))
            tpr.append(triangle_participation_ratio(community))

    print Fore.GREEN + "Scoring functions based on internal connectivity"
    m1 = [
        ["Internal Density", min(ied), max(ied), np.mean(ied), np.std(ied)],
        ["Edges inside", min(nedges), max(nedges), np.mean(nedges), np.std(nedges)],
        ["Average Degree", min(aid), max(aid), np.mean(aid), np.std(aid)],
        ["FOMD", min(fomd), max(fomd), np.mean(fomd), np.std(fomd)],
        ["TPR", min(tpr), max(tpr), np.mean(tpr), np.std(tpr)]
    ]
    df = pd.DataFrame(m1, columns=["function", "min", "max",  "avg", "std"])
    df.set_index('function', inplace=True)
    print df

    print "\n" + Fore.GREEN + "Scoring functions based on external connectivity"
    m2 = [
        ["Expansion", min(ex), max(ex), np.mean(ex), np.std(ex)],
        ["Cut Ratio", min(cr), max(cr), np.mean(cr), np.std(cr)]
    ]
    df2 = pd.DataFrame(m2, columns=["function", "min", "max",  "avg", "std"])
    df2.set_index('function', inplace=True)
    print df2

    print "\n" +Fore.GREEN + "Scoring functions that combine internal and external connectivity"
    m3 = [
        ["Conductance", min(cond), max(cond), np.mean(cond), np.std(cond)],
        ["Normalized Cut", min(n_cut), max(n_cut), np.mean(n_cut), np.std(n_cut)],
        ["Maximum-ODF", min(modf), max(modf), np.mean(modf), np.std(modf)],
        ["Average-ODF", min(aodf), max(aodf), np.mean(aodf), np.std(aodf)],
        ["Flake-ODF", min(flake), max(flake), np.mean(flake), np.std(flake)]

    ]
    df3 = pd.DataFrame(m3, columns=["function", "min", "max",  "avg", "std"])
    df3.set_index('function', inplace=True)
    print df3

    print "\n" + Fore.GREEN + "Scoring function based on a network model"
    m4 = [
        ["Modularity (no overlap)", modularity(graph, partition)]
    ]
    df4 = pd.DataFrame(m4, columns=["function", "value"])
    df4.set_index('function', inplace=True)
    print df4
