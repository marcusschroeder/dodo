#!/usr/bin/env python
# encoding: utf-8
from flask.views import MethodView
from flask import render_template, request, Response
import model
import json
import numpy as np
import methodsmap
import computation

class UploadAPI(MethodView):
    def get(self):
        if request.args.get("data_set"):
            m = request.args.get("data_set")
            d = model.load_dataset(m)
            return render_template("data_set.html",
                                   methods=methodsmap.get_available_methods(),
                                   matrix=d)
        else:
            return render_template("upload.html",
                                   methods=methodsmap.get_available_methods())

    def post(self):
        json_data = request.get_json()
        data = json_data["matrix"]
        rows = json_data["rows"]
        columns = json_data["columns"]
        methods = np.array(json_data["methods"])
        stability = json_data["stability"]

        if stability == "" or stability <= 0 or stability >= 150:
            stability = 50

        stability = int(stability)

        features = len(data[0]) if len(data[0]) < 25 else 25

        if len(rows) > 0:
            data = np.delete(data, rows, axis=0)

        if len(columns) > 0:
            data = np.delete(data, columns, axis=1)

        job_id = model.create_job(data)

        computation.batch_compute(job_id, features, methods)
        computation.find_optimal_set(job_id, methods, stability)

        return Response(json.dumps({"job_id": job_id}), 200)