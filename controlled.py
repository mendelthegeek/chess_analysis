import sys
import os

from collections import *
import math
import re
import itertools
from datetime import datetime

import pickle
import matplotlib.pyplot as plt

import chess
import chess.pgn
import chess.svg
from statistics import mean

start = datetime.now()

pgn_filename = sys.argv[1]

pgn_file = open(pgn_filename, "r")

while True:
    game = chess.pgn.read_game(pgn_file)
    if game is None:
        break

    game_board = game.board()

    count = Counter()

    for move in game.mainline_moves():
        moves = list(game_board.legal_moves)
        squares = [re.match(r'[a-h][1-8]([a-h][1-8])', str(s))[1] for s in moves]
        count[game_board.turn] += len(set(squares))
        game_board.push(move)

print(count)
print("Program run took: " + str(datetime.now() - start))
