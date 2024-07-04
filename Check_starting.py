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

pgn_filename = "first_100.pgn"

pgn_file = open(pgn_filename, "r")

next_game = chess.pgn.read_game(pgn_file)

starting = next_game.board()

for key, val in dictionary.items():
    print(starting.pieces(*key))


