oneHotIndex = {
	'Quantitative Finance': 0,
	'Quantitative Biology': 1,
	'Statistics': 2,
	'Computer Science': 3,
	'Mathematics': 4,
	'Physics': 5,
}

import csv
import json
import re
import math

with open('arxivVectorOneHot.txt', 'wb') as fout:
	writer = csv.writer(fout)
	writer.writerow(['paperid', 'vector', 'onehot'])
	with open('arxivVector.txt', 'rb') as fin:
		reader = csv.reader(fin)
		reader.next()
		for row in reader:
			(paperid, vector, categories) = row
			categories = json.loads(categories)
			for c in categories:
				onehot = [0] * 6
				onehot[oneHotIndex[c]] = 1
				onehot = json.dumps(onehot)
				writer.writerow([paperid, vector, onehot])
