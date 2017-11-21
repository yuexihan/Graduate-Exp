# coding=utf-8

import csv
import json
import re
import math
from collections import Counter
import random
import nltk
import cPickle as pickle
import os

train_data = None
validate_data = None
test_data = None


class Loader(object):
    @staticmethod
    def loader(mincount, maxlen):
        return Loader(mincount, maxlen).load()

    def save(self, save_path, filename):
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        pickle.dump(self, open(os.path.join(save_path, filename), 'wb'), True)

    def load(self, load_path='save', filename='loader.bin'):
        i = filename.find('.')
        if i == -1:
            filename = filename + '_' + str(self.mincount) + '_' + str(self.maxlen)
        else:
            filename = filename[:i] + '_' + str(self.mincount) + '_' + str(self.maxlen) + filename[i:]
        if not os.path.exists(os.path.join(load_path, filename)):
            self.statistics()
            self.train = Data(self.parse('train.csv'), maxlen=self.maxlen, rand=True)
            self.validate = Data(self.parse('validate.csv'), maxlen=self.maxlen)
            self.test = Data(self.parse('test.csv'), maxlen=self.maxlen)
            self.save(load_path, filename)
            return self
        else:
            return pickle.load(open(os.path.join(load_path, filename), 'rb'))

    def __init__(self, mincount, maxlen):
        self.mincount = mincount
        self.maxlen = maxlen

    def statistics(self):
        word_counter = Counter()
        with open('train.csv', 'rb') as fin:
            reader = csv.reader(fin)
            reader.next()
            for row in reader:
                (paperid, title, authors, abstract, category) = row
                for w in nltk.word_tokenize((title + abstract).decode('utf-8')):
                    word_counter[w.lower()] += 1

        word_dictionary = {'<UNK>': 0}
        for w in word_counter:
            if word_counter[w] >= self.mincount:
                word_dictionary[w] = len(word_dictionary)

        self.word_dictionary = word_dictionary
        self.vocabulary_size = len(self.word_dictionary)
        self.category_dictionary = {
            'Quantitative Finance': 0,
            'Quantitative Biology': 1,
            'Statistics': 2,
            'Computer Science': 3,
            'Mathematics': 4,
            'Physics': 5,
        }
        self.category_size = len(self.category_dictionary)

    def parse(self, filename):
        parsed_data = []
        with open(filename, 'rb') as fin:
            reader = csv.reader(fin)
            reader.next()
            for row in reader:
                item = {}
                words = []
                (paperid, title, authors, abstract, category) = row
                for w in nltk.word_tokenize((title + abstract).decode('utf-8')):
                    if w.lower() in self.word_dictionary:
                        words.append(self.word_dictionary[w.lower()])
                    else:
                        words.append(0)
                item['id'] = paperid
                item['words'] = words
                item['category'] = self.category_dictionary[category]
                parsed_data.append(item)
        return parsed_data

class Data(object):
    def __init__(self, data, maxlen, rand=False):
        self.data = data
        self.maxlen = maxlen
        self.rand = rand
        self.i = 0
        self.n = len(self.data)
    def next_batch(self, batch_size=1):
        ids = []
        args = []
        masks = []
        lens = []
        labels = []
        for _ in xrange(batch_size):
            if self.i == 0 and self.rand:
                random.shuffle(self.data)
            ids.append(self.data[self.i]['id'])
            args.append(self.data[self.i]['words'])
            lens.append(len(self.data[self.i]['words']))
            labels.append(self.data[self.i]['category'])
            self.i += 1
            self.i %= self.n
        maxlen = min(self.maxlen, max(lens))
        new_args = []
        new_lens = []
        for words, length in zip(args, lens):
            if length > maxlen:
                words = words[:maxlen]
                mask = [1] * maxlen
                length = maxlen
            else:
                words = words + [0] * (maxlen - length)
                mask = [1] * length + [0] * (maxlen - length)
            new_args.append(words)
            new_lens.append(length)
            masks.append(mask)
        return ids, new_args, masks, new_lens, labels

if __name__ == '__main__':
    loader = Loader.loader(5, 1000)
    print loader.vocabulary_size
    print loader.train.next_batch(2)
    print loader.validate.next_batch(2)
    print loader.test.next_batch(2)
    print loader.train.n, loader.validate.n, loader.test.n
