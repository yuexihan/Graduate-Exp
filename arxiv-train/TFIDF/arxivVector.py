# coding=utf-8

import csv
import json
import re
import math

punctuation = re.compile(ur"[\s+=`^!?\\/_.,$%^*()\[\]:;\"\'——！<>{}|，。？、~@#￥%…&（）：；‘’《》“”»〔〕]+")
ill = re.compile(ur'[\d-]')

def unify(s):
    if isinstance(s, str):
        return s.decode('utf-8')
    else:
        return s

f = open('pretrained.json')
pretrained = json.load(f)

inParentheses = re.compile(r'\(([^)]+)\)')

with open('arxivVector.txt', 'wb') as fout:
    writer = csv.writer(fout)
    writer.writerow(['paperid', 'vector', 'categories'])
    with open('arxivTFIDF.txt', 'rb') as fin:
        reader = csv.reader(fin)
        reader.next()
        for row in reader:
            (paperid, rowTFIDF, categories) = row
            rowTFIDF = json.loads(rowTFIDF)
            categories = json.loads(categories)
            vector = [0.0] * 300
            total = 0.0
            for word in rowTFIDF:
                if word in pretrained:
                    total += rowTFIDF[word]
                    vector = [x + rowTFIDF[word] * y for (x, y) in zip(vector, pretrained[word])]
            vector = [x / total for x in vector]
            vector = json.dumps(vector)
            categories = json.dumps(list(set(categories)))
            writer.writerow([paperid, vector, categories])
