"""
utilities
"""
import pandas as pd
import csv
import numpy as np

class stack:
    def __init__(self):
        self.list=[]

    def push(self,item):
        self.list.append(item)

    def pop(self):
        return self.list.pop()

    def isEmpty(self):
        return len(self.list)==0

class queue:
    def __init__(self):
        self.list=[]

    def push(self,item):
        self.list.insert(0,item)

    def pop(self):
        return self.list.pop()

    def isEmpty(self):
        return len(self.list)==0

'''######################################################
    File io
    ##################################################'''
    
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
    
def txt2CSV(filename):
    result={}
    txtfile=filename+".txt"
    with open(txtfile) as reader:
        for line in reader:
            ids = line.split()
            result[ids[0]] = set(ids[1:])
    result.pop("Id")
    csvfile="data/"+filename+".csv"
    ft=["ID","Source","Sink"]
    reader=pd.DataFrame(reader,ft)
    reader.to_csv(path=csvfile)

def conversion(filename):
    result=[]
    txtfile=filename
    with open(txtfile) as reader:
        for line in reader:
            k=line.split()
            print(k)
            result.append(k)
    ft=["Source","Sink",'y']
    result=np.array(result)
    result=pd.DataFrame(result,columns=ft)
    result.index+=1
    result.to_csv("data/fake_origin_clm.csv")
            
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

def transform(input_path):
    result = {}
    with open(input_path) as reader:
        for line in reader:
            ids = line.split()
            result[ids[0]] = set(ids[1:])
    print("read from {} successful".format(input_path))
    return result

def updatecsv(filepath,newdata,header):# new data should be an np array
    data=pd.read_csv(filepath)
    newcols=len(header)
    print(newdata.shape)
    print(newcols)
    if newcols==1:
        data[header[0]]=newdata
    else:
        for i in range(newcols):
            data[header[i]]=newdata[:,i]
    data.to_csv(filepath,index=False)
    print("update {} to {} successful".format(header,filepath))
    

def combine_dict(dict1,dict2):
    newdict={}
    for i in dict1:
        newdict[i]=dict1[i]
    for i in dict2:
        if i in newdict:
            content=newdict[i]
            newcontent=content | dict2[i]
            newdict.update({i:newcontent})
        else:
            newdict[i]=dict2[i]
    print("data combine successful")
    return newdict   

if __name__=="__main__":
    conversion("data/fake_origin_clm.txt")
