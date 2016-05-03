from collections import Counter
import math


def conv(v):
    if v.isdigit():
        return float(v)
    else:
        return v


def parse_file(filename):
    from csv import reader
    f = open(filename, 'r')
    r = reader(f)

    attrs = None
    data = []

    # get headers (if enabled)
    attrs = r.next()

    # get data
    for row in r:
        vals = map(conv, row)
        record = dict(list(zip(attrs, vals)))
        data.append(record)

    return attrs, data


def entropy(data, target):
    c = Counter([record[target] for record in data])
    total = float(len(data))
    return - sum(count / total * math.log(count / total, 2) for count in
                 c.values())


def gain(data, attr, target):
    d = [_[attr] for _ in data]
    total = float(len(d))
    c = Counter(d)
    e = 0.0

    for k, v in c.iteritems():
        p = v / total
        subset = [r for r in data if r[attr] == k]
        e += p * entropy(subset, target)

    return (entropy(data, target) - e)


def uniques(lst):
    return list(set(lst))


def most_frequent(lst):
    return Counter(lst).most_common(1)[0][0]


def predominant_value(data, target):
    return most_frequent([record[target] for record in data])


def get_values(data, target):
    return uniques([record[target] for record in data])


def create_tree(data, attrs, target, prune=False):
    data = data[:]
    vals = [record[target] for record in data]
    default = predominant_value(data, target)

    if not data or (len(attrs) - 1) <= 0:
        return default
    elif vals.count(vals[0]) == len(vals):
        return vals[0]
    else:
        best = choose_best_attribute(data, attrs, target)

    tree = {best: {}}

    for v in get_values(data, best):
        sub = create_tree(
                get_samples(data, best, v),
                [attr for attr in attrs if attr != best],
                target)
        tree[best][v] = sub

    return tree


def choose_best_attribute(data, attrs, target):
    best_gain = 0.0
    best_attr = None

    for attr in attrs:
        attr_gain = gain(data, attr, target)
        if gain >= best_gain and attr != target:
            best_gain = attr_gain
            best_attr = attr

    return best_attr


def get_samples(data, attr, value):
    results = []

    if not data:
        return results
    else:
        for record in data:
            if record[attr] == value:
                results.append(record)

        return results


def get_classification(record, tree):
    if isinstance(tree, str) or isinstance(tree, float):
        return tree
    else:
        attr = list(tree.keys())[0]
        t = tree[attr][record[attr]]
        return get_classification(record, t)


def classify(tree, data):
    classifications = []

    for record in data:
        classifications.append(get_classification(record, tree))

    return classifications


def print_tree(tree, depth=0):
    if depth == 0:
        print list(tree.keys())[0], 'is starting attribute (root):'
        depth += 1
    if isinstance(tree, dict):
        for item in list(tree.values())[0].keys():
            if not isinstance(list(tree.values())[0][item], dict):
                print '\t' * depth + "If %s == %s then" % (list(tree.keys())[0], item),
            else:
                print '\t' * depth + 'If %s == %s and' % (list(tree.keys())[0], item)
            print_tree(list(tree.values())[0][item], depth + 1)
    else:
        print 'it is class %s' % tree
