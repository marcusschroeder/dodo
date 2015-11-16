#!/usr/bin/env python
# encoding: utf-8
"""
    When removing a single odorant before using the BE methods, then often
    the result is the same (80%) when compared
    to using the full feature set and finding the top 6 features.
    In 3% of the cases, the results are better, and in ~12% the results are
    worse.

    In this script, I want to look at the 3% better results.
    The odorants that were removed are: butanal, methylbenzoat and 1-pentanol.

    What do they have in common?
"""
import pylab as pl
import numpy as np

from example.hallem.data import Hallem


hallem = Hallem()
data = np.transpose(hallem.response)

but = 78 #butanal
met = 50 #methylbenzoat
pen = 63 #1-pentanol
but_row = data[:, but]
pen_row = data[:, pen]
met_row = data[:, met]
random_row = data[:, 23]

ind = np.arange(len(but_row))
width = 0.2

fig1 = pl.figure(figsize=(20, 12))
ax1 = fig1.add_subplot(211)
ax1.bar(ind, but_row, width, color='b', label='butanal')
ax1.bar(ind + width, pen_row, width, color='y', label='1-pentanol')
ax1.bar(ind + 2 * width, met_row, width, color='r', label='methylbenzoat')
ax1.bar(ind + 3 * width, random_row, width, color='cyan', label='random')
handles, labels = ax1.get_legend_handles_labels()
ax1.legend(handles, labels)
ax1.grid()

ax2 = fig1.add_subplot(212)
ax2.bar(ind, (but_row - np.mean(data, axis=1)) / np.std(data, axis=1), width,
        color='b')
ax2.bar(ind + width, (pen_row - np.mean(data, axis=1)) / np.std(data, axis=1),
        width, color='y')
ax2.bar(ind + 2 * width,
        (met_row - np.mean(data, axis=1)) / np.std(data, axis=1), width,
        color='r')
ax2.bar(ind + 3 * width,
        (random_row - np.mean(data, axis=1)) / np.std(data, axis=1), width,
        color='cyan')
ax2.grid()
pl.savefig("figures/weird_odors_spectra.png")

fig2 = pl.figure()
ax1 = fig2.add_subplot(221)
ax1.plot(but_row, pen_row, '.')
ax1.set_title("but vs pen")

ax2 = fig2.add_subplot(222)
ax2.plot(but_row, met_row, '.')
ax2.set_title("but vs met")

ax3 = fig2.add_subplot(224)
ax3.plot(pen_row, met_row, '.')
ax3.set_title("pen vs met")
# ax1.plot(range(24), data[:, met], alpha=.5, label='met')
# ax1.plot(range(24), data[:, pen], alpha=.5, label='pen')
#
# handles, labels = ax1.get_legend_handles_labels()

# reverse the order
# ax1.legend(handles[::-1], labels[::-1])

pl.savefig("figures/weird_odors.png")
