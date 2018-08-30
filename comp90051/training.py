# -*- coding: utf-8 -*-
"""
Created on Sat Aug 25 13:57:59 2018

@author: Administrator
"""

from reader import transform
from reader import readCSV
from reader import addFeature
import extract as ft
from utils import plot_results
import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
import random
import csv

'''def trimData(data):
    for source in data:
        sinkset=data[source]
        n_sinkset={}
        for sink in sinkset:'''

    
def weightedSum(X,w,b):
    return np.dot(X,w)+b

def predict(X,w,b):
    return np.where(weightedSum(X,w,b)>=0,1,-1)

def getXY(data,namecard,ft_ex):
    X=np.array([])
    Y=np.array([])
    for source in data:
        sink_set = data[source]
        neg_sink_set=set(namecard)-sink_set-{source}
        neg_sink_list=list(neg_sink_set)

        data_size=len(neg_sink_set)
        length=min(data_size,len(sink_set))
        rand_index=randList(length,data_size)
        rand_neg=np.array([])
        for i in rand_index:
            rand_neg=np.append(rand_neg,neg_sink_list[i])
        for sink in sink_set:
            if sink in data:
                for extraction in ft_ex:
                    X=np.append(X,extraction(data,source,sink))
                Y=np.append(Y,1)
        for sink in rand_neg:
            if sink in data:
                for extraction in ft_ex:
                    X=np.append(X,extraction(data,source,sink))
                Y=np.append(Y,-1)
    X=X.reshape(len(Y),len(ft_ex))
    return X,Y


def writeCSV(data):
    myFile=open('fsttrydata.csv','w')
    with myFile:
        writer = csv.writer(myFile)
        writer.writerows(data)
    print("writing complete")

# perceptron
def percept(X,Y,n_epochs,eta):
    w=np.zeros(len(ft_ex))
    b=-1
    for t in n_epochs:
        for i in range(X.shape[0]):
            yhat=predict(X[i,:],w,b)
            if yhat*Y[i]<=0:
                w+=eta*X[i,:]*Y[i]
                b+=eta*Y[i]
    return w,b

def getFeature(data,source,sink,ft_ex):
    feature=np.array([])
    for extract in ft_ex:
        feature=np.append(feature,extract(data,source,sink))
    return feature

def LR(feature):
    data=readCSV(feature)
    m,n=data.shape

    X_train=data[:,5]
    X_train=X_train.astype(np.float)
    X_train=X_train.reshape((-1,1))
    Y_train=data[:,3]
    Y_train=Y_train.astype(np.float)
    clf=LogisticRegression()
    clf.fit(X_train,Y_train)
    
    testdata=readCSV("testfeatures.csv")
    X_test=testdata[:,5]
    X_test=X_test.astype(np.float)
    X_test=X_test.reshape((-1,1))
    Y_test=testdata[:,3]
    Y_test=Y_test.astype(np.float)
#    plot_results(X_train, Y_train,X_test,Y_test,lambda X: clf.decision_function(X))
    score=clf.score(X_test,Y_test)
    print(score)







'''get the feature score of key and all other users using a specified feature'''
def getAll(key,data,ft_ex):
    key_set=data[key]
#    length=len(key_set)
    
    # all other users except for this id and the users it is following
#    otherusers=list(set(namecard) - key_set - {key})
#    no_other_users= len(otherusers)
    w=[]
    y=[]
    for k in key_set:
        if k in data:
            w.append(ft_ex(data,key,k))
            y.append(1)
    return w,y    
    # generate a none-repeated random list
'''    rand=randList(length,no_other_users)
    for i in rand:
        thisuser=otheruser[i]
        w.append(ft_ex(data,otherusers[i],key))
        y.append(-1)'''

# generate a list of non-repeated random ints within range
def randList(length,ceil):
    thisset=set()
    while len(thisset)<length:
        thisset.add(random.randint(0,ceil-1))
    return list(thisset)



'''x,y=getXY(train,ft.adar)

x=np.array(x)
length=len(x)
x=x.reshape(length,1)
clf=LogisticRegression()
clf.fit(x,y)
error=1.0-clf.score(x,y)
print("error={}".format(error))'''
if __name__ == '__main__':
    LR("trainfeatures.csv")
    print('end...')
