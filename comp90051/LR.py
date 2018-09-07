# -*- coding: utf-8 -*-
"""
Created on Sat Aug 25 13:57:59 2018

@author: Administrator
"""
import pandas as pd
import pickle
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.metrics import roc_curve, auc, accuracy_score
from utils import updatecsv

    
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
'''############################################################################
    Training Algorithms
    ########################################################################'''
def LR(load_from,save_model_to):
    data=pd.read_csv(load_from)
    X_train=data["ER"]
    X_train=X_train.values
    X_train=X_train.reshape(-1,1)
    Y_train=data['y']
    clf=LogisticRegression()
    clf.fit(X_train,Y_train)
    pickle.dump(clf,open(save_model_to,'wb'))

def SVM(load_from, save_model_to):
    data=pd.read_csv(load_from)
    data=data.values
    X_train=data[:,4:]
    Y_train=data[:,3]
    clf=svm.SVC(probability=True,C=1,kernel='rbf')
    clf.fit(X_train,Y_train)
    pickle.dump(clf,open(save_model_to,'wb'))
    print("SVM model training complete")
    

'''##########################################################################
    Applying models to test files
    ######################################################################'''
def predictTest(testfile,modelfile):
    model=pickle.load(open(modelfile,'rb'))
    testdata=pd.read_csv(testfile)
    testdata=testdata.values
    X_test=testdata[:,4:]
    #X_test=X_test.values
    #X_test=X_test.reshape(-1,1)
    Y_test=testdata[:,3]
    Y_pred=model.predict(X_test)
    
    result=model.predict_proba(X_test)[:,1]
    fpr, tpr, thresholds = roc_curve(Y_test, result)
    area = auc(fpr, tpr)
    print('auc', area)
    print(model.score)
    return result

def predictfinal(modelfile):
    ft=pd.read_csv("data/test-public.csv")
    X=ft["ER"]
    X=X.values
    X=X.reshape(-1,1)
    model=pickle.load(open(modelfile,'rb'))
    Y=model.predict_proba(X)[:,1]
    print(model.classes_)
    updatecsv("data/output.csv",Y,["Prediction"])





if __name__ == '__main__':
    #SVM("data/traindata.csv","models/SVM_4fts2.sav")
    #predictTest("data/testdata.csv","models/SVM_4fts2.sav")
    #LR("data/traindata.csv","models/ER-LR_1.sav")
    #predictTest("data/testdata.csv","models/ER-LR_1.sav")
    #SVM("data/traindata.csv","models/ER-LR_4.sav")
    predictTest("data/testdata.csv","models/ER-LR_4.sav")
    #predictfinal("models/ER-LR_4.sav")
    '''    LR("trainfeatures.csv","ER-LR.sav")
    print("model trained complete")
    score=predictTest("testfeatures.csv","ER-LR.sav")
    print("prediction test at precision {}".format(score))
    predictfinal("ER-LR.sav")
    print('end...')'''
