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
            for word in line.split(','):
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
            for word in line.split(','):
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

    return ((tables[attr][value][clas]) + 1) / ((numberofclassgivenattr) + len(tables))


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







def bag(train,possiblevals):
    trainlen=int(len(train)/4)
    print("entering")

    tables= []
    for i in range(10):
        startpoint = random.randint(0,len(train)-trainlen -1)
        print(startpoint)
        trainbag = train[startpoint: startpoint+trainlen]
        t=[]
        for sample in trainbag:

            app=[]
            for at in sample:
                app.append(at)
            t.append(app)
        possiblevals = listofpossiblevalues(t, len(t[0]) - 1)

        table = buildTable(t,possiblevals)
        probofclasses = dict()
        for sample in t:
            if sample[len(sample) - 1] in probofclasses:
                probofclasses[sample[len(sample) - 1]] += 1
            else:
                probofclasses.update({sample[len(sample) - 1]: 1})
        for item in probofclasses:
            probofclasses[item] = probofclasses[item] / len(t)
        tables.append([table,probofclasses,possiblevals])
    return tables

def bagpredic(sample,tabless):
    vote=dict()

    for tables in tabless:
        table = tables[0][0]

        possiblevals = tables[2]

        n = 0
        classes = dict()
        for val in possiblevals:
            classes.update({val: 0})
        for dictionary in table:
            for item in table[dictionary]:
                n += table[dictionary][item]
                classes[item] += table[dictionary][item]

        pred = predict(sample,tables[0],n,tables[1])
        if (pred in vote):
            vote[pred]+=1
        else:
            vote[pred]=1

    sorted_x = sorted(vote.items(), key=operator.itemgetter(1))
    x = list(sorted_x)
    return (x[len(x) - 1][0])










def main():
    data = load("car.data", [])
    random.shuffle(data)

    print("dataloaded")
    acc = 0.0
    testlen = int(len(data) / 5)
    allacc = []

    for x in range(5):
        test = data[x * testlen:x * testlen + testlen]
        train = data[0:x * testlen] + data[x * testlen + testlen:]
        possiblevals = listofpossiblevalues(train, len(data[0]) - 1)
        tabless = bag(train, possiblevals)



        print("nb trained...")
        for j in range(10):
            accuracy=0
            for i in range(len(test)):
                if bagpredic(test[i], tabless) == test[i][len(test[0]) - 1]:
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