import tensorflow as tf
import numpy as np
from tensorflow.contrib.tensorboard.plugins import projector
import json
from Queue import Queue

paper_embedding = np.empty((387667, 3), dtype=np.float32)

seq = ['Computer Science', 'Engineering', 'Physics', 'Chemistry', 'Materials Science', 'Mathematics', 'Geology', 'Biology', 'Medicine', 'Economics', 'Sociology', 'Psychology', 'Philosophy', 'Art', 'History', 'Geography', 'Business', 'Environmental science']

categories = []
for line in open('ieee_category.txt'):
    categories.append(line.strip())

l = json.load(open('map-387667.json'))

papers = Queue()
has_c = set()
for i, (j, x, y, r) in enumerate(l):
    papers.put((x, y, 0.0, categories[j]))
    has_c.add(categories[j])

count = 0
with open('ieee_label.txt', 'w') as f:
    while len(seq) != 0:
        if seq[0] not in has_c:
            seq = seq[1:]
            continue
        x, y, z, c = papers.get()
        if seq[0] == c:
            seq = seq[1:]
            f.write(c + '\n')
            paper_embedding[count][0] = x
            paper_embedding[count][1] = y
            paper_embedding[count][2] = z
            count += 1
            continue
        papers.put((x, y, z, c))
    while papers.not_empty():
        x, y, z, c = papers.get()
        f.write(c + '\n')
        paper_embedding[count][0] = x
        paper_embedding[count][1] = y
        paper_embedding[count][2] = z
        count += 1

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

