# coding=utf-8
import sys
from collections import Counter, defaultdict
import math
from numpy import np
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

dim = len(vectors[0])


def vec_init():
    return [0.0] * dim


label2vec = defaultdict(vec_init)
label2count = Counter()

print 'adding label vectors'
# 计算每个label的向量数
# 计算每个label的中心点
for l, v in tqdm(zip(labels, vectors)):
    label2count[l] += 1
    tmp = label2vec[l]
    for i in xrange(dim):
        tmp[i] += v[i]

print 'adding vectors'
# 计算总的向量数
# 计算总的中心点
center = [0.0] * dim
total = 0
for l in label2count:
    c = label2count[l]
    tmp = label2vec[l]
    total += c
    for i in xrange(dim):
        center[i] += tmp[i]
        tmp[i] /= c
for i in xrange(dim):
    center[i] /= total
print 'center =>', center
print 'total =>', total
print 'label2count =>', label2count
print 'label2vec =>', label2vec

print 'count between'
# 计算类间
betweens = []
for l in label2count:
    tmp = [(x - y) * (x - y) for x, y in zip(label2vec[l], center)]
    tmp = sum(tmp)
    betweens.append((math.sqrt(tmp), label2count[l]))
between_mean = 0.0
for dist, c in betweens:
    between_mean += dist * c
between_mean /= total
between_variance = sum((dist - between_mean) * (dist - between_mean) * c for dist, c in betweens)
between_variance /= total
print 'between_mean =>', between_mean
print 'between_variance =>', between_variance

print 'count within'
# 计算类内
withins = []
for l, v in tqdm(zip(labels, vectors)):
    tmp = [(x - y) * (x - y) for x, y in zip(label2vec[l], v)]
    tmp = sum(tmp)
    withins.append(math.sqrt(tmp))
within_mean = np.mean(withins)
within_variance = sum((x - within_mean) * (x - within_mean) for x in withins)
within_variance /= total
print 'within_mean =>', within_mean
print 'within_variance =>', within_variance

if len(args) == 4:
    references = set()
    print 'loading references'
    with open(args[3], 'rb') as f:
        reader = csv.reader(f)
        reader.next()
        for citing_index, cited_index in tqdm(reader):
            references.add((int(citing_index), int(cited_index)))
    ref = []
    for i, j in tqdm(references):
        tmp = [(x - y) * (x - y) for x, y in zip(vectors[i], vectors[j])]
        ref.append(math.sqrt(sum(tmp)))
    ref_mean = np.mean(ref)
    ref_variance = sum((x - ref_mean) * (x - ref_mean) for x in ref)
    ref_variance /= len(references)
    noref = []
    for _ in xrange(len(references) * 15):
        while True:
            index1 = random.randint(0, total - 1)
            index2 = random.randint(0, total - 1)
            if index1 != index2 and (index1, index2) not in references and (index2, index1) not in references:
                break
        tmp = [(x - y) * (x - y) for x, y in zip(vectors[index1], vectors[index2])]
        noref.append(math.sqrt(sum(tmp)))
    noref_mean = np.mean(noref)
    noref_variance = sum((x - noref_mean) * (x - noref_mean) for x in noref)
    noref_variance /= len(references) * 15
    print 'ref_mean =>', ref_mean
    print 'ref_variance =>', ref_variance
    print 'noref_mean =>', noref_mean
    print 'noref_variance =>', noref_variance
