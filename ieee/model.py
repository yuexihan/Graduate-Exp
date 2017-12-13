from __future__ import division

import tensorflow as tf
import time
import os
import math


class Model(object):
    def save(self, save_path, filename):
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        tf.train.Saver().save(self.sess, os.path.join(save_path, filename))

    def load(self, load_path, filename):
        tf.train.Saver().restore(self.sess, os.path.join(load_path, filename))

    def __init__(self, dataloader, embedding_size, batch_size, max_epoch, learning_rate, keep_prob):
        self.dataloader = dataloader

        self.vocabulary_size = self.dataloader.vocabulary_size
        self.category_size = self.dataloader.category_size

        self.embedding_size = embedding_size
        self.batch_size = batch_size
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
        self.paper_embedding = tf.Variable(
            tf.zeros([self.dataloader.test.n, self.embedding_size]),
            trainable = False,
            name='paper_embedding'
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
                targets=self.labels, logits=logits, pos_weight=15
            )
        )

        losses = tf.get_collection('losses')
        if losses:
            self.loss += tf.add_n(losses)

        self.train_step = tf.train.AdamOptimizer(self.learning_rate).minimize(self.loss)
        predictions = tf.cast(tf.argmax(logits, 1), tf.int32)
        self.accuracy = tf.reduce_mean(
            tf.cast(tf.equal(predictions, self.labels), tf.float32)
        )

    def test(self, data=None):
        if not data:
            data = self.dataloader.test
        sess = self.sess
        ids, args, masks, lens, labels = data.next_batch(data.n)
        feed_dict = {
            self.args: args,
            self.masks: masks,
            self.lens: lens,
            self.labels: labels,
            self.prob: 1.
        }
        accuracy = sess.run(self.accuracy, feed_dict=feed_dict)
        return accuracy

    def train(self):
        train_data = self.dataloader.train
        validate_data = self.dataloader.validate
        test_data = self.dataloader.test
        sess = self.sess
        sess.run(tf.global_variables_initializer())
        last_time = time.time()
        step = 0
        best_accuracy = 0.
        while True:
            ids, args, masks, lens, labels = train_data.next_batch(self.batch_size)
            feed_dict = {
                self.args: args,
                self.masks: masks,
                self.lens: lens,
                self.labels: labels,
                self.prob: self.keep_prob
            }
            if step % 10 == 0:
                loss, accuracy, _ = sess.run(
                    [self.loss, self.accuracy, self.train_step],
                    feed_dict=feed_dict
                )
                now = time.time()
                last_time, rate = now, self.batch_size*10/(now-last_time)
                print 'Step %6d: loss = %3.2f, accuracy = %2.3f, docs/step = %8.2f'% (step, loss, accuracy, rate)
            step += 1
            if step * self.batch_size % train_data.n < self.batch_size:
                val_accuracy = self.test(validate_data)
                print '\n  Epoch %3d: validate_accuracy = %2.3f, best_accuracy = %2.3f\n' % (step*self.batch_size//train_data.n, val_accuracy, best_accuracy)
                if val_accuracy > best_accuracy:
                    best_accuracy = val_accuracy
                    self.save('save', 'best')
            if step * self.batch_size > self.max_epoch * train_data.n:
                break
        self.load('save', 'best')

    def visualize(self):
        sess = self.sess
        from tensorflow.contrib.tensorboard.plugins import projector
        word_dictionary = self.dataloader.word_dictionary
        word_reverse_dictionary = [None] * len(word_dictionary)
        for key in word_dictionary:
            word_reverse_dictionary[word_dictionary[key]] = key
        f = open('save/word.tsv', 'w')
        for word in word_reverse_dictionary:
            f.write('%s\n' % (word.encode('utf-8'),))
        f.close()
        config = projector.ProjectorConfig()
        word_embedding = config.embeddings.add()
        word_embedding.tensor_name = self.word_embedding.name
        word_embedding.metadata_path = 'save/word.tsv'

        data = self.dataloader.test
        sess = self.sess
        ids, args, masks, lens, labels = data.next_batch(data.n)
        feed_dict = {
            self.args: args,
            self.masks: masks,
            self.lens: lens,
            self.labels: labels,
            self.prob: 1.
        }
        sess.run(self.paper_embedding_assignment, feed_dict=feed_dict)
        self.save('save', 'best')

        paper_embedding = config.embeddings.add()
        paper_embedding.tensor_name = self.paper_embedding.name
        paper_embedding.metadata_path = 'test.tsv'

        summary_writer = tf.summary.FileWriter('save')
        projector.visualize_embeddings(summary_writer, config)


def variable_weight(name, shape, stddev, wd=0.):
    var = tf.get_variable(
        name = name,
        shape = shape,
        initializer = tf.truncated_normal_initializer(stddev=stddev)
    )
    if wd:
        weight_decay = tf.nn.l2_loss(var) * wd
        tf.add_to_collection('losses', weight_decay)
    return var
def variable_bias(name, shape):
    var = tf.get_variable(
        name = name,
        shape = shape,
        initializer = tf.zeros_initializer()
    )
    return var
