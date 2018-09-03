"""
out degree
"""
import math
from utils.reader import read_train_file


def _out_degree(input_path, output_path, set_dict, all_dict):

    result = []
    count = 0
    with open(input_path) as reader:
        pairs = [r.split() for r in reader.readlines()]

        for p in pairs:
            if p[0] not in set_dict:
                score = 0
            else:
                score = math.log(len(set_dict[p[0]]) + 1)

            print(count)
            count += 1

            info = (p[0], p[1]) + (str(score), p[-1])
            result.append(info)
        
    with open(output_path, 'w') as writer: 
        for r in result:
            writer.write(' '.join(r) + '\n')


if __name__ == '__main__':

    set_dict = read_train_file('../output/inbound_collect.txt')
    # all_dict = read_train_file('../output/collect_zeo.txt')

    _out_degree('../output/fakedataprop/fake_origin_huge.txt',
            '../output/outvolume/prop/outvolume_origin_huge.txt',
            set_dict, set_dict)

    # test
    _out_degree('../output/test.txt',
            '../output/outvolume/outvolume_test_huge.txt',
            set_dict, set_dict)