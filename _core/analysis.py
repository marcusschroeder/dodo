#!/usr/bin/env python
# encoding: utf-8
import doctest
import numpy as np
from scipy.spatial.distance import pdist
from scipy.stats import pearsonr


def correlation(matrix):
    '''
    Given a matrix, compute the correlation of its rows to each other.

    Args:
        matrix (numpy.array):
            The olfactory data matrix. x-dimension: receptors,
            y-dimension: odorants.

    Returns:
        corr (numpy.array):
            A list of triples, where  each entry is the computed correlation
            between two receptors, e.g. (2, 10, 0.5) means, that the correlation
            between receptor 2 and 10 is 0.5.

            To access all pairs with strong correlation call corr[corr[2] > .9]
    '''
    corr = []
    for i, rowA in enumerate(matrix):
        for j, rowB in enumerate(matrix):
            if j > i:
                c = pearsonr(rowA, rowB)[0]
                corr.append((i, j, c))

    corr = np.asarray(corr)
    return corr


def nearest_neighbour_classification(reference, data):
    """
        Assigns a value from the reference to each data points.correlation
        The name of the features must be identical.
        Args:
            reference (numpy.array):
                A matrix to which the data will be mapped. The first row should
                contain the names/indices of the features.
                The first column contains the labels.

            data (numpy.array):
                Unlabeled data. The first row should contain the names/indices
                of the features.

        Returns:
            labels (numpy.array):
                A list of labels for the data.

        >>> nearest_neighbour_classification(\
        [["", u"C1", u"C3"], \
         [u"R1", 1, 1],\
         [u"R2", 4, 4], \
         [u"R3", -10, -10]], \
        [[u"C1", u"C2", u"C3"], \
         [4, 4, 4], \
         [1, 1, 1], \
         [1, 1, 2], \
         [-10, -10, -8]])
        [(u'R2', 0.0), (u'R1', 0.0), (u'R1', 1.0), (u'R3', 2.0)]
    """
    reference = np.array(reference)
    data = np.array(data)

    reference_features = np.array(reference[0, 1:], dtype=str)
    data_features = np.array(data[0], dtype=str)
    data_names = reference[1:, 0]

    ## checking which of the features are in both arrays
    ## and saving their indices aka map
    features = np.intersect1d(reference_features, data_features)

    ## indices of features that are in reference array
    reference_map = [np.argwhere(i == reference_features)[0][0] for i in features]

    ## indices of features that are in data array
    data_map = [np.argwhere(i == data_features)[0][0] for i in features]

    ## shrinking the arrays for faster computation
    ref_tmp = reference[1:, 1:]
    ref_tmp = ref_tmp[:, reference_map]
    ref_tmp = np.asarray(ref_tmp, dtype=float)
    data_tmp = data[1:, :]
    data_tmp = data_tmp[:, data_map]
    data_tmp = np.asarray(data_tmp, dtype=float)

    labels = []
    for row in data_tmp:
        matrix = np.vstack((row, ref_tmp))
        m = pdist(matrix)
        a = m[:len(data_tmp)]
        labels.append((data_names[np.argmin(a)], np.min(a)))

    return labels

if __name__ == "__main__":
    doctest.testmod()
