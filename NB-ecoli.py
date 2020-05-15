import math
import random
import sys
from statistics import stdev

import operator


def findmostcommon(file, attr):
    dictionary = dict()
    print("inside mostcommon")
    print(attr)
    with open(file, 'r') as f:
        for line in f:
            n = 0
            for word in line.split():
                n = n + 1
                if (n == attr):
                    if (word.strip() not in dictionary):
                        dictionary[word.strip()] = 1
                    else:
                        dictionary[word.strip()] += 1
    # print(dictionary)
    sorted_x = sorted(dictionary.items(), key=operator.itemgetter(1))
    x = list(sorted_x)
    # print(x)
    return x[len(x) - 1][1]


def listofpossiblevalues(train, attr):
    l = []
    for sample in train:
        if sample[attr] not in l:
            l.append(sample[attr])
    return l


def load(file, forget):
    attr = []
    t = 0
    with open(file, 'r') as f:

        for line in f:
            t += 1
    with open(file, 'r') as f:
        for i in range(t):
            attr.append([])
        t = 0
        for line in f:
            i = 0
            for word in line.split():
                if i not in forget:
                    if word.strip() != '?':
                        attr[t].append(word.strip())
                    else:
                        x = findmostcommon(file, i)
                        attr[t].append(x)
                        # print(x)
                i = i + 1

            t += 1
    return attr


def prob(tables, attr, value, clas):
    numberofclassgivenattr = 0
    for i in tables[attr]:
        for j in tables[attr][i]:
            if j == clas:
                numberofclassgivenattr += tables[attr][i][j]
    if(value in (tables[attr])):
        return ((tables[attr][value][clas]) + 1) / ((numberofclassgivenattr) + len(tables))
    else:
        return 0

# create NB prob tables from 2D array data
# returns array of 2D dict such that arr[attr][val of attr][name of class)= p(val|class)
def buildTable(train, possiblevals):
    table = []

    for attr in range(len(train[0]) - 1):
        table.append(dict())

    for sample in train:

        claassofsample = sample[len(sample) - 1]
        for attr in range(len(train[0]) - 1):
            if (sample[attr] in table[attr]):
                if (claassofsample in table[attr][sample[attr]]):
                    table[attr][sample[attr]][claassofsample] += 1
                else:
                    newdict = dict()
                    for val in possiblevals:
                        newdict.update({val: 0})
                    newdict.update({claassofsample: 1})
                    table[attr][sample[attr]].update(newdict)
            else:
                newdict = dict()
                for val in possiblevals:
                    newdict.update({val: 0})
                newdict.update({claassofsample: 1})
                table[attr].update({sample[attr]: newdict})
    for arr in table:
        print(arr)
        print('\n')

    return table


def findrange(data,cont):
    min=sys.float_info.max
    max=sys.float_info.min

    for i in data:
        if float(i[cont])<min:
            min=float(i[cont])
        if float(i[cont])>max:
            max=float(i[cont])
    return [min,max]


def splitcont(data,cont,rangeofcont):
    newdata = []
    length=(rangeofcont[1]-rangeofcont[0])/6.0
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
        else:
            i[cont]='k'
    return newdata



def predict(sample, tables, n, pofclasses):
    prob_max = 0
    class_max = -1
    for clas in pofclasses:
        p = pofclasses[clas]
        for attr in range(len(sample) - 2):
            p = p * prob(tables, attr, sample[attr], clas)
        if p > prob_max:
            prob_max = p
            class_max = clas

    return class_max


def main():
    data = load("ecoli.data", [0])
    random.shuffle(data)

    print("dataloaded")
    acc = 0.0
    testlen = int(len(data) / 5)
    conts = [0,1,2,3,4,5,6]
    for cont in conts:
        rangeofcont = findrange(data, cont)
        data = splitcont(data, cont, rangeofcont)
    allacc = []

    for x in range(5):
        test = data[x * testlen:x * testlen + testlen]
        train = data[0:x * testlen] + data[x * testlen + testlen:]
        possiblevals = listofpossiblevalues(train, len(data[0]) - 1)
        tables = buildTable(train, possiblevals)

        classss = listofpossiblevalues(train, len(train[0]) - 1)
        probofclasses = dict()
        for sample in train:
            if sample[len(sample) - 1] in probofclasses:
                probofclasses[sample[len(sample) - 1]] += 1
            else:
                probofclasses.update({sample[len(sample) - 1]: 1})
        for item in probofclasses:
            probofclasses[item] = probofclasses[item] / len(train)

        print("nb trained...")
        for j in range(10):
            accuracy = 0
            for i in range(len(test)):
                if predict(test[i], tables, len(train), probofclasses) == test[i][len(test[0]) - 1]:
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