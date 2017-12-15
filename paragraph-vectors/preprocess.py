# coding=utf-8

with open('data/arxiv_words', 'wb') as fout:
    with open('../data/arxiv_categories_words_fasttext.txt', 'rb') as fin:
        for line in fin:
            words = line.split()
            words = [w.lower() for w in words if not w.startswith('__label__')]
            fout.write(' '.join(words) + '\n')
