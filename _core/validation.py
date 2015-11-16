#!/usr/bin/env python
# encoding: utf-8
"""
    This script should allow you to cross check the results you get from
    gurobi, be or whatsoever.
    Since we have no test set, like in many machine learning tasks,
    we generate one from the original data.
    For each glomerulus spectrum we create 100 noisy samples and try to
    reverse classify them according to the glomerulus they are based on.
    For different levels of noise, the accuracy of prediction is measured,
    e.g. how many labels could be predicted correctly.
"""
import numpy as np
from scipy.spatial.distance import pdist
import matplotlib.colors
from _core import toydata

cdict = {'red': ((0.0, 1.0, 1.0),
                 (0.97, .5, .5),
                 (1.0, .0, .3)),
         'green': ((0.0, 1.0, 1.0),
                   (0.97, .5, .5),
                   (1.0, .5, .3)),
         'blue': ((0.0, 1.0, 1.0),
                  (0.97, .5, .5),
                  (1.0, .0, .3))}
cmap = matplotlib.colors.LinearSegmentedColormap('my_colormap', cdict, 256)


def compute_accuracy(data, sample_size, sd, sub):
    """
    Computes the classification accuracy of the subset when noise is added toy
    to the data.

    Args:
        data (numpy.array):
            Data matrix. Contains no information about row or column names, e.g.
            it contains solely digits.
        sample_size (int):
            How many samples should be generated.
        sd (float)
            Noise level.
        sub (numpy.array):
            The indices of the features to use for the computation.

    Returns:
        accuracy (float):
            The accuracy in percent, e.g. 0.5 for 50%.

    """
    output = []
    # generate the samples and their classes
    samples, labels = toydata.generate_noise_samples(data,
                                                     samples=sample_size,
                                                     noise=sd)
    for sample in samples:
        sd = np.vstack([sample[sub], data[:, sub]])
        mm = pdist(sd)
        output.append(np.argmin(mm[:len(data)]))
    output = np.asarray(output)
    accuracy = 1 - np.count_nonzero(output - labels) / float(
        len(labels))

    return accuracy

def validate(data, features, noise=range(0, 50, 10), sample_size=100):
    """
    Args:
        features (numpy.ndarray):
            A list of feature lists. Normally with increasing size.
        noise (numpy.ndarray):
            Different levels of noise which should be added.
    Returns:
        results (numpy.ndarray):
                Result matrix.
    """
    results = []

    for sub in features:

        a = []

        for sd in noise:
            a.append(compute_accuracy(data, sample_size, sd, sub))
        results.append(a)

    results = np.asarray(results)

    return results