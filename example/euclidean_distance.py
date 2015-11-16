'''
The goal is to quantify how large the euclidean distance has to be,
to distinguish two receptors.
Furthermore, the influence of the standard deviation is analyzed.
'''
import numpy as np
import pylab as pl

euc = range(0, 10)  # euclidean distances
num_dim = [1, 2, 4, 8, 16, 32, 64]  # number of features (odorants)
num_samples = 500  # number of samples per receptor

miscl = np.zeros((len(euc), len(num_dim)))

for e_ind, e in enumerate(euc):
    for d_ind, d in enumerate(num_dim):
        # defining the origin for receptor one = the origin of ordinals
        spec1 = np.zeros(d)

        # sample around the origin
        o1 = np.random.normal(0, 1, (num_samples, d))


        # defining the distance between the two receptor (spectra)
        # the distance is defined as euclidean distance divided by the
        # square root of the number of features
        mu = e / np.sqrt(d)

        # defining the origin for receptor two
        spec2 = np.ones(d) * mu
        # sample around the second origin
        o2 = np.random.normal(mu, 1, (num_samples, d))


        # Nearest Neighbour Classification
        # compute the squared euclidean distance for each sample to both of
        # the origin points for each receptor type
        d1 = np.vstack(
            (np.sum((o1 - spec1) ** 2, 1), np.sum((o1 - spec2) ** 2, 1)))
        d2 = np.vstack(
            (np.sum((o2 - spec1) ** 2, 1), np.sum((o2 - spec2) ** 2, 1)))

        #count where the distance of the sample is smaller to the second
        # origin, than to the first origin
        #vice versa
        miscl[e_ind, d_ind] = np.sum(np.argmin(d1, 0) == 1) + np.sum(
            np.argmin(d2, 0) == 0)

misc2 = np.zeros((len(euc), len(num_dim)))

for e_ind, e in enumerate(euc):
    for d_ind, d in enumerate(num_dim):
        o1 = np.random.normal(0, 3, (num_samples, d))
        mu = e / np.sqrt(d)
        spec2 = np.ones(d) * mu
        o2 = np.random.normal(mu, 3, (num_samples, d))
        d1 = np.vstack((np.sum(o1 ** 2, 1), np.sum((o1 - spec2) ** 2, 1)))
        d2 = np.vstack((np.sum(o2 ** 2, 1), np.sum((o2 - spec2) ** 2, 1)))
        misc2[e_ind, d_ind] = np.sum(np.argmin(d1, 0) == 1) + np.sum(
            np.argmin(d2, 0) == 0)

print miscl / num_samples / 2.
l = ["$\mathbb{R}^{%i}$" % x for x in num_dim]
print l
#pl.rcParams.update({'font.size': 16})
fig = pl.figure(figsize=(6, 4))
ax = fig.add_subplot(111)
ax.plot(np.array(euc), miscl / num_samples / 2.)
pl.legend(l)
#ax.plot(np.array(euc)/3., misc2/num_samples/2.)
ax.set_ylabel('misclassification rate')
pl.title("Euclidean distance-noise-ratio")
ax.set_xlabel('$d_{euc}$/$\sigma_{noise}$', fontsize=16)
fig.tight_layout()
pl.savefig("figures/euclidean.png")

'''
Scatterplot a 2D example of two receptors with different centers and
different distances to each other
'''
#num_samples = 250
#fig = pl.figure(figsize=(9, 4))
#for j, v in enumerate(range(1,3)):
#    for i, e in enumerate(range(10, 0, -3)):
#        spec1 = np.zeros(2)
#
#        # sample around the origin
#        o1 = np.random.normal(0, v, (num_samples, 2))
#
#
#        # defining the distance between the two receptor (spectra)
#        # the distance is defined as euclidean distance divided by the
# square root of the number of features
#        mu = e / np.sqrt(2)
#
#        # defining the origin for receptor two
#        spec2 = np.ones(2) * mu
#        # sample around the second origin
#        o2 = np.random.normal(mu, v, (num_samples, 2))
#
#        d1 = np.vstack((np.sum((o1 - spec1) ** 2, 1), np.sum((o1 - spec2)
# ** 2, 1)))
#        d2 = np.vstack((np.sum((o2 - spec1) ** 2, 1), np.sum((o2 - spec2)
# ** 2, 1)))
#
#        mask1 = np.argmin(d1, 0) == 1
#        mask2 = np.argmin(d2, 0) == 0
#
#        print i, e
#        ax = fig.add_subplot(2, 4, 4 - i + (j-1) * 4)
#
#        ax.plot(o1[np.where(mask1 == 0), 0], o1[np.where(mask1 == 0), 1],
# 'ko', alpha=.25)
#        ax.plot(o2[np.where(mask2 == 0), 0], o2[np.where(mask2 == 0), 1],
# 'bo', alpha=.25)
#        ax.plot(o1[np.where(mask1 == 1), 0], o1[np.where(mask1 == 1), 1],
# 'ro')
#        ax.plot(o2[np.where(mask2 == 1), 0], o2[np.where(mask2 == 1), 1],
# 'mo')
#        #ax.plot(spec1[0], spec1[1], 'yv')
#        #ax.plot(spec2[0], spec2[1], 'gv')
#
#        #ax.plot(np.array(euc), miscl / num_samples / 2.)
#        #ax.plot(np.array(euc)/3., misc2/num_samples/2., 'o')
#
#        if j > 0:
#            pl.title("$d_{euc}$ = %i" % (e))
#            pl.setp( ax.get_xticklabels(), visible=False)
#        if j < 1:
#            ax.set_xlabel('odorant 1')
#
#        if i > 2:
#            ax.set_ylabel('odorant 2')
#        if i < 3:
#            pl.setp( ax.get_yticklabels(), visible=False)
#        ax.set_ylim((-3, 10))
#        ax.set_xlim((-3, 10))
#
#pl.savefig("figures/scatter2.png", bbox_inches='tight')
