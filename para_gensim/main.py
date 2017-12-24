import gensim

# docs = gensim.models.doc2vec.TaggedLineDocument('data/arxiv_words.txt')
# model = gensim.models.Doc2Vec(docs, size=100, window=8, min_count=5, workers=5)
# model.save('save/doc2vec.model')
#

#python example to infer document vectors from trained doc2vec model
import gensim.models as g
import codecs

#parameters
model="save/doc2vec.model"
test_docs="data/arxiv_words.txt"
output_file="save/test_vectors.txt"

#inference hyper-parameters
start_alpha=0.01
infer_epoch=1000

#load model
m = g.Doc2Vec.load(model)
test_docs = [x.strip().split() for x in codecs.open(test_docs, "r", "utf-8").readlines() ]

#infer test vectors
output = open(output_file, "w")
for d in test_docs:
    output.write(" ".join([str(x) for x in m.infer_vector(d, alpha=start_alpha, steps=infer_epoch)]) + "\n" )
output.flush()
output.close()
