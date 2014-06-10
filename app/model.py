#!/usr/bin/env python
# encoding: utf-8
'''
'''
import ast
import csv
import json
import os
import numpy as np
from flask import current_app, abort
import tools


def __load_csv(path):
    try:
        matrix = []

        sniffer = csv.Sniffer()

        with open(path, "rU") as csvfile:

            # sniff the csv delimiter
            dialect = sniffer.sniff(csvfile.readline())
            csvfile.seek(0)
            reader = csv.reader(csvfile, delimiter=dialect.delimiter)

            for row in reader:
                matrix.append(row)

        matrix = np.asarray(matrix)
        return matrix

    except IOError as inst:
        if inst.errno == 2:
            current_app.logger.error("Csv not found.")
            abort(404)
        else:
            abort(500)
    except Exception as inst:
        current_app.logger.error("Loading of csv failed.")
        abort(500)

def get_path_to_job(job_id):
    return os.path.join(current_app.config["APP_ROOT"],
                        current_app.config['UPLOAD_FOLDER'],
                        str(job_id))

def get_abs_path_to_job(job_id):
    return os.path.join(current_app.config["APP_ROOT"], current_app.config['UPLOAD_FOLDER'],
                        str(job_id))

def get_path_to_csv(job_id):
    return os.path.join(get_path_to_job(job_id), "data.csv")

def get_path_to_results(job_id, method):
    return os.path.join(get_path_to_job(job_id), method + ".csv")


def load_job_data(job_id):
    return __load_csv(get_path_to_csv(job_id))


def load_dataset(name):
    path_to_csv = os.path.join(current_app.config["APP_ROOT"],
                               current_app.config["DATASETS"],
                               name + ".csv")
    return __load_csv(path_to_csv)


def create_job_from_existing(name):
    matrix = load_dataset(name)
    return create_job(matrix)


def create_job(data):
    job_id = tools.generate_job_id()
    save_path = get_path_to_job(job_id)
    os.makedirs(save_path)
    __write_csv(job_id, data)
    return job_id


def __write_csv(job_id, matrix):
    try:
        path_to_csv = get_path_to_csv(job_id)
        with open(path_to_csv, "wb") as fp:
            w = csv.writer(fp, delimiter=",")
            w.writerows(matrix)
    except Exception as inst:
        current_app.logger.error(
            "Writing of csv failed. %s  -- Job: %s" % (inst, job_id))
        abort(500)


def load_results(job_id, method):
    path_to_csv = get_path_to_results(job_id, method)
    matrix = []
    with open(path_to_csv, "rU") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            matrix.append(row)

    matrix = np.asarray(matrix)
    return matrix


def get_result_feature_indices(job_id, method, features):
    features = int(features)
    path_to_csv = get_path_to_results(job_id, method)
    counter = 0
    with open(path_to_csv, "rU") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            if counter == features + 1:
                return ast.literal_eval(row[1])
            counter += 1
    return []


def save_results(job_id, results, method):
    try:
        path_to_csv = get_path_to_job(job_id)
        with open(os.path.join(path_to_csv, method + ".csv"), "wb") as fp:
            w = csv.writer(fp, delimiter=",")
            w.writerows(results)
    except Exception as inst:
        current_app.logger.error(
            "Writing of csv results failed. %s  -- Job: %s" % (inst, job_id))
        abort(500)

def get_path_to_optimal_json(job_id):
    return os.path.join(get_path_to_job(job_id), "optimal.json")

def save_optimal_set(job_id, optimal):
    with open(get_path_to_optimal_json(job_id), 'w') as outfile:
        outfile.write(json.dumps(optimal))

def load_optimal_results(job_id):
    """
        Returns:
            json (dict)
    """
    with open(get_path_to_optimal_json(job_id)) as json_file:
        return json.load(json_file)