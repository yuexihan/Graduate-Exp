import tensorflow as tf
import numpy as np
import os
import csv
import json
from tensorflow.contrib.tensorboard.plugins import projector

paper_embedding = np.empty((1216315, 300), dtype=np.float32)

if not os.path.exists('save'):
    os.makedirs('save')

with open('save/label.txt', 'w') as fout:
    with open('data/arxivVector.txt', 'rb') as fin:
        reader = csv.reader(fin)
        reader.next()
        for i, row in enumerate(reader):
            (paperid, vector, categories) = row
            vector = json.loads(vector)
            categories = json.loads(categories)
            paper_embedding[i] = vector
            fout.write(categories[0] + '\n')

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

