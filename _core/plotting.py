#!/usr/bin/env python
# encoding: utf-8
"""
    Plotting the results of subset predictions.
"""
from __future__ import division
import numpy as np
import pylab as pl
from scipy.spatial import distance
from scipy.cluster.hierarchy import linkage
from scipy.cluster.hierarchy import dendrogram
from pylab import *


def create_cmap(minimum, maximum):
    """
        Creates a red/blue color map, where blue = minimum and red = maximum.
        Everything right in the middle of maximum and minimum appears white.

        Args:
            minimum (float):
                The blue'st point in the map.
            maximum (float:)
                The reddest point in the map.

        Returns:
            colormap:
                A colormap applicable to imshow-like plots.
    """
    zero = abs(float(minimum) / (maximum - minimum))

    if minimum < 0:
        cdict = {'red': ((0.0, 1.0, 1.0),
                         (zero, 1.0, 1.0),
                         (1.0, .0, 1.0)),
                 'green': ((.0, .0, .0),
                           (zero, 1.0, 1.0),
                           (1.0, .0, .0)),
                 'blue': ((0.0, 0.0, 0.0),
                          (zero, 1.0, 1.0),
                          (1.0, 1.0, 1.0))}
    else:
        cdict = {'red': ((0.0, 1.0, 1.0),
                         (minimum, 1.0, 1.0),
                         (1.0, .0, 1.0)),
                 'green': ((.0, 1.0, 1.0),
                           (minimum, 1.0, 1.0),
                           (1.0, .0, .0)),
                 'blue': ((0.0, 1.0, 1.0),
                          (minimum, 1.0, 1.0),
                          (1.0, 1.0, 1.0))}
    return matplotlib.colors.LinearSegmentedColormap('my_colormap', cdict, 256)


def plot_progress_results(result, features=None, path=None):
    fig = pl.figure(figsize=(9, 6), dpi=300, facecolor='w', edgecolor='k')
    fig.autofmt_xdate()
    x_coord = features

    pl.plot(range(0, len(result)), result)

    if features is not None:
        pl.axvline(x_coord, color='r')
        pl.xticks([0, features, len(result)])

    else:
        pl.xticks([0, len(result)])

    pl.xlabel("#features")
    pl.ylabel("max-min euclidean distance")
    if path:
        pl.savefig(path)
    else:
        pl.show()
    return fig


def plot_fingerprints(title, feature_names, data, data_names, path=None,
                      xlabel="spikes/s"):
    '''
    Given a matrix, plots the fingerprint for each row (OR respectively), e.g.
    a dendrogram based on the columns (features) is created.

    Args:
        title (str):
            Title for the plot.
        feature_names (numpy.array):
            A list containing names of features.
        data (numpy.array):
            A matrix with $n$ rows and $m$ columns, where $m = #features$
        data_names (numpy.array):
            A list containing the names of the rows.
        path (str):
            When specified, the plot will be saved here. Otherwise the plot is
            shown (default=None)
        xlabel (str):
            Label for x-axis (default="spikes/s").
    Returns:
        a reference to the figure object
    '''

    features = len(feature_names)

    if path:
        fig = pl.figure(figsize=(12, 8), dpi=300, facecolor='w', edgecolor='k')
    else:
        fig = pl.figure(facecolor='w', edgecolor='k')

    fig.autofmt_xdate()

    # plotting dendrogram of eucledean distance between glomeruli
    pl.suptitle(title)
    pl.subplot(121)
    p = data
    pl.xlabel("Distance in " + xlabel)
    pl.ylabel("OR")
    link = linkage(distance.pdist(p, 'euclidean'), method="single")
    dend = dendrogram(link, labels=data_names, orientation="right",
                      color_threshold=1)
    sorted_list = p[dend["leaves"]]
    pl.grid()

    pl.subplot(122)
    cmap = create_cmap(np.min(sorted_list), np.max(sorted_list))
    pl.imshow(sorted_list[::-1], cmap=cmap, vmin=np.min(sorted_list),
              vmax=np.max(sorted_list), interpolation="None",
              aspect="auto")

    pl.xticks(np.arange(0.5, .5 + features), feature_names, rotation="30",
              ha='right', fontsize=10)
    pl.yticks([])
    cb = pl.colorbar()
    cb.set_label(xlabel)
    pl.grid(which="major")

    if path:
        pl.savefig(path)
    else:
        pl.show()
    return fig
