"""
neighbor similarity
"""


import math
import random
from utils.reader import simple_read, read_with_split, read_train_file

# legacy function
def score(input_path, set_path, output_path='../output/jaccard.txt', output=True):
    outbound_dict = read_with_split('../data/train.txt')
    set_dict = read_with_split(set_path)
    input_pairs = simple_read(input_path)
    result = []

    count = 1
    for key, value, sym in input_pairs: 
        key_set = set_dict[key]
        value_set = set_dict[value]


        score = 0

        if key not in outbound_dict or not outbound_dict[key]:
            result.append(' '.join((key, value, str(score), sym)) + '\n')
            continue

        for neighbor in outbound_dict[key]:
            neighbor_set = set_dict[neighbor]
            score += len(neighbor_set & value_set) / len(neighbor_set) * len(value_set)
        score = score / len(outbound_dict[key])

        result.append(' '.join((key, value, str(score), sym)) + '\n')

    with open(output_path, 'w') as writer:
        for r in result:
            writer.write(' '.join((key, value, str(score), sym)) + '\n')
            count += 1
            print(count)


def _calc_neighbor_score_03(pairs, set_dict, R=30):
    source, sink = pairs
    score = 0

    if sink not in set_dict or not set_dict[sink]:
        return 0

    if source not in set_dict or not set_dict[source]:
        return 0
    
    source_set = set_dict[source]
    
    i = 0
    sources = list(set_dict[sink])
    length = len(sources)

    if length < R + 5:
        for s in sources:
            if s == source:
                # print('here')
                continue
            cand1 = source_set - {sink} if source in set_dict[sink] else source_set
            cand2 = set_dict[s] - {sink} if source in set_dict[sink] else set_dict[s]
            score += math.atan(len(cand1) * len(cand2))
        return math.log(score + 1) / 100

    visited = set()

    while i < R:
        s = sources[random.randint(0, length - 1)]
        if sink == s or s in visited:
            # print('here')
            continue
        visited.add(s)
        cand1 = source_set - {sink} if source in set_dict[sink] else source_set
        cand2 = set_dict[s] - {sink} if source in set_dict[sink] else set_dict[s]
        score += math.atan(len(cand1) * len(cand2))
        i += 1
    
    return math.log(score + 1) / 100


def _calc_neighbor_score(pairs, set_dict, R=30):
    source, sink = pairs
    score = 0

    if source not in set_dict or not set_dict[source]:
        return 0

    if sink not in set_dict or not set_dict[sink]:
        return 0
    
    sink_set = set_dict[sink]
    
    i = 0
    sinks = list(set_dict[source])
    length = len(sinks)

    if length < R + 5:
        for s in sinks:
            if s == sink:
                # print('here')
                continue
            cand1 = sink_set - {source} if sink in set_dict[source] else sink_set
            cand2 = set_dict[s] - {source} if sink in set_dict[source] else set_dict[s]
            score += math.atan(len(cand1) * len(cand2))
        return math.log(score + 1) / 100

    visited = set()

    while i < R:
        s = sinks[random.randint(0, length - 1)]
        if sink == s or s in visited:
            # print('here')
            continue
        visited.add(s)
        cand1 = sink_set - {source} if sink in set_dict[source] else sink_set
        cand2 = set_dict[s] - {source} if sink in set_dict[source] else set_dict[s]
        score += math.atan(len(cand1) * len(cand2))
        i += 1
    
    return math.log(score + 1) / 100
    

def _neighbor_score_random(input_path, output_path, neighbor_dict, is_inbound=False):
    
    result = []
    count = 0
    with open(input_path) as reader:
        pairs = [r.split() for r in reader.readlines()]

        for p in pairs:
            key = (p[0], p[1])
            if is_inbound:
                score = _calc_neighbor_score_03(key, neighbor_dict)
            else:
                score = _calc_neighbor_score(key, neighbor_dict)

            print(count)
            count += 1

            info = key + (str(score), p[-1])
            result.append(info)
        
    with open(output_path, 'w') as writer: 
        for r in result:
            writer.write(' '.join(r) + '\n')


def _simple_score(input_path, output_path, set_dict, output=True):
    input_pairs = simple_read(input_path)
    result = []

    for key, value, sym in input_pairs:
        if key not in set_dict or value not in set_dict:
            score = 0
        else:
            key_set = set_dict[key]
            value_set = set_dict[value]
            score = len(key_set) * len(value_set)

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

    set_dict = read_train_file('../output/collect.txt')

    # _simple_score('../output/fakedataprop/fake_origin_zeo.txt',
    #                       '../output/jaccard/prop/jaccard_origin_zeo.txt', set_dict)

    _neighbor_score_random('../output/fakedataprop/fake_origin_clm.txt',
                          '../output/neighbor/prop/neighbor_clm.txt', set_dict)

    # _neighbor_score_random('../output/fake.txt',
    #                       '../output/neighbor/prop/neighbor_inbound.txt', set_dict, is_inbound=True)

    # _simple_score('../output/test.txt',
    #                       '../output/jaccard/jaccard_test_zeo.txt', set_dict)

    _neighbor_score_random('../output/test.txt',
                          '../output/neighbor/neighbor_test_clm.txt', set_dict)

    # _neighbor_score_random('../output/test.txt',
    #                       '../output/neighbor/neighbor_inbound_test_huge.txt', set_dict, is_inbound=True)