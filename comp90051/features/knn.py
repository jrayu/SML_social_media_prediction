"""
KNN Similarity
"""
import math

def _simple_score(source_neigh, sink_neigh):
    source_out =  1 / math.sqrt(1 + source_neigh[0])
    sink_in =  1 / math.sqrt(1 + sink_neigh[1])
    return source_out + sink_in


def _simple_multi_score(source_neigh, sink_neigh):
    source_out =  1 / math.sqrt(1 + source_neigh[0])
    sink_in =  1 / math.sqrt(1 + sink_neigh[1])
    return source_out * sink_in


def knn_weight(input_path, output_path, set_path):
    count_dict = {}
    with open(set_path) as reader:
        for r in reader:
            index, outbound, inbound = r.split()
            count_dict[index] = (int(outbound), int(inbound))

    with open(input_path) as reader:
        with open(output_path, 'w') as writer:
            for r in reader:
                source, sink, cls = r.split()
                source_neigh = count_dict[source]
                sink_neigh = count_dict[sink]
                score = _simple_multi_score(source_neigh, sink_neigh)

                result = (source, sink, str(score), cls)
                writer.write(' '.join(result) + '\n')
                

if __name__ == '__main__':
    knn_weight('../output/fake_data.txt',
            '../output/knn/knn.txt',
            '../output/set_count.txt')
