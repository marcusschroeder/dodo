"""
"""
import numpy as np


def generate_noise_samples(data, samples=100, noise=10):
    """
    Generates a number of labeled samples. Samples are based on the given data
    to which noise is added.

    Args:
        data (numpy.array):
            Data matrix.
        samples (int):
            (default=100) Number of samples to generate.
        noise (float):
            (default = 10) Noise level that will be added to real data. Noise
            is generated with normal distribution. Normally one should use the
            standard deviation as a level for noise.

    Returns:
        big_matrix (numpy.array):
                A matrix containing the generated data.
        labels (list):
                A list containing the labels for the generated data. Can be
                used for training in machine learning algorithms.
    """
    big_matrix = []

    size = data.shape[1]

    labels = []

    for i, row in enumerate(data):
        for j in range(samples):
            if noise != 0:
                v = np.random.normal(0, noise, size)
            else:
                v = 0
            big_matrix.append(v + row)
            labels.append(i)

    big_matrix = np.asarray(big_matrix)
    return big_matrix, labels


def generate_random_data(data, features):
    """
    Creates a data-set, where entries a sampled from uniform distribution
    [0, 200].

    Args:
        data (numpy.array):
            number of data points (rows).
        features (int):
            number of features for the random data (columns).

    Returns:
        (numpy.array):
            A random data set as a matrix with m-columns and n-rows, where m is
            the number of features and n is the number of data-points.
    """

    return np.random.randint(0, 200, (data, features))