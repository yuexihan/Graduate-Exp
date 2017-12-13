from __future__ import division

import tensorflow as tf
import time
import os


class Model(object):
    def save(self, save_path, filename):
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        tf.train.Saver().save(self.sess, os.path.join(save_path, filename))

    def load(self, load_path, filename):
        tf.train.Saver().restore(self.sess, os.path.join(load_path, filename))

    def __init__(self, dataloader, embedding_size, max_epoch, learning_rate, keep_prob):
        self.dataloader = dataloader

        self.vocabulary_size = len(self.dataloader.vocabulary)

        self.embedding_size = embedding_size
        self.max_epoch = max_epoch
        self.learning_rate = learning_rate
        self.keep_prob = keep_prob

        self.build_graph()

        self.sess = tf.Session()

    def represent(self, args, masks, lens):
        with tf.variable_scope('embedding_layer'):
            inputs = tf.nn.embedding_lookup(self.word_embedding, args) * \
                     tf.nn.embedding_lookup(self.mask_embedding, masks)
            inputs = tf.nn.dropout(inputs, self.prob)

        with tf.variable_scope('hidden_layer'):
            hiddens = tf.reduce_sum(inputs, 1) / tf.expand_dims(tf.cast(lens, tf.float32), 1)

        return hiddens

    def build_graph(self):
        self.mask_embedding = tf.constant(
            [[0.]*self.embedding_size, [1.]*self.embedding_size],
            name='mask_embedding'
        )
        self.word_embedding = tf.Variable(
            tf.random_uniform(
                [self.vocabulary_size, self.embedding_size],
                -0.5/self.vocabulary_size,
                0.5/self.vocabulary_size
            ),
            name='word_embedding'
        )

        self.args1 = tf.placeholder(tf.int32, [None, None])
        self.args2 = tf.placeholder(tf.int32, [None, None])
        self.masks1 = tf.placeholder(tf.int32, [None, None])
        self.masks2 = tf.placeholder(tf.int32, [None, None])
        self.lens1 = tf.placeholder(tf.int32, [None])
        self.lens2 = tf.placeholder(tf.int32, [None])
        self.labels = tf.placeholder(tf.int32, [None])
        self.prob = tf.placeholder(tf.float32)

        represent1 = self.represent(self.args1, self.masks1, self.lens1)
        represent2 = self.represent(self.args2, self.masks2, self.lens2)

        with tf.variable_scope('interact_layer'):
            logits = tf.reduce_sum(represent1 * represent2, 1)

        self.loss = tf.reduce_mean(
            tf.nn.weighted_cross_entropy_with_logits(
                targets=tf.cast(self.labels, dtype=tf.float32), logits=logits, pos_weight=15
            )
        )

        losses = tf.get_collection('losses')
        if losses:
            self.loss += tf.add_n(losses)

        self.train_step = tf.train.AdamOptimizer(self.learning_rate).minimize(self.loss)
        predictions = tf.cast(tf.greater(logits, 0.0), tf.int32)
        self.accuracy = tf.reduce_mean(
            tf.cast(tf.equal(predictions, self.labels), tf.float32)
        )

    def test(self, data=None):
        if not data:
            data = self.dataloader.test
        sess = self.sess
        args1, masks1, lens1, args2, masks2, lens2, labels = data.next_batch()
        feed_dict = {
            self.args1: args1,
            self.args2: args2,
            self.masks1: masks1,
            self.masks2: masks2,
            self.lens1: lens1,
            self.lens2: lens2,
            self.labels: labels,
            self.prob: 1.
        }
        accuracy = sess.run(self.accuracy, feed_dict=feed_dict)
        return accuracy

    def train(self, full_train=False):
        train_data = self.dataloader.train
        test_data = self.dataloader.test
        sess = self.sess
        sess.run(tf.global_variables_initializer())
        last_time = time.time()
        step = 0
        best_accuracy = 0.
        while True:
            args1, masks1, lens1, args2, masks2, lens2, labels = train_data.next_batch()
            feed_dict = {
                self.args1: args1,
                self.args2: args2,
                self.masks1: masks1,
                self.masks2: masks2,
                self.lens1: lens1,
                self.lens2: lens2,
                self.labels: labels,
                self.prob: self.keep_prob
            }
            if step % 100 == 0:
                loss, accuracy = sess.run(
                    [self.loss, self.accuracy],
                    feed_dict=feed_dict
                )
                now = time.time()
                last_time, rate = now, 8 * 100 / (now-last_time)
                print 'Step %6d: loss = %3.2f, accuracy = %2.3f, docs/second = %8.2f'% (step, loss, accuracy, rate)
            sess.run(self.train_step, feed_dict=feed_dict)
            step += 1
            if step * 8 % train_data.n < 8:
                if not full_train:
                    val_accuracy = self.test(test_data)
                    print '\n  Epoch %3d: validate_accuracy = %2.3f, best_accuracy = %2.3f\n' \
                          % (step * 8 // train_data.n, val_accuracy, best_accuracy)
                if full_train:
                    self.save('save', 'best')
            if step * 8 > self.max_epoch * train_data.n:
                break

    def save_doc_vector(self):
        self.load('save', 'best')
        represents = self.represent(self.args1, self.masks1, self.lens1)
        sess = self.sess
        with open('data/ieee_vectors.txt', 'wb') as f:
            for paper in self.dataloader.papers:
                args = [paper['arg']]
                masks = [paper['mask']]
                lens = [paper['len']]
                feed_dict = {
                    self.args1: args,
                    self.masks1: masks,
                    self.lens1: lens,
                    self.prob: 1.
                }
                results = sess.run(represents, feed_dict=feed_dict)
                result = results[0]
                result = [str(x) for x in result]
                f.write(' '.join(result) + '\n')

    def many_test(self):
        for i in xrange(10):
            val_accuracy = self.test()
            print val_accuracy