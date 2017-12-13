import tensorflow as tf
from model import Model
from dataloader import Loader

flags = tf.app.flags
flags.DEFINE_integer('embedding_size', 50, 'The dimension of word vector.')
flags.DEFINE_integer('max_epoch', 50, 'The epoch times of total training.')
flags.DEFINE_float('keep_prob', 0.5, 'The probability of keeping in dropout.')
flags.DEFINE_float('learning_rate', 1e-2, 'The initial learning rate.')
flags.DEFINE_integer('mincount', 5, 'Words whose appearing times less than this valve will be treated as unknown words.')
flags.DEFINE_integer('maxlen', 400, 'Documents whose words more than this valve will be truncated.')

FLAGS = flags.FLAGS


def main(_):
    print 'begin loading data...'
    loader = Loader(FLAGS.mincount, FLAGS.maxlen)
    print 'finished loading data\n'
    print 'begin building model...'
    # dataloader, embedding_size, max_epoch, learning_rate, keep_prob
    model = Model(
        loader,
        embedding_size = FLAGS.embedding_size,
        max_epoch = FLAGS.max_epoch,
        learning_rate = FLAGS.learning_rate,
        keep_prob = FLAGS.keep_prob
    )
    print 'finished building model\n'
    model.train()


if __name__ == '__main__':
    tf.app.run()
