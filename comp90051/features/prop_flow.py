"""
prop flow
"""

import random
from utils.reader import read_train_file

def _random_pick(cand, count=30):
    if len(cand) <= count * 1.5:
        return cand
    
    cand_list = list(cand)

    length = len(cand)
    result = set()

    while len(result) < count:
        c = cand_list[random.randint(0, length - 1)] 
        if c not in result:
            result.add(c)
    
    return result


def _calc_prop_flow(key, set_dict, max_depth=4):

    source, sink = key

    upbound = _random_pick(set_dict[source]) | _random_pick(set_dict[sink])
    upbound |= {sink}

    def _dfs(node, weight, visited, score, depth):

        if node == sink:
            return score * 1 / weight
        
        if depth == max_depth:
            return 0

        if node not in set_dict or not set_dict[node]:
            return 0

        cands = set_dict[node] & upbound - visited

        if not cands:
            return 0

        new_score = 0
        score = score * 1 / weight

        for c in cands:
            new_score += _dfs(c, len(cands), visited | {node}, score, depth + 1)
        
        return new_score
    
    score = 0

    neighbor = set_dict[source] & upbound
    for s in neighbor:
        if s == sink:
            continue
        score += _dfs(s, len(neighbor), {source}, 1, 0)
    
    return score


def _prop_flow(input_path, output_path, set_dict, is_inbound=False):

    result = []
    count = 0
    with open(input_path) as reader:
        pairs = [r.split() for r in reader.readlines()]

        for p in pairs:
            key = (p[0], p[1])
            if is_inbound:
                score = _calc_prop_flow(key[::-1], set_dict)
            else:
                score = _calc_prop_flow(key, set_dict)

            print(count, score)
            count += 1

            info = key + (str(score), p[-1])
            result.append(info)
        
    with open(output_path, 'w') as writer: 
        for r in result:
            writer.write(' '.join(r) + '\n')


if __name__ == '__main__':

    set_dict = read_train_file('../output/collect.txt')

    _prop_flow('../output/fakedataprop/fake_origin_clm.txt',
            '../output/propflow/prop/propflow_clm_02.txt',
            set_dict)

    # test
    _prop_flow('../output/test.txt',
            '../output/propflow/propflow_test_clm_02.txt',
            set_dict)