#!/usr/bin/env python
"""
The setup is: Gurobi has the time of BE and must beat its score in that time
"""
# encoding: utf-8
import time
import csv

import numpy as np

from example.dorsal_door import DoOR


def write_csv(f, x):
    with open(f, 'wb') as ff:
        writer = csv.writer(ff, delimiter=";")
        writer.writerows(x)


door = DoOR()
data, ors, odorants = door.get_dorsal_data()

features = np.arange(2, 100)
times = np.zeros((len(features), 4))

matrix = []
for i, x in enumerate(data):
    for j in range(i + 1, len(data)):
        matrix.append(np.power(data[i] - data[j], 2))

matrix = np.asarray(matrix)
try:
    # Create a new model
    m = Model("mip1")

    # Create variables
    for i in range(data.shape[1]):
        m.addVar(vtype=GRB.BINARY, name="x" + str(i))

    z = m.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=GRB.INFINITY, name="z")

    m.update()

    vars = m.getVars()


    # Set constraints
    odorants_exp = LinExpr()
    for v in vars[:-1]:
        odorants_exp += v

    for row in matrix:
        row_exp = LinExpr()
        for i in range(len(row)):
            row_exp += row[i] * vars[i]

        row_exp += -1 * z
        m.addConstr(row_exp, GRB.GREATER_EQUAL, 0)

    # Set objective
    m.setObjective(z, GRB.MAXIMIZE)

    for ii, vv in enumerate(features):
        print vv
        number_features = float(vv)
        if ii > 0:
            m.remove(m.getConstrs()[-1])

        m.addConstr(odorants_exp, GRB.EQUAL, number_features)

        m.update()

        start = time.time()
        m.optimize()
        stop = time.time()

        x = []
        for v in m.getVars():
            x.append(v.x)
        times[ii, 0] = vv
        times[ii, 1] = stop - start
        times[ii, 2] = np.sqrt(m.objVal)
        #times[ii, 3] = np.array_str(np.where(np.asarray(x) == 1.0)[0])


        write_csv("results/g_features_door.csv", times)
except GurobiError:
    print 'Error reported'