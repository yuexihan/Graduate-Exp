from collections import defaultdict
import json

g = open('ieee_category.txt')

category = []
for line in g:
        category.append(line.strip())

print len(category)

nodes = set()
d = defaultdict(set)
for line in open('edges.txt'):
    a, b = line.split()
    a = int(a)
    b = int(b)
    d[a].add(b)
    nodes.add(a)
    nodes.add(b)

j = []
for a in nodes:
    l = {}
    l['id'] = a
    l['allcats'] = category[a]
    l['refs'] = []
    if a in d:
        for b in d[a]:
            l['refs'].append([b, 1])
    j.append(l)

with open('edges.json', 'w') as f:
    json.dump(j, f)