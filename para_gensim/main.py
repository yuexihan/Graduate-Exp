import gensim

docs = gensim.models.doc2vec.TaggedLineDocument('data/arxiv_words')
model = gensim.models.Doc2Vec(docs, size=100, window=8, min_count=5, workers=5)
model.save('save/doc2vec.model')
