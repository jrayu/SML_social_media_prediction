"""
local path
"""

import random
import numpy as np
from utils.reader import read_train_file


def _random_pick(cand, count=80):
    if len(cand) < count:
        return cand
    return set(np.random.choice(list(cand), count, replace=False))


def _calc_local_path(key, set_dict, A=0.02, T=2):
    """
    calc local path
    : param key: id pairs of two nodes
    : param set_dict: dicionary storing all nodes and their out neighbors
    : param A: constant used when calc neighbors at different depths
    """
    source, sink = key

    upbound = _random_pick(set_dict[source] - {sink}) | _random_pick(set_dict[sink])

    def _dfs(node, visited, level):
        if level > T:
            return 0

        score = 0
        if sink in set_dict[node]:
            score = A ** level
        
        cands = set_dict[node] & upbound
        cands -= visited

        for c in cands:
            score += _dfs(c, {node} | visited, level + 1)
        
        return score

    score = 0
    neighbors = set_dict[source] & upbound
    for s in neighbors:
        score += _dfs(s, {source, sink}, 1)

    return score


def _local_path(input_path, output_path, set_dict):

    result = []
    count = 0
    with open(input_path) as reader:
        pairs = [r.split() for r in reader.readlines()]

        for p in pairs:
            key = (p[0], p[1])

            score = _calc_local_path(key, set_dict)

            if not count % 10:
                print(count, score)
            count += 1

            info = key + (str(score), p[-1])
            result.append(info)
        
    with open(output_path, 'w') as writer: 
        for r in result:
            writer.write(' '.join(r) + '\n')


if __name__ == '__main__':

    set_dict = read_train_file('../output/collect.txt')

    print('Read set ready')

    _local_path('../output/fakedataprop/fake_origin_clm.txt',
            '../output/localpath/prop/localpath_clm_11.txt',
            set_dict)

    # # test
    _local_path('../output/test.txt',
            '../output/localpath/localpath_test_clm_11.txt',
            set_dict)