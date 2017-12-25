import tensorflow as tf
import numpy as np
import os
import csv
import json
from tensorflow.contrib.tensorboard.plugins import projector

paper_embedding = np.empty((1216315, 300), dtype=np.float32)

with open('arxivVectorTFIDF.txt', 'rb') as fin:
    for i, line in enumerate(fin):
        for j, x in enumerate(line.split()):
            x = float(x)
            paper_embedding[i, j] = x

paper_embedding = tf.Variable(paper_embedding, trainable=False, name='paper_embedding', dtype=tf.float32)

sess = tf.Session()
sess.run(tf.global_variables_initializer())
tf.train.Saver().save(sess, 'save/best')

config = projector.ProjectorConfig()

paper_projector = config.embeddings.add()
paper_projector.tensor_name = paper_embedding.name
paper_projector.metadata_path = 'label.txt'

summary_writer = tf.summary.FileWriter('save')
projector.visualize_embeddings(summary_writer, config)

