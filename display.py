

# between_mean = 0.0
# within_mean = 0.0
# ref_mean = 0.0
# noref_mean = 0.0
# precisions = 0.0
# for line in open('metric.md'):
#     if line.startswith('between_mean'):
#         between_mean = float(line.split()[-1])
#     elif line.startswith('within_mean'):
#         within_mean = float(line.split()[-1])
#     elif line.startswith('ref_mean'):
#         ref_mean = float(line.split()[-1])
#     elif line.startswith('noref_mean'):
#         noref_mean = float(line.split()[-1])
#     elif line.startswith('precisions'):
#         precisions = float(line.split()[-1])
#         print '%s & %s & %s' % (between_mean/within_mean, noref_mean/ref_mean, precisions)

f = open('metric.md')
metric_label = 0.0
metric_category = 0.0
knn_label = 0.0
knn_category = 0.0
while True:
    line = f.readline()
    if line.startswith('--metric label'):
        between_mean = float(f.readline().split()[-1])
        f.readline()
        within_mean = float(f.readline().split()[-1])
        f.readline()
        metric_label = between_mean / within_mean
    elif line.startswith('--metric category'):
        between_mean = float(f.readline().split()[-1])
        f.readline()
        within_mean = float(f.readline().split()[-1])
        f.readline()
        metric_category = between_mean / within_mean
    elif line.startswith('--knn label'):
        knn_label = float(f.readline().split()[-1])
    elif line.startswith('--knn category'):
        knn_category = float(f.readline().split()[-1])
        print ' & %.4f & %.4f & %.4f & %.4f' % (metric_label, metric_category, knn_label, knn_category)
