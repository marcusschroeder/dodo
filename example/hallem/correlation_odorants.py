#!/usr/bin/env python
# encoding: utf-8
"""

Just plotting the hallem rows (Odorants) as a boxplot to get a look and
feel which odorant might carry the most/the least information

"""
import pylab as pl
import numpy as np
from scipy import stats

from example.hallem.data import Hallem
import example


hallem = Hallem()
matrix = hallem.response
corr = example.correlation(matrix)
strong_corr = corr[corr[:, 2] > 0.9]

pl.figure(figsize=(6, 5), dpi=320)
n, bins, patches = pl.hist(corr[:, 2], bins=20, histtype='stepfilled',
                           normed=1)
#plot gauss curve
print np.min(corr[:, 2]), np.max(corr[:, 2])
mu, sigma = stats.norm.fit(corr[:, 2])
x_curve = np.arange(-1, 1, 0.01)
pl.plot(x_curve, stats.norm.pdf(x_curve, mu, sigma), 'r', lw=3)

#fix scaling
nmax = np.max(n)
scale = np.max(n * np.diff(bins))
n_ticks = 6.
pl.yticks(np.arange(nmax / n_ticks, nmax * (1 + 2 / n_ticks), nmax / n_ticks),
          np.round(np.arange(scale / n_ticks, scale * (1 + 2 / n_ticks),
                             scale / n_ticks), 2))

pl.grid()
pl.xlim(-1, 1)
pl.title("Correlation between odorants")
pl.xlabel("Pearson Correlation")
pl.ylabel("Frequency")
pl.legend([r"$\mathcal{N}(\mu=%1.2f,\sigma^2=%1.2f)$" % (mu, sigma)])
pl.savefig("../figures/hallem/correlation/odorants/pearson_odorants.png")

#
#sort = np.argsort(np.abs(strong_corr[:, 2]))
#
#for i in strong_corr[sort]:
#    a = np.var(hallem.response[i[0], :])
#    b = np.var(hallem.response[i[1], :])
#
#    # printing results as table
#    if a > b:
#        print "\t \\textbf{%s} & %s & %1.2f \\\\ \\hline" % (hallem
# .odorant_list[i[0]], hallem.odorant_list[i[1]], i[2])
#    else:
#        print "\t %s & \\textbf{%s} & %1.2f \\\\ \\hline" % (hallem
# .odorant_list[i[0]], hallem.odorant_list[i[1]], i[2])
#
#
## plot the spectra of of two correlated odorants against each other
#for index, value in enumerate(strong_corr[sort]):
#    o1 = value[0]
#    o2 = value[1]
#
#    o1_name = hallem.odorant_list[o1]
#    o2_name = hallem.odorant_list[o2]
#
#    c = round(value[2], 3)
#
#    fig = pl.figure(figsize=(8.7, 4.2))
#    pl.title(o1_name + " against " + o2_name + "| correlation=" + str(c))
#
#    o1_spec = matrix[o1]
#    o2_spec = matrix[o2]
#
#    sorting = np.argsort(o1_spec)
#
#    ax1 = pl.subplot2grid((1, 4), (0, 0), colspan=4)
#    ax1.bar(np.arange(0.2, len(o1_spec) + .2, 1), o1_spec[sorting], width=0
# .3, color='b', alpha=.6)
#    ax1.bar(np.arange(.5, len(o2_spec) + .5, 1), o2_spec[sorting], width=0
# .3, color='r', alpha=.6)
#    ax1.get_xaxis().set_ticks(np.arange(0.5, len(o1_spec), 1))
#    ax1.set_xticklabels(hallem.or_list[sorting], rotation=75)
#    ax1.legend((o1_name, o2_name), loc=2)
#    ax1.set_xlabel("ORs")
#    ax1.set_ylabel("spikes/s")
#    ax1.grid()
#
#    fig.tight_layout()
#    #ax2 = pl.subplot2grid((2, 4), (0, 3), colspan=1)
#    #ax2.plot(o1_spec, o2_spec, 'o')
#    #ax2.grid()
#    #ax2.set_xlabel(o1_name)
#    #ax2.set_ylabel(o2_name)
#
#    #sorting = np.argsort(o2_spec)
#    #
#    #ax3 = pl.subplot2grid((2, 4), (1, 1), colspan=3)
#    #ax3.bar(np.arange(0, len(o1_spec), 1), o1_spec[sorting], width=0.3,
# color='b', alpha=.6)
#    #ax3.bar(np.arange(.3, len(o2_spec) + .3, 1), o2_spec[sorting], width=0
# .3, color='r', alpha=.6)
#    #ax3.get_xaxis().set_ticks(np.arange(0.15, len(o1_spec), 1))
#    #ax3.set_xticklabels(hallem.or_list[sorting])
#    #ax3.legend((o1_name, o2_name), loc=2)
#    #ax3.set_xlabel("ORs")
#    #ax3.set_ylabel("spikes/s")
#    #ax3.grid()
#    #
#    #ax4 = pl.subplot2grid((2, 4), (1, 0), colspan=1)
#    #ax4.plot(o2_spec, o1_spec, 'o')
#    #ax4.grid()
#    #ax4.set_xlabel(o2_name)
#    #ax4.set_ylabel(o1_name)
#
#    pl.savefig("../figures/hallem/correlation/odorants/" + str(c) + "_" +
# o1_name + "_" + o2_name + ".png")
#
#
#
#    #
#    ## what happens, if we perform be after we remove some redundant data,
# e.g. remove those odorants which
#    ## have a high correlation with another odorant
#    #
#    #max_corr = strong_corr[np.argsort(strong_corr[:, 2])[-2]] # select the
# pair with the strongest pos. correlation
#    #print max_corr
#    #
#    #o1_name = hallem.odorant_list[max_corr[0]]
#    #o2_name = hallem.odorant_list[max_corr[1]]