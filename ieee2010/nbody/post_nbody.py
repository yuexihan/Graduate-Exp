import json
import csv

l = json.load(open('map-387667.json'))

d = {}
with open('ieee_vector_nbody.txt','w') as f:
    for i, (j, x, y, r) in enumerate(l):
        f.write(str(x) + ' ' + str(y) + '\n')
        d[j] = i

with open('ieee_reference.csv', 'rb') as fin:
    with open('ieee_reference_nbody.csv', 'wb') as fout:
        fout.write(fin.readline())
        reader = csv.reader(fin)
        writer = csv.writer(fout)
        for i, j in reader:
            i = int(i)
            j = int(j)
            i = d[i]
            j = d[j]
            writer.writerow([i, j])
