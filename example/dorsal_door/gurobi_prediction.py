#!/usr/bin/env python
# encoding: utf-8
#
"""
Analysis of stability of Gurobi prediction.
"""
import datetime
import numpy as np
import matplotlib.pyplot as pl
from example.door import DoOR
from _core import validation

data, ors, odorants = np.transpose(DoOR().get_dorsal_data())

top = [
    [28],
    [16, 38],
    [5, 9, 28],
    [5, 9, 16, 58],
    [5, 16, 58, 202, 214],
    [16, 25, 40, 58, 98, 214],
    [5, 16, 58, 74, 92, 98, 214],
    [14, 38, 57, 58, 65, 72, 74, 214],
    [57, 58, 72, 74, 77, 81, 98, 141, 214],
    [5, 57, 58, 72, 74, 77, 81, 98, 198, 214],
    [5, 20, 57, 58, 72, 74, 77, 81, 98, 198, 214],
    [5, 39, 57, 58, 72, 74, 77, 81, 83, 85, 98, 214],
    [5, 45, 57, 58, 72, 74, 77, 81, 98, 118, 198, 212, 214],
    [5, 18, 39, 57, 58, 72, 74, 77, 81, 83, 98, 155, 212, 214],
    [5, 18, 39, 57, 58, 72, 74, 77, 81, 83, 91, 98, 202, 212, 214],
    [5, 13, 18, 39, 57, 58, 61, 72, 74, 77, 81, 85, 91, 98, 112, 118, 141, 202,
     212, 214],
    [5, 18, 39, 40, 52, 57, 58, 61, 64, 72, 74, 77, 81, 85, 91, 98, 112, 118,
     119, 126, 127, 172, 202, 212, 214]
]
top = np.asarray(top)

# levels of noise which will be added
sd_range = np.arange(0, 0.15, 0.01)

results = validation.validate(data, top, noise=sd_range, sample_size=50)

fig = pl.figure(figsize=(6, 4))
pl.suptitle("NN-Classification with features predicted by Gurobi")
ax2 = fig.add_subplot(111)
im = ax2.imshow(np.transpose(results), cmap=validation.cmap,
                interpolation='none', aspect='auto')
ax2.set_ylabel('sd noise')
ax2.set_xlabel('#features')
ax2.yaxis.set_ticklabels(sd_range)
ax2.yaxis.set_ticks(np.arange(len(sd_range)))
ax2.xaxis.set_ticklabels(range(1, len(top) + 1))
ax2.xaxis.set_ticks(range(len(top)))
cb = pl.colorbar(im, orientation='vertical')
cb.set_label("accuracy")

pl.savefig(
    "../figures/gurobi_door_performance_" + datetime.datetime.now().strftime(
        "%Y_%m_%d") + ".png")