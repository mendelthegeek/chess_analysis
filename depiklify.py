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
    listy = pickle.load(pkl)
print(listy)
print(mean(listy))
