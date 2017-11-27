import csv
import json
import re
import math

with open('arxivVectorOneHot.txt', 'rb') as fin:
    reader = csv.reader(fin)
    reader.next()
    total = [0] * 6
    for row in reader:
        (paperid, vector, onehot) = row
        onehot = json.loads(onehot)
        total = [x + y for (x, y) in zip(total, onehot)]

print total