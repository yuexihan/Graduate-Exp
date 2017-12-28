# coding=utf-8
import sys
from sklearn.neighbors import NearestNeighbors
from collections import Counter, defaultdict
import math
import numpy as np
import csv
from tqdm import tqdm
import random

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

def f():
    print 'grouping'
    label2vecs = defaultdict(list)
    for l, v in tqdm(zip(labels, vectors)):
        label2vecs[l].append(v)

    print 'candidates'
    total = len(vectors)
    for l in tqdm(label2vecs):
        vecs = label2vecs[l]
        n = len(vecs)
        n = 10000 * n / total
        random.shuffle(vecs)
        label2vecs[l] = vecs[:n]

    new_labels = []
    new_vectors = []
    for l in label2vecs:
        for v in label2vecs[l]:
            new_labels.append(l)
            new_vectors.append(v)

    print 'knn'
    nbrs = NearestNeighbors(n_neighbors=6, algorithm='ball_tree').fit(new_vectors)
    distances, indices = nbrs.kneighbors(new_vectors)
    pricision = 0.0
    for line in indices:
        i = line[0]
        for j in line[1:]:
            if new_labels[i] == new_labels[j]:
                pricision += 1.0
    pricision /= (len(indices) * 10)
    print 'pricision =>', pricision
    return pricision

pricisions = [f() for i in xrange(10)]
print 'prcisions =>', pricisions
print 'prcision =>', np.mean(pricisions)
