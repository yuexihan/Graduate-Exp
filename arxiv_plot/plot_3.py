import csv
import json

fin = open('arxivVector.txt', 'rb')
reader = csv.reader(fin)
print reader.next()

category_index = {
	'Quantitative Finance': 0,
	'Quantitative Biology': 1,
	'Statistics': 2,
	'Computer Science': 3,
	'Mathematics': 4,
	'Physics': 5
}
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
# fig = plt.figure()
# # ax = Axes3D(fig)
# ax = fig.add_subplot(111, projection='3d')

# color = 'bgrcmy'
plot_only =100000

from mayavi import mlab

x = []
y = []
z = []
s = []

for i in xrange(plot_only):
	paperid, vector, category = reader.next()
	vector = json.loads(vector)
	category = int(category)
	# while category != i%6:
	# 	paperid, vector, category = reader.next()
	# 	vector = json.loads(vector)
	# 	category = int(category)
	x.append(vector[0])
	y.append(vector[1])
	z.append(vector[2])
	s.append(2.0/(category+100))

mlab.points3d(x, y, z, s, scale_factor=1)
mlab.show()