import random
from datetime import datetime

import numpy as np

from clustering_engine import dataset, compute_distance

start = datetime.now()
k=5
count = 0
stable = False
def initialize_centroids(k):
    global stable
    global centroids
    for i in range(k):
        arr = []
        for r in range(random.randint(3,10)):
            arr.append([
                random.betavariate(.75, .75)*2+2,
                random.betavariate(.75, .75)*7+5,
                2-random.betavariate(.75, .75)*(r-2)/5,
                2-random.betavariate(.75, .75)*(r-2)/5,
                random.betavariate(.75, .75) + 1 + r/5,
                random.betavariate(.75, .75) + 1 + r/5
            ])
        centroids.append(arr)
    stable = False
def update(k):
    global start, count
    print("Next round of update after: " + str(datetime.now() - start), flush=True)
    global stable
    global clusters
    global centroids
    print([len(i) for i in centroids], flush=True)
    clusters = [[centroid] for centroid in centroids]
    for point in dataset:
        smallestDistance = compute_distance(centroids[0], point)
        index = 0
        # print("Next point after: " + str(datetime.now() - start), flush=True)
        for i in range(1, k):
            distance = compute_distance(centroids[i], point)
            if distance < smallestDistance:
                smallestDistance = distance
                index = i
        clusters[index].append(point)
    print(str(datetime.now() - start), flush=True)
    new_centroids = []
    for cluster in clusters:
        length = int(min(np.percentile([len(pt) for pt in cluster], 35), 6))
        if length > 6:
            length = 6
        elif length < 3:
            length = 3
        pts = []
        for point in cluster:
            temp = [random.randint(0, len(point) - 1) for l in range(length)]
            pts.append([point[i] for i in sorted(temp)])
        new_centroids.append([[round(sum(x)/len(l),3) for x in zip(*l)] for l in pts])
        print(pts, flush=True)
    if new_centroids == centroids or count > k**2:
        stable = True
    else:
        centroids = new_centroids

initialize_centroids(k)
while not stable:
    update(k)
    count += 1
