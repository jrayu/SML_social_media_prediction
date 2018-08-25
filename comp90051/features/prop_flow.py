"""
prop flow
"""

import random
from utils.reader import read_train_file

def _random_pick(cand, count=20):
    if len(cand) <= count + 10:
        return cand
    
    cand_list = list(cand)

    length = len(cand)
    result = set()

    while len(result) < count:
        c = cand_list[random.randint(0, length - 1)] 
        if c not in result:
            result.add(c)
    
    return c

def _calc_prop_flow(key, set_dict, max_depth=6):

    source, sink = key

    # no outbound
    if source not in set_dict:
        return 0

    def _dfs(node, prev, visited, score, depth):
        
        if depth == max_depth:
            return 0

        if node not in set_dict:
            return 0

        # hit sink node
        if sink in set_dict[node]:
            return (score * 1 / len(set_dict[prev])) * 1 / len(set_dict[node])

        # hit visited nodes
        if set_dict[node] & visited:
            return 0

        new_score = 0
        score = score * 1 / len(set_dict[prev]) 

        cands = _random_pick(set_dict[node])
        for s in cands:
            if s == prev:
                continue
            new_score += _dfs(s, node, visited | {prev}, score, depth + 1)
        
        return new_score
    
    score = 0

    # if sink in set_dict[source]:
    #     score += 1 / len(set_dict[source])

    for s in set_dict[source]:
        if s == sink:
            continue
        score += _dfs(s, source, set(), 1, 0)
    
    return score


def _prop_flow(input_path, output_path, set_dict):

    result = []
    count = 0
    with open(input_path) as reader:
        pairs = [r.split() for r in reader.readlines()]

        for p in pairs:
            key = (p[0], p[1])
            score = _calc_prop_flow(key, set_dict)

            print(count)
            count += 1

            info = key + (str(score), p[-1])
            result.append(info)
        
    with open(output_path, 'w') as writer: 
        for r in result:
            writer.write(' '.join(r) + '\n')


if __name__ == '__main__':
    # train
    # prop_flow('../output/fake_data.txt',
    #         '../output/propflow/propflow_02.txt',
    #         '../data/train.txt')

    # prop_flow('../output/fakedata/fake_data_a.txt',
    #         '../output/propflow/propflow_a.txt',
    #         '../data/train.txt')

    # prop_flow('../output/fakedata/fake_data_b.txt',
    #         '../output/propflow/propflow_b.txt',
    #         '../data/train.txt')

    # prop_flow('../output/fakedata/fake_data_c.txt',
    #         '../output/propflow/propflow_c.txt',
    #         '../data/train.txt')

    # prop_flow('../output/fakedata/fake_data_d.txt',
    #         '../output/propflow/propflow_d.txt',
    #         '../data/train.txt')

    set_dict = read_train_file('../data/train.txt')

    _prop_flow('../output/fakedataprop/fake_origin_bit.txt',
            '../output/propflow/prop/propflow_origin_bit.txt',
            set_dict)

    # test
    _prop_flow('../output/test.txt',
            '../output/propflow/propflow_test_bit.txt',
            set_dict)