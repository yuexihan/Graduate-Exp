import tensorflow as tf
import numpy as np
from tensorflow.contrib.tensorboard.plugins import projector
import json
from Queue import Queue

seq = ['Computer Science', 'Engineering', 'Physics', 'Chemistry', 'Materials Science', 'Mathematics', 'Geology', 'Biology', 'Medicine', 'Economics', 'Sociology', 'Psychology', 'Philosophy', 'Art', 'History', 'Geography', 'Business', 'Environmental science']

categories = []
for line in open('ieee_category_2014.txt'):
    categories.append(line.strip())

l = []
with open('ieee-deepwalk-2014.txt.vec') as f:
    f.readline()
    for line in f:
        line = line.split()
        i = int(line[0])
        X = [float(x) for x in line[1:]]
        l.append((X, categories[i]))

papers = Queue()
has_c = set()
for X, c in l:
    papers.put((X, c))
    has_c.add(c)

paper_embedding = []
with open('ieee-deepwalk-label.txt', 'w') as f:
    while len(seq) != 0:
        if seq[0] not in has_c:
            seq = seq[1:]
            continue
        X, c = papers.get()
        if seq[0] == c:
            seq = seq[1:]
            f.write(c + '\n')
            paper_embedding.append(X)
            continue
        papers.put((X, c))
    while not papers.empty():
        X, c = papers.get()
        f.write(c + '\n')
        paper_embedding.append(X)

paper_embedding = tf.Variable(paper_embedding, trainable=False, name='paper_embedding', dtype=tf.float32)

sess = tf.Session()
sess.run(tf.global_variables_initializer())
tf.train.Saver().save(sess, 'save/embedding')

config = projector.ProjectorConfig()

paper_projector = config.embeddings.add()
paper_projector.tensor_name = paper_embedding.name
paper_projector.metadata_path = 'ieee-deepwalk-label.txt'

summary_writer = tf.summary.FileWriter('save')
projector.visualize_embeddings(summary_writer, config)

