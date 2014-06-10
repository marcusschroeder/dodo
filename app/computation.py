#!/usr/bin/env python
# encoding: utf-8
'''
'''
import ast
from flask import current_app, abort
import model
import numpy as np
import methodsmap
from _core import featureselection, validation

try:
    from _core import gurobi, pipelining
except:
    print "Gurobi loading failed"

def batch_compute(job_id, features, methods):

    current_app.logger.debug("Computation for " + job_id)
    matrix = model.load_job_data(job_id)

    data = np.asarray(matrix[1:, 1:], dtype=float)
    for m in methods:
        if m == methodsmap.backward_elimination["key"]:
            try:
                f, r = featureselection.backward_elimination(data)
                f = [str(f[:i].tolist()) for i in range(features)]
                save_results(job_id, f[:features], r[:features],
                                  features, m)
            except Exception as inst:
                current_app.logger.error(inst)
                abort(500)
        elif m == methodsmap.forward_selection["key"]:
            try:
                f, r = featureselection.forward_selection(data)
                f = [str(f[:i].tolist()) for i in range(features)]
                save_results(job_id, f[:features], r[:features],
                                  features, m)
            except Exception as inst:
                current_app.logger.error(inst)
                abort(500)
        elif m == methodsmap.gurobi["key"]:
            try:
                f, r = gurobi.optimize(data,
                                       number_features=features,
                                       batch=True)

                #convert arrays to string
                f = [str(i.tolist()) for i in f]
                save_results(job_id, f, r, features, m)
            except Exception as inst:
                current_app.logger.error(inst)
                abort(500)
        elif m == methodsmap.pipelining["key"]:
                threshold = features + 1 if len(data[0]) > features else len(data[0])
                f, r = pipelining.optimize(data,
                                       number_features=features,
                                       threshold=threshold,
                                       corr=0.94,
                                       batch=True)
                #convert arrays to string
                f = [str(i.tolist()) for i in f]
                save_results(job_id, f, r, features, m)
            #except Exception as inst:
            #    current_app.logger.error(inst)
            #    abort(500)
        else:
            pass

def find_optimal_set(job_id, methods, stability):
    current_app.logger.debug("computing optimal results")
    data = model.load_job_data(job_id)
    data = np.array(data[1:, 1:], dtype=float)

    #### compute the std per recepter and find the maximal value
    max_std = np.max(np.std(data, axis=1))

    #### range of the data
    r = np.max(data) - np.min(data) #range

    #### how large is the max_std compared to the range r

    #### define the default noise level
    noise = max_std * max_std / r

    #### this is the max level a user can get, but he requested maybe just a fraction of it:
    noise = noise * stability/100

    #### now lets find the sets where the accuracy is larger than 99%

    optimal = {}
    optimal["noise"] = noise
    optimal["stability"] = stability
    optimal["methods"] = {}
    for m in methods:
        results = model.load_results(job_id, m)
        for i, v in enumerate(results):
            if i > 1:
                sub = np.array(ast.literal_eval(v[1]))
                acc = validation.compute_accuracy(data=data, sample_size=100, sd=noise,
                                                  sub=sub)
                if acc >= 0.99:
                    optimal["methods"][m] = i-1
                    break

    model.save_optimal_set(job_id, optimal)

def save_results(job_id, features, scores, nf, method):
    head = ["features"]
    head.append("ids")
    head.append("score")

    data = zip(range(nf), features, scores)
    data = np.vstack((head, data))
    model.save_results(job_id, data, method)