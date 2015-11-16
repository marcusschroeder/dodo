#!/usr/bin/env python
# encoding: utf-8
"""
Implementation of feature selection methods (backward elimination and forward
selection).
"""
import numpy as np
import doctest
from scipy.spatial import distance


def find_best_value(distanceMatrix, k=0):
    """
    Returns the k-th minimal value of a given distance matrix.

    Args:
        distanceMatrix (numpy.array):
            a matrix containing the distances between data points
        k (int) :
            specifies, which minimum should be returned. if k=0,
            then its the real minimum. if k=1, its, the second smallest
            value, etc.

    Returns:
        The best (smallest) value.

    >>> find_best_value([3, 10, 2, 7])
    2

    >>> find_best_value([3, 10, 2, 7], 2)
    7
    """
    return np.sort(distanceMatrix)[k]


def compute_distance_matrix(matrix, metric='euclidean', noise_threshold=None):
    """
    Computes the pairwise distance between each row of the input matrix.

    Args:
        matrix (numpy.array):
            A matrix where the distance between each row will be computed.

        metric (str) :
            Possible values 'euclidean' (default), 'noisy'.
            'euclidean' : standard euclidean distance

            'noisy': computes the pairwise euclidean distance but
                whenever an element has a value below the threshold,
                it is set to zero.

    Returns:
        Returns a distance matrix, where each entry represents the
        distance between to rows.


    For example, lets compute the standard euclidean distance between three
    two-dimensional points (2,0), (0,0), and (2,1).
    >>> compute_distance_matrix(np.array([[2, 0],[0,0], [2, 1]]))
    array([ 2.        ,  1.        ,  2.23606798])

    Now, lets compute the 'noisy' distance between the same points with a
    threshold of 1.1, e.g. the value of the third point will be changed
    from (2,1) to (2,0) before the computation.
    >>> compute_distance_matrix(np.array([[2, 0],[0,0], [2, 1]]), \
        metric='noisy', noise_threshold=1.1)
    array([ 2.,  0.,  2.])

    """
    if metric == 'noisy':

        m, n = matrix.shape

        distance_matrix = np.zeros(m * (m - 1) / 2, )
        if noise_threshold == None:
            print "Error: Provide a noise threshold"

        counter = 0

        #for each pairwise combination, e.g. row-wise)
        for i in range(0, m - 1):
            for j in range(i + 1, m):
                # substract row j from row i
                v = matrix[i] - matrix[j]

                # set all values below the threshold to zero
                v[abs(v) < noise_threshold] = 0.

                # compute euclidean distance of v
                distance_matrix[counter] = float(np.sqrt((v ** 2).sum()))
                counter += 1

        return distance_matrix
    else:
        return distance.pdist(matrix, metric)


def backward_elimination(data, features=None, distance_measure='euclidean'):
    """
    Performs a backward elimination on the given data.


    Args:
        data (numpy.array):
            A matrix consisting solely of digits.
        features (int):
            Specifies how many features are selected. If not specified,
            a list of all features sorted decreasingly by their importance
            will be returned.
        distance_measure (string):
            Possible values 'euclidean', 'manhattan', 'noisy'.

    Returns: tuple (f,r)
        f (list) :
            A list of the feature indices in reversed order they where removed
            from the feature set (most important feature is at the beginning).
        r (list or int) :
            Either a list of the optimal values after a feature was removed or
            a single score (if features was specified).


    Example:
        Given a matrix with three odorants and four receptors.
        5   10  4
        7   5   7
        8   3   12
        1   1   9

        Backward elimination should return a list of odorants with the most
        important feature at the beginning and a list that contains the
        distances computed with 0 features up to n-features.

    >>> backward_elimination(np.array([[5, 10, 4], [7, 5, 7], [8, 3, 12], \
            [1, 1, 9]]))
    ([2, 1, 0], [0.0, 2.0, 3.6055512754639891])

    """
    columns = len(data[0])

    f = []
    b = range(columns)
    r = []

    while len(b) > 0:
        maximum = -100
        index = -1

        for odor in range(0, columns):
            if odor in b:
                ff = list(b)
                ff.remove(odor)

                # take just the columns f from the whole data and compute
                # the distance matrix, e.g. take all odors which have not been
                # removed yet
                dm = compute_distance_matrix(data[:, ff], distance_measure)
                local_min = find_best_value(dm)

                if local_min > maximum:
                    maximum = local_min
                    index = odor

        f.append(index)
        b.remove(index)

        r.append(maximum)

    # reverse the order to have the most important features at the beginning.
    f = np.array(f[::-1])
    r = np.array(r[::-1])

    if features:
        return f[:features], r[features]
    else:
        return f, r


def forward_selection(data, features=None, distance_measure='euclidean'):
    """
    Performs a forward selection on the given data.

    Args:
        data (numpy.array):
            A matrix consisting solely of digits.
        features (int):
            Specifies how man features are selected. If not specified,
            a list of all features sorted decreasingly by their importance
            will be returned.
        distance_measure (str):
            Possible values 'euclidean', 'manhattan'.

    Returns:
        f (list):
            A list of the indices in the order they where added to the
            feature set.
        r (list or int) :
            Either a list of the optimal values after a feature was removed or
            a single score (if features was specified).


    Example:
        Given a matrix with three odorants and four receptors.
        5   10  4
        7   5   7
        8   3   12
        1   1   9

        Forward selection should return a list of odorants with the most
        important feature at the beginning and a list that contains the
        distances computed with 0 features up to n-features.

    >>> forward_selection(np.array([[5, 10, 4], [7, 5, 7], [8, 3, 12], \
            [1, 1, 9]]))
    ([0, 2, 1], [0, 0, 3.6055512754639891, 5.4772255750516612])

    """

    f = []
    r = []
    columns = len(data[0])

    # repeat until every column is taken into account
    while len(f) < columns:
        max_value = -1
        index = -1
        for i in range(0, columns):
            if i not in f:
                ff = list(f)
                ff.append(i)

                dm = compute_distance_matrix(data[:, ff], distance_measure)
                min_value = find_best_value(dm)

                if min_value > max_value:
                    max_value = min_value
                    index = i
        f.append(index)
        r.append(max_value)

    f = np.array(f)
    r = np.array(r)
    if features:
        return f[:features], r[features]
    else:
        return f, r


if __name__ == "__main__":
    doctest.testmod()
