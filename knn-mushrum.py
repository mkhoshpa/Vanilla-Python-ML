

import sys
import random

import operator
from statistics import stdev

def findrange(data,cont):
    min=sys.float_info.max
    max=sys.float_info.min

    for i in data:
        if float(i[cont])<min:
            min=float(i[cont])
        if float(i[cont])>max:
            max=float(i[cont])
    return [min,max]


def findmostcommon(file,attr,splitor):
    dictionary=dict()
    print("inside mostcommon")
    print(attr)
    with open(file, 'r') as f:
        for line in f:
            n=0
            if(splitor != ' '):
                for word in line.split(splitor):
                    n=n+1
                    if(n==attr):
                        if(word.strip() not in dictionary):
                            dictionary[word.strip()]=1
                        else:
                            dictionary[word.strip()] += 1
            else:
                for word in line.split():
                    n=n+1
                    if(n==attr):
                        if(word.strip() not in dictionary):
                            dictionary[word.strip()]=1
                        else:
                            dictionary[word.strip()] += 1
    print(dictionary)
    sorted_x = sorted(dictionary.items(), key=operator.itemgetter(1))
    x=list(sorted_x)
    print(x)
    return x[len(x)-1][1]


def load(file,forget,splitor):
    attr = []
    t = 0
    with open(file, 'r') as f:

        for line in f:
            t += 1
    with open(file, 'r') as f:
        for i in range(t):
            attr.append([])
        t=0
        for line in f:
            i = 0
            if(splitor != ' '):
                for word in line.split(splitor):
                    if i not in forget:
                        if word.strip()!='?':
                            attr[t].append(word.strip())
                        else:
                            x=findmostcommon(file, i,splitor)
                            attr[t].append(x)
                            print(x)
                    i=i+1

                t += 1
            else:
                for word in line.split():
                    if i not in forget:
                        if word.strip() != '?':
                            attr[t].append(word.strip())
                        else:
                            x = findmostcommon(file, i, splitor)
                            attr[t].append(x)
                            print(x)
                    i = i + 1

                t += 1
    return attr



def splitcont(data,cont,rangeofcont):
    newdata = []
    length=(rangeofcont[1]-rangeofcont[0])/3.0
    for i in data:
        newdata.append([])
    y = 0
    for i in data:
        y = y + 1
        for j in i:
            newdata[y - 1].append(j)
    for i in newdata:
        cat = int((float(i[cont]) - rangeofcont[0]) / length)
        if cat==0 :
            i[cont]='a'
        elif cat==1 :
            i[cont]='b'
        elif cat == 2:
            i[cont] = 'c'
        elif cat == 3:
            i[cont] = 'd'
        elif cat == 4:
            i[cont] = 'e'
        elif cat ==5:
            i[cont] = 'f'
        elif cat == 6:
            i[cont] = 'g'
        elif cat == 7:
            i[cont] = 'h'
        elif cat == 8:
            i[cont] = 'i'
        elif cat == 9:
            i[cont] = 'j'
        elif cat==10:
            i[cont]='k'
        elif cat == 11:
            i[cont] = 'l'
        elif cat == 12:
            i[cont] = 'm'
        elif cat == 13:
            i[cont] = 'n'
        elif cat == 14:
            i[cont] = 'o'
        elif cat == 15:
            i[cont] = 'p'
        elif cat == 16:
            i[cont] = 'q'
        elif cat == 17:
            i[cont] = 'r'
        else:
            i[cont]='s'
    return newdata



def distanceCtegorical(a,b):
    dis=0
    for i in range(len(a)-1):
        if a[i] != b[i]:
            dis+=1
    return dis

def distancenumerical(a,b):
    dis = 0
    for i in range(len(a) - 1):
        dis+= abs(float(a[i])-float(b[i]))
    return dis


def distancenumerical2(a,b):
    dis = 0
    for i in range(len(a) - 1):
        dis+= abs(float(a[i])-float(b[i]))**2
    return dis

def distancenumerical3(a,b):
    dis = 0
    for i in range(len(a) - 1):
        if(abs(float(a[i])-float(b[i]))>dis):
            dis=abs(float(a[i])-float(b[i]))
    return dis

def predict(train,sample,k=5):
    alldistance=[]
    for i in train:
        dist=distanceCtegorical(i,sample)
        alldistance.append([dist,i[len(i)-1]])
    sorted_distance = sorted(alldistance, key=lambda tup: tup[0])
    sorted_distance=sorted_distance[0:k]
    dict={}
    for i in sorted_distance:
        if i[1] in dict:
            dict[i[1]]+=1
        else:
            dict.update({i[1]:1})

    sorted_x = sorted(dict.items(), key=operator.itemgetter(1),reverse=True)
    x = list(sorted_x)
    return x[0][0]

def loadfirstcol(file,forget):
    attr = []
    t = 0
    with open(file, 'r') as f:

        for line in f:
            t += 1
    with open(file, 'r') as f:
        for i in range(t):
            attr.append([])
        t=0
        for line in f:
            i = 0
            w = ""
            for word in line.split(','):

                if(i != 0):
                    if i not in forget:
                        if word.strip()!='?':
                            attr[t].append(word.strip())
                        else:
                            x=findmostcommon(file, i)
                            attr[t].append(x)
                            #print(x)
                    i=i+1
                else:
                    w= word.strip()
                    i+=1
            attr[t].append(w)


            t += 1
    return attr



def main():

    data = loadfirstcol("agaricus-lepiota.data", [11])
    random.shuffle(data)

    print("dataloaded")
    acc = 0.0
    testlen = int(len(data) / 5)
    x = 1
    conts = []
    for cont in conts:
        rangeofcont = findrange(data, cont)
        data = splitcont(data, cont, rangeofcont)
    # print(data)
    allacc = []

    for x in range(5):
        test = data[x * testlen:x * testlen + testlen]
        train = data[0:x * testlen] + data[x * testlen + testlen:]
        predict(train,test[50],5)
        for j in range(10):
            accuracy =0
            for i in range(len(test)):
                if predict(train,test[i]) == test[i][len(test[0]) - 1]:
                    acc = acc + 1
                    accuracy += 1
            allacc.append(accuracy / len(test))
            print(accuracy / (len(test)))

    print("accuracy is:")
    print(acc / (len(test) * 50))
    print("accuracy is:")
    print(acc / (len(test) * 50))
    print(stdev(allacc))


if __name__ == "__main__": main()