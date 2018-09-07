""" transform txt source file to [key: [set]]
"""


import numpy as np
import pandas as pd
from utils import transform,combine_dict,put2TXT
import matplotlib.pyplot as plt

'''############################################################################
    Data reduction
    ########################################################################'''
def trimzeros(mydict):
    newdict={}
    for i in mydict:
        if not len(mydict[i])<2:
            newdict[i]=mydict[i]
    return newdict

# leave the nodes with the most neigbours, used in bfs
def trimMaxNB(mydict,th=50): # trim considering both in and out bounds
    newdict={}
    for i in mydict:
        if len(mydict[i])<th:
            newdict[i]=mydict[i]
        else:
            srt_lst=[]
            for nb in mydict[i]:
                if nb in mydict:
                    srt_lst.append([len(mydict[nb]),nb])
                else:
                    srt_lst.append([0,nb])
            srt_lst=sorted(srt_lst,reverse=True)
            
            newnb=set()
            for newnbs in range(th):
                newnb.add(srt_lst[newnbs][1])
            newdict[i]=newnb
    put2TXT(newdict,"data/nbtMax.txt")

# leave with the followers who follows the least users, used in page/edge rank
def trimMinIB(outb,inb,th=50): # trim considering both in and out bounds
    newdict={}
    for sink in inb:
        sources=inb[sink]
        if len(sources)<th:
            newdict[sink]=sources
        else:
            srt_lst=[]
            for source in sources:
                if source in outb:
                    srt_lst.append([len(outb[source]),source])
            srt_lst=sorted(srt_lst)
            newsrc=set()
            for news in range(th):
                newsrc.add(srt_lst[news][1])
            newdict[sink]=newsrc
    put2TXT(newdict,"data/inbtMin.txt")
        
def inBound(data):
    newdata={}
    for i in data:
        iset=data[i]
        for j in iset:
            newdata.setdefault(j,set()).add(i)
    put2TXT(newdata,"data/complete_in.txt")
    return newdata



'''###############################################################################
    Aimed to make a training set in the form of source-sink-y
    including 10000 real data (True positives) and
    10000 fake data (True negatives and False negatives)
    #############################################################################'''
def makeTrainingset(outB,inB):

    pos=makepositive(outB,inB)
    neg=makenegative(outB,inB)
    trainingdata=pos+neg
    trainingdata.sort()
    # add an id for each list of data
    index=1
    for data in trainingdata:
        data.insert(0,index)
        index+=1
    return trainingdata

def makeTestingset(outB,inB):
    outBPath="data/train.txt"
    inBPath="data/followers.txt"

    outB=transform(outBPath)
    outB=trimzeros(outB)
    inB=transform(inBPath)
    inB=trimzeros(inB)
    sources=list(outB.keys)
    sinks=list(inB.keys)
    pos=makepositive(outB,sources,sinks)
    neg=makenegative(outB,sources,sinks)
    trainingdata=pos+neg
    trainingdata.sort()
    # add an id for each list of data
    index=1
    for data in trainingdata:
        data.insert(0,index)
        index+=1
    return trainingdata

def makepositive(outB,inB):
    
    sources=list(outB.keys())
    
    sinks=list(inB.keys())
    
    positiveset=[]
    for i in range(40):
        sourceset=np.random.choice(sources,25)
        for source in sourceset:
            sinkset=outB[source]
            if len(sinkset)>0:
                
                sink=np.random.choice(list(sinkset))
                newdata=[source,sink,1]
                if newdata not in positiveset:
                    positiveset.append(newdata)
    print("positive batch making finished, current length of data {}".format(len(positiveset)))
    while len(positiveset)<1000:
        source=np.random.choice(sources)
        sinkset=outB[source]
        if len(sinkset)>0:
            sink=np.random.choice(list(sinkset))
            newdata=[source,sink,1]
            if newdata not in positiveset:
                positiveset.append(newdata)
    print("positive training set created. {}".format(len(positiveset)))
    return positiveset

def makenegative(outB,inB):
    sources=list(outB.keys())
    sinks=list(inB.keys())
    negativeset=[]
    for i in range(40):
        print(len(negativeset))
        sourceset=np.random.choice(sources,25)
        for source in sourceset:
            sink=np.random.choice(sinks)
            if sink not in outB[source]:
                newdata=[source,sink,0]
                if newdata not in negativeset:
                    negativeset.append(newdata)
    print("negative batch making finished, current length of data {}".format(len(negativeset)))
    while len(negativeset)<1000:
        source = np.random.choice(sources)
        sink=np.random.choice(sinks)
        if sink not in outB[source]:
            newdata=[source,sink,0]
            if newdata not in negativeset:
                negativeset.append(newdata)
    print("negative training set created. {}".format(len(negativeset)))
    return negativeset

'''############################################################################
    Data obvervation
    ########################################################################'''
def data_properties():
    outbdata=transform("data/train.txt")
    inbdata=transform("data/followers.txt")
    overall=combine_dict(outbdata,inbdata)
    minlen=9999
    maxlen=0
    bd={}
    avg=0
    for index in overall:
        item=overall[index]
        mylen=len(item)
        if mylen not in bd:
            bd[mylen]=0
        bd[mylen]+=1
        avg+=mylen
        if minlen > mylen:
            minlen=mylen
        if maxlen < mylen:
            maxlen=mylen
    avg/=len(overall)
    sbd=[[k,bd[k]] for k in sorted(bd,key=bd.get,reverse=True)]

    print("node with the minimum link has a number of {}".format(minlen))
    print("node with the max has a number of {}".format(maxlen))
    print("average bounds for overall data being {}".format(avg))
    print("number of bounds top 10:")
    print(sbd[:10])

