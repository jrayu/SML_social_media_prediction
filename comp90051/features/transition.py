"""
transition similarity
"""


import math
import random
from utils.reader import simple_read, read_with_split, read_train_file

def _calc_neighbor_score_03(pairs, set_dict, inbound_dict, R=30):
    source, sink = pairs
    score = 0

    if sink not in inbound_dict or not inbound_dict[sink]:
        return 0

    if source not in set_dict or not set_dict[source]:
        return 0
    
    source_set = set_dict[source]
    
    i = 0
    sources = list(inbound_dict[sink])
    length = len(sources)

    if length < R + 5:
        for s in sources:
            if s == source:
                # print('here')
                continue
            if s not in inbound_dict or not inbound_dict[s]:
                continue
            score += math.atan(len(inbound_dict[s] & source_set))
        return math.log(score + 1)    

    visited = set()

    while i < R:
        s = sources[random.randint(0, length - 1)]
        if sink == s or s in visited:
            # print('here')
            continue
        visited.add(s)
        if s not in inbound_dict or not inbound_dict[s]:
            i += 1
            continue
        score += math.atan(len(inbound_dict[s] & source_set))
        i += 1
    
    return math.log(score + 1)


def _calc_neighbor_score(pairs, set_dict, inbound_dict, R=30):
    source, sink = pairs
    score = 0

    if source not in set_dict or not set_dict[source]:
        return 0
    
    if sink not in inbound_dict or not inbound_dict[sink]:
        return 0

    sink_set = inbound_dict[sink]
    
    i = 0
    sinks = list(set_dict[source])
    length = len(sinks)

    if length < R + 5:
        for s in sinks:
            if s == sink:
                # print('here')
                continue
            if s not in set_dict or not set_dict[s]:
                continue
            # cand1 = sink_set - {source} if sink in set_dict[source] else sink_set
            # cand2 = set_dict[s] - {source} if sink in set_dict[source] else set_dict[s]
            score += math.atan(len(set_dict[s] & sink_set))
        return math.log(score + 1)

    visited = set()

    while i < R:
        s = sinks[random.randint(0, length - 1)]
        if sink == s or s in visited:
            # print('here')
            continue
        if s not in set_dict or not set_dict[s]:
            i += 1
            continue
        visited.add(s)
        score += math.atan(len(set_dict[s] & sink_set))
        i += 1
    
    return math.log(score + 1)
    

def _neighbor_score_random(input_path, output_path, set_dict, inbound_dict, is_inbound=False):
    
    result = []
    count = 0
    with open(input_path) as reader:
        pairs = [r.split() for r in reader.readlines()]

        for p in pairs:
            key = (p[0], p[1])
            if is_inbound:
                score = _calc_neighbor_score_03(key, set_dict, inbound_dict)
            else:
                score = _calc_neighbor_score(key, set_dict, inbound_dict)

            print(count)
            count += 1

            info = key + (str(score), p[-1])
            result.append(info)
        
    with open(output_path, 'w') as writer: 
        for r in result:
            writer.write(' '.join(r) + '\n')


def _simple_score(input_path, output_path, set_dict, inbound_dict, output=True):
    input_pairs = simple_read(input_path)
    result = []

    for key, value, sym in input_pairs:
        if key not in set_dict or value not in inbound_dict:
            score = 0
        else:
            key_set = set_dict[key]
            value_set = inbound_dict[value]
            score = len(key_set & value_set) / len(key_set | value_set)

        print(len(result))

        result.append((key, value, str(score), sym))

    if output:
        with open(output_path, 'w') as writer:
            for r in result:
                writer.write(' '.join(r) + '\n')
    return result


if __name__ == '__main__':
    # result = score('../output/fake_false.txt', '../output/collect.txt')

    # result = simple_score('../output/fakedata/fake_data_a.txt', '../output/collect.txt',
    #         output_path='../output/jaccard/jaccard_a.txt')

    # result = simple_score('../output/fakedata/fake_data_b.txt', '../output/collect.txt',
    #         output_path='../output/jaccard/jaccard_b.txt')

    # result = simple_score('../output/fakedata/fake_data_c.txt', '../output/collect.txt',
    #         output_path='../output/jaccard/jaccard_c.txt')

    # result = simple_score('../output/fakedata/fake_data_d.txt', '../output/collect.txt',
    #         output_path='../output/jaccard/jaccard_d.txt')

    set_dict = read_train_file('../data/train.txt')
    inbound_dict = read_train_file('../output/inbound_collect.txt')
# 
    _simple_score('../output/fakedataprop/fake_origin_clm.txt',
                          '../output/transition/prop/transition_clm.txt', set_dict, inbound_dict)

    # _neighbor_score_random('../output/fakedataprop/fake_origin_clm.txt',
    #                       '../output/transition/prop/transition_neighbor_clm.txt', set_dict, inbound_dict)
#n
    #n_neighbor_score_random('../output/fake.txt',
    #                      '../output/transition/prop/transition_inbound.txt', set_dict, inbound_dict, is_inbound=True)

    # _neighbor_score_random('../output/fakedataprop/fake_origin_zeo.txt',
    #                       '../output/consineneighbor/prop/consine_inbound_neighbor_origin_zeo.txt', set_dict, is_inbound=True)

    # _neighbor_score_random('../output/fakedataprop/fake_origin_huge.txt',
    #                       '../output/consineneighbor/prop/consine_outbound_neighbor_origin_huge.txt', outbound_dict)

    # _neighbor_score_random('../output/fakedataprop/fake_origin_huge.txt',
    #                       '../output/consineneighbor/prop/consine_inbound_neighbor_origin_huge.txt', outbound_dict, is_inbound=True)

    _simple_score('../output/test.txt',
                          '../output/transition/transition_test_clm.txt', set_dict, inbound_dict)

    # _neighbor_score_random('../output/test.txt',
    #                       '../output/transition/transition_neighbor_test_clm.txt', set_dict, inbound_dict)

    # _neighbor_score_random('../output/test.txt',
    #                       '../output/transition/transition_inbound_neighbor_test_huge.txt', set_dict, inbound_dict, is_inbound=True)

    # _neighbor_score_random('../output/test.txt',
    #                       '../output/consineneighbor/consine_inbound_neighbor_test_zeo.txt', set_dict, is_inbound=True)

    # _neighbor_score_random('../output/test.txt',
    #                       '../output/consineneighbor/consine_outbound_neighbor_test_huge.txt', set_dict)