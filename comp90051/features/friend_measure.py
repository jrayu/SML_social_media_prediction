"""
friend measure
"""

import math
from utils.reader import read_train_file

def _cal_measure(key, set_dict):
    source, sink = key

    if source not in set_dict or sink not in set_dict:
        return 0

    score = 0

    source_set = set_dict[source]
    sink_set = set_dict[sink]

    if not source_set or not sink_set:
        return 0

    for s1 in source_set:
        for s2 in sink_set:
            if s1 in set_dict and s2 in set_dict[s1]:
                score += 1
            if s2 in set_dict and s1 in set_dict[s2]:
                score += 1
            elif s1 == s2:
                score += 1
    
    return score / (len(source_set) * len(sink_set))


def _friend_measure(input_path, output_path, set_dict):

    result = []
    count = 0
    with open(input_path) as reader:
        pairs = [r.split() for r in reader.readlines()]
        # cache = {}
        for p in pairs:
            key = (p[0], p[1])
            score = _cal_measure(key, set_dict)

            print(count)
            count += 1

            info = key + (str(score), p[-1])
            result.append(info)
        
    with open(output_path, 'w') as writer: 
        for r in result:
            writer.write(' '.join(r) + '\n')


if __name__ == '__main__':
    set_dict = read_train_file('../output/inbound_collect.txt')

    _friend_measure('../output/fakedataprop/fake_origin_clm.txt', 
                    '../output/friendmeasure/prop/friendmeasure_clm_04.txt', set_dict)

    _friend_measure('../output/test.txt', 
                    '../output/friendmeasure/friendmeasure_test_clm_04.txt', set_dict)