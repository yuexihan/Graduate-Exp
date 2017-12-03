# coding=utf-8

import csv
import json
import re
import nltk
from tqdm import tqdm

punctuation = re.compile(ur"[\s+=`^!?\\/_.,$%^*()\[\]:;\"\'——！<>{}|，。？、~@#￥%…&（）：；‘’《》“”»〔〕]+")
ill = re.compile(ur'[\d-]')

f = open('../data/belong_arxiv.json')
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


with open('../data/arxiv_categories_words_fasttext.txt', 'wb') as fout:
    with open('../data/arxiv.csv', 'rb') as fin:
        reader = csv.reader(fin)
        reader.next()
        for row in tqdm(reader):
            (paperid, title, authors, abstract, categories) = row
            text = re.sub(r'[\r\n]+', ' ', (title + abstract).decode('utf-8'))
            words = ' '.join(nltk.word_tokenize(text))
            categories = inParentheses.findall(categories)
            categories = ' '.join(['__label__' + c for c in categories])
            fout.write(categories + ' ' + words + '\n')
