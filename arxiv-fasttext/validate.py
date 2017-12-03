import random

with open('../data/arxiv_categories_words_fasttext_lower.txt', 'rb') as f_in:
    with open('../data/arxiv_categories_words_fasttext_lower.train', 'wb') as f_train:
        with open('../data/arxiv_categories_words_fasttext_lower.test', 'wb') as f_test:
            for row in f_in:
                if random.random() < 0.8:
                    f_train.write(row)
                else:
                    f_test.write(row)
