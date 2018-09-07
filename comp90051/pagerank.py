# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 22:38:52 2018

@author: Administrator
"""
from reader import transform
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


def pagerank(iteration=20):
    outbdata=transform("data/train_pr.txt")
    d=0.85

    pagerank_dict={i:1/len(outbdata) for i in outbdata}
    n=len(pagerank_dict)

    for iter in range(iteration):
        for node in outbdata:
            local_pr=0

            for neighbour in outbdata[node]:
                if neighbour in outbdata and len(outbdata[neighbour])!=0:
                    local_pr+=pagerank_dict[neighbour]/len(outbdata[neighbour])
            pagerank_dict[node]=(1-d)/n+d*local_pr

    return pagerank_dict

def extPR(filepath):
    pagerank_dict=pagerank()
    data=pd.read_csv(filepath)
    data=data.values
    result=[]
    for source,sink in data[:,1:3]:
        source=int(source)
        source=str(source)
        sink=int(sink)
        sink=str(sink)


        if source in pagerank_dict:
            result.append(pagerank_dict[source])
        else:
            result.append(0)
        if sink in pagerank_dict:
            result.append(pagerank_dict[sink])
        else:
            result.append(0)
    result=np.array(result)
    result=result.reshape(len(data),2)
    utils.updatecsv(filepath,result,["PR_src","PR_snk"])
    
    
    
if __name__=='__main__':
    extPR("data/testdata.csv")
    
