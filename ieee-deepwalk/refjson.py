from collections import defaultdict
import json

category = []
for line in open('ieee_category.txt'):
        category.append(line.strip())

print len(category)

# nodes = set()
# d = defaultdict(set)
# for line in open('edges.txt'):
#     a, b = line.split()
#     a = int(a)
#     b = int(b)
#     d[a].add(b)
#     nodes.add(a)
#     nodes.add(b)
#
# j = []
# for a in nodes:
#     l = {}
#     l['id'] = a
#     l['allcats'] = category[a]
#     l['refs'] = []
#     if a in d:
#         for b in d[a]:
#             l['refs'].append([b, 1])
#     j.append(l)

nodes = set()
links = set()
for line in open('edges.txt'):
    a, b = line.split()
    a = int(a)
    b = int(b)
    nodes.add(a)
    nodes.add(b)
    links.add((a,b))

j = []
for a in nodes:
    l = {'id': a, 'allcats': '', 'ref': []}
    j.append(l)
for a,b in links:
    l = {'id': a, 'ref': [(b, 1)], 'allcats': ''}
    j.append(l)

with open('edges.json', 'w') as f:
    json.dump(j, f)