# coding=utf-8
import csv
import json
import os
import lda
import numpy as np
from collections import Counter
from scipy import sparse
from tqdm import tqdm

from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer

tokenizer = RegexpTokenizer(r'\w+')
stop = stopwords.words('english')
lanste = LancasterStemmer()

if os.path.exists('../data/arxiv_process_for_lda.json'):
    processed = json.load(open('../data/arxiv_process_for_lda.json'))
else:
    processed = []
    with open('../data/arxiv.csv', 'rb') as f:
        f.readline()
        reader = csv.reader(f)
        for paper_id, title, authors, abstract, categories in tqdm(reader):
            document = title + ' ' + abstract
            tmp = tokenizer.tokenize(document)
            tmp = [i.lower() for i in tmp if i not in stop]
            tmp_2 = []
            for i in tmp:
                try:
                    i = i.decode('utf-8')
                    i = lanste.stem(i)
                    tmp_2.append(i)
                except:
                    print i
                    continue
            processed.append(tmp_2)
    with open('../data/arxiv_process_for_lda.json', 'w') as f:
        json.dump(processed, f)


def word_count():
    """
    统计单词出现的次数
    """
    c = Counter()
    for words in processed:
        c.update(words)
    return c


def doc_count():
    """
    统计文档总数
    """
    return len(processed)


def init_word_index():
    c = word_count()
    index_to_word = []
    for k, v in c.most_common(50000):
        index_to_word.append(k)
    word_to_index = {w: i for i, w in enumerate(index_to_word)}
    with open('../data/re_index_to_word.json', 'w') as f:
        json.dump(index_to_word, f)
    with open('../data/re_word_to_index.json', 'w') as f:
        json.dump(word_to_index, f)


def load_word_index():
    with open('../data/re_index_to_word.json') as f:
        index_to_word = json.load(f)
    with open('../data/re_word_to_index.json') as f:
        word_to_index = json.load(f)
    return index_to_word, word_to_index


def main():
    print 'start getting vocabulary'
    if os.path.exists('../data/re_index_to_word.json') and os.path.exists('../data/re_word_to_index.json'):
        index_to_word, word_to_index = load_word_index()
    else:
        init_word_index()
        index_to_word, word_to_index = load_word_index()
    print 'finish getting vocabulary'

    print 'start getting doc size'
    doc_num = doc_count()
    print '%s docs' % doc_num
    print 'finish getting doc size'

    word_num = len(index_to_word)

    print 'start generating train data'
    X = sparse.lil_matrix((doc_num, word_num), dtype=np.int32)

    for i, words in enumerate(processed):
        for w in words:
            if w in word_to_index:
                X[i, word_to_index[w]] += 1
    print 'finish generating train data'

    print 'start training'
    model = lda.LDA(n_topics=50)
    model.fit(X)
    print 'finish training'

    print 'start saving result'
    np.save('re_topic_word.np', model.topic_word_)
    np.save('re_doc_topic.np', model.doc_topic_)
    print 'finish saving result'


if __name__ == '__main__':
    main()
