import sys
import os

import pickle
import re
import itertools
from collections import defaultdict
from datetime import datetime

import chess
import chess.pgn
import chess.svg
from statistics import mean

write_file = open("move_ranking.txt", "w", encoding = "utf-8")

start = datetime.now()

pgn_filename = sys.argv[1]

pgn_file = open(pgn_filename, "r")

count = 1

piece_activity_per_game = []

def find_activity(game):
    value_arr = []
    game_board = game.board()

    if not bool(game.mainline_moves()):
        return []

    for move in game.mainline_moves():
        game_board.push(move)
        if game_board.fullmove_number % 5 == 0:
            board_str = re.sub(r'[\s.]', '', str(game_board))
            game_board.pop()
            wht_act = game_board.pseudo_legal_moves.count()
            game_board.push(move)
            blk_act = game_board.pseudo_legal_moves.count()
            value_arr.append((wht_act, blk_act))

    return value_arr

while True:
    next_game = chess.pgn.read_game(pgn_file)
    if next_game is None:
        break
    if next_game.headers["Variant"] != "Standard":
        write_file.write(str(count) + ": Nonstandard variant skipped\n")
        continue

    activity_arr = find_activity(next_game)

    piece_activity_per_game.append(activity_arr)
    count += 1

print("Pickled five move piece activity data for all games")
with open("testnone.pickle", "wb") as pkl:
    pickle.dump(piece_activity_per_game, pkl, pickle.HIGHEST_PROTOCOL)

print("Program run took: " + str(datetime.now() - start))
