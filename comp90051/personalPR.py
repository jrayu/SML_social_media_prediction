# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 22:38:52 2018

@author: Administrator
"""
from utils import transform
import operator
import collections
from multiprocessing import Pool
import pandas as pd
from functools import partial
from utils import put2TXT
import utils
import numpy as np
"""
    new page rank
"""



def getNeighbours(tobevisited,subgraph,outbdatda,inbdata,iteration):
    if iteration==0:
        return subgraph
    newvisited=set()
    for node in tobevisited:
        forward=getfromdict(node,outbdata)
        backward=getfromdict(node,inbdata)
        friends=forward|backward
        if node not in subgraph and len(friends)!=0:
            subgraph[node]=friends
        newvisit=newvisit|friends
        
    getNeighbours(newvisit,subgraph,outbdata,inbdata,iteration-1)
        

def pagerank(node1,outbdata,inbdata,iteration=3):
    
    pagerank_dict={node1:1}
    pr_list=pagerankGenerator(node1,pagerank_dict,iteration,outbdata,inbdata)

    # construct a list sorted by values
    mylist=[[k,pr_list[k]] for k in sorted(pr_list,key=pr_list.get,reverse=True)]
    
    return mylist[:25]

def pagerankGenerator(node,pagerank_dict,iteration,obd,ibd,alpha=0.5):
    #print(pagerank_dict)
    if iteration<=0:
        return pagerank_dict
    visited={}
    visited[node]=1-alpha
    for item in pagerank_dict:
        prev_score=pagerank_dict[item]
        followers=getfromdict(item,ibd)
        followees=getfromdict(item,obd)
        #if len(followers)+len(followees)==0:
        score=alpha*prev_score/(len(followers)+len(followees))

        for neighbour in (followers | followees):
            if neighbour not in visited:
                visited[neighbour]=0
            visited[neighbour]+=score
    return pagerankGenerator(node,visited,iteration-1,obd,ibd)


    
def getfromdict(node,data):
    #print("getting {} from dict".format(node))
    if node in data:
        #print("node {} found!".format(node))
        return data[node]
    else:
        #print("node {} not found oops :(".format(node))
        return set()



def extPR(filepath):
    outbdata=transform("data/complete_in.txt")
    inbdata=transform("data/complete_out.txt")
    data=pd.read_csv(filepath)
    data=data.values
    result=[]
    for source,sink in data[:,1:3]:
        source=int(source)
        source=str(source)
        sink=int(sink)
        sink=str(sink)
        print("{}-{}".format(source,sink))
        result.append(catchscore(source,sink,outbdata,inbdata))

    utils.updatecsv(filepath,result,["PPR"])
    
    
    
if __name__=='__main__':
    outbdata=transform("data/complete_in.txt")
    inbdata=transform("data/complete_out.txt")
    '''
    outbdata={1:{3},2:{3},3:{5,6,7,13},5:{4,8,9,10},6:{10,11},7:{10,12,13,14,15},10:{19},13:{19},17:{19},18:{19},20:{19},
       19:{13,21,22,23},11:{19}}
    inbdata={3: {1, 2}, 13: {19, 3, 7}, 5: {3}, 6: {3}, 7: {3}, 8: {5}, 9: {5}, 10: {5, 6, 7}, 4: {5}, 11: {6}, 12: {7},
             14: {7}, 15: {7}, 19: {10, 11, 13, 17, 18, 20}, 21: {19}, 22: {19}, 23: {19}}
    '''
    newdata=[]
    for source in outbdata:
        print(source)
        if len(outbdata[source])>10000:
            continue
        iset=pagerank(source,outbdata,inbdata)
        for i in iset:
            sink,score=i
            if sink in outbdata[source]:
                newdata.append([source,sink,1,score])
            else:
                newdata.append([source,sink,0,score])

    df=pd.DataFrame(newdata,columns=["ID","source","sink","PPR"])
    df.index+=1
    
    df.to_csv("data/newdata.csv")
    #extPR("data/testdata.csv")
    
