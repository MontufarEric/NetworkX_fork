#-*- coding: utf-8 -*-
#    Copyright (C) 2011 by 
#    Jordi Torrents <jtorrents@milnou.net>
#    Aric Hagberg <hagberg@lanl.gov>
#    All rights reserved.
#    BSD license.
import networkx as nx
__author__ = """\n""".join(['Jordi Torrents <jtorrents@milnou.net>',
                            'Aric Hagberg (hagberg@lanl.gov)'])
__all__=['bipartite_degree_centrality',
         'bipartite_betweenness_centrality',
         'bipartite_closeness_centrality']

def bipartite_degree_centrality(G, nodes):
    """Compute the degree centrality for nodes in a bipartite network.

    The degree centrality for a node :math:`v` is the fraction of nodes 
    connected to it.

    Parameters
    ----------
    G : graph
       A bipartite network

    nodes : list or container
      Container with all nodes in one bipartite node set.

    Returns
    -------
    centrality : dictionary
       Dictionary keyed by node with bipartite degree centrality as the value.

    See Also
    --------
    bipartite_betweenness_centrality,
    bipartite_closeness_centrality,
    bipartite_sets,
    is_bipartite

    Notes
    -----
    The nodes input parameter must conatin all nodes in one bipartite node set,
    but the dictionary returned contains all nodes from both bipartite node
    sets.

    For unipartite networks, the degree centrality values are 
    normalized by dividing by the maximum possible degree (which is 
    :math:`n-1` where :math:`n` is the number of nodes in G). 
    In the bipartite case, the maximum possible degree of a node in a
    bipartite node set is the number of nodes in the opposite node set
    [1]_.  The degree centrality for a node :math:`v` in the bipartite
    sets :math:`U` with :math:`n` nodes and :math:`V` with :math:`m`
    nodes is

    .. math::

        d_{v} = \\frac{deg(v)}{m}, \mbox{for} v \in U ,

        d_{v} = \\frac{deg(v)}{n}, \mbox{for} v \in V ,


    where :math:`deg(v)` is the degree of node :math:`v`.        

    References
    ----------
    .. [1] Borgatti, S.P. and Halgin, D. In press. "Analyzing Affiliation 
        Networks". In Carrington, P. and Scott, J. (eds) The Sage Handbook 
        of Social Network Analysis. Sage Publications.
        http://www.steveborgatti.com/papers/bhaffiliations.pdf
    """
    top = set(nodes)
    bottom = set(G) - top
    s = 1.0/len(bottom)
    centrality = dict((n,d*s) for n,d in G.degree_iter(top))
    s = 1.0/len(top)
    centrality.update(dict((n,d*s) for n,d in G.degree_iter(bottom)))
    return centrality


def bipartite_betweenness_centrality(G, nodes):
    """Compute betweenness centrality for nodes in a bipartite network.

    Betweenness centrality of a node :math:`v` is the sum of the
    fraction of all-pairs shortest paths that pass through :math:`v`. 

    Values of betweenness are normalized by the maximum possible
    value which for bipartite graphs is limited by the relative size 
    of the two node sets [1]_.

    Let :math:`n` be the number of nodes in the node set :math:`U` and
    :math:`m` be the number of nodes in the node set :math:`V`, then
    nodes in :math:`U` are normalized by dividing by 

    .. math::

        \\frac{1}{2} [m^2 (s + 1)^2 + 
                      m (s + 1)(2t - s - 1) - 
                      t (2s - t + 3)] ,

    where
    
    .. math::
        
        s = (n - 1) \div m , t = (n - 1) \mod m ,
    
    and nodes in :math:`V` are normalized by dividing by

    .. math::    

        \\frac{1}{2} [n^2 (p + 1)^2 + 
                      n (p + 1)(2r - p - 1) - 
                      r (2p - r + 3)] ,

    where,
    
    .. math::

        p = (m - 1) \div n , r = (m - 1) \mod n .

    Parameters
    ----------
    G : graph
        A bipartite graph

    nodes : list or container
        Container with all nodes in one bipartite node set.

    Returns
    -------
    betweenness : dictionary
        Dictionary keyed by node with bipartite betweenness centrality 
        as the value.

    See Also
    --------
    betweenness_centrality,
    bipartite_degree_centrality,
    bipartite_closeness_centrality,
    bipartite_sets,
    is_bipartite

    Notes
    -----
    The nodes input parameter must contain all nodes in one bipartite node set,
    but the dictionary returned contains all nodes from both node sets.

    References
    ----------
    .. [1] Borgatti, S.P. and Halgin, D. In press. "Analyzing Affiliation 
        Networks". In Carrington, P. and Scott, J. (eds) The Sage Handbook 
        of Social Network Analysis. Sage Publications.
        http://www.steveborgatti.com/papers/bhaffiliations.pdf
    """
    top = set(nodes)
    bottom = set(G) - top
    n = float(len(top))
    m = float(len(bottom))
    s = (n-1) // m
    t = (n-1) % m
    bet_max_top = (((m**2)*((s+1)**2))+
                   (m*(s+1)*(2*t-s-1))-
                   (t*((2*s)-t+3)))/2.0
    p = (m-1) // n
    r = (m-1) % n
    bet_max_bot = (((n**2)*((p+1)**2))+
                   (n*(p+1)*(2*r-p-1))-
                   (r*((2*p)-r+3)))/2.0
    betweenness = nx.betweenness_centrality(G, normalized=False, 
                                            weighted_edges=False)
    for node in top:
        betweenness[node]/=bet_max_top
    for node in bottom:
        betweenness[node]/=bet_max_bot
    return betweenness

