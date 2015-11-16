#!/usr/bin/env python
# encoding: utf-8
"""
Analysis of Hallem data with forward selection method.
"""

from example.hallem.data import Hallem
from _core import featureselection, plotting

hallem = Hallem()

data = hallem.response

features = 6

f_list, score = featureselection.forward_selection(data)

feature_names = hallem.odorant_list
data_names = hallem.or_list

title = 'Forward Selection of Hallem'

print title
print "Top", str(features), "features"
print "Score:", score[features - 1]
print feature_names[f_list[:features]]

path = "/Users/marcus/Desktop/hallem_fs_" + str(features) + "_performance.png"
plotting.plot_progress_results(score, features, path)

path = "/Users/marcus/Desktop/hallem_fs_" + str(features) + ".png"
plotting.plot_fingerprints(title, feature_names[f_list[:features]],
                           data[:, f_list[:features]],
                           data_names, path)

#m = np.column_stack((np.arange(0, len(feature_names) + 1), scores))
#np.savetxt("../results/fs_features.csv", m, delimiter=";")