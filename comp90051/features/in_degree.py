"""
in degree
"""
import math
from utils.reader import read_train_file


def _in_degree(input_path, output_path, set_dict):

    result = []
    count = 0
    with open(input_path) as reader:
        pairs = [r.split() for r in reader.readlines()]

        for p in pairs:
            score = math.log(len(set_dict[p[1]]))

            print(count)
            count += 1

            info = (p[0], p[1]) + (str(score), p[-1])
            result.append(info)
        
    with open(output_path, 'w') as writer: 
        for r in result:
            writer.write(' '.join(r) + '\n')


if __name__ == '__main__':

    set_dict = read_train_file('../output/inbound_collect.txt')

    _in_degree('../output/fakedataprop/fake_origin_bit.txt',
            '../output/indegree/prop/indegree_origin_bit.txt',
            set_dict)

    # test
    _in_degree('../output/test.txt',
            '../output/indegree/indegree_test_bit.txt',
            set_dict)