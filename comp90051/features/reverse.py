"""
    reverse
"""

import random
from utils.reader import read_train_file, simple_read

def _calc_reverse_score_03(pairs, set_dict, sink_dict, R=30):
    source, sink = pairs
    score = 0

    i = 0
    sinks = list(sink_dict[sink])
    length = len(sinks)

    if length < R + 5:
        for s in sinks:
            if s not in set_dict:
                continue
            else:
                score += 1 if source in set_dict[s] else 0
        return  score / length

    visited = set()

    while i < R:
        s = sinks[random.randint(0, length - 1)]
        if s in visited:
            continue
        visited.add(s)

        if s not in set_dict:
            continue
        else:
            score += 1 if source in set_dict[s] else 0
            i += 1
    
    return score / R

    
def _calc_reverse_score(pairs, set_dict, R=30):
    source, sink = pairs
    score = 0

    i = 0
    sinks = list(set_dict[source])
    length = len(sinks)

    if length < R + 5:
        for s in sinks:
            if sink not in set_dict:
                continue
            else:
                score += 1 if s in set_dict[sink] else 0
        return score

    visited = set()

    while i < R:
        s = sinks[random.randint(0, length - 1)]
        if s == sink or s in visited:
            # print('here')
            continue
        visited.add(s)

        if sink not in set_dict:
            i += 1
            continue
        else:
            score += 1 if s in set_dict[sink] else 0
            i += 1
    
    return score


def _simple_score(input_path, output_path, set_dict, output=True):
    input_pairs = simple_read(input_path)
    result = []
    count = 0

    for key, value, sym in input_pairs:
        if value not in set_dict:
            score = 0
        else:
            score = 1 if key in set_dict[value] else 0

        result.append((key, value, str(score), sym))

        print(count + 1)
        count += 1

    if output:
        with open(output_path, 'w') as writer:
            for r in result:
                writer.write(' '.join(r) + '\n')
    return result


def _reverse_score_random(input_path, output_path, set_dict, sink_dict=None, is_inbound=False):
    
    result = []
    count = 0

    with open(input_path) as reader:
        pairs = [r.split() for r in reader.readlines()]

        for p in pairs:
            key = (p[0], p[1])
            if is_inbound:
                score = _calc_reverse_score_03(key, set_dict, sink_dict)
            else:
                score = _calc_reverse_score(key, set_dict)

            print(count)
            count += 1

            info = key + (str(score), p[-1])
            result.append(info)
        
    with open(output_path, 'w') as writer: 
        for r in result:
            writer.write(' '.join(r) + '\n')


if __name__ == '__main__':
    set_dict = read_train_file('../data/train.txt')
    sink_dict = read_train_file('../output/inbound_collect.txt')

    # _simple_score('../output/fakedataprop/fake_origin_huge.txt', '../output/reverse/prop/reverse_origin_huge.txt', set_dict)
    # _simple_score('../output/test.txt', '../output/reverse/reverse_origin_test.txt', set_dict)

    _reverse_score_random('../output/fakedataprop/fake_origin_clm.txt', '../output/reverse/prop/reverse_clm.txt',
                          set_dict, sink_dict, is_inbound=True)
    _reverse_score_random('../output/test.txt', '../output/reverse/reverse_test_clm.txt',
                          set_dict, sink_dict, is_inbound=True)