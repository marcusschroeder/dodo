#!/usr/bin/env python
# encoding: utf-8
#
"""
Analysis of stability of backward prediction on DoOR dorsal dataset.
"""
import datetime
import numpy as np
import matplotlib.pyplot as pl
from example.door import DoOR
from _core import featureselection, validation

door = DoOR()

data, ors, odorants = door.get_dorsal_data()

# compute features
print data.shape
feature_list, scores = featureselection.backward_elimination(data)


# creating a list of feature-lists with increasing size
top = []
for i in range(15):
    top.append((feature_list[:i])[::-1])

print top

# # levels of noise which will be added
sd_range = np.arange(0, 0.15, 0.01)
results = validation.validate(data, top, noise=sd_range)

x = sd_range
y = np.asarray(range(1, results.shape[0] + 1))
X, Y = np.meshgrid(x, y)

Z = results

fig = pl.figure(figsize=(6, 4))
pl.suptitle("NN-Classification with features predicted by BE")
ax2 = fig.add_subplot(111)
im = ax2.imshow(np.transpose(Z), cmap=validation.cmap, interpolation='none',
                aspect='auto')
ax2.set_ylabel('sd noise')
ax2.set_xlabel('#features')
ax2.yaxis.set_ticklabels(sd_range)
ax2.yaxis.set_ticks(np.arange(len(sd_range)))
ax2.xaxis.set_ticklabels(range(1, len(top) + 1))
ax2.xaxis.set_ticks(range(len(top)))
cb = pl.colorbar(im, orientation='vertical')
cb.set_label("accuracy")

#pl.savefig(
#    "../figures/be_door_performance_distorted" + datetime.datetime.now()
#    .strftime(
#        "%Y_%m_%d") + ".png")

pl.show()