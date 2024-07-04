import sys

import random
from datetime import datetime

import chess
import chess.pgn

trials = int(sys.argv[1])

start = datetime.now()

games = ""

for _ in range(trials):
    board = chess.Board()
    while board.result() == '*':
        move = random.choice(list(board.legal_moves))
        board.push(move)
    game = board.move_stack
    new_board = chess.Board()
    games += new_board.variation_san(game) + "\n\n"

with open("random_games.pgn", "a+") as f:
    f.write(games)

print("Program run took: " + str(datetime.now() - start))

# results = Counter()
# length = Counter()

#     results[board.result()] += 1
#     length[board.fullmove_number] += 1

# total = sum([key*val for key, val in length.items()])

# print("Longest game: " + str(max(length.keys())))
# print("Game result: " + str(results))
# print("Average length: " + str(total/trials))
