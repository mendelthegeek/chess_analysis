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

write_file = open("chess_test.txt", "w", encoding = "utf-8")

start = datetime.now()

pgn_filename = sys.argv[1]

pgn_file = open(pgn_filename, "r")

count = 1

pawn_position_data = []

def find_pawn_pos(game):
    track_pawn_pos = []
    game_board = game.board()

    if not bool(game.mainline_moves()):
        return []

    for move in game.mainline_moves():
        game_board.push(move)
        if game_board.fullmove_number % 5 == 0:

            white_pawns = str(game_board.pieces(chess.PAWN, chess.WHITE))
            wht_pawn_pos = white_pawns.split('\n')
            wht_pos_list = {}
            wht_row_num = 8

            for row in wht_pawn_pos:
                temp = [i.start() for i in re.finditer('1', row)]
                wht_pos_list[wht_row_num] = [int(n/2+1) for n in temp]
                wht_row_num -= 1

            black_pawns = str(game_board.pieces(chess.PAWN, chess.BLACK))
            blk_pawn_pos = black_pawns.split('\n')
            blk_pos_list = {}
            blk_row_num = 8

            for row in blk_pawn_pos:
                temp = [i.start() for i in re.finditer('1', row)]
                blk_pos_list[blk_row_num] = [int(n/2+1) for n in temp]
                blk_row_num -= 1

            move_no = game_board.fullmove_number
            wht_weighted_sum = sum([key*len(val) for key, val in wht_pos_list.items()])
            wht_pwn_ct = str(game_board).count("P")
            if wht_pwn_ct > 0:
                wht_pwn_avg = wht_weighted_sum/wht_pwn_ct
            else:
                wht_pwn_avg = 0
            blk_weighted_sum = sum(key*len(val) for key, val in blk_pos_list.items())
            blk_pwn_ct = str(game_board).count("p")
            if blk_pwn_ct > 0:
                blk_pwn_avg = blk_weighted_sum/blk_pwn_ct
            else:
                blk_pwn_avg = 0
            track_pawn_pos.append((round(wht_pwn_avg, 3), round(blk_pwn_avg, 3)))

    return track_pawn_pos

while True:
    next_game = chess.pgn.read_game(pgn_file)
    if next_game is None:
        break
    if next_game.headers["Variant"] != "Standard":
        continue
    avg_pawn_pos = find_pawn_pos(next_game)
    pawn_position_data.append(avg_pawn_pos)
    count += 1

print("Pickled five move aggregated pawn position data")
with open("pawn_position.pickle", "wb") as pkl:
    pickle.dump(pawn_position_data, pkl, pickle.HIGHEST_PROTOCOL)
# print(pawn_position_data)
print("Program run took: " + str(datetime.now() - start))
