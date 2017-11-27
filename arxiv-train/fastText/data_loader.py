import csv
import json
import cPickle as pickle


word_counter = Counter()
with open('../arxiv_word_category.csv', 'rb') as fin:
    reader = csv.reader(fin)
    reader.next()
    total = [0] * 6
    for row in reader:
        (paperid, words, category) = row
        words = json.loads(words)
        for


print total

word_counter = Counter()
with open('train.csv', 'rb') as fin:
    reader = csv.reader(fin)
    reader.next()
    for row in reader:
        (paperid, title, authors, abstract, category) = row
        for w in nltk.word_tokenize((title + abstract).decode('utf-8')):
            word_counter[w.lower()] += 1

word_dictionary = {'<UNK>': 0}
for w in word_counter:
    if word_counter[w] >= self.mincount:
        word_dictionary[w] = len(word_dictionary)

self.word_dictionary = word_dictionary
self.vocabulary_size = len(self.word_dictionary)
self.category_dictionary = {
    'Quantitative Finance': 0,
    'Quantitative Biology': 1,
    'Statistics': 2,
    'Computer Science': 3,
    'Mathematics': 4,
    'Physics': 5,
}
self.category_size = len(self.category_dictionary)
