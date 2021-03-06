# coding=utf-8

import re

vocabulary = set()
with open('arxiv_words.txt', 'rb') as f:
    for line in f:
        words = line.split()
        vocabulary.update(words)
print 'vocabulary size: %s' % len(vocabulary)

pretrained = {}
splitChar = re.compile(r'\s+')
with open('../GoogleNews-vectors-negative300.txt', 'rb') as f:
    f.readline()
    for line in f:
        splitWord = splitChar.split(line.strip())
        word = splitWord[0]
        vector = splitWord[1:]
        if word in vocabulary:
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
                    vector = [x + y for (x, y) in zip(vector, pretrained[word])]
            if total > 0:
                vector = [x / total for x in vector]
            vector = [str(x) for x in vector]
            fout.write(' '.join(vector) + '\n')
