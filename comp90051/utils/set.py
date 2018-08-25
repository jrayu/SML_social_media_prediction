"""
legacy module (temporary)
set-related funcs
"""
from utils.reader import read_with_split

def store_set_length(input_path, output_path, outbound_path):
    with open(input_path) as reader:
        outbound_dict = read_with_split(outbound_path)
        with open(output_path, 'w') as writer:
            for r in reader:
                ids = r.split()
                key = ids[0]
                outbound = 0 if key not in outbound_dict else len(outbound_dict[key])
                inbound = len(ids) - 1 - outbound
                info = (ids[0], str(outbound), str(inbound))
                writer.write(' '.join(info) + '\n')


if __name__ == '__main__':
    store_set_length('../output/collect.txt', '../output/set_count.txt',
            '../data/train.txt')
