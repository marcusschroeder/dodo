#!/usr/bin/env python
# encoding: utf-8
import pylab as pl
import numpy as np
import scipy as sp
from scipy import stats

from example.dorsal_door import DoOR


door = DoOR()
matrix, or_names, odorant_names = door.get_dorsal_data()

corr = []
strong_corr = []
for i, rowA in enumerate(matrix):
    for j, rowB in enumerate(matrix):
        if j > i:
            c = sp.stats.pearsonr(rowA, rowB)[0]
            if c > 0.9:
                strong_corr.append((i, j, c))
            corr.append(c)

corr = np.asarray(corr)
strong_corr = np.asarray(strong_corr)
print strong_corr

pl.figure(figsize=(5, 4), dpi=320)
pl.title("Correlation between odorants")
pl.xlabel("Pearson Correlation")
pl.ylabel("Count")
pl.hist(corr, bins=40, color='b')
pl.grid()
pl.xlim(-1, 1)
pl.savefig("../figures/door/correlation/odorants/pearson_odorants.png")

sort = np.argsort(np.abs(strong_corr[:, 2]))

for index, value in enumerate(strong_corr[sort]):
    o1 = value[0]
    o2 = value[1]

    o1_name = odorant_names[o1]
    o2_name = odorant_names[o2]

    c = round(value[2], 3)

    pl.figure(figsize=(24, 12), dpi=320)
    pl.title(o1_name + " against " + o2_name + "| correlation=" + str(c))

    o1_spec = matrix[o1]
    o2_spec = matrix[o2]

    sorting = np.argsort(o1_spec)

    ax1 = pl.subplot2grid((2, 4), (0, 0), colspan=3)
    ax1.bar(np.arange(0, len(o1_spec), 1), o1_spec[sorting], width=0.3,
            color='b', alpha=.6)
    ax1.bar(np.arange(.3, len(o2_spec) + .3, 1), o2_spec[sorting], width=0.3,
            color='r', alpha=.6)
    ax1.get_xaxis().set_ticks(np.arange(0.15, len(o1_spec), 1))
    ax1.set_xticklabels(or_names[sorting])
    ax1.legend((o1_name, o2_name), loc=2)
    ax1.set_xlabel("ORs")
    ax1.set_ylabel("spikes/s")
    ax1.grid()

    ax2 = pl.subplot2grid((2, 4), (0, 3), colspan=1)
    ax2.plot(o1_spec, o2_spec, 'o')
    ax2.grid()
    ax2.set_xlabel(o1_name)
    ax2.set_ylabel(o2_name)

    sorting = np.argsort(o2_spec)

    ax3 = pl.subplot2grid((2, 4), (1, 1), colspan=3)
    ax3.bar(np.arange(0, len(o1_spec), 1), o1_spec[sorting], width=0.3,
            color='b', alpha=.6)
    ax3.bar(np.arange(.3, len(o2_spec) + .3, 1), o2_spec[sorting], width=0.3,
            color='r', alpha=.6)
    ax3.get_xaxis().set_ticks(np.arange(0.15, len(o1_spec), 1))
    ax3.set_xticklabels(or_names[sorting])
    ax3.legend((o1_name, o2_name), loc=2)
    ax3.set_xlabel("ORs")
    ax3.set_ylabel("spikes/s")
    ax3.grid()

    ax4 = pl.subplot2grid((2, 4), (1, 0), colspan=1)
    ax4.plot(o2_spec, o1_spec, 'o')
    ax4.grid()
    ax4.set_xlabel(o2_name)
    ax4.set_ylabel(o1_name)

    pl.savefig("../figures/correlation/odorants/" + str(
        c) + "_" + o1_name + "_" + o2_name + ".png")




# what happens, if we perform be after we remove some redundant data,
# e.g. remove those odorants which
# have a high correlation with another odorant

max_corr = strong_corr[np.argsort(strong_corr[:, 2])[
    -2]] # select the pair with the strongest pos. correlation
print max_corr

o1_name = odorant_names[max_corr[0]]
o2_name = odorant_names[max_corr[1]]