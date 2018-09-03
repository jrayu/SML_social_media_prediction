""" data transform module..
"""
import numpy as np

"""
modified raw format (fake data)
"""
def simple_read(input_path):
    """
    Read files by lines
    """
    result = []
    with open(input_path) as reader:
        for r in reader:
            line = tuple(r.split())
            result.append(line)
    return result


"""
raw format
"""

# duplicated function, use read_train_data instead
def read_with_split(input_path):
    """
    Simply read source file, split source and sink...
    """
    result = {}
    with open(input_path) as reader:
        for r in reader:
            line = r.split()
            result[line[0]] = set(line[1:])

            if len(result) % 1000000 == 0:
                print(len(result))

    return result


def read_with_entries(input_path):
    """
    Read source file, split source and sink, with all unique
    entries..
    @return (unique_entries, source-sink pairs)
    """
    entries, result = set(), {}
    with open(input_path) as reader:
        for r in reader:
            line = r.split()
            result[line[0]] = set(line[1:])
            for index in line:
                entries.add(index)
    return entries, result


def transform(input_path, output_dir):
    """
    transform txt source file to [key: [set]]
    """
    in_bound, out_bound, mixed_bound = {}, {}, {}

    with open(input_path) as reader:

        for line in reader:
            ids = line.split()
            key, values = ids[0], ids[1:]
            outs = set(values)
            out_bound[key] = outs

            if key in mixed_bound:
                mixed_bound[key] |= outs
            else:
                mixed_bound[key] = outs

            for out in values:
                if out in in_bound:
                    in_bound[out].add(key)
                else:
                    in_bound[out] = {key}
                if out in mixed_bound:
                    mixed_bound[out].add(key)
                else:
                    mixed_bound[out] = {key}

    with open(output_dir, 'w') as writer:
        for k, v in mixed_bound.items():
            line = k + ' ' + ' '.join(list(v))
            writer.write(line + '\n')

    # with open(output_dir, 'w') as writer:
    #     for k in out_bound.keys():
    #         cand = []
    #         vs = list(out_bound[k])
    #         for v in vs:
    #             if len(mixed_bound[v]) >= 7:
    #                 cand.append(v)
    #         if cand:
    #             line = k + ' ' + ' '.join(cand)
    #         # print(line)
    #             writer.write(line + '\n')

    # with open('../output/inbound_collect_tie.txt', 'w') as writer:
    #     for k in in_bound.keys():
    #         if len(mixed_bound[k]) < 7:
    #             continue
    #         line = k + ' ' + ' '.join(in_bound[k])
    #         # print(line)
    #         writer.write(line + '\n')

    # return in_bound, out_bound, mixed_bound


def unique_entries(input_path, last_index=None):
    """
    check unique entries
    """
    keys = set()

    with open(input_path) as reader:
        for line in reader:
            ids = line.split()
            if last_index is not None:
                ids = ids[:last_index]
            for i in ids:
                keys.add(i)
    print(len(keys))
    return len(keys)


"""
to numpy input format
"""
def read_from_txt(input_path):
    data = np.genfromtxt(input_path, delimiter=' ',
            dtype=[('source', 'U8'),
                ('sink', 'U8'), 
                ('score', 'f8'),
                ('class', 'i8')])
    return data


def transform_test_data(input_path, source_path,
        output_path='../output/test.txt', output=True):
    source_dict = read_with_split(source_path)
    result = []
    with open(input_path) as reader:
        content = reader.readlines()[1:]
        count = 1
        for c in content:
            index, source, sink = c.split()
            if source in source_dict:
                print('count:', count)
                count += 1
            if source in source_dict and sink in source_dict[source]:
                print('here')
                result.append((source, sink, '1'))
            else:
                result.append((source, sink, '0'))
    if output:
        with open(output_path, 'w') as writer:
            for r in result:
                writer.write(' '.join(r) + '\n')
    return result


def read_train_file(input_path):
    """
    : param input_path: the path of train file
    : data format: source sink1 sink2 sink3
    """
    set_dict = {}

    with open(input_path) as reader:
        for r in reader:
            infos = r.split()
            set_dict[infos[0]] = set(infos[1:])
    
    return set_dict


def tmp():
    with open('../output/friendmeasure/friendmeasure_test_clm_06.txt', 'w') as writer:
        with open('../output/friendmeasure/friendmeasure_test_clm_03.txt') as reader:
            for r in reader:
                s = r.split()
                s = s[:2] + [str(float(s[2]) / 100)] + s[3:]
                writer.write(' '.join(s) + '\n')


if __name__ == '__main__':
    # transform_test_data('../data/test-public.txt', '../data/train.txt')
    # transform('../data/train.txt', '../output/outbound_collect_tie.txt')
    # unique_entries('../output/outbound_collect_tie.txt')
    # unique_entries('../output/inbound_collect_tie.txt')

    transform('../output/outbound_collect_tie.txt', '../output/collect_tie.txt')
    unique_entries('../output/collect_tie.txt')
    # tmp()
