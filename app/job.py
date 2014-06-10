#!/usr/bin/env python
# encoding: utf-8
'''
'''
import os
import json
import numpy as np
from flask.views import MethodView
from flask import (render_template, request,
                   send_from_directory, Response)
from app import methodsmap
import model


class JobAPI(MethodView):
    def get(self, job_id, method=None, features=None):
        if job_id:
            if request.args.get("get_data"):
                path = model.get_abs_path_to_job(job_id)
                return send_from_directory(path, "data.csv")
            if method and "results" in request.path.split("/"):
                path = model.get_abs_path_to_job(job_id)
                return send_from_directory(path, method + ".csv")
            if method and features:
                return self.download_results(features, method, job_id)
            if "optimal" in request.path.split("/"):
                payload = model.load_optimal_results(job_id)
                return Response(json.dumps(payload), status=200)

            return self.render_job(job_id)
        pass

    def render_job(self, job_id):
        matrix = model.load_job_data(job_id)
        optimal = model.load_optimal_results(job_id)
        data = np.transpose(np.array(matrix[1:, 1:], dtype=float))
        row_names = matrix[1:, 0]
        feat_names = matrix[0, 1:]
        table = render_template("job/job_table.html",
                                features=feat_names,
                                rows=row_names,
                                table=data)
        print optimal["methods"]
        return render_template("job.html",
                               job_id=job_id,
                               features=len(feat_names),
                               rows=len(row_names),
                               odorants=feat_names,
                               table=table,
                               noise=np.round(optimal["noise"], 3),
                               stability=optimal["stability"],
                               optimal=optimal["methods"],
                               methods=self.get_methods_used(job_id=job_id))

    def get_methods_used(self, job_id):
        methods = []
        for k, v in methodsmap.get_all_methods().items():
            s = model.get_path_to_results(job_id, k)
            if os.path.isfile(s):
                methods.append([k, v])
        return methods

    def download_results(self, number_features, method, job_id):
        """
        """
        matrix = model.load_job_data(job_id)
        indices = model.get_result_feature_indices(job_id, method,
                                                   number_features)

        indices = np.array(indices, dtype=int) + 1
        indices = np.hstack(([0], indices))

        matrix = matrix[:, indices]
        def generate():
            for row in matrix:
                for i, v in enumerate(row):
                    yield str(v)
                    if i < len(row) - 1:
                        yield ","
                yield '\n'

        r = Response(generate())
        r.mimetype = "text/csv"
        r.headers["Content-Type"] = "text/csv"
        r.headers["Content-Disposition"] = "attachment; filename="\
                                           + job_id + "_" + method + "_" \
                                           + number_features + ".csv"
        return r