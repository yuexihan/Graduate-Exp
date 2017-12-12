import tensorflow as tf
import numpy as np
import os
from tensorflow.contrib.tensorboard.plugins import projector

paper_embedding = np.array([1216315, 50], dtype=np.float32)
with open('data/arxiv_fasttext_vector.txt') as f:
    for i, line in enumerate(f):
        for j, x in enumerate(line.split()):
            x = float(x)
            paper_embedding[i][j] = x

paper_embedding = tf.Variable(paper_embedding, trainable=False, name='paper_embedding', dtype=tf.float32)

sess = tf.Session()
sess.run(tf.global_variables_initializer())

config = projector.ProjectorConfig()

paper_projector = config.embeddings.add()
paper_projector.tensor_name = paper_embedding.name
paper_projector.metadata_path = 'data/arxiv_main_category.txt'

if not os.path.exists('save'):
    os.makedirs('save')
summary_writer = tf.summary.FileWriter('save')
projector.visualize_embeddings(summary_writer, config)

