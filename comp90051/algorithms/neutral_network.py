import numpy as np
import tensorflow as tf
from tensorflow.contrib.tensor_forest.python import tensor_forest
from sklearn.cross_validation import train_test_split
from algorithms.logistic import _read_data

data_path = [
    # '../output/jaccard/prop/jaccard_origin_large.txt',
    '../output/simrank/prop/simrank_origin_large_04.txt',
    '../output/localpath/prop/localpath_origin_large.txt',
    '../output/propflow/prop/propflow_origin_large.txt',
    '../output/jaccardneighbor/prop/jaccard_neighbor_origin_large_04.txt',
    '../output/outdegree/prop/outdegree_origin_large.txt',
    '../output/indegree/prop/indegree_origin_large.txt',
    # '../output/adar/prop/adar_origin_large.txt',
    ]

features, labels = _read_data(data_path)
features_train, features_test, labels_train, labels_test = train_test_split(features, labels, test_size=0.3, random_state=99999)

class DatasetIterator:
    """
    An iterator that returns randomized batches from a data set (with features and labels)
    """
    def __init__(self, features, labels, batch_size):
        assert(features.shape[0]==labels.shape[0])
        assert(batch_size > 0 and batch_size <= features.shape[0])
        self.features = features
        self.labels = labels
        self.num_instances = features.shape[0]
        self.batch_size = batch_size
        self.num_batches = self.num_instances//self.batch_size
        if (self.num_instances%self.batch_size!=0):
            self.num_batches += 1
        self._i = 0
        self._rand_ids = None

    def __iter__(self):
        self._i = 0
        self._rand_ids = np.random.permutation(self.num_instances)
        return self
        
    def __next__(self):
        if self.num_instances - self._i >= self.batch_size:
            this_rand_ids = self._rand_ids[self._i:self._i + self.batch_size]
            self._i += self.batch_size
            return self.features[this_rand_ids], self.labels[this_rand_ids]
        elif self.num_instances - self._i > 0:
            this_rand_ids = self._rand_ids[self._i::]
            self._i = self.num_instances
            return self.features[this_rand_ids], self.labels[this_rand_ids]
        else:
            raise StopIteration()

# global parameter
display_step = 100

num_input = 6
num_class = 2
n_hidden_1 = 10
n_hidden_2 = 10

num_steps = 200

learning_rate = 0.1

batch_size = 100
train_iterator = DatasetIterator(features_train, labels_train, batch_size)

weights = {
    'h1': tf.Variable(tf.random_normal([num_input, n_hidden_1])),
    'h2': tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2])),
    'out': tf.Variable(tf.random_normal([n_hidden_2, num_class]))
}

biases = {
    'b1': tf.Variable(tf.random_normal([n_hidden_1])),
    'b2': tf.Variable(tf.random_normal([n_hidden_2])),
    'out': tf.Variable(tf.random_normal([num_class]))
}

def neural_net(x):
    # Hidden fully connected layer with 256 neurons
    layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
    # Hidden fully connected layer with 256 neurons
    layer_2 = tf.add(tf.matmul(layer_1, weights['h2']), biases['b2'])
    # Output fully connected layer with a neuron for each class
    out_layer = tf.matmul(layer_2, weights['out']) + biases['out']
    return out_layer

X = tf.placeholder(dtype=tf.float32, shape=[None, num_input])
Y = tf.placeholder(dtype=tf.uint8, shape=[None, ])

# logistic
# logits = neural_net(X)
# prediction = tf.nn.sigmoid(logits)
# Y_one_hot = tf.one_hot(Y, num_class)
# loss_op = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(
#     logits=logits, labels=Y_one_hot))
# 
# optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate)
# train_op = optimizer.minimize(loss_op)
# 
# correct_pred = tf.equal(tf.argmax(prediction, 1), tf.argmax(Y_one_hot, 1))
# accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

# random forest
hparams = tensor_forest.ForestHParams(num_classes=num_class, num_features=num_input, num_trees=500).fill()
forest_graph = tensor_forest.RandomForestGraphs(hparams)
train_op = forest_graph.training_graph(X, Y)
loss_op = forest_graph.training_loss(X, Y)

infer_op, _, _ = forest_graph.inference_graph(X)
correct_prediction = tf.equal(tf.argmax(infer_op, 1), tf.cast(Y, tf.int64))
accuracy_op = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

init = tf.global_variables_initializer()

def start_train():
    with tf.Session() as sess:

        # Run the initializer
        sess.run(init)

        for step in range(1, num_steps+1):
            for batch_x, batch_y in train_iterator:
            # Run optimization op (backprop)
                _, l = sess.run([train_op, loss_op], feed_dict={X: batch_x, Y: batch_y})
                if step % display_step == 0 or step == 1:
                # Calculate batch loss and accuracy
                    # loss, acc = sess.run([loss_op, accuracy], feed_dict={X: batch_x,
                    #                                                    Y: batch_y})
                    # print("Step " + str(step) + ", Minibatch Loss= " + \
                    #       "{:.4f}".format(loss) + ", Training Accuracy= " + \
                    #       "{:.3f}".format(acc))

                    acc = sess.run(accuracy_op, feed_dict={X: features_train, Y: labels_train})
                    print('Step %i, Loss: %f, Acc: %f' % (step, l, acc))

        print("Optimization Finished!")

        # Calculate accuracy for MNIST test images
        print("Testing Accuracy:", \
            sess.run(accuracy_op, feed_dict={X: features_test,
                                          Y: labels_test}))
                                
if __name__ == '__main__':
    start_train()