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

piece_val_per_game = []

wht_piece_value = {
    'p': 1,
    'b': 3,
    'n': 3,
    'r': 5,
    'q': 9
}

blk_piece_value = {
    'P': 1,
    'B': 3,
    'N': 3,
    'R': 5,
    'Q': 9
}

def count_material(game):
    value_arr = []
    game_board = game.board()

    if not bool(game.mainline_moves()):
        return []

    for move in game.mainline_moves():
        game_board.push(move)
        if game_board.fullmove_number % 5 == 0:
            board_str = re.sub(r'[\s.]', '', str(game_board))
            wht_val, blk_val = 0, 0
            for piece in board_str:
                if piece in wht_piece_value:
                    wht_val += wht_piece_value[piece]
                if piece in blk_piece_value:
                    blk_val += blk_piece_value[piece]
            value_arr.append((wht_val, blk_val))

    return value_arr

while True:
    next_game = chess.pgn.read_game(pgn_file)
    if next_game is None:
        break
    if next_game.headers["Variant"] != "Standard":
        write_file.write("Nonstandard variant skipped\n")
        continue

    material_arr = count_material(next_game)

    piece_val_per_game.append(material_arr)
    count += 1

print("Pickled five move material data for all games")
with open("material_data.pickle", "wb") as pkl:
    pickle.dump(piece_val_per_game, pkl, pickle.HIGHEST_PROTOCOL)

print("Program run took: " + str(datetime.now() - start))
