#!/usr/bin/env python
# encoding: utf-8

"""
Backward Elimination on dorsal subset of DoOR data.
"""
from example.door import DoOR
from _core import featureselection, plotting

door = DoOR()

# load the responses from the dorsal odorant receptors
data, ors, odorants = door.get_dorsal_data(debug=False)


# perform backward elimination
feature_list, score = featureselection.backward_elimination(data, 6)

# specify number of features
features = 6

print "Top", str(features), "features"
print "Score:", score
print "Odorants:", odorants[feature_list]
print "Indices:", feature_list

title = 'Backward Elimination of DoOr with %i features' % (features)
path = "../figures/door/be/door_be_min_" + str(features) + ".png"
plotting.plot_fingerprints(title,
                           odorants[feature_list],
                           data[:, feature_list],
                           ors,
                           path=None,
                           xlabel="DoOR units")

#path = "../figures/door/be/door_be_progress.png"
#plotting.plot_progress_results(scores, features, path)
#np.savetxt("../results/be_features_door.csv", backward_result[::-1],
# delimiter=";")
