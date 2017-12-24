from gensim.model import Doc2Vec

model = Doc2Vec('data/arxiv_words', size=100, window=8, min_count=5, workers=5)
model.save('save/doc2vec.model')
