from reader import transform
from reader import readCSV
from reader import addFeature
import features as ft
import numpy as np
from sklearn.linear_model import LogisticRegression
import random
import csv

def extractER(purpose):
    filename=purpose+"data.csv"
    train=readCSV(filename)
    print(train[1:])
    raw_out,sources=transform("train.txt")
    raw_in,sinks=transform("followers.txt")
    edgerank=[]
    for line in train:
        ID,source,sink,y=line
        er=ft.edgerank(raw_out,raw_in,source,sink)
        edgerank.append(er)
        print("edgerank {}-{} solved".format(source,sink))
    addFeature(edgerank,"edgerank2",purpose)
    print("Edgerank extraction complete")

if __name__ == '__main__':
    extractER("test")
    print('end...')
