import pickle

pickles = ['material_data', 'activity_data', 'pawn_position']

for pckl in pickles:
    with open(pckl+".pickle", "rb") as pkl1:
        better = [arr for arr in pickle.load(pkl1) if arr != []]
    with open(pckl+".pickle", "wb") as pkl2:
        pickle.dump(better, pkl2, pickle.HIGHEST_PROTOCOL)
