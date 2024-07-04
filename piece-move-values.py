import sys
import os

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

move_dict = defaultdict(float)

while True:
    next_game = chess.pgn.read_game(pgn_file)
    if next_game is None:
        break
    if next_game.headers["Variant"] != "Standard":
        write_file.write("Nonstandard variant skipped\n")
        continue

    pgn_text = str(next_game.mainline_moves())
    if not(bool(next_game.mainline_moves())):
        continue

    if next_game.headers["Result"] == "1/2-1/2":
        continue

    if next_game.headers["Result"] == "1-0":
        factor = 1
    elif next_game.headers["Result"] == "0-1":
        factor = -1

    pgn_temp = [re.sub(r'[+#]', '', move) for move in pgn_text.split(' ')]
    pgn_arr = [move[-2:] for move in pgn_temp]
    white_moves = pgn_arr[1::3]
    black_moves = pgn_arr[2::3]
    for move in white_moves:
        if 'x' in move:
            move_dict[move] += .03 * factor
        move_dict[move] += .01 * factor
    for move in black_moves:
        if 'x' in move:
            move_dict[move] -= .03 * factor
        move_dict[move] -= .01 * factor

    count += 1

print("Analyzed best and worst squares to move to")
winning = sorted(move_dict, key=move_dict.get, reverse=True)[:8]
print("Best squares w/ values: " + str({k: round(move_dict[k],3) for k in winning}))
losing = sorted(move_dict, key=move_dict.get)[:8]
print("Worst squares w/ values: " + str({k: round(move_dict[k],3) for k in losing}))
print("Program run took: " + str(datetime.now() - start))
