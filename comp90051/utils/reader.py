""" transform txt source file to [key: [list]]
"""

def transform(input_path):
    result = {}
    with open(input_path) as reader:
        for line in reader:
            ids = line.split()
            result[ids[0]] = set(ids[1:])
    return result
