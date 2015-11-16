#!/usr/bin/env python
# encoding: utf-8
"""
Analysis of Hallem data with backward elimination method.
"""
import numpy as np
import scipy as sp
from scipy import stats

from example.hallem.data import Hallem
from _core import featureselection


hallem = Hallem()
data = np.transpose(hallem.response)

feature_names = hallem.odorant_list
data_names = hallem.or_list
features = 6


# finding all pairs of features with a high correlation
# the feature with the lower variance will be removed
removables = []
for i, rowA in enumerate(data):
    for j, rowB in enumerate(data):
        if j > i:
            c = sp.stats.pearsonr(rowA, rowB)[0]
            if c > 0.92:

                if np.std(rowA) > np.std(rowB):
                    removables.append(j)
                else:
                    removables.append(i)

removables = np.unique(removables)
print "remove (%s)" % (len(removables)), removables

data = np.delete(data, removables, axis=0)
feature_names = np.delete(feature_names, removables)
data = np.transpose(data)
feature_list, scores = featureselection.backward_elimination(data)

title = 'Backward Elimination with preprocessing of Hallem with %s features' % str(
    features)
sub_list = feature_list[:features]
print title
print "Score:", scores[features]
print sub_list
print feature_names[sub_list]


#path = "../figures/hallem/be/hallem_be_" + str(features) + "_performance_preprocessing.png"
#plotting.plot_progress_results(scores, features, path=path)
#
#path = "../figures/hallem/be/hallem_be_" + str(features) + "_preprocessing.png"
#plotting.plot_fingerprints(title,
#                           feature_names[feature_list],
#                           data[:, feature_list],
#                           data_names,
#                           path)