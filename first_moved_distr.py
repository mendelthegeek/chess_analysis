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

write_file = open("chess_test.txt", "w", encoding = "utf-8")

start = datetime.now()

pgn_filename = sys.argv[1]

pgn_file = open(pgn_filename, "r")

count = 1

firsts = []

final_dict = defaultdict(lambda: defaultdict(lambda: Counter()))

piece_dict = {
    1: "Pawn",
    2: "Knight",
    3: "Bishop",
    4: "Rook",
    5: "Queen",
    6: "King"
}

with open("Starting.pickle", "rb") as pkl:
    start_dict = pickle.load(pkl)

def find_first_moves(game):
    track_pawn_pos = []
    game_board = game.board()
    result = {}
    start_dict_copy = start_dict.copy()

    if not bool(game.mainline_moves()):
        return result

    start = ""
    for move in game.mainline_moves():
        game_board.push(move)
        remove_these = []
        for key, val in start_dict_copy.items():
            if game_board.pieces(*key) != val:
                result[key] = game_board.fullmove_number
                remove_these.append(key)
        for key in remove_these:
            del start_dict_copy[key]

    return result

while True:
    next_game = chess.pgn.read_game(pgn_file)
    if next_game is None:
        break
    if next_game.headers["Variant"] != "Standard":
        continue
    first_moves = find_first_moves(next_game)
    first_moves['result'] = next_game.headers["Result"]
    firsts.append(first_moves)
    count += 1

# print(firsts[0])

for game in firsts:
    if game['result'] == "1/2-1/2":
        result = {True: "D", False: "D"}
    elif game['result'] == "1-0":
        result = {True: "W", False: "L"}
    elif game['result'] == "0-1":
        result = {True: "L", False: "W"}
    del game['result']
    for k, v in game.items():
        final_dict[k[0]][v][result[k[1]]] += 1

# print("Pickled first bishop move by white")
# with open("1st_moved.pickle", "wb") as pkl:
#     pickle.dump(firsts, pkl, pickle.HIGHEST_PROTOCOL)

fig = plt.figure()

for piece, dictionary in final_dict.items():
    highest = max(dictionary)
    plt.subplot(3, 2, piece)
    Wins = [dictionary[move]["W"] for move in range(1, highest+1)]
    Losses = [dictionary[move]["L"] for move in range(1, highest+1)]
    Sum = [Wins[i] + Losses[i] for i in range(len(Wins))]
    Draws = [dictionary[move]["D"] for move in range(1, highest+1)]
    print(Wins, Losses, flush=True)
    w = plt.bar(dictionary.keys(), Wins, 10/highest)
    l = plt.bar(dictionary.keys(), Losses, 10/highest, bottom=Wins)
    d = plt.bar(dictionary.keys(), Draws, 10 /highest, bottom=Sum)
plt.show()

print(final_dict)

print("Program run took: " + str(datetime.now() - start))
















