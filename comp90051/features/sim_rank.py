"""
SimRank
"""

import random
from utils.reader import read_train_file


def _calc_sim_random_work(key, set_dict, R=40, T=10, C=0.8):
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
            
            # Hit intersection, stop this walk
            ratio = len(set_dict[n1] & set_dict[n2]) / len(set_dict[n1] | set_dict[n2])
            if ratio:
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
        # cache = {}
        for p in pairs:
            key = (p[0], p[1])
            score = _calc_sim_random_work(key, set_dict)

            if not count % 50:
                print(count)
            count += 1

            info = key + (str(score), p[-1])
            result.append(info)
        
    with open(output_path, 'w') as writer: 
        for r in result:
            writer.write(' '.join(r) + '\n')


if __name__ == '__main__':

    set_dict = read_train_file('../data/train.txt')

    sim_rank('../output/fakedataprop/fake_origin_clm.txt',
            '../output/simrank/prop/simrank_clm_03.txt',
            set_dict)

    # test
    sim_rank('../output/test.txt',
            '../output/simrank/simrank_test_clm_03.txt',
            set_dict)