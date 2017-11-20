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
f = open('wordIDF.json')
wordIDF = json.load(f)

inParentheses = re.compile(r'\(([^)]+)\)')

def category(s):
	ss = inParentheses.findall(s)
	return [Belong[s.lower()] for s in ss]


totalDF = 0
with open('arxivTFIDF.txt', 'wb') as fout:
	writer = csv.writer(fout)
	writer.writerow(['paperid','tfidf', 'categories'])
	with open('../arxiv.csv', 'rb') as fin:
		reader = csv.reader(fin)
		reader.next()
		for row in reader:
			(paperid, title, authors, abstract, categories) = row
			words = punctuation.split(unify(title.lower())) + punctuation.split(unify(abstract.lower()))
			rowTFIDF = {}
			for word in words:
				if word in wordIDF:
					if word in rowTFIDF:
						rowTFIDF[word] += wordIDF[word]
					else:
						rowTFIDF[word] = wordIDF[word]
			rowTFIDF = json.dumps(rowTFIDF)
			categories = json.dumps(category(categories))
			writer.writerow([paperid, rowTFIDF, categories])