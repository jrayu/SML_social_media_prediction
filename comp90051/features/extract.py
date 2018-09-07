from utils import transform
from reader import readCSV
from reader import addFeature
import features as ft
import numpy as np
from sklearn.linear_model import LogisticRegression
import random
import csv
import pandas as pd
import utils

def extractER(filepath):
    outbdata=transform("data/train.txt")
    inbdata=transform("data/followers.txt")
    traindata=pd.read_csv(filepath)
    traindata=traindata.values
    result=[]
    for source,sink in traindata[:,1:3]:
        source=int(source)
        source=str(source)
        sink=int(sink)
        sink=str(sink)
        print("{}-{}".format(source,sink))
        result.append(ft.edgerank(outbdata,inbdata,source,sink))
    result=np.array(result)
    result=result.reshape(len(traindata),1)
    utils.updatecsv(filepath,result,["ER_ddi1"])

def extractSD(filepath):
    outbdata=transform("data/train.txt")
    inbdata=transform("data/followers.txt")
    traindata=pd.read_csv(filepath)
    traindata=traindata.values
    result=[]
    for source,sink in traindata[:,1:3]:
        source=int(source)
        source=str(source)
        sink=int(sink)
        sink=str(sink)
        result.append(ft.self_deg(outbdata,inbdata,source,sink))
    result=np.array(result)
    result=result.reshape(len(traindata),4)
    utils.updatecsv(filepath,result,["u_out","u_in","v_out","v_in"])

def extractCN(filepath):
    outbdata=transform("data/train.txt")
    inbdata=transform("data/followers.txt")
    combinedata=utils.combine_dict(outbdata,inbdata)
    traindata=pd.read_csv(filepath)
    traindata=traindata.values
    result=[]
    for source,sink in traindata[:,1:3]:
        print("working for {}-{}".format(source,sink))
        source=int(source)
        source=str(source)
        sink=int(sink)
        sink=str(sink)
        result.append(ft.cnExtract(combinedata,source,sink))
    result=np.array(result)
    result=result.reshape(len(traindata),1)
    utils.updatecsv(filepath,result,["CN"])

def extractJC(filepath):
    outbdata=transform("data/train.txt")
    inbdata=transform("data/followers.txt")
    combinedata=utils.combine_dict(outbdata,inbdata)
    traindata=pd.read_csv(filepath)
    traindata=traindata.values
    result=[]
    for source,sink in traindata[:,1:3]:
        source=int(source)
        source=str(source)
        sink=int(sink)
        sink=str(sink)
        result.append(ft.jaccard(combinedata,source,sink))
    result=np.array(result)
    result=result.reshape(len(traindata),1)
    utils.updatecsv(filepath,result,["jaccard"])

def extractCosine(filepath):
    outbdata=transform("data/train.txt")
    inbdata=transform("data/followers.txt")
    combinedata=utils.combine_dict(outbdata,inbdata)
    traindata=pd.read_csv(filepath)
    traindata=traindata.values
    result=[]
    for source,sink in traindata[:,1:3]:
        source=int(source)
        source=str(source)
        sink=int(sink)
        sink=str(sink)
        result.append(ft.cosineExtract(combinedata,source,sink))
    result=np.array(result)
    result=result.reshape(len(traindata),1)
    utils.updatecsv(filepath,result,["cosine"])

def test():
    outbdata=transform("data/train.txt")
    inbdata=transform("data/followers.txt")
    ft.edgerank(outbdata,inbdata,"1000021",'4335682')

if __name__ == '__main__':
    test()
    
    #extractER("data/traindata.csv")
    #extractER("data/fake_origin_clm.csv")
    #extractER("data/test-public.csv")
    #extractER("data/testdata.csv")

    #extractCosine("data/traindata.csv")
    #extractCosine("data/test-public.csv")
    #extractCosine("data/testdata.csv")
    #extractCosine("data/fake_origin_clm.csv")
    
    #extractJC("data/testdata.csv")
    #extractJC("data/traindata.csv")
    #extractJC("data/test-public.csv")
    #extractJC("data/fake_origin_clm.csv")
    
    print('end...')
