import tensorflow as tf
from fastText import Model
from dataloader import Loader, Data

flags = tf.app.flags
flags.DEFINE_integer('embedding_size', 10, 'The dimension of word vector.')
flags.DEFINE_integer('batch_size', 128, 'The number of samples per batch.')
flags.DEFINE_integer('max_epoch', 50, 'The epoch times of total training.')
flags.DEFINE_float('keep_prob', 0.5, 'The probability of keeping in dropout.')
flags.DEFINE_float('learning_rate', 1e-2, 'The initial learning rate.')
flags.DEFINE_bool('retrain', False, 'Whether to train model.')
flags.DEFINE_integer('mincount', 5, 'Words whose appearing times less than this valve will be treated as unknown words.')
flags.DEFINE_integer('maxlen', 1000, 'Documents whose words more than this valve will be truncated.')

FLAGS = flags.FLAGS

def main(_):
	print 'begin loading data...'
	loader = Loader.loader(FLAGS.mincount, FLAGS.maxlen)
	print 'finished loading data\n'
	print 'begin building model...'
	model = Model(
		loader, 
		embedding_size = FLAGS.embedding_size, 
		batch_size = FLAGS.batch_size, 
		max_epoch = FLAGS.max_epoch,
		learning_rate = FLAGS.learning_rate,
		keep_prob = FLAGS.keep_prob
	)
	print 'finished building model\n'
	if FLAGS.retrain:
		model.train()
		test_accuracy = model.test()
	else:
		try:
			model.load('save', 'best')
			test_accuracy = model.test()
		except tf.errors.NotFoundError:
			model.train()
			test_accuracy = model.test()
		except Exception, e:
			print 'Error may be caused by changing parameters without retraining. Try setting --retrain to True.'
			raise e
	print 'test_accuracy = %2.3f' % (test_accuracy,)
	model.visualize()

if __name__ == '__main__':
	tf.app.run()

