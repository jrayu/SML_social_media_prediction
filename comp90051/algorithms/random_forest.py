import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold, GridSearchCV
from sklearn.metrics import roc_curve, auc, accuracy_score, classification_report, roc_auc_score
from utils.reader import read_from_txt
from algorithms.cross_evaluate import cross_evaluate


def _random_forest(x_train, y_train, x_test=None, y_test=None):
    clf = RandomForestClassifier(n_estimators=1000, n_jobs=-1,
    # class_weight={0: 1, 1: 2.4}
                                 )
    # clf = LogisticRegression(C=1)
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


data_path = [
    # '../output/simrank/prop/simrank_clm_02.txt',
    # '../output/propflow/prop/propflow_clm.txt',
    # '../output/localpath/prop/localpath_clm_11.txt',
    # '../output/jaccardneighbor/prop/jaccard_neighbor_clm_02.txt',
    # '../output/jaccardneighbor/prop/jaccard_neighbor_inbound_clm_02.txt',
    '../output/consineneighbor/prop/consine_neighbor_inbound_kim.txt',
    # '../output/shortestpath/prop/shortestpath_clm_03.txt',
    ]

kim_path = [
    # '../output/simrank/prop/simrank_clm_02.txt',
    # '../output/propflow/prop/propflow_clm.txt',
    # '../output/localpath/prop/localpath_clm_11.txt',
    # '../output/jaccardneighbor/prop/jaccard_neighbor_kim_02.txt',
    # '../output/jaccardneighbor/prop/jaccard_neighbor_inbound_clm_02.txt',
    '../output/consineneighbor/prop/consine_neighbor_inbound_clm.txt',
    # '../output/shortestpath/prop/shortestpath_clm_03.txt',
    ]

test_path = [
    # '../output/simrank/simrank_test_clm_02.txt',
    # '../output/propflow/propflow_test_clm.txt',
    # '../output/localpath/localpath_test_clm_11.txt',
    # '../output/jaccardneighbor/jaccard_neighbor_test_kim_02.txt',
    # '../output/jaccardneighbor/jaccard_neighbor_inbound_test_clm_02.txt',
    '../output/consineneighbor/consine_neighbor_inbound_test_kim.txt',
    # '../output/shortestpath/shortestpath_test_clm_03.txt',
    ]
    

def _split_evaluate():
    combined_features, labels = _read_data(data_path)

    test_features, test_labels = _read_data(kim_path)

    clf = RandomForestClassifier(n_estimators=1000,
                                 oob_score=True, n_jobs=-1,
                                 )

    cv = StratifiedKFold(n_splits=10)
    areas = []

    for train, test in cv.split(combined_features, labels):
        clf.fit(combined_features[train], labels[train]).predict_proba(combined_features[test])
        # print(clf.oob_score_)
        y_predict = clf.predict(combined_features[test])
        print(y_predict[y_predict==1].size)
        print(y_predict[y_predict==0].size)
        print(classification_report(labels[test], y_predict))

        proba = clf.predict_proba(combined_features[test])
        y_pred = clf.predict(combined_features[test])
        print(np.mean(proba[:, 1]))
        area = roc_auc_score(labels[test], proba[:, 1])
        areas.append(area)
        print('accuracy:', accuracy_score(labels[test], y_pred))
        print('auc', area)
    
    print('average', sum(areas) / len(areas))

    test_proba = clf.predict_proba(test_features)
    print('test: ', roc_auc_score(test_labels, test_proba[:, 1]))

        
def _run_for_test(output_path):

    train_features, train_labels = _read_data(data_path)
    clf = _random_forest(train_features, train_labels)


    test_features, test_labels = _read_data(test_path)

    y_predict = clf.predict(test_features)

    print(y_predict[y_predict==1].size)
    print(y_predict[y_predict==0].size)

    scores = clf.predict_proba(test_features)[:, 1]

    print(np.mean(scores))
    with open(output_path, 'w') as writer:
        writer.write('Id,Prediction\n')
        for i, s in enumerate(scores):
            writer.write(f'{i+1},{s}\n')


if __name__ == '__main__':
    _split_evaluate()
    _run_for_test('../output/result/prediction_j.csv')