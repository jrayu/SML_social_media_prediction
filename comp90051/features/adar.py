import math
from utils.reader import simple_read, read_with_split

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



if __name__ == '__main__':
    # result = score('../output/fake_false.txt', '../output/collect.txt')
    result = score('../output/fakedataprop/fake_origin_large.txt', '../output/collect.txt',
            output_path='../output/adar/prop/adar_origin_large.txt')

    result = score('../output/test.txt', '../output/collect.txt',
            output_path='../output/adar/adar_test.txt')
