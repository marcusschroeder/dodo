#!/usr/bin/env python
# encoding: utf-8
"""

Just plotting the hallem rows (Odorants) as a boxplot to get a look and
feel which odorant might carry the most/the least information

"""
import pylab as pl
import numpy as np
from example.hallem.data import Hallem

hallem = Hallem()
fig = pl.figure(figsize=(30, 15))
fig.autofmt_xdate()
t = []
for i in hallem.odorant_list:
    t.append(i.decode("utf8"))

a = np.transpose(hallem.response)
b = np.mean(a, axis=0)
c = np.std(a, axis=0)

a = (a - b) / c
d = np.median(a, axis=0)
sorting = np.argsort(d)

t = np.asarray(t)

pl.boxplot(a[:, sorting], bootstrap=10000, vert=True)
pl.xticks(np.arange(1, len(hallem.odorant_list) + 1), t[sorting],
          rotation="vertical")
pl.grid()
pl.savefig("figures/odorant_boxplot_normalized.png")

print hallem.odorant_list[[15, 43]]
print np.std(hallem.response, axis=1)[[15, 43]]

#creating the odorant spectra figures
matrix = hallem.response

#plot spectra of top6 Gurobi features in one barplot
#top6 predicted by gurobi [ 0  6 20 43 82 90]
top6 = np.asarray([0, 6, 20, 44, 83, 91])
offset = 5
pl.figure(figsize=(24, 8))
x_range = np.arange(0, (len(top6) + offset) * matrix.shape[1],
                    len(top6) + offset)
colors = ['y', 'r', 'g', 'c', 'grey', 'b']
for i, v in enumerate(top6):
    spectrum = matrix[v]

    print x_range + i
    print spectrum
    pl.bar(x_range + i, spectrum, width=1, color=colors[i])

pl.ylabel("spikes/s")
pl.xlabel("ORs")
# pl.ylim((-100, 350))
pl.xlim((-offset, (len(top6) + offset) * len(spectrum)))
pl.xticks(x_range + len(top6) / 2, hallem.or_list)
pl.grid()
pl.legend(hallem.odorant_list[top6], loc='upper center',
          bbox_to_anchor=(0.5, 1.1),
          ncol=len(top6), fancybox=True, shadow=True)
pl.savefig("figures/spectrum/odorant/top_features_bar.png")