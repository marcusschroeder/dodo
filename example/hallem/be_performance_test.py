"""
Performance Test for Backward Elimination.

In this performance setup, the time and score of BE is tracked for different
number of data and features.
The goal is to analyse which of the two parameters has a bigger impact on
the running time and to compare that to gurobi.
"""
import time
import csv

import numpy as np

from example.hallem import sample_generator
from _core.featureselection import backward_elimination
from example.hallem.data import Hallem

size_data = [8, 16, 32, 64, 128]
size_feat = [8, 16, 32, 64, 128]
times = np.zeros((len(size_data), len(size_feat)))
scores = np.zeros((len(size_data), len(size_feat)))

rounds = 5


def write_csv(f, matrix):
    x = np.column_stack((np.transpose(size_data), matrix))
    v = np.hstack(["Size", size_feat])

    with open(f, 'wb') as ff:
        writer = csv.writer(ff, delimiter=";")
        writer.writerow(v)
        writer.writerows(x)


for k in range(1, rounds + 1):
    for i, v_i in enumerate(size_data):
        for j, v_j in enumerate(size_feat):
            d = sample_generator.generate_random_data(v_i, v_j)

            start = time.time()
            feature_list, score = backward_elimination(d, 4)
            stop = time.time()

            delta = stop - start
            times[i, j] += delta
            scores[i, j] += score
            print "Round %s, data: %s, features: %s, time: %s" \
                  % (k, v_i, v_j, round(delta, 4))

            write_csv("../results/be_times_pew.csv", times / k)
            write_csv("../results/be_scores_pew.csv", scores / k)