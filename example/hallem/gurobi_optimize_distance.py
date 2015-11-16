#!/usr/bin/env python
# encoding: utf-8
from data import Hallem
from _core import gurobi as gb
from _core import plotting

#loading the data
hallem = Hallem()
data = hallem.response
feature_names = hallem.odorant_list
data_names = hallem.or_list

path = "/Users/marcus/Desktop/hallem_gu.pckl"
feature_list, score = gb.optimize(data,
                                  number_features=30,
                                  batch=True,
                                  path=path)

title = 'Gurobi on Mouse'
print title
print "Score:", score[-1]

path = "/Users/marcus/Desktop/mouse_be_performance.png"
plotting.plot_progress_results(score, path)

