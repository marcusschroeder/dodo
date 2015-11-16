#!/usr/bin/env python
# encoding: utf-8
"""
Forward Selection on dorsal subset of DoOR data.
"""
from example.door import DoOR
from _core import featureselection

door = DoOR()

data, ors, odorants = door.get_dorsal_data()

features = 10
feature_list, score = featureselection.forward_selection(data, features)

print "Top", str(features), "features"
print "Score:", score
print feature_list
print odorants[feature_list]

# title = 'Backward Elimination of DoOr with %i features' % (features)
# path = "../figures/dorsal_door/be/door_be_progress.png"
# toolbox.plot_progress_results(forward_results, features, path)
# path = "../figures/dorsal_door/be/door_be_min_" + str(features) + ".png"
# toolbox.plot_fingerprints(title, odorants[sub_list], data[:, sub_list],
# ors, path, "DoOR units")
