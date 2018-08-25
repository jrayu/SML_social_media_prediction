import numpy as np
from sklearn import svm
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import roc_curve, auc, accuracy_score
from utils.reader import read_from_txt
from algorithms.cross_evaluate import cross_evaluate

def _svm(x_train, y_train, x_test=None, y_test=None):
    clf = svm.SVC(probability=True, C=1, kernel='rbf')
    clf.fit(x_train, y_train)

    if x_test is None or y_test is None:
        return clf

    y_pred = clf.predict(x_test)
    scores = clf.predict_proba(x_test)[:, 1]

    print('accuracy:', accuracy_score(y_test, y_pred))

    print(y_pred[y_pred==1].size)

    fpr, tpr, thresholds = roc_curve(y_test, scores)
    area = auc(fpr, tpr)
    print('auc', area)

    return clf


def svm_split(x, y):

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=99999)
    clf = svm.SVC(probability=True, C=1, kernel='rbf')
    clf.fit(x_train, y_train)


    y_pred = clf.predict(x_test)
    scores = clf.predict_proba(x_test)[:, 1]

    print('accuracy:', accuracy_score(y_test, y_pred))

    print(y_pred[y_pred==1].size)

    fpr, tpr, thresholds = roc_curve(y_test, scores)
    area = auc(fpr, tpr)
    print('auc', area)



    t2 = read_from_txt('../output/jaccard/jaccard_test.txt')['score']
    t5 = read_from_txt('../output/simrank/simrank_test_04.txt')['score']
    t6 = read_from_txt('../output/localpath/localpath_test.txt')['score']
    t7 = read_from_txt('../output/propflow/propflow_test.txt')['score']
    t8 = read_from_txt('../output/jaccardneighbor/jaccard_neighbor_test_04.txt')['score']
    t9 = read_from_txt('../output/outdegree/outdegree_test.txt')['score']
    t10 = read_from_txt('../output/indegree/indegree_test.txt')['score']
    t11 = read_from_txt('../output/adar/adar_test.txt')['score']

    test = np.c_[t2, t5, t6, t7, t8, t9, t10]

    y_test = clf.predict(test)

    print(y_test[y_test==1].size)

    return clf


def _read_data(path):
    data = []
    for p in path:
        data.append(read_from_txt(p))

    features = np.array([d['score'] for d in data])
    labels = data[0]['class']

    combined_features = features[0]

    if features.shape[0] == 1:
        return combined_features.reshape(-1, 1), labels

    for f in features[1:]:
        combined_features = np.c_[combined_features, f]

    return combined_features, labels


def _cross_evaluate():
    data_path = [
        '../output/jaccard/prop/jaccard_origin_large.txt',
        '../output/simrank/prop/simrank_origin_large_04.txt',
        '../output/localpath/prop/localpath_origin_large_02.txt',
        '../output/propflow/prop/propflow_origin_large.txt',
        '../output/jaccardneighbor/prop/jaccard_neighbor_origin_large_04.txt',
        # '../output/outdegree/prop/outdegree_origin_large.txt',
        # '../output/indegree/prop/indegree_origin_large.txt',
        ]


    combined_features, labels = _read_data(data_path)

    cross_evaluate(_svm, combined_features, labels, split=4)


def _split_evaluate():
    data_path = [
        '../output/jaccard/prop/jaccard_origin_large.txt',
        '../output/simrank/prop/simrank_origin_large_04.txt',
        '../output/localpath/prop/localpath_origin_large.txt',
        '../output/propflow/prop/propflow_origin_large.txt',
        '../output/jaccardneighbor/prop/jaccard_neighbor_origin_large_04.txt',
        '../output/outdegree/prop/outdegree_origin_large.txt',
        '../output/indegree/prop/indegree_origin_large.txt',
        # '../output/adar/prop/adar_origin_large.txt',
        ]

    combined_features, labels = _read_data(data_path)

    clf = svm_split(combined_features, labels)

    clf = svm.SVC(probability=True, C=1, kernel='rbf')

    cv = StratifiedKFold(n_splits=6)

    for train, test in cv.split(combined_features, labels):
        clf.fit(combined_features[train], labels[train]).predict_proba(combined_features[test])
        proba = clf.predict_proba(combined_features[test])
        y_pred = clf.predict(combined_features[test])
        fpr, tpr, thresholds = roc_curve(labels[test], proba[:, 1])
        area = auc(fpr, tpr)
        print('accuracy:', accuracy_score(labels[test], y_pred))
        print('auc', area)

    # scores = cross_val_score(clf, combined_features, labels, cv=10)
    # print(scores)
        

def _run_for_test(output_path):
    data_path = [
        '../output/jaccard/prop/jaccard_origin_large.txt',
        '../output/simrank/prop/simrank_origin_large_04.txt',
        '../output/localpath/prop/localpath_origin_large.txt',
        '../output/propflow/prop/propflow_origin_large.txt',
        '../output/jaccardneighbor/prop/jaccard_neighbor_origin_large_04.txt',
        '../output/outdegree/prop/outdegree_origin_large.txt',
        '../output/indegree/prop/indegree_origin_large.txt',
        # '../output/adar/prop/adar_origin_large.txt',
        ]

    train_features, train_labels = _read_data(data_path)
    clf = _svm(train_features, train_labels)


    test_path = [
        '../output/jaccard/jaccard_test.txt',
        '../output/simrank/simrank_test_04.txt',
        '../output/localpath/localpath_test.txt',
        '../output/propflow/propflow_test.txt',
        '../output/jaccardneighbor/jaccard_neighbor_test_04.txt',
        '../output/outdegree/outdegree_test.txt',
        '../output/indegree/indegree_test.txt',
        # '../output/adar/adar_test.txt',
        ]
    
    test_features, test_labels = _read_data(test_path)

    y_predict = clf.predict(test_features)

    print(y_predict[y_predict==1].size)

    scores = clf.predict_proba(test_features)[:, 1]

    with open(output_path, 'w') as writer:
        writer.write('Id,Prediction\n')
        for i, s in enumerate(scores):
            writer.write(f'{i+1},{str(s)}\n')



if __name__ == '__main__':
    # svm('../output/knn/knn.txt')
    # _cross_evaluate()
    _split_evaluate()
    _run_for_test('../output/test/prediction_op.csv')