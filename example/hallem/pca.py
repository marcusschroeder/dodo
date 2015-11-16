#!/usr/bin/env python
# encoding: utf-8
"""
John Doe PCA, simple stuff, simple plot
"""

import numpy as np
import pylab as pl
from sklearn.decomposition.pca import PCA

from example.hallem.data import Hallem


hallem = Hallem()

matrix = np.transpose(hallem.response)

print matrix.shape
x = PCA()
x.fit(matrix)

fig = pl.figure()
ax = fig.add_subplot(111)

a = x.explained_variance_ratio_
b = x.explained_variance_
print len(a)
ax.plot(range(len(a)), a)
ax.plot(np.cumsum(a))
ax.grid()
pl.show()
