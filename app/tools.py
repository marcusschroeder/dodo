#!/usr/bin/env python
# encoding: utf-8
import random

ALLOWED_EXTENSIONS = ["csv"]


def generate_job_id():
    return str(random.randint(10000, 99999)) + \
           random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
