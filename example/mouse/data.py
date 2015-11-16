#!/usr/bin/env python
# encoding: utf-8
'''
'''
import numpy as np


class MouseData:
    response = []
    feature_names = []
    cluster = []
    data_names = []

    def __init__(self):
        data = np.load(
            "/Users/marcus/_workspace/repos/olfactory/data/opti.pik")
        self.response = np.array(np.transpose(data['matrix']))
        self.data_names = range(len(self.response))
        self.feature_names = np.array(data['odors'])
        self.cluster = np.array(data['cluster'])