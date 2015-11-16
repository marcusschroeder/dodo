#!/usr/bin/env python
# encoding: utf-8
'''
'''
import numpy as np


def generate_random_data(data, features):
    '''
    Generates a toy dataset. Generation happens iteratively, e.g. row by row.
    For each row, there is a chance that up to three similar rows will be
    generated. This way some of the rows are correlated.

    Args:
        data (int):
            Number of data points.
        features (int):
            Number of features.

    Returns:
        m (numpy.array):
            A matrix with data x features dimension.

    '''
    m = np.array([])

    while len(m) < data:
        correlates = np.random.randint(0, 3, 1)
        template = np.round(np.random.normal(26.76, 52.57, (1, features)), 0)

        if len(m) == 0:
            m = template
        else:
            m = np.append(m, template, axis=0)

        if correlates > 0:
            samples = template + np.random.randint(-10, 10,
                                                   (correlates, features))
            m = np.append(m, samples, axis=0)
    return m