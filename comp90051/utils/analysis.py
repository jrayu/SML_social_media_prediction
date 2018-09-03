"""
Module for analysis test data
"""

from utils.reader import read_train_file

def analysis(input_path, set_dict, inbound_dict, output_path, is_test=False):
    """ analysis test data
    1. the proportion of source nodes that appear as source nodes in training data (100%)
    2. the proportion of sink nodes that appear as source nodes in training data (around 18.8%)
    """

    result_pairs = []
    c = 0

    c2 = 0

    c3 = 0
    s3 = []

    c4 = 0
    s4 = []

    c5 = 0
    s5 = []

    c6 = 0
    s6 = []

    with open(input_path) as reader:
        for r in reader:
            if is_test:
                source, sink = r.split()[1:]
            else:
                source, sink = r.split()[:2]
            
            # print(r.split())

            # skip the first line
            if source == 'Source':
                continue

            degree = inbound_dict[sink]
            s1 = str(1) if source in set_dict else str(0)

            if source in inbound_dict:
                c2 += 1
            
            if sink in set_dict:
                c += 1
                s2 = str(1)
            else:
                s2 = str(0)
            
            c3 += len(inbound_dict[sink])
            s3.append(len(inbound_dict[sink]))

            if sink in set_dict:
                c4 += len(set_dict[sink])
                s4.append(len(set_dict[sink]))

            c5 += len(inbound_dict[source])
            s5.append(len(inbound_dict[source]))

            c6 += len(set_dict[source])
            s6.append(len(set_dict[source]))

            result_pairs.append((s1, s2))
    
    print(f'Mean: {c3/len(result_pairs)}')
    print(f'Mean: {c4/len(result_pairs)}')
    print(f'Mediam: {sorted(s3)[len(s3)//2]}')
    print(f'Mediam: {sorted(s4)[len(s4)//2]}')
    print('\n')
    print(f'Mean: {c5/len(result_pairs)}')
    print(f'Mean: {c6/len(result_pairs)}')
    print(f'Mediam: {sorted(s5)[len(s5)//2]}')
    print(f'Mediam: {sorted(s6)[len(s6)//2]}')
    print('\n')

    # with open(output_path, 'w') as writer:
    #     for s1, s2 in result_pairs:
    #         writer.write(f'{s1} {s2}\n')


def analysis_train_set(test_path, train_path):
    test_set = set()

    with open(test_path) as reader:
        for r in reader:
            infos = r.split()
            test_set.add(infos[0])

    count = 0
    with open(train_path) as reader:
        for r in reader:
            infos = r.split()
            # print(infos[0], infos[1])
            if infos[0] in test_set:
                count += 1
                print(infos[0], infos[1])
    
    print(count)


def analysis_inbound(train_path, inbound_path):
    train_dict = read_train_file(train_path)
    inbound_dict = read_train_file(inbound_path)
    
    for k, vs in inbound_dict.items():
        for v in vs:
            if k not in train_dict[v]:
                print('Abnormal!!')
                break


if __name__ == '__main__':
    # analysis('../output/fake.txt', '../data/train.txt', '../output/inbound_collect.txt', '../output/analysis/test.txt')
    set_dict = read_train_file('../data/train.txt')
    collect_dict = read_train_file('../output/inbound_collect.txt')

    analysis('../output/fakedataprop/fake_origin_tie.txt', set_dict, collect_dict, '../output/analysis/test.txt')
    analysis('../output/test.txt', set_dict, collect_dict, '../output/analysis/test.txt')
    # analysis_train_set('../output/test.txt', '../output/fakedataprop/fake_origin_large.txt')
    # analysis_inbound('../data/train.txt', '../output/inbound_collect.txt')