import numpy as np
import os
import pickle


with open(os.path.join('last_data', 'data.pkl'), 'rb') as f:
    d = pickle.load(f)

for e in d:
    print(e[0].shape, e[1])
