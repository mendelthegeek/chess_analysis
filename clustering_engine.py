import sys
import os

import logging
import pickle
import re
import itertools
from datetime import datetime
import random

import numpy as np
import chess
import chess.pgn
import chess.svg
from statistics import mean

write_file = open("chess_test.txt", "w", encoding = "utf-8")

prev_time = start = datetime.now()

logging.basicConfig(handlers=[logging.FileHandler('logs.log', 'w', 'utf-8')],
        level=logging.ERROR,
        format='%(asctime)s:%(message)s')

k = int(sys.argv[1])
centroids = []

stable = True

count = 0

dataset = []

test = []

clusters = []

pickles = ['material_data', 'activity_data']

for pckl in pickles:
    with open(pckl+".pickle", "rb") as pkl:
        test.append(pickle.load(pkl)[:50])
test = [[[(pair[0]/20, pair[1]/20) for pair in game] for game in type] for type in test]
with open("pawn_position.pickle", "rb") as pkl:
    test.append(pickle.load(pkl)[:50])

# print("test")
# print(test)

dataset = [
    [
        [ent for tpl in move for ent in tpl]
        for move in zip(*game)
    ] for game in zip(*test)
]

# print("dataset")
# print(dataset)

# sys.exit()

#divide material by 20, moves by 10
#eventually make dynamic
def compute_distance(a, b):
    logging.debug("entered compute")
    def gen_tuples(n_rows, n_cols):
        row = col = 0
        while row <= n_rows and col <= n_cols:
            for i in range(row, n_rows + 1):
                yield (i, col)

            for j in range(col + 1, n_cols + 1):
                yield (row, j)

            row += 1
            col += 1

    def find_prev(i, j):
        prev = []
        if i > 0:
            prev.append(DTW_mat[i - 1][j])
        if j > 0:
            prev.append(DTW_mat[i][j - 1])
            if i > 0:
                prev.append(DTW_mat[i - 1][j - 1])
        logging.debug("found prev of " + str((i, j)) + " to be " + str(prev))
        return prev

    def point_distance(point_a, point_b):
        p_dist = 0
        for i in range(len(point_a)):
            p_dist += (point_a[i] - point_b[i])**2
        logging.debug("Computed distance as: " + str(p_dist))
        return p_dist

    distance = 0
    ##### memeke color
    ##### castled
    ##### result

    #compute DTW path
    # a, b = a[3:], b[3:]
    DTW_mat = np.zeros((len(a), len(b)))

    for i,j in gen_tuples(len(a) - 1, len(b) - 1):
        prev = find_prev(i, j)
        DTW_mat[i][j] = point_distance(a[i], b[j]) + min(prev, default=0)
        logging.debug("DTW state is: " + str(DTW_mat))

    #work backwards to find total distance
    while i+j > 0:
        prev = find_prev(i, j)
        prev_min = min(prev)
        if i > 0 and DTW_mat[i - 1][j] == prev_min:
            i -= 1
        elif j > 0 and DTW_mat[i][j - 1] == prev_min:
            j -= 1
        else:
            i -= 1
            j -= 1
        distance += prev_min
        logging.debug("Curr dist: " + str(distance) + ", iter: " + str((i, j)))
    return distance

def initialize_centroids(k):
    global stable
    global centroids
    centroids = random.sample(dataset, k)
    stable = False

def update():
    global prev_time
    print("Next round of update after: " + str(datetime.now() - prev_time), flush=True)
    prev_time = datetime.now()
    global stable
    global clusters
    global centroids
    print([len(i) for i in centroids], flush=True)
    clusters = [[centroid] for centroid in centroids]
    for point in dataset:
        smallestDistance = compute_distance(centroids[0], point)
        index = 0
        print("Next point after: " + str(datetime.now() - prev_time), flush=True)
        prev_time = datetime.now()
        for i in range(1, k):
            distance = compute_distance(centroids[i], point)
            if distance < smallestDistance:
                smallestDistance = distance
                index = i
        clusters[index].append(point)
    print("Ready to compute centeroids after: " + str(datetime.now() - prev_time), flush=True)
    prev_time = datetime.now()
    new_centroids = []
    for cluster in clusters:
        length = 7
        pts = []
        for point in cluster:
            temp = [random.randint(0, len(point) - 1) for l in range(length)]
            pts.append([point[i] for i in sorted(temp)])
        new_centroids.append([[round(sum(x)/len(l),3) for x in zip(*l)] for l in pts])
    newer_centroids = []
    for i in range(len(new_centroids)):
        least_dist = compute_distance(clusters[i][0], new_centroids[i])
        pointy = clusters[i][0]
        for pt in clusters[i]:
            distance = compute_distance(pt, new_centroids[i])
            if distance < least_dist:
                least_dist = distance
                pointy = pt
        newer_centroids.append(pointy)
    if newer_centroids == centroids or count > 10:
        stable = True
    else:
        centroids = newer_centroids

initialize_centroids(k)
while not stable:
    print("Time since start: " + str(datetime.now() - start), flush=True)
    update()
    count += 1


cluster_by_num = [[dataset.index(game) for game in cluster[1:]] for cluster in clusters]
print("Tested clustering {} games into {} clusters using DTW-kmeans".format(len(dataset),k))
print("Clustered games as follows" + str(cluster_by_num))
print("Program run took: " + str(datetime.now() - start))

