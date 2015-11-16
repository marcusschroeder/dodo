#!/usr/bin/env python
# encoding: utf-8
"""
Analysis of Hallem data with backward elimination method.
"""
from dodo._core import plotting
from dodo._core.featureselection import backward_elimination
from dodo.data.data_manager import HallemFromDoOR

def be_hallem(plotpath=None):
	hallem = HallemFromDoOR()
	hallem.load_data()
	hallem.provide_compatible_data()

	data = hallem.response
	feature_names = hallem.odorant_list
	data_names = hallem.or_list
	features = 6

	a = backward_elimination(data)
	feature_list, score = backward_elimination(data)

	title = 'Backward Elimination on Hallem'
	print(title)
	print("Minimal Euclidean distance with %d odorants: %.2f"%(features, score[features]))
	print "Top", str(features), "features"
	print feature_names[feature_list[:features]]

	fig_dendrogram = plotting.plot_fingerprints(title, feature_names[feature_list[:features]],
	                           data[:, feature_list[:features]],
	                           data_names,
	                           path=plotpath)

	fig_distance = plotting.plot_progress_results(score, features, plotpath)

	return {'be_results':a, 
			'feature_list':feature_list, 
			'score':score, 
			'fig_distance':fig_distance, 
			'fig_dendrogram':fig_dendrogram}
