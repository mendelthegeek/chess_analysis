import sys
import os

import pickle
import re
import itertools
from datetime import datetime

import chess
import chess.pgn
import chess.svg
from statistics import mean
from matplotlib import pyplot as plt

start = datetime.now()

readpickle_name = sys.argv[1] + ".pickle"

with open(readpickle_name, "rb") as pkl:
    dictionary = pickle.load(pkl)
wht = dictionary["wht"]
blk = dictionary["blk"]
mmk = dictionary["color"]

mmk_wht = [(wht[i], blk[i]) for i in range(len(mmk)) if mmk[i] == "White"]
mmk_blk = [(wht[i], blk[i]) for i in range(len(mmk)) if mmk[i] == "Black"]


f, axes = plt.subplots(ncols = 3)
axes[0].scatter(*zip(*mmk_wht))
axes[1].scatter(*zip(*mmk_blk))
axes[2].scatter(wht, blk)

print(max(wht))
print(min(blk))
print(len([pos for pos in blk if pos < 5.5]))
print(len([pos for pos in wht if pos > 3.5]))
print("Program run took: " + str(datetime.now() - start))
plt.show()
