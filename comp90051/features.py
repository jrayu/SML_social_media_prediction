 # -*- coding: cp936 -*-
import math
import numpy as np
from utils import queue, combine_dict, transform
import multiprocessing
import collections
import operator
import networkx as nx
'''input data, node a b, return the score from a to b'''
def cosineExtract(data, node_1,node_2):
    set_1=data[node_1]
    set_2=data[node_2]
    same_item=cnExtract(data,node_1,node_2)
    cosine=same_item/(len(set_1)*len(set_2))
    if node_1=="1001158":
        print("cn:{}".format(same_item))
        print("nm1:{}".format(len(set_1)))
        print("nm2:{}".format(len(set_2)))
    return math.log1p(cosine)
        
'''returns a list of common neighbours between two nodes'''
def commonNeighbours(data,node_1,node_2):
    set_1=data[node_1]
    set_2=data[node_2]
    return set_1 & set_2

def cnExtract(data,node_1,node_2):
    return math.log1p(len(commonNeighbours(data,node_1,node_2)))

def adar(data,node_1,node_2):
    common=commonNeighbours(data,node_1,node_2)
    adar=0
    for instance in common:
        friendset=data.get(instance)
        if not friendset==None:
            if not len(friendset)<2:
                adar+=1/(math.log(len(friendset)))
    return math.log1p(adar)

def jaccard(data,node_1,node_2):
    set_1=data[node_1]
    set_2=data[node_2]
    return math.log1p((len(set_1 & set_2)/len(set_1 | set_2)))

def neighbourDifference(data,node_1,node_2):
    set_1=data[node_1]
    set_2=data[node_2]
    return (len(set_1)-len(set_2))

'''
    if the follower of node 2 is more than that of node 1, there is a possibility
    that node 2 will less likely to follow node 1, and more vice versa
    needs the data of T_in
    '''
def followerDifference(data,node_1,node_2):
    set_1=data[node_1]
    set_2=data[node_2]
    return (len(set_2)-len(set_1))

'''
    returns the shortest length from node 1 to 2, if there is no such
    path, return a sufficiently large value
    we don't care about nodes that are more than 6 steps away

    '''
def BFS(outbdata,inbdata,start,goal):
    if start not in outbdata:
        return None
    midset1=outbdata[start]

    # a direct link
    #if goal in midset1:
    #    return [start,goal],1
    # path of 3 nodes
    if goal not in inbdata:
        return None
    midset2=inbdata[goal]
    intersect=midset1 & midset2
    if len(intersect)>0:
        if len(intersect)>100:
            intersect=np.random.choice(list(intersect),100)
        return [start,intersect,goal],2
    else:
        return None

def getfromdict(node,data):
    if node in data:
        return data[node]
    else:
        return set()
    
def subGraph(outbdata,inbdata,node_1,node_2,w):
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
    for node in union:
        node_sink=getfromdict(node,outbdata)
        node_source=getfromdict(node,inbdata)
        w_out=1/(len(node_sink)+w*len(node_source))
        w_in=w/(len(node_sink)+w*len(node_source))
        int_src=node_source & union
        int_snk=node_sink & union
        for sink in int_snk:
            g.add_edge(node,sink,weight=w_out)
        for source in int_src:
            g.add_edge(node,source,weight=w_in)
    if g.has_edge(node_1,node_2):
        g.remove_edge(node_1,node_2)
    return g

def makeset(set1,set2,th=10000):
    if len(set2)>th:
        set2=np.random.choice(list(set2),10000)
        set2=set(set2)
    return set1 | set2
        
