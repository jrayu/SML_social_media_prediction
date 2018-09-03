"""
degree sub
"""
import math
from utils.reader import read_train_file


def _degree_sub(input_path, output_path, set_dict):

    result = []
    count = 0
    with open(input_path) as reader:
        pairs = [r.split() for r in reader.readlines()]

        for p in pairs:
            if p[1] not in set_dict:
                score1 = 0
            else:
                score1 = len(set_dict[p[1]])
            if p[0] not in set_dict:
                score2 = 0
            else:
                score2 = len(set_dict[p[0]])
            
            score = math.log(abs(score1 - score2) + 1)
            print(count)
            count += 1

            info = (p[0], p[1]) + (str(score), p[-1])
            result.append(info)
        
    with open(output_path, 'w') as writer: 
        for r in result:
            writer.write(' '.join(r) + '\n')


if __name__ == '__main__':

    set_dict = read_train_file('../output/collect.txt')

    _degree_sub('../output/fake.txt',
            '../output/degreesub/prop/degreesub.txt',
            set_dict)

    # test
    # _degree_sub('../output/test.txt',
    #         '../output/degreesub/degreesub_test_huge.txt',
    #         set_dict)