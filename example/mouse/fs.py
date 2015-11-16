#!/usr/bin/env python
# encoding: utf-8
import numpy as np
from example.mouse.data import MouseData
from _core import plotting
from _core.featureselection import forward_selection

mouse = MouseData()
data = mouse.response
feature_names = mouse.feature_names
data_names = mouse.data_names

feature_list, score = forward_selection(data)
features = 6
title = 'Backward Elimination on Mouse'
print title
print "Score:", score[-1]
print feature_names[feature_list]

path = "/Users/marcus/Desktop/mouse_fs_" + str(features) + "_performance.png"
plotting.plot_progress_results(score, features, path)

#path = "/Users/marcus/Desktop/mouse_be_" + str(features) + ".png"
#plotting.plot_fingerprints(title, feature_names[feature_list],
#                           data[:, feature_list],
#                           data_names)