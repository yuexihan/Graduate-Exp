# coding=utf-8
import sys
from collections import Counter, defaultdict
import math
import numpy as np
import csv
from tqdm import tqdm
import random
from sklearn import linear_model

args = sys.argv
print args[1], args[2]

labels = []
vectors = []

print 'loading labels'
for line in tqdm(open(args[1])):
    labels.append(line.strip())

print 'loading vectors'
for line in tqdm(open(args[2])):
    v = [float(x) for x in line.split()]
    vectors.append(v)

print 'training'
LR = linear_model.LogisticRegression()
LR.fit(vectors, labels)

print 'testing'
print LR.score(vectors, labels)
