import csv
import json
from collections import Counter, defaultdict
import random
import math
import numpy as np
import os


class Loader(object):
    def __init__(self, mincount, maxlen, full_train=False):
        self.mincount = mincount
        self.maxlen = maxlen
        self.embedding, self.vocabulary = self.get_vocabulary()
        self.papers = self.get_papers()
        self.references = self.get_references()
        if full_train:
            ref = list(self.references)
            i = int(len(ref) * 0.8)
            train = ref
            test = ref[i:]
        else:
            ref = list(self.references)
            i = int(len(ref) * 0.8)
            train = ref[:i]
            test = ref[i:]
        self.train = Data(train, self.papers, self.references, is_train=True)
        self.test = Data(test, self.papers, self.references, is_train=False)

    def get_vocabulary(self):
        embedding = []
        vocabulary = {}
        with open('../data/ieee_words.vec') as f:
            f.readline()
            for line in f:
                line = line.split()
                w = line[0]
                v = [float(x) for x in line[1:]]
                vocabulary[w] = len(vocabulary)
                embedding.append(v)

        wordIDF = defaultdict(int)
        totalDF = 0
        with open('../data/ieee_words.txt', 'rb') as fin:
            for line in fin:
                totalDF += 1
                words = set(x.lower() for x in line.split())
                for w in words:
                    if w in vocabulary:
                        wordIDF[w] += 1

        for word in wordIDF:
            wordIDF[word] = math.log(totalDF * 1.0 / wordIDF[word])
        print 'wordIDF size: %s' % len(wordIDF)
        idf_mean = np.mean(wordIDF.values())
        for w in wordIDF:
            i = vocabulary[w]
            weight = wordIDF[w] / idf_mean
            embedding[i] = [x * weight for x in embedding[i]]
        return embedding, vocabulary

    def get_papers(self):
        papers = []
        with open('../data/ieee_words.txt', 'rb') as f:
            for line in f:
                p = {}
                words = []
                for w in line.split():
                    if w.lower() in self.vocabulary:
                        words.append(self.vocabulary[w.lower()])
                length = len(words)
                if length > self.maxlen:
                    words = words[:self.maxlen]
                    mask = [1] * self.maxlen
                    length = self.maxlen
                else:
                    words = words + [0] * (self.maxlen - length)
                    mask = [1] * length + [0] * (self.maxlen - length)
                p['arg'] = words
                p['mask'] = mask
                p['len'] = length
                papers.append(p)
        return papers

    def get_references(self):
        references = set()
        with open('../data/ieee_reference.csv', 'rb') as f:
            reader = csv.reader(f)
            reader.next()
            for citing_index, cited_index in reader:
                citing_index = int(citing_index)
                cited_index = int(cited_index)
                references.add((citing_index, cited_index))
        return references


class Data(object):
    def __init__(self, data, papers, references, is_train=True):
        self.data = data
        self.papers = papers
        self.references = references
        self.is_train = is_train
        self.max_index = len(self.papers) - 1
        self.i = 0
        self.n = len(self.data)

    def next_batch(self):
        args1 = []
        masks1 = []
        lens1 = []
        args2 = []
        masks2 = []
        lens2 = []
        labels = []

        if self.is_train:
            positive_sample = 8
            negative_sample = 120
        else:
            positive_sample = 64
            negative_sample = 64

        for _ in xrange(positive_sample):
            if self.i == 0:
                random.shuffle(self.data)
            paper1 = self.papers[self.data[self.i][0]]
            paper2 = self.papers[self.data[self.i][1]]
            args1.append(paper1['arg'])
            masks1.append(paper1['mask'])
            lens1.append(paper1['len'])
            args2.append(paper2['arg'])
            masks2.append(paper2['mask'])
            lens2.append(paper2['len'])
            labels.append(1)
            self.i += 1
            self.i %= self.n

        for _ in xrange(negative_sample):
            while True:
                index1 = random.randint(0, self.max_index)
                index2 = random.randint(0, self.max_index)
                if index1 != index2 and (index1, index2) not in self.references and (index2, index1) not in self.references:
                    break
            paper1 = self.papers[index1]
            paper2 = self.papers[index2]
            args1.append(paper1['arg'])
            masks1.append(paper1['mask'])
            lens1.append(paper1['len'])
            args2.append(paper2['arg'])
            masks2.append(paper2['mask'])
            lens2.append(paper2['len'])
            labels.append(0)

        return args1, masks1, lens1, args2, masks2, lens2, labels


if __name__ == '__main__':
    loader = Loader(5, 400)
    print loader.train.next_batch()
    print loader.test.next_batch()
    print loader.train.n, loader.test.n
    print len(loader.vocabulary)
