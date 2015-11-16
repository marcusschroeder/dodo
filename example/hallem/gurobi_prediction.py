#!/usr/bin/env python
# encoding: utf-8
#
"""
Analysis of stability of Gurobi prediction.
"""
import datetime
import numpy as np
import matplotlib.pyplot as pl
from example.hallem.data import Hallem
from _core import validation

hallem = Hallem()
data = np.transpose(hallem.response)

top = [
    [45, 53, 22, 32, 44, 5, 20, 105, 29, 64]
    #[8],
    #[6, 95],
    #[44, 53, 83],
    #[7, 60, 63, 93],
    #[6, 33, 63, 83, 93],
    #[0, 6, 20, 44, 83, 91],
    #[3, 6, 20, 44, 73, 83, 91],
    #[0, 6, 33, 44, 63, 64, 83, 91],
    #[3, 6, 7, 33, 44, 63, 64, 73, 91],
    #[3, 6, 7, 33, 44, 63, 64, 68, 73, 91],
    #[3, 6, 7, 33, 44, 63, 64, 68, 73, 78, 91],
    #[3, 6, 7, 20, 33, 43, 44, 63, 64, 73, 83, 91],
    #[3, 6, 7, 33, 44, 49, 63, 64, 73, 78, 80, 85, 91],
    #[3, 6, 7, 8, 33, 44, 49, 62, 63, 64, 73, 78, 91, 98],
    #[3, 6, 7, 20, 33, 44, 49, 63, 64, 68, 73, 78, 91, 95, 98],
    #[3,  6, 7, 20, 27, 30, 31, 33, 44, 49, 63, 64, 73, 78, 80, 83, 90, 91,
    # 95, 98],
    #[2, 3, 6, 7, 8, 9, 20, 27, 30, 31, 33, 41, 43, 49, 56, 60, 63, 64, 73,
    # 78, 80, 83, 90, 91, 98]
]


# levels of noise which will be added
sd_range = range(0, 50, 10)

results = validation.validate(data, top, noise=sd_range, sample_size=50)

np.set_printoptions(suppress=True, precision=3)
print results

fig = pl.figure(figsize=(6, 4))
pl.suptitle("NN-Classification with features predicted by Gurobi")
ax2 = fig.add_subplot(111)
im = ax2.imshow(np.transpose(results), cmap=validation.cmap,
                interpolation='none', aspect='auto')
ax2.set_ylabel('$\sigma$')
ax2.set_xlabel('#features')
ax2.yaxis.set_ticklabels(sd_range)
ax2.yaxis.set_ticks(np.arange(len(sd_range)))
ax2.xaxis.set_ticklabels(range(1, len(top) + 1))
ax2.xaxis.set_ticks(range(len(top)))
cb = pl.colorbar(im, orientation='vertical')
cb.set_label("accuracy")

pl.savefig("../figures/dg_performance_" + datetime.datetime.now().strftime(
    "%Y_%m_%d") + ".png")