from id3 import parse_file, create_tree, classify, print_tree
from random import shuffle
import sys

if len(sys.argv) < 3:
    print 'Not enough arguments'
    sys.exit(1)

# load
attrs, data = parse_file(sys.argv[1])
attrs = attrs[1:]  # exclude record name

# grab about 20% of our records to test
tests = []
shuffle(data)
for _ in range(int(len(data) * 0.2)):
    tests.append(data.pop())

# create tree sample
tree = create_tree(data, attrs, sys.argv[2])

# print tree
print_tree(tree)

# test classification
for s in tests:
    try:
        r = classify(tree, [s])[0]
        rx = s[sys.argv[2]]
        valid = '[!]' if r != rx else ''
        print s['Record#'], 'classified as:', r, 'actually is', rx, valid
    except KeyError:
        # unfortunately some records' values might not be a part of the tree
        # so silently error out if a KeyError occurs
        pass
