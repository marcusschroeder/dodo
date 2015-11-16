#!/usr/bin/env python
# encoding: utf-8
import sys

sys.path.append("/Library/Python/2.7/site-packages/gurobipy")
# must be system python
from gurobipy import *
import numpy as np
import pickle


def optimize(data,
             number_features=10,
             batch=False,
             cluster=None,
             path=None):
    '''
    Finds the optimal set of odorants with set size number_features with integer
    optimization (IP).

    Args:
        data (numpy.array):
            The olfactory data matrix. x-dimension: receptors,
            y-dimension: odorants.
        number_features (int):
            Optimize the distance for/up to the given number of features.
        batch (bool):
            (default=False) If false, only a single set of optimal odorants is
            computed. This set has the size given in number_features.
            If true, it computes optimal features sets from size one
            to number_features.
        cluster (list):
            (default=None) If you want to optimize the distance between some
            receptors against the rest, you have to specify this value .
        path (str):
            If specified, the results are dumped in a pickle file at the given
            location. To read the file call numpy.load().

    Returns:
        features (numpy.array):
            An array of arrays, where each array contains the indices of the
            selected features.
        scores (numpy.array):
            List of scores for different sizes of features.
            Higher scores are better.
    '''

    print "Number of data points:", data.shape[0]
    print "Number of features:", data.shape[1]
    if cluster != None:
        print "Cluster:", cluster

    matrix = []
    for i in range(len(data)):
        for j in range(len(data)):
            if cluster != None:
                if j not in cluster and i in cluster:
                    matrix.append(np.power(data[i] - data[j], 2))
            else:
                if j > i:
                    matrix.append(np.power(data[i] - data[j], 2))

    matrix = np.asarray(matrix)

    print "#Constraints: ", matrix.shape[0]

    scores = []
    features = []
    # Create a new model
    m = Model("mip1")
    m.params.OutputFlag = 0 #0=silent mode, 1= verbose

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

    lower_bound = number_features

    if batch:
        lower_bound = 1

    for i, nf in enumerate(range(lower_bound, number_features + 1)):

        print "##### Computing %s features" % nf
        if i > 0:
            m.remove(m.getConstrs()[-1])

        m.addConstr(odorants_exp, GRB.EQUAL, nf)
        m.update()
        m.optimize()

        x = []
        for v in m.getVars():
            x.append(v.x)

        scores.append(np.sqrt(m.objVal))
        features.append(np.where(np.asarray(x) == 1.0)[0])

    if path:
        d = {"num_feat": range(lower_bound, number_features),
             "scores": scores,
             "f_lists": features}
        f = open(path, 'w')
        pickle.dump(d, f)
    if batch:
        return features, scores
    else:
        return features[0], scores[0]