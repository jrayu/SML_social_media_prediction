# -*- coding: utf-8 -*-
"""
Created on Sat Aug 25 13:57:59 2018

@author: Administrator
"""
import pandas as pd
import pickle
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC, SVC
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV,cross_val_score
from sklearn.metrics import roc_curve, auc, accuracy_score
from utils import updatecsv,transform
import matplotlib.pyplot as plt
    

'''############################################################################
    Training Algorithms
    ########################################################################'''

def _svm(x_train, y_train, x_test=None, y_test=None):
    clf = svm.SVC(probability=True, C=1, kernel='rbf')
    clf.fit(x_train, y_train)

    if x_test is None or y_test is None:
        return clf

    y_pred = clf.predict(x_test)
    scores = clf.predict_proba(x_test)[:, 1]

    print('accuracy:', accuracy_score(y_test, y_pred))

    print(y_pred[y_pred==1].size)

    fpr, tpr, thresholds = roc_curve(y_test, scores)
    area = auc(fpr, tpr)
    print('auc', area)

    return clf

def readdata(filename):
    df=pd.read_csv(filename)
    
    train_df,test_df=train_test_split(df,test_size=0.3,random_state=1)
    x_train=extfeature(train_df)
    y_train=train_df.y

    x_test=extfeature(test_df)
    y_test=test_df.y
    print(y_test.size)

    
    
    
    cv=StratifiedKFold(n_splits=6)
    clf=SVC(probability=True,C=1,kernel='rbf')
    for train,test in cv.split(x_train,y_train):
        clf.fit(x_train,y_train)
        proba=clf.predict_proba(x_test)
        y_pred=clf.predict(x_test)
        print(y_pred[y_pred==1].size)
        fpr, tpr, thresholds = roc_curve(y_test,proba[:, 1])
        area = auc(fpr, tpr)
        print('accuracy:', accuracy_score(y_test,y_pred))
        print('auc', area)
    pickle.dump(clf,open("models/ER_SVM_ddi1",'wb'))
    #'''
    #return x_train,y_train,x_test,y_test

def _cross_evaluate():
    df=pd.read_csv("data/traindata.csv")
    x,y=extfeature(df)
    cross_evaluate(_svm,x,y,split=4)

def extfeature(df):
    scaler=StandardScaler()
    x1=df.ER_ddi
    x2=df.jaccard
    
    x7=df.cosine
    x=np.c_[x2,x7]
    x8=df.ER_ddi1
    x_test=scaler.fit_transform(x8.values.reshape(-1,1))
    return x_test
    
def predict():
    df=pd.read_csv("data/test-public.csv")
    #x=df.ER_ddi.values.reshape(-1,1)
    x=extfeature(df)
    #x=scaler.fit_transform(df.ER_ddi.values.reshape(-1,1))
    model=pickle.load(open("models/ER_SVM_ddi1",'rb'))
    y_pred=model.predict(x)
    print(y_pred[y_pred==1].size)
    y=model.predict_proba(x)[:,1]
    updatecsv("data/output.csv",y,["Prediction"])

def test():
    df=pd.read_csv("data/testdata.csv")
    x=extfeature(df)
    y=df.y
    model=pickle.load(open("models/ER_SVM_ddi1",'rb'))
    y_pred=model.predict(x)
    proba=model.predict_proba(x)
    print(y_pred[y_pred==1].size)
    fpr, tpr, thresholds = roc_curve(y,proba[:, 1])
    area = auc(fpr, tpr)
    print('accuracy:', accuracy_score(y,y_pred))
    print('auc', area)

def plotscatter(filename):
    df=pd.read_csv(filename)
    x=extfeature(df)
    y=df.y
    plt.scatter(x[y==1,-1],x[y==1,0],label="real link",c='r')
    plt.scatter(x[y==0,-1],x[y==0,0],label="fake link",c='b')
    plt.xlabel("ER_ddi1")
    plt.legend()
    plt.show()
    
if __name__ == '__main__':
    #plotscatter("data/testdata.csv")
    #readdata("data/testdata.csv")
    #_cross_evaluate()
    #predict()
    #test()
