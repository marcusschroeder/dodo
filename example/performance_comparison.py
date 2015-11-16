#!/usr/bin/env python
# encoding: utf-8
'''
'''
import csv
import numpy as np
import os
import pylab as pl


def load_csv(file):
    path_to_csv = os.path.join(os.path.dirname(__file__), file)
    d = []
    with open(path_to_csv) as csvfile:
        reader = csv.reader(csvfile, delimiter=';')

        for row in reader:
            d.append(row)

    d = np.asarray(d)
    return np.asarray(d[1:, 1:], dtype=float)


gscore = load_csv("/Users/marcus/Desktop/results/corr_50_pipelined_scores_pew.csv")
gtimes = load_csv("/Users/marcus/Desktop/results/corr_50_pipelined_times_pew.csv")

bscore = load_csv("results/be_scores_gauss.csv")
btimes = load_csv("results/be_times_gauss.csv")

np.set_printoptions(suppress=True, precision=6)

b1 = np.mean(btimes[:, 1:] / btimes[:, :-1], axis=0)
b2 = np.mean(btimes[1:, :] / btimes[:-1, :], axis=1)
g1 = np.mean(gtimes[:, 1:] / gtimes[:, :-1], axis=0)
g2 = np.mean(gtimes[1:, :] / gtimes[:-1, :], axis=1)

bs1 = np.mean(bscore[:, 1:] / bscore[:, :-1], axis=0) - 1
bs2 = np.mean(bscore[1:, :] / bscore[:-1, :], axis=1) - 1
gs1 = np.mean(gscore[:, 1:] / gscore[:, :-1], axis=0) - 1
gs2 = np.mean(gscore[1:, :] / gscore[:-1, :], axis=1) - 1

print bs1
print bs2
print gs1
print gs2

print "be features"
print b1
print
print "be data"
print b2
print
print "g features"
print g1
print
print "g data"
print g2
print
print "gtimes"
print gtimes
print "btimes"
print btimes
print
print "times ratio"
print gtimes / btimes
print "min:%1.2f, max: %1.2f, mean: %1.2f" % (
    np.min(gtimes / btimes), np.max(gtimes / btimes), np.mean(gtimes / btimes))
print
print "bscore"
print bscore
print
print "gscore"
print gscore
print
print "score ratio"
print gscore / bscore
print "min:%1.2f, max: %1.2f, mean: %1.2f" % (
    np.min(gscore / bscore), np.max(gscore / bscore), np.mean(gscore / bscore))
print "avg. g scores/be scores"
print "axis=0"
print np.mean(gscore, axis=0) / np.mean(bscore, axis=0)
print "axis=1"
print np.mean(gscore, axis=1) / np.mean(bscore, axis=1)

print "times ratio"
print gtimes / btimes

scale = np.array([1, 2, 4, 8, 16])

print b1
#print np.cumprod(g2)

pl.figure()
pl.plot(scale, np.hstack(([1], np.cumprod(b1))), 'b', linewidth=2)
pl.plot(scale, np.hstack(([1], np.cumprod(b2))), 'b--', linewidth=2)
pl.plot(scale, np.hstack(([1], np.cumprod(g1))), 'g', linewidth=2)
pl.plot(scale, np.hstack(([1], np.cumprod(g2))), 'g--', linewidth=2)
pl.plot(np.arange(1, 16, 0.2), np.arange(1, 16, 0.2) ** 2, 'm', linewidth=3,
        alpha=.3)
pl.plot(np.arange(1, 16, 0.2), np.arange(1, 16, 0.2) ** 3, 'r', linewidth=3,
        alpha=.3)
pl.legend(["BE feature", "BE data", "Gurobi feature", "Gurobi data", "$n^2$",
           "$n^3$"], fancybox=True, loc=0)
pl.xlim(1, 16)
pl.ylim(0, 1000)
pl.title("Slope of running time of Gurobi and BE")
pl.xlabel("Factor by which number of features or data is increased")
pl.ylabel("Average factor by which running time increases")
pl.savefig("figures/times.png")


