import json
import re

f = open('wordIDF.json')
wordIDF = json.load(f)
print len(wordIDF)

pretrained = {}
splitChar = re.compile(r'\s+')
f = open('../GoogleNews-vectors-negative300.txt')
f.readline()
for line in f:
	splitWord = splitChar.split(line.strip())
	word = splitWord[0]
	vector = splitWord[1:]
	if word in wordIDF:
		# print vector
		pretrained[word] = [float(x) for x in vector]

print len(pretrained)

with open('pretrained.json', 'w') as fout:
	json.dump(pretrained, fout)