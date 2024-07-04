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

pgn_filename = "first_100.pgn"

pgn_file = open(pgn_filename, "r")

next_game = chess.pgn.read_game(pgn_file)

starting = next_game.board()

starting_dict = {}

for piece in range(1,7):
    for booly in [True, False]:
        starting_dict[(piece, booly)] = starting.pieces(piece, booly)

print("Pickled starting positions of all pieces")
with open("Starting.pickle", "wb") as pkl:
    pickle.dump(starting_dict, pkl, pickle.HIGHEST_PROTOCOL)
print("Program run took: " + str(datetime.now() - start))
