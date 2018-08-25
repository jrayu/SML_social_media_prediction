"""
Module for analysis test data
"""


def analysis(input_path, set_path, inbound_path, output_path, is_test=True):
    """ analysis test data
    1. the proportion of source nodes that appear as source nodes in training data (100%)
    2. the proportion of sink nodes that appear as source nodes in training data (around 18.8%)
    """

    set_dict = {}

    with open(set_path) as reader:
        for r in reader:
            infos = r.split()
            set_dict[infos[0]] = set(infos[1:])

    inbound_dict = {}

    with open(inbound_path) as reader:
        for r in reader:
            infos = r.split()
            inbound_dict[infos[0]] = set(infos[1:])

    result_pairs = []
    c = 0

    c2 = 0

    # c3 = 0

    with open(input_path) as reader:
        for r in reader:
            if is_test:
                source, sink = r.split()[1:]
            else:
                source, sink = r.split()[:2]

            # skip the first line
            if source == 'Source':
                continue

            s1 = str(1) if source in set_dict else str(0)

            if source in inbound_dict:
                c2 += 1
            
            if sink in set_dict:
                c += 1
                s2 = str(1)
            else:
                s2 = str(0)

            result_pairs.append((s1, s2))
    
    print(f'proportion: {c/len(result_pairs)}')

    print(f'proportion (source inbound): {c2/len(result_pairs)}')

    with open(output_path, 'w') as writer:
        for s1, s2 in result_pairs:
            writer.write(f'{s1} {s2}\n')


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

if __name__ == '__main__':
    # analysis('../output/fakedataprop/fake_origin_large.txt', '../data/train.txt', '../output/inbound_collect.txt', '../output/analysis/test.txt')
    # analysis('../data/test-public.txt', '../data/train.txt', '../output/inbound_collect.txt', '../output/analysis/test.txt')
    analysis_train_set('../output/test.txt', '../output/fakedataprop/fake_origin_large.txt')