def bipartite_closeness_centrality(G, nodes, normalized=True):
    """Compute the closeness centrality for nodes in a bipartite network.

    The closeness of a node is the distance to all other nodes in the 
    graph or in the case that the graph is not connected to all other nodes
    in the connected component containing that node.

    Parameters
    ----------
    G : graph
        A bipartite network

    nodes : list or container
        Container with all nodes in one bipartite node set.

    normalized : bool, optional      
      If True (default) normalize by connected component size.

    Returns
    -------
    closeness : dictionary
        Dictionary keyed by node with bipartite closeness centrality 
        as the value.

    See Also
    --------
    closeness_centrality,
    bipartite_betweenness_centrality,
    bipartite_degree_centrality
    bipartite_sets,
    is_bipartite

    Notes
    -----
    The nodes input parameter must conatin all nodes in one bipartite node set,
    but the dictionary returned contains all nodes from both node sets.

    Closeness centrality is normalized by the minimum distance possible. 
    In the bipartite case the minimum distance for a node in one bipartite 
    node set is 1 from all nodes in the other node set and 2 from all 
    other nodes in its own set [1]_. Thus the closeness centrality
    for node :math:`v`  in the two bipartite sets :math:`U` with 
    :math:`n` nodes and :math:`V` with :math:`m` nodes is 
 
    .. math::

        c_{v} = \\frac{m + 2(n - 1)}{d}, \mbox{for} v \in U,

        c_{v} = \\frac{n + 2(m - 1)}{d}, \mbox{for} v \in V,

    where :math:`d` is the sum of the distances from :math:`v` to all
    other nodes.

    Higher values of closeness  indicate higher centrality.

    As in the unipartite case, setting normalized=True causes the
    values to normalized further to n-1 / size(G)-1 where n is the
    number of nodes in the connected part of graph containing the
    node.  If the graph is not completely connected, this algorithm
    computes the closeness centrality for each connected part
    separately.

    References
    ----------
    .. [1] Borgatti, S.P. and Halgin, D. In press. "Analyzing Affiliation 
        Networks". In Carrington, P. and Scott, J. (eds) The Sage Handbook 
        of Social Network Analysis. Sage Publications.
        http://www.steveborgatti.com/papers/bhaffiliations.pdf
    """
    closeness={}
    path_length=nx.single_source_shortest_path_length
    top = set(nodes)
    bottom = set(G) - top
    n = float(len(top))
    m = float(len(bottom))
    for node in top:
        sp=path_length(G,node)
        totsp=sum(sp.values())
        if totsp > 0.0 and len(G) > 1:
            closeness[node]= (m + 2*(n-1)) / totsp
            if normalized:
                s=(len(sp)-1.0) / ( len(G) - 1 )
                closeness[node] *= s
        else:
            closeness[n]=0.0
    for node in bottom:
        sp=path_length(G,node)
        totsp=sum(sp.values())
        if totsp > 0.0 and len(G) > 1:
            closeness[node]= (n + 2*(m-1)) / totsp
            if normalized:
                s=(len(sp)-1.0) / ( len(G) - 1 )
                closeness[node] *= s
        else:
            closeness[n]=0.0
    return closeness

