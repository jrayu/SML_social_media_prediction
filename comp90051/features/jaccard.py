""" Jaccard similarity
"""

import random
from utils.reader import simple_read, read_with_split, read_train_file


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

    minus = 1 if sink in set_dict[source] else 0

    if length < R + 5:
        for s in sources:
            if s == source:
                continue
            if not set_dict[s]:
                continue
            intersect = len(source_set & set_dict[s]) - minus
            score += intersect / len(source_set | set_dict[s]) 
        return score / length

    visited = set()

    while i < R:
        s = sources[random.randint(0, length - 1)]
        if source == s or s in visited:
            continue
        visited.add(s)
        if not set_dict[s]:
            i += 1
            continue
        intersect = len(source_set & set_dict[s]) - minus
        score += intersect / len(source_set | set_dict[s]) 
        i += 1
    
    return score / R


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

    minus = 1 if source in sink_set else 0

    if length - minus == 0:
        return 0

    if length < R + 5:
        for s in sinks:
            if s == sink:
                continue
            if not set_dict[s]:
                continue
            intersect = len(sink_set & set_dict[s]) - minus
            union = len(sink_set | set_dict[s]) - minus
            if union == 0:
                continue
            score += intersect / union
        return score / (length - minus) 

    visited = set()

    while i < R:
        s = sinks[random.randint(0, length - 1)]
        if sink == s or s in visited:
            continue
        visited.add(s)
        if not set_dict[s]:
            i += 1
            continue
        intersect = len(sink_set & set_dict[s]) - minus
        union = len(sink_set | set_dict[s]) - minus
        if union == 0:
            continue
        score += intersect / union
        i += 1
    
    return score / R
    

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

            if not count % 10:
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
            score = len(key_set & value_set) / len(key_set | value_set)

        print(len(result))

        result.append((key, value, str(score), sym))

    if output:
        with open(output_path, 'w') as writer:
            for r in result:
                writer.write(' '.join(r) + '\n')
    return result


if __name__ == '__main__':
    set_dict = read_train_file('../output/collect.txt')

    # _simple_score('../output/fakedataprop/fake_origin_clm.txt', '../output/jaccard/prop/jaccard_clm.txt', set_dict)

    _neighbor_score_random('../output/fakedataprop/fake_origin_kim.txt',
                          '../output/jaccardneighbor/prop/jaccard_neighbor_kim.txt', set_dict)

    # _neighbor_score_random('../output/fakedataprop/fake_origin_kim.txt',
    #                       '../output/jaccardneighbor/prop/jaccard_neighbor_inbound_kim.txt', set_dict, is_inbound=True)

    # _simple_score('../output/test.txt', '../output/jaccard/jaccard_test_clm.txt', set_dict)

    # _neighbor_score_random('../output/test.txt',
    #                       '../output/jaccardneighbor/jaccard_neighbor_test_kim_02.txt', set_dict)

    # _neighbor_score_random('../output/test.txt',
    #                       '../output/jaccardneighbor/jaccard_neighbor_inbound_test_kim.txt', set_dict, is_inbound=True)