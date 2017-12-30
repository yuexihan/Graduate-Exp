import tensorflow as tf
import numpy as np
import os
from tensorflow.contrib.tensorboard.plugins import projector

paper_embedding = []
with open('ieee_vectors_v2.txt') as f:
    for line in f:
        line = [float(x) for x in line.split()]
        paper_embedding.append(line)

paper_embedding = tf.Variable(paper_embedding, trainable=False, name='paper_embedding', dtype=tf.float32)

sess = tf.Session()
sess.run(tf.global_variables_initializer())
tf.train.Saver().save(sess, 'save/best')

config = projector.ProjectorConfig()

paper_projector = config.embeddings.add()
paper_projector.tensor_name = paper_embedding.name
paper_projector.metadata_path = 'ieee_category.txt'

if not os.path.exists('save'):
    os.makedirs('save')
summary_writer = tf.summary.FileWriter('save')
projector.visualize_embeddings(summary_writer, config)

