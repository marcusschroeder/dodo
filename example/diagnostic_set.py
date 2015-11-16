#!/usr/bin/env python
# encoding: utf-8
'''
Compute the euclidean distance of the reference set (deBruyne) on Hallem and
DoOR.
'''
import numpy as np
from scipy.spatial import distance

from example.hallem.data import Hallem
from example.dorsal_door import DoOR


hallem = Hallem()
data, or_list, odorants = hallem.get_reference_set()

title = "Diagnostic set from DeBruyne 2001 on Hallem"
path = "figures/debruyne_hallem.png"
#plotting.plot_fingerprints(title, odorants, data, or_list, path)
print "Euclidean distance Hallem:", np.min(distance.pdist(data, 'euclidean'))

door = DoOR()
door_data, door_ors, door_odorants = door.get_dorsal_reference_data()

print "Euclidean distance DoOR:", np.min(
    distance.pdist(door_data, 'euclidean'))
title = "Diagnostic set from DeBruyne 2001 on dorsal DoOR"
path = "figures/debruyne_door.png"
#plotting.plot_fingerprints(title, door_odorants, door_data, door_ors, path)