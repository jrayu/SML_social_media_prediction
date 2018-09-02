# -*- coding: cp936 -*-
import math
import numpy as np
from utils import queue, combine_dict, transform
import multiprocessing
import collections
import operator
import networkx as nx

'''#########################################################
    return a subgraph of Gamma(node1) union Gamma(node2)
########################################################'''
def subGraph(outbdata,inbdata,node_1,node_2):
    set1=set()
    set2=set()
    if node_1 in outbdata:
        set1 = makeset(set1,outbdata[node_1])
    if node_1 in inbdata:
        set1 = makeset(set1,inbdata[node_1])
    if node_2 in outbdata:
        set2 = makeset(set2,outbdata[node_2])
    if node_2 in inbdata:
        set2 = makeset(set2,inbdata[node_2])
    union=set1|set2|{node_1}|{node_2}
    g=nx.DiGraph()

    # for all nodes in the union set, insert a link
    # to g if it has an outbound inside the graph
    for node in union:
        if node in outbdata:
            
            node_sink=outbdata[node]
            intersect=node_sink & union
            for sink in intersect:
                g.add_edge(node,sink)
    return g

# limit the newly joint set to size of 10000
def makeset(set1,set2,th=10000):
    if len(set2)>th:
        set2=np.random.choice(list(set2),10000)
        set2=set(set2)
    return set1 | set2
  
'''###########################################################
    Return the edgerank of node2 (possibility of stopping at
    node2 starting at node1)
############################################################'''      
def edgerank(outbdata,inbdata,node1,node2,w=1,d=0.5,iterations=20):
    g=subGraph(outbdata,inbdata,node1,node2)

    # E=0
    if g.size()==0:
        return 0

    # tranform to adjacency matrix
    adj=nx.to_pandas_adjacency(g)
    loc1=adj.columns.get_loc(node1)
    loc2=adj.columns.get_loc(node2)

    # weighted undirected graph
    undAdj=adj+w*np.transpose(adj)
    rows,cols=undAdj.shape

    # normalising the undirected graph
    new=undAdj.values
    for col in range(cols):
        new[:,col]=new[:,col]/sum(new[:,col])
    x_0=np.zeros(rows)
    x_0[loc1]=1
    x=x_0
    for i in range(iterations):
        x=(1-d)*x_0+d*np.dot(new,x)
    return x[loc2]
    
