import math
import random
import sys
from statistics import stdev
import operator
class Node:
    def __init__(self, attrs=[], predict = ""):
        self.attrs = attrs
        self.predict = predict
        self.children=[]
        self.leaf=False

    def addchild(self,child):
        self.children.append(child)

    def setpredict(self,value):
        self.leaf=True
        self.predict=value
    def isleaf(self):
        return (self.leaf)
    def getpredicts(self):
        return self.predict
    def getattrs(self):
        return self.attrs
    def getchildren(self):
        return self.children
    def setattrs(self,attrs):
        self.attrs = attrs


def findmostcommon(file,attr):
    dictionary=dict()
    print("inside mostcommon")
    print(attr)
    with open(file, 'r') as f:
        for line in f:
            n=0
            for word in line.split(','):
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


def load(file,forget):
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
            for word in line.split(','):
                if i not in forget:
                    if word.strip()!='?':
                        attr[t].append(word.strip())
                    else:
                        x=findmostcommon(file, i)
                        attr[t].append(x)
                        print(x)
                i=i+1

            t += 1
    return attr

def listofnumberofsamoles(train, attrs):
    if len(attrs)==0:
        return len(train)
    total=0
    for sample in train:
        n = 0
        for attr in attrs:
            if (sample[attr[0]] == attr[1]):
                n = n + 1
                if (n == len(attrs)):
                    total = total+1
    return total

def listofpossiblevalues(train,attr):
    l=[]
    for sample in train:
        if sample[attr] not in l:
            l.append(sample[attr])
    return l


def entropy(train, attrs):
    if(len(attrs)!=0):
        dictionary = dict()
        total = listofnumberofsamoles(train,attrs)
        for sample in train:
            n = 0
            for attr in attrs:
                if (sample[attr[0]] == attr[1]):
                    n = n + 1
                    if (n == len(attrs)):
                        if (sample[len(sample) - 1] in dictionary):
                            dictionary[sample[len(sample) - 1]] = dictionary[sample[len(sample) - 1]] + 1
                        else:
                            dictionary[sample[len(sample) - 1]] = 1
        ent=0
        for i in dictionary.items():
            p_x = i[1]/total
            ent += - p_x * math.log(p_x, 2)
        return ent
    else:
        dictionary = dict()
        total = listofnumberofsamoles(train,attrs)
        for sample in train:
            if (sample[len(sample) - 1] in dictionary):
                dictionary[sample[len(sample) - 1]] = dictionary[sample[len(sample) - 1]] + 1
            else:
                dictionary[sample[len(sample) - 1]] = 1
        ent=0
        for i in dictionary.items():
            total=float(total)
            p_x = float(i[1]/total)
            ent += - p_x * math.log(p_x, 2)
        return ent


def infogain(train,attrs,attr):
    #with current attrs in place, what is info gain of attr
    total = listofnumberofsamoles(train,attrs)
    currententr = entropy(train,attrs)
    reduce = 0
    listofpossible=listofpossiblevalues(train,attr)
    for l in listofpossible:
        newattre = []
        for a in attrs:
            newattre.append(a)
        newattre.append([attr, l])
        newtotal = listofnumberofsamoles(train,newattre)
        e=entropy(train,newattre)



        reduce = reduce+(newtotal/total)*e
    #print(currententr-reduce)
    return currententr-reduce


