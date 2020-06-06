import networkx as nx
import numpy as np
import pandas as pd

__author__ = "Giulio Rossetti"
__contact__ = "giulio.rossetti@gmail.com"
__github__ = "https://github.com/GiulioRossetti"


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
        internal_density = float(ms) / (float(ns * (ns - 1)) / 2)
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
    ns = coms.number_of_nodes()
    degs = coms.degree()

    med = median([d[1] for d in degs])
    above_med = len([d[0] for d in degs if d[1] > med])
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


def pquality_summary(graph, partition):

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

    m1 = [
        ["Internal Density", min(ied), max(ied), np.mean(ied), np.std(ied)],
        ["Edges inside", min(nedges), max(nedges), np.mean(nedges), np.std(nedges)],
        ["Average Degree", min(aid), max(aid), np.mean(aid), np.std(aid)],
        ["FOMD", min(fomd), max(fomd), np.mean(fomd), np.std(fomd)],
        ["TPR", min(tpr), max(tpr), np.mean(tpr), np.std(tpr)],
        ["Expansion", min(ex), max(ex), np.mean(ex), np.std(ex)],
        ["Cut Ratio", min(cr), max(cr), np.mean(cr), np.std(cr)],
        ["Conductance", min(cond), max(cond), np.mean(cond), np.std(cond)],
        ["Normalized Cut", min(n_cut), max(n_cut), np.mean(n_cut), np.std(n_cut)],
        ["Maximum-ODF", min(modf), max(modf), np.mean(modf), np.std(modf)],
        ["Average-ODF", min(aodf), max(aodf), np.mean(aodf), np.std(aodf)],
        ["Flake-ODF", min(flake), max(flake), np.mean(flake), np.std(flake)],

    ]
    df = pd.DataFrame(m1, columns=["Index", "min", "max",  "avg", "std"])
    df.set_index('Index', inplace=True)

    m2 = [
        ["Modularity (no overlap)", modularity(graph, partition)]
    ]
    df2 = pd.DataFrame(m2, columns=["Index", "value"])
    df2.set_index('Index', inplace=True)

    results = {
        "Indexes": df,
        "Modularity": df2
    }

    return results

