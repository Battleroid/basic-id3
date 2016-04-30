from id3 import parse_file, create_tree, classify, print_tree
from random import shuffle
import sys

if len(sys.argv) < 3:
    print 'Not enough arguments'
    sys.exit(1)

# load
attrs, data = parse_file(sys.argv[1])
label = attrs[0]   # get record name
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
print 'Testing sampled records ...'
good = 0.0
bads = []
for s in tests:
    try:
        r = classify(tree, [s])[0]
        rx = s[sys.argv[2]]
        valid = '[!]' if r != rx else ''
        print '{:4}'.format(s[label]), 'classified as:', r, 'actually is', rx, valid
        if r == rx:
            good += 1.0
    except KeyError:
        bads.append(s[label])
        pass

print '--'
print 'Could not classify the following:', ', '.join(bads)
print 'Total accuracy: {:.2f}%, {}/{}'.format(100 * good/len(tests), int(good), len(tests))