def id3(train,attrs):
    #print("entering id3")
    #print(attrs)
    node=Node()
    node.setattrs(attrs)
    if(len(attrs)==0):
        infogains=[]
        info=0
        useattr=-1
        for attr in range(len(train[0])-1):
            gain=infogain(train,attrs,attr)
            if gain > info:
                useattr=attr
                info=gain
        listofposval = listofpossiblevalues(train,useattr)
        for l in listofposval:
            newattr=[]
            for a in attrs:
                newattr.append(a)

            newattr.append([useattr, l])
            #print(newattr)
            n = id3(train, newattr)
            if (not n.isleaf()):
                node.addchild(n)
            else:
                if (n.getpredicts() != " "):
                    node.addchild(n)

        return node
    else:
        dictionary = dict()
        for sample in train:
            n = 0
            for attr in attrs:
                if (sample[attr[0]] == attr[1]):
                    n = n + 1
                    if (n == len(attrs)):
                        if (sample[len(sample) - 1] in dictionary):
                            dictionary[sample[len(sample) - 1]] = dictionary[sample[len(sample) - 1]] + 1
                        else:
                            dictionary[sample[len(sample) - 1]] = 1
        #print("dictionary:")
        #print(dictionary)
        if len(dictionary.keys()) > 1:
            #nopure
            if(len(attrs)>5):
                sorted_x = sorted(dictionary.items(), key=operator.itemgetter(1))
                x = list(sorted_x)
                node.setpredict(x[len(x)-1][0])
                return node

            infogains = []
            info = -1
            useattr = -1
            canuseattrs=[]
            allattrs=[]
            for attr in range(len(train[0])-1):
                allattrs.append(attr)
            for attr in attrs:
                allattrs.remove(attr[0])
            for attr in allattrs:
                gain = infogain(train, attrs, attr)
                if gain > info:
                    useattr = attr
                    info = gain
            listofposval = listofpossiblevalues(train, useattr)
            for l in listofposval:
                newattr = []
                for a in attrs:
                    newattr.append(a)

                newattr.append([useattr, l])
                #print(newattr)
                n=id3(train, newattr)
                if(not n.isleaf()):

                    node.addchild(n)
                else:
                    if(n.getpredicts() != " "):
                        node.addchild(n)

            return node

        else:
            #pure
            if(len(list(dictionary.keys()))==1):
                node.setpredict(list(dictionary.keys())[0])
                return node
            else:
                #r=random.randint(0, len(train)-1)
                #print(r)
                #print(train[r])
                node.setpredict(" ")
                return node


def samplematchattrs(sample, attrs):
    # attrs non empty
    n = 0
    for a in attrs:
        #print(sample[a[0]])
        #print(a[1])
        if (type(sample[a[0]]) == type(1)):
            sample[a[0]] = str(sample[a[0]])
        if (type(a[0]) == type(1)):
            a[1] = str(a[1])
        if (sample[a[0]] == a[1]):
            n = n + 1
            if (n == len(attrs)):
                return True
    return False


def predict(sample,root):
    if(root.isleaf()):
        #print("inleaf")
        return root.getpredicts()
    else:
        attrs=root.getattrs()
        #print("attrs in predict:")
        #print(attrs)
        #print(root.getchildren())
        if(len(attrs)==0):
            for child in root.getchildren():
               # print("child attrs")
                #print(child.getattrs())
                if(samplematchattrs(sample,child.getattrs())):
                    #print("samplematch")
                    return predict(sample,child)
            return predict(sample,root.getchildren()[0])

        else:
            for child in root.getchildren():
                #print("child attrs2")
               # print(child.getattrs())
                if(samplematchattrs(sample,child.getattrs())):
                    #print("samplematch2")
                    return predict(sample,child)
            return predict(sample,root.getchildren()[0])


def findrange(data,cont):
    min=sys.float_info.max
    max=sys.float_info.min

    for i in data:
        if float(i[cont])<min:
            min=float(i[cont])
        if float(i[cont])>max:
            max=float(i[cont])
    return [min,max]


def findgainofcont(data,cont,splitpoint):
    newdata=[]
    for i in data:
        newdata.append([])
    y=0
    for i in data:
        y=y+1
        for j in i:
            newdata[y-1].append(j)
    for i in newdata:
        if float(i[cont])>splitpoint:
            i[cont]='a'
        else:
            i[cont]='b'
    return infogain(data,[],cont)

def splitcont(data,cont,rangeofcont):
    newdata = []
    length=(rangeofcont[1]-rangeofcont[0])/10.0
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
    return newdata



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
    data = loadfirstcol("letter-recognition.data", [])
    random.shuffle(data)
    conts = []
    for cont in conts:
        rangeofcont = findrange(data, cont)
        data = splitcont(data, cont, rangeofcont)
    print("dataloaded")
    acc = 0.0
    testlen = int(len(data) / 5)
    allacc = []

    for x in range(5):
        test = data[x * testlen:x * testlen + testlen]
        train = data[0:x * testlen] + data[x * testlen + testlen:]
        root = id3(train, [])



        print("id3 trained...")
        for j in range(10):
            accuracy=0
            for i in range(len(test)):
                if predict(test[i], root) == test[i][len(test[0]) - 1]:
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

