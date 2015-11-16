#!/usr/bin/env python
# encoding: utf-8
"""
Analysis of Hallem data with pipelining
"""
import sys

sys.path.append('/Users/marcus/_workspace/repos/olfactory')
from example.hallem.data import Hallem
from _core import plotting, pipelining, gurobi
import time

hallem = Hallem()
data = hallem.response
feature_names = hallem.odorant_list
data_names = hallem.or_list

features = 6
threshold = 50

feature_list, score = pipelining.optimize(data, features, threshold)

title = 'Pipelining on Hallem'
print title
print "Top", str(features), "features"
print "Score:", score
print feature_names[feature_list]

path = "/Users/marcus/Desktop/hallem_pip_" + str(features) + ".png"
plotting.plot_fingerprints(title, feature_names[feature_list],
                           data[:, feature_list],
                           data_names,
                           path=path)
