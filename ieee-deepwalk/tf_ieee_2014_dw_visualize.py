import tensorflow as tf
import numpy as np
from tensorflow.contrib.tensorboard.plugins import projector
import json

categories = []
for line in open('ieee_category_2014.txt'):
    categories.append(line)

l = []
with open('ieee-deepwalk-lable.txt', 'w') as fout:
    with open('ieee-deepwalk-2014.txt.vec') as f:
        f.readline()
        for line in f:
            line = line.split()
            i = int(line[0])
            X = [float(x) for x in line[1:]]
            l.append(X)
            fout.write(categories[i])

paper_embedding = tf.Variable(l, trainable=False, name='paper_embedding', dtype=tf.float32)

sess = tf.Session()
sess.run(tf.global_variables_initializer())
tf.train.Saver().save(sess, 'save/embedding')

config = projector.ProjectorConfig()

paper_projector = config.embeddings.add()
paper_projector.tensor_name = paper_embedding.name
paper_projector.metadata_path = 'ieee-deepwalk-lable.txt'

summary_writer = tf.summary.FileWriter('save')
projector.visualize_embeddings(summary_writer, config)

