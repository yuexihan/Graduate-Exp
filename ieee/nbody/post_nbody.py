import json
import csv

l = json.load(open('map-071684.json'))

categories = []
for line in open('ieee_category.txt'):
    categories.append(line)

d = {}
with open('ieee_label_nbody.txt', 'w') as f1:
    with open('ieee_vector_nbody.txt','w') as f2:
        for i, (j, x, y, r) in enumerate(l):
            f1.write(categories[j])
            f2.write(str(x) + ' ' + str(y) + '\n')
            d[j] = i

with open('ieee_reference.csv', 'rb') as fin:
    with open('ieee_reference_nbody.csv', 'wb') as fout:
        fout.write(fin.readline())
        reader = csv.reader(fin)
        writer = csv.writer(fout)
        for i, j in reader:
            i = int(i)
            j = int(j)
            if i in d and j in d:
                i = d[i]
                j = d[j]
                writer.writerow([i, j])
