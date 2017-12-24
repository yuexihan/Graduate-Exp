# coding=utf-8

import json

f = open('pretrained.json')
pretrained = json.load(f)

with open('arxivVectorAvg.txt', 'wb') as fout:
    with open('arxiv_words.txt', 'rb') as fin:
        for row in fin:
            words = row.split()
            vector = [0.0] * 300
            total = 0.0
            for word in words:
                if word in pretrained:
                    total += 1
                    vector = [x + y for (x, y) in zip(vector, pretrained[word])]
            vector = [x / total for x in vector]
            vector = [str(x) for x in vector]
            fout.write(' '.join(vector))
