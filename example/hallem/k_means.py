#!/usr/bin/env python
# encoding: utf-8
"""
k - means test script

Testing the feature selection by clustering
"""
import random

from numpy.core.multiarray import arange
import pylab as pl
import numpy as np
from scipy.spatial import distance
from scipy.cluster.hierarchy import linkage
from scipy.cluster.hierarchy import dendrogram
from sklearn.cluster import KMeans

from example.hallem.data import Hallem


hallem = Hallem()
data = np.transpose(
    hallem.response) # Glomeruli x Odorants instead of Odorants x Glomeruli

features = 5
km = KMeans(n_clusters=features, init='random', max_iter=100, n_init=10,
            verbose=0)
km.fit(hallem.response)

centers = km.cluster_centers_

odorants = []
for i in range(0, features):
    odorants.append(random.choice(np.where(km.labels_ == i)[0]))

print odorants
fig = pl.figure(figsize=(25, 10), facecolor='w', edgecolor='k')
fig.autofmt_xdate()

p = data[:, odorants]
# p = np.transpose(centers)
pl.suptitle('K-Means with ' + str(features) + " features")
pl.subplot(131)
pl.xlabel("Euclidean Distance between \nglomeruli with " + str(
    features) + " features")
pl.ylabel("Glomerulus")
link = linkage(distance.pdist(p, 'euclidean'), method="single")
dend = dendrogram(link, labels=hallem.or_list, orientation="right")
sorted_list = p[dend["leaves"]]

pl.subplot(132)
pl.pcolor(sorted_list)
pl.ylim((0, 23))
pl.xticks(arange(.5, .5 + features), hallem.odorant_list[odorants],
          rotation="vertical")
pl.title("Heat Map of \nGlomeruli Activity")
pl.colorbar()

pl.subplot(133)
pl.title("Fingerprint")
for odor in range(0, len(sorted_list)):
    x = range(0, len(sorted_list[odor]))
    y = [odor] * len(sorted_list[odor])
    values = sorted_list[odor]
    pl.scatter(x, y, s=values, c="green", alpha=.75)
    pl.scatter(x, y, s=values * -1, c="red", alpha=1)

    pl.ylim((-.5, 22.5))
    pl.xlim((-.5, features))
    pl.xticks(arange(features), hallem.odorant_list[odorants],
              rotation="vertical")

#pl.show()


pl.savefig("figures/k-means_" + str(features) + ".png")