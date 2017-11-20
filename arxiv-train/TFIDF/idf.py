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

f = open('../belong_arxiv.json')
Belong = json.load(f)
f = open('../belong_extend_arxiv.json')
Belong_extend = json.load(f)
f = open('wordCountMoreThanFour.json')
wordCount = json.load(f)

inParentheses = re.compile(r'\(([^)]+)\)')

wordIDF = {}
for word in wordCount:
	wordIDF[word] = 0

totalDF = 0

with open('../arxiv.csv', 'rb') as fin:
	reader = csv.reader(fin)
	for row in reader:
		totalDF += 1
		(paperid, title, authors, abstract, categories) = row
		words = punctuation.split(unify(title.lower())) + punctuation.split(unify(abstract.lower()))
		words = set(words)
		for word in words:
			if word in wordCount:
				wordIDF[word] += 1

for word in wordIDF:
	wordIDF[word] = math.log(totalDF * 1.0 / wordIDF[word])

f = open('wordIDF.json', 'w')
json.dump(wordIDF, f)