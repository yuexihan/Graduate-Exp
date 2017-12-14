import tensorflow as tf
import numpy as np
import os
from tensorflow.contrib.tensorboard.plugins import projector
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA

old_paper_embedding = np.empty((1216315, 50), dtype=np.float32)
with open('data/arxiv_fasttext_vector.txt') as f:
    for i, line in enumerate(f):
        for j, x in enumerate(line.split()):
            x = float(x)
            old_paper_embedding[i, j] = x

labels = []
with open('save/arxiv_label.txt') as f:
    for line in f:
        label = line.strip()
        labels.append(label)

clf = LDA(n_components=2)
clf.fit(old_paper_embedding, labels)
paper_embedding = clf.transform(old_paper_embedding)

paper_embedding = tf.Variable(paper_embedding, trainable=False, name='paper_embedding', dtype=tf.float32)

sess = tf.Session()
sess.run(tf.global_variables_initializer())
tf.train.Saver().save(sess, 'save/best')

config = projector.ProjectorConfig()

paper_projector = config.embeddings.add()
paper_projector.tensor_name = paper_embedding.name
paper_projector.metadata_path = 'label.txt'

if not os.path.exists('save'):
    os.makedirs('save')
summary_writer = tf.summary.FileWriter('save')
projector.visualize_embeddings(summary_writer, config)

