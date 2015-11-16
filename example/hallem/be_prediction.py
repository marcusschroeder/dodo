#!/usr/bin/env python
# encoding: utf-8
#
"""
Analysis of stability of backward prediction.

Since we have no test set, like in many machine learning tasks, we generate
one from the original data.
For each glomerulus we create 100 samples and classify them according to the
glomerulus they are based on.
For different levels of noise, the accuracy of prediction is measured,
e.g. how many labels could be predicted correctly.
"""
import numpy as np
import matplotlib.pyplot as pl
from example.hallem.data import Hallem
from _core import featureselection, validation

data = np.transpose(Hallem().response)

# compute features
feature_list, scores = featureselection.backward_elimination(data)

# creating a list of feature lists with increasing size
top = []
for i in range(15):
    top.append((feature_list[:i + 1])[::-1])

# # levels of noise which will be added
sd_range = range(0, 50, 10)
results = validation.validate(data, top, noise=sd_range)

np.set_printoptions(suppress=True, precision=3)

Z = results

fig = pl.figure(figsize=(6, 4))
pl.suptitle("NN-Classification with features predicted by BE")
ax2 = fig.add_subplot(111)
im = ax2.imshow(np.transpose(Z), cmap=validation.cmap, interpolation='none',
                aspect='auto')
ax2.set_ylabel('$\sigma$')
ax2.set_xlabel('#features')
ax2.yaxis.set_ticklabels(sd_range)
ax2.yaxis.set_ticks(np.arange(len(sd_range)))
ax2.xaxis.set_ticklabels(range(1, len(top) + 1))
ax2.xaxis.set_ticks(range(len(top)))
cb = pl.colorbar(im, orientation='vertical')
cb.set_label("accuracy")

#pl.savefig("../figures/be_performance_" + datetime.datetime.now().strftime(
#    "%Y_%m_%d") + ".png")
pl.show()