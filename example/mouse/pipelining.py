#!/usr/bin/env python
# encoding: utf-8
"""
Analysis of Mouse data with pipelining
"""
import sys

sys.path.append('/Users/marcus/_workspace/repos/olfactory')
from example.mouse.data import MouseData
from _core import plotting, pipelining

mouse = MouseData()
data = mouse.response
feature_names = mouse.odorant_list
data_names = mouse.or_list

features = 6
threshold = 23

feature_list, score = pipelining.optimize(data, features, threshold)

title = 'Pipelining on Mouse'
print title
print "Top", str(features), "features"
print "Score:", score
print feature_names[feature_list]

path = "/Users/marcus/Desktop/mouse_pip_" + str(features) + ".png"
plotting.plot_fingerprints(title, feature_names[feature_list],
                           data[:, feature_list],
                           data_names,
                           path=path)
