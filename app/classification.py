#!/usr/bin/env python
# encoding: utf-8
'''
'''
from _core.analysis import nearest_neighbour_classification
from flask.views import MethodView
from flask import (render_template, request, Response, json)

class ClassificationAPI(MethodView):
    def get(self):
        return render_template('classification.html')

    def post(self):
        json_data = request.get_json()

        data = json_data["data"]
        reference = json_data["reference"]

        x = nearest_neighbour_classification(reference, data)

        def generate():
            yield json.dumps(x)

        r = Response(generate())
        r.mimetype = "application/json"
        r.headers["Content-Type"] = "application/json"
        return r