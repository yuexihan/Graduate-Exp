# coding=utf-8

import csv
import json
import re

punctuation = re.compile(ur"[\s+=`^!?\\/_.,$%^*()\[\]:;\"\'——！<>{}|，。？、~@#￥%…&（）：；‘’《》“”»〔〕]+")
ill = re.compile(ur'[\d-]')

f = open('../belong_arxiv.json')
Belong = json.load(f)
f = open('../belong_extend_arxiv.json')
Belong_extend = json.load(f)
f = open('../allwords.json')
Allwords = set(json.load(f))


def unify(s):
    if isinstance(s, str):
        return s.decode('utf-8')
    else:
        return s

# vocabulary = set()
vocabulary = {}


with open('../arxiv.csv', 'rb') as fin:
    reader = csv.reader(fin)
    for row in reader:
        (paperid, title, authors, abstract, categories) = row
        words = punctuation.split(unify(title.strip().lower())) + punctuation.split(abstract.strip().lower())
        words = [word for word in words if word]
        for word in words:
            if word and not ill.search(word):
                # vocabulary.add(word)
                if word in vocabulary:
                    vocabulary[word] += 1
                else:
                    vocabulary[word] = 1

# print vocabulary
print len(vocabulary)

import json
f = open('wordCount.json', 'w')
json.dump(vocabulary, f)
f.close()
