# coding=utf-8

import re
import math
from collections import defaultdict


wordIDF = defaultdict(int)
totalDF = 0
with open('arxiv_words.txt', 'rb') as fin:
    for line in fin:
        totalDF += 1
        words = line.split()
        for w in set(words):
            w = w.lower()
            wordIDF[w] += 1

for word in wordIDF:
    wordIDF[word] = math.log(totalDF * 1.0 / wordIDF[word])
print 'wordIDF size: %s' % len(wordIDF)

pretrained = {}
splitChar = re.compile(r'\s+')
with open('../GoogleNews-vectors-negative300.txt', 'rb') as f:
    f.readline()
    for line in f:
        splitWord = splitChar.split(line.strip())
        word = splitWord[0]
        vector = splitWord[1:]
        if word in wordIDF:
            pretrained[word] = [float(x) for x in vector]
print 'pretrained size: %s' % len(pretrained)

with open('arxivVectorAvg.txt', 'wb') as fout:
    with open('arxiv_words.txt', 'rb') as fin:
        for line in fin:
            words = line.split()
            vector = [0.0] * 300
            total = 0
            for word in words:
                if word in pretrained:
                    total += 1
                    vector = [x + wordIDF[word] * y for (x, y) in zip(vector, pretrained[word])]
            if total > 0:
                vector = [x / total for x in vector]
            vector = [str(x) for x in vector]
            fout.write(' '.join(vector) + '\n')
