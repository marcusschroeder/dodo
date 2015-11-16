#!/usr/bin/env python
# encoding: utf-8
from example.door import DoOR
from _core import plotting

door = DoOR()
data, ors, odorants = door.get_dorsal_data()

#feature_list = np.array([5, 13, 18, 39, 57, 58, 61, 72, 74, 77, 81, 85, 91,
# 98, 112, 118, 141, 202, 212, 214]) #20
#feature_list = np.array([5, 57, 58, 72, 74, 77, 81, 98, 198, 214]) #10
#feature_list = [57, 58, 72, 74, 77, 81, 98, 141, 214] #9
feature_list = [5, 9, 16, 58] #4

title = "Gurobi on DoOR with " + str(len(feature_list)) + " features"

path = "../figures/door/gurobi/gurobi_" + str(len(feature_list)) + ".png"

plotting.plot_fingerprints(title, odorants[feature_list],
                           data[:, feature_list], ors, path, "DoOR units")


# subset = data[:, feature_list]
#
# stds = np.std(subset, axis=0)
# std_sorting = np.array(np.argsort(stds))
#
# goods = odorants[feature_list[std_sorting]]
#
# print goods
#
# for i, v in enumerate(goods):
#     print v[0], "\t", str(((stds[std_sorting])[i])).replace(".", ",")
