#!/usr/bin/env python
# encoding: utf-8
"""
"""
import numpy as np

from example.hallem.data import Hallem
from _core import plotting


hallem = Hallem()
data = np.transpose(
    hallem.response) # Glomeruli x Odorants instead of Odorants x Glomeruli
data_names = hallem.or_list

#feature_list = [6, 33, 63, 83, 93]
feature_list = [0, 6, 20, 44, 83, 91, ]
#feature_list = [3, 6, 20, 44, 73, 83, 91]
#feature_list = [0, 6, 33, 44, 63, 64, 83, 91]

feature_names = hallem.odorant_list[feature_list]

title = "Gurobi on Hallem with " + str(len(feature_list)) + " features"
path = "figures/hallem/gurobi/gurobi_" + str(len(feature_list)) + ".png"
plotting.plot_fingerprints(title, feature_names, data[:, feature_list],
                           data_names, path)