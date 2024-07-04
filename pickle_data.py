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

start = datetime.now()

readfile_name = sys.argv[1]

data_file = open(readfile_name, "r")

memeke = []
wht_avg = []
blk_avg = []

line = data_file.readline()

while line:
    if line[:4] == "Game":
        memeke.append(re.search(r'(\w{5}$)', line).group(1))
        white_pawns = data_file.readline()
        white_str = re.search(r'\[(.+?)\]', white_pawns).group(1)
        white_arr = white_str.split(", ")
        wht_avg.append(round(mean([float(x) for x in white_arr]),3))
        black_pawns = data_file.readline()
        black_str = re.search(r'\[(.+?)\]', black_pawns).group(1)
        black_arr = black_str.split(", ")
        blk_avg.append(round(mean([float(x) for x in black_arr]),3))

    line = data_file.readline()

dictionary = {
    'color': memeke,
    'wht': wht_avg,
    'blk': blk_avg
}

with open("pawn_data.pickle", "wb") as pkl:
    pickle.dump(dictionary, pkl, pickle.HIGHEST_PROTOCOL)

print("Pickled pawn data as game average for statistical analysis")
print("Program run took: " + str(datetime.now() - start))
