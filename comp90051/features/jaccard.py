""" Jaccard similarity
"""

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
            score += len(neighbor_set & value_set) / len(neighbor_set | value_set)
        score = score / len(outbound_dict[key])

        result.append(' '.join((key, value, str(score), sym)) + '\n')

    with open(output_path, 'w') as writer:
        for r in result:
            writer.write(' '.join((key, value, str(score), sym)) + '\n')
            count += 1
            print(count)


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
                # print('here')
                continue
            cand1 = sink_set - {source} if sink in set_dict[source] else sink_set
            cand2 = set_dict[s] - {source} if sink in set_dict[source] else set_dict[s]
            if not cand1 and not cand2:
                continue
            score += len(cand1 & cand2) / len(cand1 | cand2) 
        return score    

    visited = set()

    while i < R:
        s = sinks[random.randint(0, length - 1)]
        if sink == s or s in visited:
            # print('here')
            continue
        visited.add(s)
        cand1 = sink_set - {source} if sink in set_dict[source] else sink_set
        cand2 = set_dict[s] - {source} if sink in set_dict[source] else set_dict[s]
        if not cand1 and not cand2:
            i += 1
            continue
        score += len(cand1 & cand2) / len(cand1 | cand2) 
        i += 1
    
    return score
    

def _neighbor_score_random(input_path, output_path, neighbor_dict):
    
    result = []
    count = 0
    with open(input_path) as reader:
        pairs = [r.split() for r in reader.readlines()]

        for p in pairs:
            key = (p[0], p[1])
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

    _simple_score('../output/fakedataprop/fake_origin_bit.txt',
                          '../output/jaccard/prop/jaccard_origin_bit.txt', set_dict)

    _neighbor_score_random('../output/fakedataprop/fake_origin_bit.txt',
                          '../output/jaccardneighbor/prop/jaccard_neighbor_origin_bit.txt', set_dict)

    _simple_score('../output/test.txt',
                          '../output/jaccard/jaccard_test_bit.txt', set_dict)

    _neighbor_score_random('../output/test.txt',
                          '../output/jaccardneighbor/jaccard_neighbor_test_bit.txt', set_dict)
