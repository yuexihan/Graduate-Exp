from __future__ import division
from six.moves import xrange
import random
import sys
import math

MAX_LOOP = 100

def norm_2(vector):
    s = sum([x**2 for x in vector])
    return math.sqrt(s)
    
def minus(v1, v2):
    return [x-y for x, y in zip(v1, v2)]
    
def add(v1, v2):
    return [x+y for x, y in zip(v1, v2)]

def k_means(vectors, k):
    assert len(vectors) >= k, 'length less than k'
    k_centers = random.sample(vectors, k)
    k_centers = [center[:] for center in k_centers]
    old_belongs = list(range(len(vectors)))
    
    for i in xrange(MAX_LOOP):
        k_clusters = [[] for _ in range(k)]   
        new_belongs = [0] * len(vectors)
        for v_index, vector in enumerate(vectors):
            min_distance = float('inf')
            min_index = -1
            for c_index, center in enumerate(k_centers):
                distance = norm_2(minus(vector, center))
                if distance < min_distance:
                    min_distance = distance
                    min_index = c_index
            k_clusters[min_index].append(vector)
            new_belongs[v_index] = min_index
        
        if old_belongs == new_belongs:
            break
        old_belongs = new_belongs   
        
        k_centers = []
        for cluster in k_clusters:
            assert len(cluster) > 0, 'encounter an empty cluster'
            center = cluster[0][:]
            for node in cluster[1:]:
                center = add(center, node)
            center = [x/len(cluster) for x in center]
            k_centers.append(center)
            
    return k_clusters
        
        
if __name__ == '__main__':
    print(norm_2([1,2,1]))
    print(add([1,0,0],[0,1,0]))
#    sys.exit()
    vectors = [[1,0,0,],[0,1,0,],[0,0,1,],[0,0,0],[1,0.5,0,],[0,1,0.5,],[0,1,0.5]]
    k = 3
    print(k_means(vectors, k))