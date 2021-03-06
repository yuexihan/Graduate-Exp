# coding=utf-8
import csv
import json
import os
import lda
import numpy as np
from collections import Counter
from scipy import sparse


def word_count():
    """
    统计单词出现的次数
    """
    c = Counter()
    with open('../data/arxiv_word_category_nltk.csv', 'rb') as fin:
        fin.readline()
        reader = csv.reader(fin)
        for paper_id, words, category in reader:
            words = json.loads(words)
            words = [w.lower() for w in words]
            c.update(words)
    return c


def doc_count():
    """
    统计文档总数
    """
    c = 0
    with open('../data/arxiv_word_category_nltk.csv', 'rb') as fin:
        fin.readline()
        reader = csv.reader(fin)
        for _ in reader:
            c += 1
    return c


def init_word_index():
    c = word_count()
    index_to_word = []
    for k, v in c.most_common(50000):
        index_to_word.append(k)
    word_to_index = {w: i for i, w in enumerate(index_to_word)}
    with open('../data/index_to_word.json', 'w') as f:
        json.dump(index_to_word, f)
    with open('../data/word_to_index.json', 'w') as f:
        json.dump(word_to_index, f)


def load_word_index():
    with open('../data/index_to_word.json') as f:
        index_to_word = json.load(f)
    with open('../data/word_to_index.json') as f:
        word_to_index = json.load(f)
    return index_to_word, word_to_index


def main():
    print 'start getting vocabulary'
    if os.path.exists('../data/index_to_word.json') and os.path.exists('../data/word_to_index.json'):
        index_to_word, word_to_index = load_word_index()
    else:
        init_word_index()
        index_to_word, word_to_index = load_word_index()
    print 'finish getting vocabulary'

    print 'start getting doc size'
    doc_num = doc_count()
    print 'finish getting doc size'

    word_num = len(index_to_word)

    print 'start generating train data'
    X = sparse.lil_matrix((doc_num, word_num), dtype=np.int32)
    # with open('../data/arxiv_word_category_nltk.csv', 'rb') as fin:
    #     fin.readline()
    #     reader = csv.reader(fin)
    #     for i, (paper_id, words, category) in enumerate(reader):
    #         words = json.loads(words)
    #         for w in words:
    #             w = w.lower()
    #             if w in word_to_index:
    #                 X[i, word_to_index[w]] += 1
    with open('../data/arxiv_categories_words_fasttext.txt', 'rb') as fin:
        for i, line in enumerate(fin):
            words = line.split()
            for w in words:
                if not w.startswith('__label__'):
                    w = w.lower()
                    if w in word_to_index:
                        X[i, word_to_index[w]] += 1
    print 'finish generating train data'

    print 'start training'
    model = lda.LDA(n_topics=50)
    model.fit(X)
    print 'finish training'

    print 'start saving result'
    np.save('topic_word.np', model.topic_word_)
    np.save('doc_topic.np', model.doc_topic_)
    print 'finish saving result'


if __name__ == '__main__':
    main()
