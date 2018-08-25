"""
cross evaluate
"""

import numpy as np
from utils.reader import read_from_txt

def cross_evaluate(algo, features, labels, split=10):
    size = features.shape[0]

    batch = int(size / split)
    i = 0


    while i <= size - batch:
        left_features = features[i: i + batch]
        left_labels = labels[i: i + batch]

        train_features = np.vstack((features[0: i], features[i + batch + 1:]))
        train_labels = np.hstack((labels[0: i], labels[i + batch + 1:]))

        print(f'Batch {i + 1}')

        algo(train_features, train_labels, left_features, left_labels)

        print('\n')

        i += batch