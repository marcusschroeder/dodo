#!/usr/bin/env python
# encoding: utf-8
import os
from flask import Flask, render_template, request
from flask.wrappers import Response
from app.classification import ClassificationAPI
from job import JobAPI
from upload import UploadAPI
from werkzeug.contrib.fixers import ProxyFix
from email.mime.text import MIMEText
from subprocess import Popen, PIPE


def module_exists(module_name):
    try:
        __import__(module_name)
    except ImportError:
        return False
    else:
        return True

app = Flask(__name__)

app.config.from_pyfile("config.py")
try:
    app.config.from_envvar("CONFIG")
except RuntimeError as inst:
    app.logger.info("No development config specified. Use production config.")

app.config["GUROBI"] = module_exists("gurobipy")
app.config["DATASETS"] = "app/static/datasets/"
app.config["JQUERY"] = "plugins/jquery-2.0.3.min.js"
app.config["FEEDBACK_ME_JS"] = "plugins/feedback_me/js/jquery.feedback_me.js"
app.config["FEEDBACK_ME_CSS"] = "plugins/feedback_me/css/jquery.feedback_me.css"
app.config["JQUERY_UI_JS"] = "plugins/jquery-ui.js"
app.config["JQUERY_UI_CSS"] = "plugins/jquery-ui.css"
app.config["BOOTSTRAP_JS"] = "plugins/bootstrap/js/bootstrap.min.js"
app.config["BOOTSTRAP_CSS"] = "plugins/bootstrap/css/bootstrap.min.css"
app.config["FOOTABLE_JS"] = "plugins/FooTable-2/js/footable.js"
app.config["FOOTABLE_JS_SORT"] = "plugins/FooTable-2/js/footable.sort.js"
app.config["FOOTABLE_CSS"] = "plugins/FooTable-2/css/footable.core.css"
app.config["D3_JS"] = "plugins/d3.v3.min.js"
app.config["UPLOAD_FOLDER"] = "results"
app.config["MAIL"] = os.getenv("OLFACTORY_MAIL")

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/fs")
def feature_selection():
    # TODO: add more datasets
    datasets = {"hallem2006": "Hallem, 2006",
                "dorsal_door": "Dorsal Door"}
    return render_template('featureselection.html', datasets=datasets)

@app.route("/feedback", methods=["POST"])
def feedback():
    # TODO 01.03.: find a better mailer solution
    if request.form.get("name") and request.form.get(
            "email") and request.form.get("message"):
        msg = MIMEText(request.form.get("name") + "(" + request.form.get(
            "email") + ") send you:" + request.form.get("message"))
        msg["From"] = request.form.get("email")
        msg["To"] = app.config["MAIL"]
        msg["Subject"] = "Olfactory App"
        p = Popen(["/usr/sbin/sendmail", "-t"], stdin=PIPE)
        p.communicate(msg.as_string())

    return Response(status=204)

classification_view = ClassificationAPI.as_view("classification")
app.add_url_rule('/cs', view_func=classification_view, methods=["GET", "POST"])

upload_view = UploadAPI.as_view('upload')
app.add_url_rule('/upload', view_func=upload_view, methods=["GET", "POST"])

job_view = JobAPI.as_view('job')
app.add_url_rule('/job/<job_id>', view_func=job_view, methods=["GET", "PUT"])
app.add_url_rule('/job/<job_id>/optimal', view_func=job_view, methods=["GET"])
app.add_url_rule('/job/<job_id>/method/<method>/features/<features>',
                 view_func=job_view, methods=["GET"])
app.add_url_rule('/job/<job_id>/method/<method>/results', view_func=job_view,
                 methods=["GET"])


@app.route("/about")
def about():
    return render_template("about.html")


@app.errorhandler(400)
def bad_request(e):
    app.logger.debug(e)


@app.errorhandler(404)
def page_not_found(e):
    app.logger.error(e)
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    app.logger.error(e)
    return render_template('errors/500.html'), 500

app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
    app.run()
