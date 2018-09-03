import math
import random
from utils.reader import simple_read, read_with_split, read_train_file

def score(input_path, set_path, output_path='../output/adar.txt', output=True):
    input_pairs = simple_read(input_path)
    set_dict = read_with_split(set_path)
    result = []

    for key, value, sym in input_pairs:
        key_set = set_dict[key]
        value_set = set_dict[value]

        intersection = key_set & value_set

        score = 0
        for common in intersection:
            if not set_dict[common]:
               continue 
            score += 1 / math.log(len(set_dict[common]) + 1)

        print(len(result))

        result.append((key, value, str(score), sym))

    if output:
        with open(output_path, 'w') as writer:
            for r in result:
                writer.write(' '.join(r) + '\n')
    return result

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
                continue
            if not set_dict[s]:
                continue
            intersect = source_set & set_dict[s]
            if not intersect:
                continue
            for c in intersect:
                if not set_dict[c] or c == sink:
                    continue
                score += 1 / (math.log(len(set_dict[c]) + 1))
            # score = score / len(intersect)
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
        intersect = source_set & set_dict[s]
        if not intersect:
            i += 1
            continue
        for c in intersect:
            if not set_dict[c] or c == sink:
                i += 1
                continue
            score += 1 / (math.log(len(set_dict[c]) + 1))
        # score = score / len(intersect)
        i += 1
    
    return score / R


def _calc_neighbor_score(pairs, set_dict, R=30):
    source, sink = pairs
    score = 0

    if source not in set_dict or not set_dict[source]:
        return 0
    
    sink_set = set_dict[sink]
    
    i = 0
    sinks = list(set_dict[source])
    length = len(sinks)

    if length < R + 5:
        for s in sinks:
            if s == sink:
                continue
            if not set_dict[s]:
                continue
            intersect = sink_set & set_dict[s]
            if not intersect:
                continue
            for c in intersect:
                if not set_dict[c] or c == source:
                    continue
                score += 1 / (math.log(len(set_dict[c]) + 1))
        return score / length

    visited = set()

    while i < R:
        s = sinks[random.randint(0, length - 1)]
        if sink == s or s in visited:
            continue
        visited.add(s)
        if not set_dict[s]:
            i += 1
            continue
        intersect = sink_set & set_dict[s]
        if not intersect:
            i += 1
            continue
        for c in intersect:
            if not set_dict[c] or c == source:
                i += 1
                continue
            score += 1 / (math.log(len(set_dict[c]) + 1))
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

    # _simple_score('../output/fakedataprop/fake_origin_huge.txt',
    #                       '../output/jaccard/prop/jaccard_origin_huge.txt', set_dict)

    # _neighbor_score_random('../output/fakedataprop/fake_origin_huge.txt',
    #                       '../output/adarneighbor/prop/adar_neighbor_origin_huge.txt', set_dict)

    _neighbor_score_random('../output/fakedataprop/fake_origin_clm.txt',
                          '../output/adarneighbor/prop/adar_inbound_neighbor_clm.txt', set_dict)

    # _simple_score('../output/test.txt',
    #                       '../output/jaccard/jaccard_test_huge.txt', set_dict)

    _neighbor_score_random('../output/test.txt',
                          '../output/adarneighbor/adar_neighbor_test_clm.txt', set_dict)

    # _neighbor_score_random('../output/test.txt',
    #                       '../output/adarneighbor/adar_inbound_neighbor_test_huge.txt', set_dict, is_inbound=True)