def edgerank(outbdata,inbdata,node1,node2,w=1,d=0.5,iterations=3):
    g=subGraph(outbdata,inbdata,node1,node2,w)
    if g.size()==0:
        return 0
    print("size of subgraph: {}".format(g.size()))
    adj=nx.to_pandas_adjacency(g)
    print(adj)
    loc1=adj.columns.get_loc(node1)
    loc2=adj.columns.get_loc(node2)
    
    rows,cols=adj.shape
    print("shape: {},{}".format(rows,cols))
    new=adj.values
    for row in range(rows):
        if sum(new[row,:]) !=0:
            new[row,:]=new[row,:]/sum(new[row,:])
    x_0=np.zeros(rows)
    x_0[loc1]=1
    x=x_0
    print(x)
    for i in range(iterations):
        x=(1-d)*x_0+d*np.dot(new,x)
        print(x)
    return x[loc2]
    


def randomtrim(data):
    if len(data)>100:
        data=np.random.choice(list(data),100)
    return set(data)


'''
    Return the local rank of node by traversing subgraph centered with it.
    We don't care about nodes that are more than 12 steps away.
    The reason we are asking for 12 is that by doing this, the difference
    between the adjacency matrices of the two nodes in A* doesn't effect
    much. Keeping their environment similar will guarantee a higher accuracy of
    A* algorithm
   '''
def pagerank(outBoundDict,inBoundDict,start,goal):
    # generate subgraph
    bfs=BFS(outBoundDict,inBoundDict,start,goal)
    if bfs==None:
        return 0
    path,cost=bfs
    subgraph=subGraph(outBoundDict,inBoundDict,path)
    N=len(subgraph)
    rank=0
    rankDict=dict.fromkeys(subgraph,1)
    lastrank=0
    #'''
    for i in range(cost):
        lastrank=rankDict[start]
        for node in rankDict:
            fanset=inBoundDict[node]
            fanrank=0
            for fan in fanset:
                fan_follows=outBoundDict[fan]
                if fan in rankDict:
                    fanrank+=rankDict[fan]/len(fan_follows)
            rankDict[node]=fanrank
    return rankDict[goal]

'''
def adjMatrix(outBoundDict,subgraph):
    N=len(subgraph)
    A=np.zeros((N,N))
    sglist=list(subgraph)
    for i in range(N):
        source=sglist[i]
        if source in outBoundDict:
            for j in range(N):
                sink=sglist[j]
                if sink in outBoundDict[source]:
                    A[i][j]=1
        # normalize the adjacency matrix, as corresponse to the pagerank algorithm
        if sum(A[i]) !=0:
            A[i]=A[i]/sum(A[i])
    
    return A
    '''
'''
    Returns list of possibilities of it'''
'''def edgerank(outBoundDict,inBoundDict,start,goal):
    bfs=BFS(outBoundDict,inBoundDict,start,goal)
    if bfs==None:
        return 0
    path,cost=bfs
    subgraph=subGraph(outBoundDict,inBoundDict,path)
    print("subgraph done for {}-{}".format(start,goal))
    A=adjMatrix(outBoundDict,subgraph)
    d=0.5
    w=1
    index=9999
    tgindex=index
    N=len(subgraph)
    for i in range(N):
        if list(subgraph)[i]==start:
            index=i
    for i in range(N):
        if list(subgraph)[i]==goal:
            tgindex=i
    x0=np.zeros(N)
    x0[index]=1
    x_last=x0
    x=x0
    for i in range(cost):
        x_last=x
        x=(1-d)*x0+np.dot(d*(A+w*np.transpose(A)),x_last)
    print("edgerank completed for {}-{}".format(start,goal))
    return x[tgindex]'''
    

def self_deg(outbdata,inbdata,node1,node2):
    result=[0,0,0,0]
    if node1 in outbdata:
        result[0]=len(outbdata[node1])
    if node1 in inbdata:
        result[1]=len(inbdata[node1])
    if node2 in outbdata:
        result[2]=len(outbdata[node2])
    if node2 in inbdata:
        result[3]=len(inbdata[node2])
    return result

'''if __name__=="__main__":
    outbdata=transform("data/train.txt")
    inbdata=transform("data/followers.txt")
    combinedata=combine_dict(outbdata,inbdata)
    subGraph(combinedata,outbdata,"1866350","725231")
'''
