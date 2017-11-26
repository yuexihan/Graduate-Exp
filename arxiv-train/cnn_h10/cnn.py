from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from six.moves import xrange
import collections

import numpy as np
import tensorflow as tf

import csv
import json
import time
import random
import os
import math

flags = tf.app.flags

flags.DEFINE_integer("embedding_size", 10, "The embedding dimension size.")
flags.DEFINE_integer("vocabulary_size", 50000, "The number of terms in vocabulary.")
flags.DEFINE_integer("batch_size", 128, "The number of samples per batch.")
flags.DEFINE_integer("max_step", 50000, "The circulation times of train.")
flags.DEFINE_string("train_dir", "CNN_train/", "Directory where to write event logs and checkpoint.")
flags.DEFINE_boolean("all_train", False, "Whether to use all datas to train model.")

FLAGS = flags.FLAGS

def build_dataset():
    all_train = FLAGS.all_train
    f = open('../TFIDF/wordCount.json')
    wordCount = json.load(f)
    wordCount = collections.Counter(wordCount)
    count = [['<UNK>', -1]]
    count.extend(wordCount.most_common(FLAGS.vocabulary_size - 1))
    FLAGS.vocabulary_size = len(count)

    dictionary = dict()
    for word, _ in count:
        dictionary[word] = len(dictionary)
    reverse_dictionary = dict(zip(dictionary.values(), dictionary.keys()))
    category_index = {
        'Quantitative Finance': 0,
        'Quantitative Biology': 1,
        'Statistics': 2,
        'Computer Science': 3,
        'Mathematics': 4,
        'Physics': 5
    }

    unk_count = 0
    train_datas = []
    train_labels = []
    test_datas = []
    test_labels = []
    with open('../arxiv_word_category.csv', 'rb') as fin:
        valve = 0.8
        reader = csv.reader(fin)
        reader.next()
#		i = 0
        for row in reader:
#			if i > 10000:
#				break
#			i += 1
            (paperid, words, category) = row
            words = json.loads(words)
            if len(words) < 12:
                continue
            data = []
            for word in words:
                if word in dictionary:
                    index = dictionary[word]
                else:
                    index = 0
                    unk_count += 1
                data.append(index)
            label = category_index[category]
            if not all_train:
                if random.random() < valve:
                    train_datas.append(data)
                    train_labels.append(label)
                else:
                    test_datas.append(data)
                    test_labels.append(label)
            else:
                train_datas.append(data)
                train_labels.append(label)
        count[0][1] = unk_count
    return train_datas, train_labels, test_datas, test_labels, count, dictionary, reverse_dictionary

class Cnn(object):
    def __init__(self, filename=None):
#		self.sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))
#		gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.5, allow_growth=True)
        gpu_options = tf.GPUOptions(allow_growth=True)
        self.sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))
        self.build_graph()
        self.saver = tf.train.Saver(tf.global_variables())
        if filename:
            self.saver.restore(sess, filename)

    def hidden(self, x):
        with tf.device('/cpu:0'):
            embed = tf.nn.embedding_lookup(self.embedding, x)
            output = []
        for i in range(10):
            embed = tf.reshape(embed, [1,-1,1])
            conv = tf.nn.relu(
                tf.nn.conv1d(
                    embed, filters=self.W_conv[i], stride=(i+3)*FLAGS.embedding_size, padding='VALID'
                ) + self.b_conv[i]
            )
            pool = tf.reduce_max(conv)
            output.append(pool)
        output = tf.stack(output)
        return tf.reshape(output, [-1])

    def forward(self, xx, yy):
        hiddens = [self.hidden(x) for x in xx]
        hiddens = tf.stack(hiddens)
        logits = tf.matmul(hiddens, self.weight) + self.biase
        return logits

    def build_graph(self):
        with tf.device("/cpu:0"):
            init_width = 0.5 / FLAGS.embedding_size
            embedding = tf.Variable(
                tf.random_uniform(
                    [FLAGS.vocabulary_size, FLAGS.embedding_size], -init_width, init_width
                ),
                name="embedding"
            )
        print("embedding:", embedding)
        self.embedding = embedding

#		with tf.device("/cpu:0"):
        W_conv = [
            tf.Variable(
                tf.truncated_normal(
                    [(i+3)*FLAGS.embedding_size, 1, 1],
                    stddev=1.0/math.sqrt((i+3)*FLAGS.embedding_size)
                ),
                name=("W_conv_" + str(i))
            )
            for i in range(10)
        ]
        print("W_conv:", W_conv)
        b_conv = [
            tf.Variable(tf.constant(0.1), name=("b_conv_" + str(i)))
            for i in range(10)
        ]
        print("b_conv:", b_conv)
        self.W_conv = W_conv
        self.b_conv = b_conv

