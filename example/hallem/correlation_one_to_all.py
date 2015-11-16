#!/usr/bin/env python
# encoding: utf-8
"""
    Compute the correlation one-to-all  of a specified odorant.
"""
import scipy as sp
import pylab as pl
import numpy as np
from scipy import stats

from example.hallem.data import Hallem


hallem = Hallem()
data = hallem.response

o1 = hallem.get_odorant_index("E2 Hexenol")
o1_name = hallem.odorant_list[o1]
o1_spec = data[o1]

correlations = []

for i, spec in enumerate(data):
    o2 = i
    o2_name = hallem.odorant_list[o2]
    o2_spec = spec

    c = sp.stats.pearsonr(o1_spec, o2_spec)[0]
    correlations.append(c)
    print o2_name, c

correlations = np.round(np.asarray(correlations), 3)
sorting = np.argsort(correlations)

print correlations[sorting]
pl.figure(figsize=(24, 16))
x_range = np.arange(len(correlations))
pl.bar(x_range, correlations[sorting], width=1)
pl.ylabel("pearson correlation")
pl.xlabel("odorant")
pl.xticks(x_range, hallem.odorant_list[sorting], rotation="90")
pl.grid()
pl.savefig("figures/correlation/odorants/one_to_all/" + o1_name + ".png")