def csv_datafrequencies(filepath):
    outbdata=transform("data/complete_out.txt")
    #inbdata=transform("data/complete_in.txt")
    data=pd.read_csv(filepath)
    sources=data["source"].values
    sinks=data["sink"].values
    # newdict stores follower-|followees|
    newdict={}
    for i in outbdata:
        newdict[i]=len(outbdata[i])
    newdict2={}
    for i in range(len(sources)):
        source=str(int(sources[i]))
        if source not in outbdata:
            continue
        iset = outbdata[source]
        if len(iset) not in newdict2:
            newdict2[len(iset)]=0
        newdict2[len(iset)]+=1
    x=[]
    y=[]
    for i in newdict2:
        x.append(i)
        y.append(newdict2[i])
    plt.plot(x,y,'o')
    plt.xlabel("number of followees")
    plt.ylabel("count")
    plt.xlim(0,6000)
    plt.show()
        
        

def csv_dataproperties(filepath):
    outbdata=transform("data/train.txt")
    outbdata=trimzeros(outbdata)
    inbdata=transform("data/followers.txt")
    data=pd.read_csv(filepath)
    data=data.values
    avg_outb=0
    avg_inb=0
    fake_source=[]# sources that are actually sinks (but not source)
    fake_sink=[]# sinks that are actually sources (but not a sink)
    outbdict={}
    inbdict={}
    non_data=[]
    for source,sink in data[:,1:3]:
        source=str(source)
        if source not in outbdata:
            if source in inbdata:
                fake_source.append(source) 
            else:
                non_data.append(source)
            continue
        outb=len(outbdata[source])
        if outb not in outbdict:
            outbdict[outb]=0
        outbdict[outb]+=1
        avg_outb+=outb
        
   
        sink=str(source)
        if sink not in inbdata:
            if sink in outbdata:
                fake_sink.append(sink) 
            else:
                non_data.append(sink)
            continue
        inb=len(inbdata[sink])
        if inb not in inbdict:
            inbdict[inb]=0
        inbdict[inb]+=1
        avg_inb+=inb
    avg_inb/=len(data)     
    avg_outb/=len(data)-len(fake_source)
    o=[[k,outbdict[k]] for k in sorted(outbdict,key=outbdict.get,reverse=True)]
    i=[[k,inbdict[k]] for k in sorted(inbdict,key=inbdict.get,reverse=True)]
    #d=[(k,outbdict[k]) for k in sorted(outbdict)]
    #mid=int(len(d)/2)
    print("average outbounds for {} being {}".format(filepath,avg_outb))
    print("number of fake sources being {}".format(len(fake_source)))
    print("number of sources disappeared in data {}".format(len(non_data)))
    print("number of outbounds top 10:")
    print(o)
    print("average inbounds for {} being {}".format(filepath,avg_inb))
    print("number of fake sinks being {}".format(len(fake_sink)))
    print("number of sinks disappeared in data {}".format(len(non_data)))
    print("number of inbounds top 10:")
    print(i[:10])
    ss=np.array(o)
    print(ss.shape)
    plt.plot(ss[:,0],ss[:,1],'ro')
    plt.xscale('log')
    plt.show()
    #print("outbound mid number: {}".format(d[mid]))

def oridata():
    '''outbdata=transform("data/complete_out.txt")
    newdict1=[[k,len(outbdata[k])] for k in outbdata]
    x,y=getFreq(outbdata)
    dt1=pd.DataFrame.from_dict(newdict1)
    plt.plot(x,y,'o')
    plt.xlim(0,6000)
    plt.xlabel("number of followees")
    plt.ylabel("count")
    plt.show()
    print(dt1.describe())'''
    inbdata=transform("data/complete_in.txt")
    newdict2=[[k,len(inbdata[k])] for k in inbdata]
    x,y=getFreq(inbdata)
    plt.plot(x,y,'o')
    plt.xlabel("number of followers")
    plt.xlim(0,600)
    plt.ylabel("count")
    plt.show()
    dt2=pd.DataFrame.from_dict(newdict2)
    print(dt2.describe())

def invert(d):
    newdict={}
    for k in d:
        for v in d[k]:
            newdict.setdefault(v,[]).append(k)
    return newdict

def getFreq(mydict):

    # newdict stores follower-|followees|
    newdict={}
    for i in mydict:
        newdict[i]=len(mydict[i])

    # newdict2 stores |followees|-|followers|
    newdict2={}
    for i in newdict:
        num=newdict[i]
        if num not in newdict2:
            newdict2[num]=0
        newdict2[num]+=1
    x=[]
    y=[]
    for i in newdict2:
        x.append(i)
        y.append(newdict2[i])
    return x,y
    
def trimPR():
    outbdata=transform("data/train.txt")
    newdict={}
    for item in outbdata:
        if len(outbdata[item])<10000:
            newdict[item]=outbdata[item]
    put2TXT(newdict,"train_pr")

def completeSet():
    data=transform("data/train.txt")
    newdata={}
    for i in data:
        iset=data[i]
        newdata[i]=iset
        for j in iset:
            if j not in data:
                newdata.setdefault(j,set())
    put2TXT(data,"data/complete.txt")
    return data
if __name__ == '__main__':
    
    #data=transform("data/complete_out.txt")
    #inBound(data)
    #trimPR()
    oridata()
    #data_properties()
    #set_properties("data/test-public.csv")
    #outbdata=transform("data/train.txt")
    #inbdata=transform("data/followers.txt")
    #combine=combine_dict(outbdata,inbdata)
    #trimMinIB(outbdata,inbdata)
    '''testingset=makeTestingset()
    ft=['ID',"source",'sink','y']
    putlist2CSV(testingset,ft,"testdata")
    _
    path='tryout'
    readCSV(path)
    '''
    

    

