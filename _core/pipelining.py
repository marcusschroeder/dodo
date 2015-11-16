#!/usr/bin/env python
# encoding: utf-8
'''
'''
from _core import gurobi, featureselection, analysis
import numpy as np


def optimize(data, number_features, threshold, corr=None, batch=False):
    '''
    This function computes the optimal set of odorants with a more efficient
    approach that includes two possible pre-processing steps of the data
    before a linear optimization is applied.

    First, one decides to omit highly correlated pairs of odorants from the
    data-set. Normally, these only contain redundant information. To activate
    set corr=True.

    In a second step, a fast backward elimination is performed to find a larger
    set (threshold), e.g. all other odorants are removed as well.

    Gurobi is then applied on the remaining odorants. If the values are chosen
    carefully, one can drastically speed up the computation of the optimal
    number_features.

    In my thesis I showed, that backward elimination is often close to optimal
    but much faster than Gurobi, so theoretically a combination of both should
    boost computation without losing stability.

    Args:
        data (numpy.array):
            The olfactory data matrix. x-dimension: receptors,
            y-dimension: odorants.
        number_features (int):
            Specifies the desired size of the optimal set.
        threshold (int):
            Speficies how many number_features are computed by backward_elimination.
        corr (bool):
            (default=False). If true, pairwise correlation between
            number_features is computed and one feature from pairs with high correlation
            is removed.

    Returns:
        f_list (numpy.array):
            The optimal odorant set. Odorants are sorted increasingly by odorants
            standard deviation.
        score (float):
            The score. Higher scores are better.
    '''

    if threshold <= number_features:
        print "threshold must be larger than number_features"

    removables = []

    if corr:
        c = analysis.correlation(np.transpose(data))

        l = c[c[2] > corr]
        for i in l:
            if np.std(i[0]) > np.std(i[1]):
                removables.append(i[0])
            else:
                removables.append(i[1])

    f_list = np.setdiff1d(range(data.shape[1]), removables)

    f_tmp, score = featureselection.backward_elimination(data[:, f_list],
                                                         threshold)
    # keep number_features computed by backward elimination
    f_list = np.intersect1d(f_list, f_list[f_tmp])

    f, s = gurobi.optimize(data[:, f_list], number_features=number_features,
                           batch=batch)

    for i, v in enumerate(f):
        f[i] = f_list[v]

    return f, s




