import tensorflow as tf
import numpy as np
from tensorflow.contrib.tensorboard.plugins import projector

paper_embedding = np.empty((1072213, 50), dtype=np.float32)
with open('data/ieee_vectors.txt') as f:
    for i, line in enumerate(f):
        for j, x in enumerate(line.split()):
            x = float(x)
            paper_embedding[i, j] = x

paper_embedding = tf.Variable(paper_embedding, trainable=False, name='paper_embedding', dtype=tf.float32)

sess = tf.Session()
sess.run(tf.global_variables_initializer())
tf.train.Saver().save(sess, 'save/embedding')

config = projector.ProjectorConfig()

paper_projector = config.embeddings.add()
paper_projector.tensor_name = paper_embedding.name
paper_projector.metadata_path = 'ieee_category.txt'

summary_writer = tf.summary.FileWriter('save')
projector.visualize_embeddings(summary_writer, config)

