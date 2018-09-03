import random
from utils.reader import read_train_file


def _random_pick(cand, count=20):
    if len(cand) <= count * 1.5:
        return cand
    
    cand_list = list(cand)

    length = len(cand)
    result = set()

    while len(result) < count:
        c = cand_list[random.randint(0, length - 1)] 
        if c not in result:
            result.add(c)
    
    return result


def _calc_shortest_path(key, set_dict, max_depth=4):

    source, sink = key

    upbound = _random_pick(set_dict[source] | set_dict[sink])

    def _dfs(node, visited, score, depth):
        
        if depth == max_depth:
            return max_depth

        if node not in set_dict or not set_dict[node]:
            return max_depth

        # hit sink node
        if sink in set_dict[node]:
            return depth + 1

        cands = set_dict[node] & upbound - visited
        if not cands:
            return max_depth

        min_depth = max_depth
        for c in cands:
            min_depth = min(_dfs(c, visited | {node}, score, depth + 1), min_depth)
        
        return min_depth
    
    depth = max_depth

    for s in set_dict[source]:
        if s == sink:
            continue
        depth = min(_dfs(s, {source, sink}, 1, 0), depth)
    
    return depth


def _shortest_path(input_path, output_path, set_dict, is_inbound=False):

    result = []
    count = 0
    with open(input_path) as reader:
        pairs = [r.split() for r in reader.readlines()]

        for p in pairs:
            key = (p[0], p[1])
            if is_inbound:
                score = _calc_shortest_path(key[::-1], set_dict)
            else:
                score = _calc_shortest_path(key, set_dict)

            print(count, score)
            count += 1

            info = key + (str(score), p[-1])
            result.append(info)
        
    with open(output_path, 'w') as writer: 
        for r in result:
            writer.write(' '.join(r) + '\n')


if __name__ == '__main__':

    set_dict = read_train_file('../output/collect.txt')

    print('Read ready')

    _shortest_path('../output/fakedataprop/fake_origin_clm.txt',
            '../output/shortestpath/prop/shortestpath_clm_04.txt',
            set_dict)

    # test
    _shortest_path('../output/test.txt',
            '../output/shortestpath/shortestpath_test_clm_04.txt',
            set_dict)