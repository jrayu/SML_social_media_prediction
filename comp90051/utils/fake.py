""" fake training data
"""
from random import randint # surely we may use more sophisticate random functions instead.
from utils.reader import read_with_entries, read_with_split, simple_read, unique_entries, read_train_file


# legacy function
def fake_false_data(input_path,
        output_path='../output/fake_false.txt',
        size=2000,
        output=True):
    """ based on existing edges in training data,
    this function will fake pairs not existing.
    """
    keys, outbound_dict = read_with_entries(input_path)
    keys = list(keys)
    i, total_size = 0, len(keys)
    result = set()
    
    while i < size:
        key1 = keys[randint(0, total_size - 1)]
        key2 = keys[randint(0, total_size - 1)]
        if key1 == key2:
            continue
        if (key1 not in outbound_dict or key2 not in outbound_dict[key1]) and \
                (key1, key2) not in result:

                    print(key1, key2)

                    result.add((key1, key2))
                    i += 1

    if output:
        with open(output_path, 'w') as writer:
            for r in result:
                writer.write(' '.join(r) + ' 0 ' + '\n')
    
    return result


# legacy function
def fake_false_with_sink_data(input_path,
        output_path='../output/fake_false_test.txt',
        size=2000,
        output=True):
    """ based on existing edges in training data,
    this function will fake pairs not existing.
    """
    outbound_dict = read_with_split(input_path)
    keys = list(outbound_dict.keys())
    i, total_size = 0, len(keys)
    result = set()

    while i < size:
        key1 = keys[randint(0, total_size - 1)]
        if not outbound_dict[key1]:
            continue

        key2 = keys[randint(0, total_size - 1)]

        if key2 in outbound_dict[key1]:
            continue


        if (key1, key2) not in result:
            print(key1, key2)
            result.add((key1, key2))
            i += 1

    if output:
        with open(output_path, 'w') as writer:
            for r in result:
                writer.write(' '.join(r) + ' 0 ' + '\n')
    
    return result


# legacy function
def fake_true_data(input_path,
        output_path='../output/fake_true.txt',
        size=2000,
        output=True):
    """ randomly pick existing edges from training data
    """
    outbound_dict = read_with_split(input_path)
    keys = list(outbound_dict.keys())
    i, total_size = 0, len(keys)
    result = set()

    while i < size:
        source = keys[randint(0, total_size - 1)]
        # see line 8370... not sinks for 4483378...
        if not outbound_dict[source]:
            continue
        sinks = list(outbound_dict[source])
        value_size = len(sinks)

        print(source, sinks)

        value = sinks[randint(0, value_size - 1)]
        if (source, value) not in result:
            result.add((source, value))
            i += 1

    if output:
        with open(output_path, 'w') as writer:
            for r in result:
                writer.write(' '.join(r) + ' 1 ' + '\n')
    
    return result


# legacy function (temporary)
def check_fake_data(input_path, fake_path, is_true=True):
    outbound_dict = read_with_split(input_path)
    fake_set = simple_read(fake_path)
    for key, value, sym in fake_set:
        # if key not in outbound_dict:
        #     print("Abnormal data detected!!!")
        #     break

        if (key in outbound_dict and value in outbound_dict[key] and
                not is_true) or ((key not in outbound_dict or value not
                    in outbound_dict[key]) and is_true):
                    print("Abnormal data detected!!!")
                    break
    else:
        print("Everything is Okay!!!")


# legacy function (temporary)
def filter_set(input_path, set_path, output_path='../output/fake_set.txt',
        output=True):
    set_dict = read_with_split(set_path)
    pairs = simple_read(input_path)
    result = {}

    for key, value, sym in pairs:
        result[key] = set_dict[key]
        result[value] = set_dict[value]

    if output:
        with open(output_path, 'w') as writer:
            for k in result.keys():
                line = k + ' ' + ' '.join(list(result[k]))
                print(line)
                writer.write(line + '\n')
        

# legacy function (temporary)
def check_unique(input_path):

    size = unique_entries(input_path, -1)
    print(size)
    return size

all_dict = read_train_file('../data/train.txt')

def _fake_true_with_prop(set_dict, output_path, size=2000, C=0.2):
    """ From analysis only 18.8% of sink nodes in test-files appear as source nodes in
    training data. Here we approximate the proportion as 20% to ensure our training set
    has similar proportion.
    """
        
    keys = list(set_dict.keys())
    length = len(keys)
    result = set()

    i = 0

    while i < size:
        source = keys[randint(0, length - 1)]

        if not set_dict[source]:
            continue

        cands = list(set_dict[source])
        cand_size = len(cands)

        sink = cands[randint(0, cand_size - 1)]

        if (source, sink) in result:
            continue

        if sink in set_dict and len(all_dict[sink]) < 20:
            continue

        result.add((source, sink))
        i += 1

    with open(output_path, 'w') as writer:
        for r in result:
            writer.write(' '.join(r) + ' 1 ' + '\n')


def _fake_false_with_prop(set_dict, sink_dict, output_path, size=2000, C=0.2):
    """ (same as the previous function) From analysis only 18.8% of sink nodes in test-files appear as source nodes in
    training data. Here we approximate the proportion as 20% to ensure our training set
    has similar proportion.
    """

    keys = list(set_dict.keys())
    sinks = list(sink_dict.keys())

    length = len(keys)
    sink_length = len(sinks)
    result = set()

    i = 0

    while i < size:
        source = keys[randint(0, length - 1)]

        if not set_dict[source]:
            continue

        sink = sinks[randint(0, sink_length - 1)]

        if (source, sink) in result or sink in set_dict[source] or source == sink:
            continue
        
        if sink in set_dict and len(all_dict[sink]) < 20:
            continue

        result.add((source, sink))
        i += 1
    
    with open(output_path, 'w') as writer:
        for r in result:
            writer.write(' '.join(r) + ' 0 ' + '\n')
        

def _check_merge_data(input_path, set_dict):
    """ Check if fake data meet our requirement of proportion
    """
    t_k = 0
    f_k = 0

    with open(input_path) as reader:
        for r in reader:
            source, sink, sym = r.split()
            if int(sym):
                if source not in set_dict or sink not in set_dict[source]:
                    print('abnormal!!')
                    break
                if sink in set_dict:
                    t_k += 1
            else:
                if source in set_dict and sink in set_dict[source]:
                    print('abnormal!!')
                    break
                if sink in set_dict:
                    f_k += 1
    
    print(t_k)
    print(f_k)


def _merge_fake_data(true_path, false_path, output_path):
    """ merge true & false fake data
    """
    with open(output_path, 'w') as writer:
        with open(false_path) as reader:
            writer.write(reader.read())
        with open(true_path) as reader:
            writer.write(reader.read())


if __name__ == '__main__':
    true_path = '../output/fakedataprop/true_origin_kim_03.txt'
    false_path = '../output/fakedataprop/false_origin_kim_03.txt'
    final_path = '../output/fakedataprop/fake_origin_kim_03.txt'

    set_dict = read_train_file('../output/outbound_collect_kim.txt')
    sink_dict = read_train_file('../output/inbound_collect_kim.txt')

    _fake_true_with_prop(set_dict, true_path, size=10000)
    _fake_false_with_prop(set_dict, sink_dict, false_path, size=10000)

    _merge_fake_data(true_path=true_path,
                    false_path=false_path,
                    output_path=final_path)
    
    _check_merge_data(final_path, set_dict)