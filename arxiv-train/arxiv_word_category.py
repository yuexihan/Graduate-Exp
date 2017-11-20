# coding=utf-8

import csv
import json
import re
import math

punctuation = re.compile(ur"[\s+=`^!?\\/_.,$%^*()\[\]:;\"\'——！<>{}|，。？、~@#￥%…&（）：；‘’《》“”»〔〕]+")
ill = re.compile(ur'[\d-]')

f = open('belong_arxiv.json')
Belong = json.load(f)

inParentheses = re.compile(r'\(([^)]+)\)')
def get_categories(s):
	ss = inParentheses.findall(s)
	return [Belong[s.lower()] for s in ss]

def unify(s):
	if isinstance(s, str):
		return s.decode('utf-8')
	else:
		return s
with open('arxiv_word_category.csv', 'wb') as fout:
	writer = csv.writer(fout)
	writer.writerow(['paperid', 'words', 'category'])
	with open('arxiv.csv', 'rb') as fin:
		reader = csv.reader(fin)
		reader.next()
		for row in reader:
			(paperid, title, authors, abstract, categories) = row
			words = punctuation.split(unify(title.lower())) + punctuation.split(unify(abstract.lower()))
			words = [word for word in words if word]
			words = json.dumps(words)
			categories = get_categories(categories)
			for category in categories:
				writer.writerow([paperid, words, category])

