"""
local path
"""

from utils.reader import read_train_file

def _calc_local_path(key, set_path, A=0.8):
    """
    calc local path
    : param key: id pairs of two nodes
    : param set_dict: dicionary storing all nodes and their out neighbors
    : param A: constant used when calc neighbors at different depths
    """
    count = 0
    source, sink = key

    if source not in set_path:
        return 0

    # if sink in set_path[source]:
    #     count += 1 / len(set_path[source])

    first_neighbor = set_path[source]
    second_neighbor = set()
    # visited = {source}

    for n in first_neighbor:
        if n == sink:
            continue
        # if n in visited:
        #     continue
        # visited.add(n)
        if n in set_path:
            if sink in set_path[n]:
                count += 1 / len(set_path[n])
            second_neighbor |= set_path[n]
    
    for n in second_neighbor:
        if n == sink:
            continue
        # if n in visited:
        #     continue
        # visited.add(n)
        if n in set_path and sink in set_path[n]:
            count += A / len(set_path[n])

    return count    


def _local_path(input_path, output_path, set_dict):

    result = []
    count = 0
    with open(input_path) as reader:
        pairs = [r.split() for r in reader.readlines()]

        for p in pairs:
            key = (p[0], p[1])
            # score = _calc_sim(key, {}, set_dict, 0, set())
            score = _calc_local_path(key, set_dict)

            print(count)
            count += 1

            info = key + (str(score), p[-1])
            result.append(info)
        
    with open(output_path, 'w') as writer: 
        for r in result:
            writer.write(' '.join(r) + '\n')


if __name__ == '__main__':
    # train
    # local_path('../output/fake_data.txt',
    #         '../output/localpath/localpath_02.txt',
    #         '../data/train.txt')

    # local_path('../output/fakedata/fake_data_a.txt',
    #         '../output/localpath/localpath_a.txt',
    #         '../data/train.txt')

    # local_path('../output/fakedata/fake_data_b.txt',
    #         '../output/localpath/localpath_b.txt',
    #         '../data/train.txt')

    # local_path('../output/fakedata/fake_data_c.txt',
    #         '../output/localpath/localpath_c.txt',
    #         '../data/train.txt')

    # local_path('../output/fakedata/fake_data_d.txt',
    #         '../output/localpath/localpath_d.txt',
    #         '../data/train.txt')

    set_dict = read_train_file('../data/train.txt')

    _local_path('../output/fakedataprop/fake_origin_bit.txt',
            '../output/localpath/prop/localpath_origin_bit.txt',
            set_dict)

    # test
    _local_path('../output/test.txt',
            '../output/localpath/localpath_test_bit.txt',
            set_dict)