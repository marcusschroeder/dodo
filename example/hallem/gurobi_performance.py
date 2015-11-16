#!/usr/bin/env python
"""
The setup is: Gurobi has the time of BE and must beat its score in that time
"""
# encoding: utf-8
import time
import csv

import numpy as np

from example.hallem import sample_generator

np.set_printoptions(suppress=True, precision=2)
solution_counter = 0


def set_counter(time):
    solution_counter = time


def write_csv(f, matrix):
    x = np.column_stack((np.transpose(size_data), matrix))
    v = np.hstack(["Size", size_feat])

    with open(f, 'wb') as ff:
        writer = csv.writer(ff, delimiter=";")
        writer.writerow(v)
        writer.writerows(x)

# whenever the solution could not be improved for 30seconds, then stop
# searching
def callback(model, where):
    if where == GRB.Callback.MIPSOL:
        set_counter(model.cbGet(GRB.Callback.RUNTIME))
    elif where == GRB.Callback.MIP:
        if model.cbGet(GRB.Callback.RUNTIME) - solution_counter > 30:
            print "JUMPED"
            model.terminate()


def load_csv(file):
    path_to_csv = os.path.join(os.path.dirname(__file__), file)
    d = []
    with open(path_to_csv) as csvfile:
        reader = csv.reader(csvfile, delimiter=';')

        for row in reader:
            d.append(row)

    d = np.asarray(d)
    return np.asarray(d[1:, 1:], dtype=float)


size_data = np.array([8, 16, 32, 64, 128])
size_feat = np.array([8, 16, 32, 64, 128])

times = np.zeros((len(size_data), len(size_feat)))
sol = np.zeros((len(size_data), len(size_feat)))
creation_time = np.zeros((len(size_data), len(size_feat)))

be_times = load_csv("../results/be_times.csv")


## five rounds of benchmarking, results will be average
rounds = 5

for kk in range(1, rounds + 1):
    for ii, v_i in enumerate(size_data):
        for jj, v_j in enumerate(size_feat):
            data = sample_generator.generate_random_data(v_i, v_j)

            matrix = []
            for i, x in enumerate(data):
                for j in range(i + 1, len(data)):
                    matrix.append(np.power(data[i] - data[j], 2))

            matrix = np.asarray(matrix)
            number_features = 4

            try:
                start = time.time()
                # Create a new model
                m = Model("mip1")

                # Create variables
                for i in range(data.shape[1]):
                    m.addVar(vtype=GRB.BINARY, name="x" + str(i))

                z = m.addVar(vtype=GRB.INTEGER, lb=0, ub=GRB.INFINITY,
                             name="z")

                m.update()

                vars = m.getVars()


                # Set constraints
                odorants_exp = LinExpr()
                for v in vars[:-1]:
                    odorants_exp += v

                m.addConstr(odorants_exp, GRB.EQUAL, number_features)
                for row in matrix:
                    row_exp = LinExpr()
                    for i in range(len(row)):
                        row_exp += row[i] * vars[i]

                    row_exp += -1 * z
                    m.addConstr(row_exp, GRB.GREATER_EQUAL, 0)

                print v_i, v_j, kk, be_times[ii, jj]
                # Set objective
                m.setObjective(z, GRB.MAXIMIZE)
                #m.params.TimeLimit = 3*be_times[ii, jj]
                m.update()

                stop = time.time()
                creation_time[ii, jj] += stop - start

                start = time.time()
                solution_counter = 0
                #m.optimize(callback)
                m.optimize()
                stop = time.time()
                times[ii, jj] += stop - start
                sol[ii, jj] += m.objVal

                write_csv("results/g_times_gauss_be_l_" + str(
                    number_features) + ".csv", times / kk)
                write_csv("results/g_create_gauss_be_l_" + str(
                    number_features) + ".csv", creation_time / kk)
                write_csv("results/g_scores_gauss_be_l_" + str(
                    number_features) + ".csv", np.sqrt(sol / kk))
            except GurobiError:
                print 'Error reported'


