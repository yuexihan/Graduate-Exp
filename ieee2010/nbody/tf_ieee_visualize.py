import tensorflow as tf
import numpy as np
from tensorflow.contrib.tensorboard.plugins import projector
import json

paper_embedding = np.empty((387667, 3), dtype=np.float32)

categories = []
for line in open('ieee_category.txt'):
    categories.append(line)

l = json.load(open('map-387667.json'))

with open('ieee_label.txt', 'w') as f:
    for i, (j, x, y, r) in enumerate(l):
        paper_embedding[i][0] = x
        paper_embedding[i][1] = y
        paper_embedding[i][2] = 0.0
        f.write(categories[j])

paper_embedding = tf.Variable(paper_embedding, trainable=False, name='paper_embedding', dtype=tf.float32)

sess = tf.Session()
sess.run(tf.global_variables_initializer())
tf.train.Saver().save(sess, 'save/embedding')

config = projector.ProjectorConfig()

paper_projector = config.embeddings.add()
paper_projector.tensor_name = paper_embedding.name
paper_projector.metadata_path = 'ieee_label.txt'

summary_writer = tf.summary.FileWriter('save')
projector.visualize_embeddings(summary_writer, config)

