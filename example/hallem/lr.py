#!/usr/bin/env python
# encoding: utf-8

import numpy as np
from sklearn.linear_model import LogisticRegression
from mpl_toolkits.mplot3d import Axes3D
from example.hallem.data import Hallem
from _core import toydata


hallem = Hallem()
data = np.transpose(hallem.response)

print data.shape

big_matrix, labels = toydata.generate_noise_samples(data)

c_range = np.arange(0.001, 0.008, 0.00001)
f = []
a = []
b1 = True
b2 = True

## Probing over c to find the number of features for each c
for c in c_range:
    lr = LogisticRegression(penalty='l1', C=c)
    lr.fit(data, range(data.shape[0]))

    # number of features
    f.append(np.sum(np.sum(np.abs(lr.coef_), axis=0) > 0))

    output = lr.predict(big_matrix)
    accuracy = 1 - np.count_nonzero(output - labels) / float(len(labels))
    a.append(accuracy)

#f.remove(0)
f = np.asarray(f)

m = np.unique(f[f < 11])

indices = []
for c in m:
    indices.append(np.max(np.where(f == c)))

print indices

lr = LogisticRegression(penalty='l1', C=c[indices[6]])
lr.fit(data, range(data.shape[0]))
print np.sum(np.abs(lr.coef_), axis=0)