#		with tf.device("/cpu:0"):
        weight = tf.Variable(
            tf.truncated_normal(
                [10, 6],
                stddev=1.0/60
            ),
            name="weight"
        )
        biase = tf.Variable(
            tf.zeros([6]),
            name="biase"
        )
        print("weight:", weight)
        print("biase:", biase)
        self.weight = weight
        self.biase = biase

        with tf.device("/cpu:0"):
            xx = [tf.placeholder(tf.int32, [None]) for _ in xrange(FLAGS.batch_size)]
            yy = tf.placeholder(tf.int32, [FLAGS.batch_size])
        self.xx = xx
        self.yy = yy
        logits = self.forward(xx, yy)
        loss = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(logits=logits, labels=yy))
        train_step = tf.train.AdamOptimizer(1e-2).minimize(loss)
        self.loss = loss
        self.train_step = train_step
        indices = tf.argmax(logits, 1)
        indices = tf.cast(indices, dtype=tf.int32)
        with tf.device("/cpu:0"):
            accuracy = tf.reduce_mean(tf.cast(tf.equal(indices, yy), tf.float32))
        self.accuracy = accuracy
        print("Have finished building model.")
    def train(self, train_datas, train_labels, test_datas=None, test_labels=None):
        print("Start training...")
        n = len(train_datas)
        sess = self.sess
        sess.run(tf.global_variables_initializer())
        print("Have initialized variables.")
        last_time = time.time()
        moving_loss = 0
        moving_accuracy = 0
        for step in xrange(FLAGS.max_step):
            start = step * FLAGS.batch_size % n
            stop = (step + 1) * FLAGS.batch_size % n
            if start < stop:
                xx = train_datas[start:stop]
                yy = train_labels[start:stop]
            else:
                xx = train_datas[start:] + train_datas[:stop]
                yy = train_labels[start:] + train_labels[:stop]
            feed_dict = {k: v for k, v in zip(self.xx, xx)}
            feed_dict[self.yy] = yy

            if step>0 and step%100==0:
                loss, accuracy = sess.run([self.loss, self.accuracy], feed_dict=feed_dict)
                now = time.time()
                last_time, rate = now, FLAGS.batch_size*100/(now-last_time)
                print("Step %8d: loss = %6.2f docs/step = %8.2f accuracy = %2.3f." % (step, loss, rate, accuracy))
            sess.run(self.train_step, feed_dict=feed_dict)

            if step>0 and step%1000==0:
                checkpoint_path = os.path.join(FLAGS.train_dir, 'model.ckpt')
                self.saver.save(sess, checkpoint_path, global_step=step)

            if step>0 and step%100==0:
                if not FLAGS.all_train:
                    m = len(test_datas)
                    step = step // 1000
                    start = step * FLAGS.batch_size % m
                    stop = (step + 1) * FLAGS.batch_size % m
                    if start < stop:
                        xx = test_datas[start:stop]
                        yy = test_labels[start:stop]
                    else:
                        xx = test_datas[start:] + test_datas[:stop]
                        yy = test_labels[start:] + test_labels[:stop]
                    feed_dict = {k: v for k, v in zip(self.xx, xx)}
                    feed_dict[self.yy] = yy
                    loss, accuracy = sess.run([self.loss, self.accuracy], feed_dict=feed_dict)
                    moving_loss = 0.9 * moving_loss + 0.1 * loss
                    moving_accuracy = 0.9 * moving_accuracy + 0.1 * accuracy
                    print("On test dataset: loss = %2.2f accuracy = %2.3f moving_loss = %2.2f moving_accuracy = %2.3f." % (loss, accuracy, moving_loss, moving_accuracy))


def main(_):
    train_datas, train_labels, test_datas, test_labels, count, dictionary, reverse_dictionary = build_dataset()
    print('Most common words (+UNK)', count[:10])
    l = range(len(train_datas))
    random.shuffle(l)
    train_datas = [train_datas[i] for i in l]
    train_labels = [train_labels[i] for i in l]
    l = range(len(test_datas))
    random.shuffle(l)
    test_datas = [test_datas[i] for i in l]
    test_labels = [test_labels[i] for i in l]
    model = Cnn()
    model.train(train_datas, train_labels, test_datas, test_labels)

if __name__ == "__main__":
    tf.app.run()
