#!/usr/bin/env python
# encoding: utf-8
'''
Call this script in terminal via:

    gurobi.sh example/mouse/gu.py

'''
import sys

sys.path.append('/Users/marcus/_workspace/repos/olfactory')
from data import MouseData
from _core import gurobi as gb
from _core import plotting
import numpy as np


mouse = MouseData()
data = mouse.response
feature_names = mouse.feature_names
data_names = mouse.data_names
cluster = mouse.cluster

path = "/Users/marcus/Desktop/mouse_gu.pckl"
#feature_list, score = gb.optimize(data,
#                                           number_features=len(feature_names),
#                                           batch=True,
#                                           cluster=cluster,
#                                           path=path)

score = np.load(path)['scores']
print score
title = 'Gurobi on Mouse'
print title
print "Score:", score[-1]

path = "/Users/marcus/Desktop/mouse_gu_performance.png"
plotting.plot_progress_results(score, path=path)


#path = "/Desktop/mouse_gu_" + str(features) + ".png"
#plotting.plot_fingerprints(title, feature_names[feature_list],
#                           data[:, feature_list],
#                           data_names)