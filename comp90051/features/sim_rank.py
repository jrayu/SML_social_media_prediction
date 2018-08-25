"""
SimRank
"""

import random
from utils.reader import read_train_file

def _calc_sim(key, cache, set_dict, depth, record, C=0.8, max_depth=6):
    """
    calc similarity betweeen two nodes.
    : param key: id pairs of two nodes
    : param cache: dictionary storing already known similarity
    : param set_dict: dicionary storing all nodes and their neighbors
    : param depth: current depth of search
    : param record: walked nodes, prevent circle walk
    : param C: constant when calc similarity
    : param max_depth: max_depth when searching neighbors
    """
    if key in cache:
        print('Hit cache!!')
        return cache[key]

    # if two nodes are identical, we set similarity to 1
    if key[0] == key[1]:
        cache[key] = 1
        return cache[key]

    score = 0

    # if either of nodes has no neighbors, set similarity to 0
    if key[0] not in set_dict or key[1] not in set_dict:
        cache[key] = score
        return score

    list1 = list(set_dict[key[0]])
    list2 = list(set_dict[key[1]])

    # same as above
    if not len(list1) or not len(list2):
        cache[key] = score
        return score

    # hit max_depth
    if depth == max_depth:
        # cache[key] = score
        print('Hit max_depth!')
        return score
    
    for s1 in list1:
        for s2 in list2:
            # recursively call _calc_sim
            if s1 in record or s2 in record:
                print('Hit circle!!')
                continue
            score += _calc_sim((s1, s2), cache, set_dict, depth + 1, record | {key[0], key[1]}) 
    
    score /= (len(list1) * len(list2))

    cache[key] = score
    return score
    

def _calc_sim_random_work(key, set_dict, R=40, T=5, C=0.9):
    """
    calc similarity betweeen two nodes, through random walk
    : param key: id pairs of two nodes
    : param set_dict: dicionary storing all nodes and their neighbors
    : param R: times of random walk
    : param T: maximum depth of each walk
    : param C: constant when calc similarity
    """
    score = 0

    # Hit no inbound node, return 0 directly
    n1, n2 = key
    if n1 not in set_dict or n2 not in set_dict or \
        not set_dict[n1] or not set_dict[n2]:
            return 0


    for i in range(R):
        n1, n2 = key
        # record = set()
        j = 0

        while j < T:

            # Hit no inbound node, stop walk
            if n1 not in set_dict or n2 not in set_dict or \
                not set_dict[n1] or not set_dict[n2]:
                score += C ** T
                break
            
            # Only inbound node is previous one, stop walk
            # if (len(set_dict[n1]) == 1 and set_dict[n1] == {n1}) or \
            #     (len(set_dict[n2]) == 1 and set_dict[n2] == {n2}):
            #     score += C ** T
            #     break

            # Hit intersection, stop this walk
            if len(set_dict[n1] & set_dict[n2]) > 1:
                # k = len(set_dict[n1] & set_dict[n2]) / len(set_dict[n1] | set_dict[n2])
                score += C ** j
                break

            # add n1, n2 to walked nodes
            # record |= {n1, n2}

            list1 = list(set_dict[n1])
            list2 = list(set_dict[n2])

            # Random walk
            rand1 = random.randint(0, len(list1) - 1)
            rand2 = random.randint(0, len(list2) - 1)

            n1 = list1[rand1]
            n2 = list2[rand2]

            # if n1 in record or n2 in record:
            #     score += C ** T
            #     break

            j += 1

    return score / R


def sim_rank(input_path, output_path, set_dict):

    result = []
    count = 0
    with open(input_path) as reader:
        pairs = [r.split() for r in reader.readlines()]

        for p in pairs:
            key = (p[0], p[1])
            # score = _calc_sim(key, {}, set_dict, 0, set())
            score = _calc_sim_random_work(key, set_dict)

            print(count)
            count += 1

            info = key + (str(score), p[-1])
            result.append(info)
        
    with open(output_path, 'w') as writer: 
        for r in result:
            writer.write(' '.join(r) + '\n')


if __name__ == '__main__':
    # train
    # sim_rank('../output/fake_data.txt',
    #         '../output/simrank/simrank_03.txt',
    #         '../output/inbound_collect.txt')

    # sim_rank('../output/fakedata/fake_data_a.txt',
    #         '../output/simrank/simrank_a.txt',
    #         '../output/inbound_collect.txt')

    # sim_rank('../output/fakedata/fake_data_b.txt',
    #         '../output/simrank/simrank_b.txt',
    #         '../output/inbound_collect.txt')

    # sim_rank('../output/fakedata/fake_data_c.txt',
    #         '../output/simrank/simrank_c.txt',
    #         '../output/inbound_collect.txt')

    # sim_rank('../output/fakedata/fake_data_d.txt',
    #         '../output/simrank/simrank_d.txt',
    #         '../output/inbound_collect.txt')

    set_dict = read_train_file('../output/inbound_collect.txt')

    sim_rank('../output/fakedataprop/fake_origin_bit.txt',
            '../output/simrank/prop/simrank_origin_bit.txt',
            set_dict)

    # test
    sim_rank('../output/test.txt',
            '../output/simrank/simrank_test_bit.txt',
            set_dict)