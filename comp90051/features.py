# -*- coding: cp936 -*-
import math
import numpy as np
from utils import queue

'''input data, node a b, return the score from a to b'''
def cosineExtract(data, node_1,node_2):
    set_1=data[node_1]
    set_2=data[node_2]
    same_item=len(commonNeighbours(data,node_1,node_2))
    cosine=same_item/(len(set_1)*len(set_2))
    return cosine
        
'''returns a list of common neighbours between two nodes'''
def commonNeighbours(data,node_1,node_2):
    set_1=data[node_1]
    set_2=data[node_2]
    return set_1 & set_2

def cnExtract(data,node_1,node_2):
    return len(commonNeighbours(data,node_1,node_2))

def adar(data,node_1,node_2):
    common=commonNeighbours(data,node_1,node_2)
    adar=0
    for instance in common:
        friendset=data.get(instance)
        if not friendset==None:
            if not len(friendset)<2:
                adar+=1/(math.log(len(friendset)))
    return adar

def jaccard(data,node_1,node_2):
    set_1=data[node_1]
    set_2=data[node_2]
    return (len(set_1 & set_2)/len(set_1 | set_2))

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
    midset1=outbdata[start]

    # a direct link
    if goal in midset1:
        return [start,goal],1
    # path of 3 nodes
    midset2=inbdata[goal]
    intersect=midset1 & midset2
    if len(intersect)>0:
        if len(intersect)>100:
            intersect=np.random.choice(list(intersect),100)
        return [start,intersect,goal],2
    else:
        return None

    # path of 4 nodes
'''
    nodelist=queue()
    nodelist.push(([node_1],node_1))
    visited=[]
    while not nodelist.isEmpty():
        # pop the first element in list, usually one with the least steps
        steps,expandNode=nodelist.pop()
        # if node_2 is reached, return the steps taken to it
        if expandNode==node_2:
            return steps,len(steps)-1
        

        # if length of step is more than 6 which indicates its
        # sequential nodes are at least 7, node_1 and 2 are treated
        # as irrelevant
        if len(steps)>3:
            return [],99999

        # to expand the node
        if expandNode in data and expandNode not in visited:
            followset=data[expandNode]
            for sqtNode in followset:
                nodelist.push((steps+[sqtNode],sqtNode))
        
        visited.append(expandNode)'''

def subGraph(outBoundDict,inBoundDict,path):
    fanset=set()
    N=[]
    subgraph=set()
    if len(path)==3:
        source,midset,sink=path
        N=[source,sink]+list(midset)
    else:
        source,sink=path
        N=[source,sink]
    for node in N:
        if node in outBoundDict:
            followset=outBoundDict[node]
            followset=randomtrim(followset)
        if node in inBoundDict:
            fanset=inBoundDict[node]
            fanset=randomtrim(fanset)
        subgraph=subgraph|followset|fanset|{node}
    return subgraph

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
    Returns list of possibilities of it'''
def edgerank(outBoundDict,inBoundDict,start,goal):
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
    return x[tgindex]
    
