""" transform txt source file to [key: [set]]
"""


import csv
import numpy as np

'''
def transform(input_path):
    result = {}
    namecard=[]
    i=0
    with open(input_path) as reader:
        for line in reader:
            ids = line.split()
            if i < 30:
                result[ids[0]] = set(ids[1:])
                namecard.append(ids[0])
                i+=1
    return result,namecard
'''
def readCSV(path):
    data=[]
    with open(path,'r') as trainingset:
        reader=csv.reader(trainingset)
        data=np.array(list(reader))
    print(data.shape)
    print(type(data))
    print("read from {} complete".format(path))
    return data[1:]
    
def transform(input_path):
    result = {}
    namecard=[]
    maxfollow=0
    minfollow=200
    with open(input_path) as reader:
        for line in reader:
            ids = line.split()
            result[ids[0]] = set(ids[1:])
            namecard.append(ids[0])
            l=len(ids[1:])
            if maxfollow<l:
                maxfollow=l
            if minfollow>l:
                minfollow=l
    print("the maximum number of accounts a user follows is {}".format(maxfollow))
    print("likewise, the minimum is {}".format(minfollow))
    return result,namecard
#'''

def put2TXT(data,filename):
    filename+=".txt"
    myfile=open(filename,'w')
    for key in data:
        row=key
        keyset=data[key]
        for item in keyset:
            row+=" "+item
        myfile.write(row)
        myfile.write('\n')
    myfile.close()
    print("write to txt complete")
    
# put data (complete set)
def put2CSV(data,features,filename):
    with open(filename,'w',newline='') as outcsv:
        writer=csv.writer(outcsv)
        writer.writerow(features)
        for key in data:
            row=[key]
            keyset=data[key]
            for item in keyset:
                row.append(item)
            writer.writerow(row)
    print("write in csv complete")
    
# put data (complete set)
def putlist2CSV(data,features,filename):
    with open(filename,'w',newline='') as outcsv:
        writer=csv.writer(outcsv)
        writer.writerow(features)
        writer.writerows(data)
    print("write in csv complete")
    
# update by feature
def addFeature(newfeature,name,purpose):
    filepath=purpose+"features.csv"
    with open(filepath,'r') as incsv:
        reader=csv.reader(incsv)

        all=[]
        hrow=next(reader)
        hrow.append(name)

        i=0
        for row in reader:
            print(i)
            print(row)
            print(newfeature[i])
            row.append(newfeature[i])
            all.append(row)
            i+=1
    with open(filepath,'w',newline='') as outcsv:
        writer=csv.writer(outcsv)
        writer.writerow(hrow)
        writer.writerows(all)
    print("update rows complete")

def inBound(data):
    dt={}
    i=0
    for source in data:
        myset=data[source]
        for sink in myset:
            followerset=dt.get(sink)

            if followerset==None:
                followerset=set([source])
            else:
                if sink=='2789436':
                    i+=1
                followerset.add(source)
            dt[sink]=followerset
    print("followers collection complete")
    print("i={}".format(i))
    return dt

'''
    Aimed to make a training set in the form of source-sink-y
    including 10000 real data (True positives) and
    10000 fake data (True negatives and False negatives)
    '''
def makeTrainingset():
    outBPath="train.txt"
    inBPath="followers.txt"

    outB,sources=transform(outBPath)
    inB,sinks=transform(inBPath)

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

def makeTestingset():
    outBPath="train.txt"
    inBPath="followers.txt"

    outB,sources=transform(outBPath)
    inB,sinks=transform(inBPath)

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

def makepositive(outB,sources,sinks):
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

def makenegative(outB,sources,sinks):
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


if __name__ == '__main__':
    testingset=makeTestingset()
    ft=['ID',"source",'sink','y']
    putlist2CSV(testingset,ft,"testdata")
    '''_
    path='tryout'
    readCSV(path)

    trainingset=makeTrainingset()
    ft=['ID',"source",'sink','y']
    putlist2CSV(trainingset,ft,"features")

    dt,nc=transform("train.txt")
    inb=inBound(dt)
    
    put2TXT(inb,'followers')
    '''

    

