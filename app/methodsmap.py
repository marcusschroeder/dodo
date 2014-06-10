from flask import current_app

backward_elimination = {"key": "be", "name": "Backward Elimination"}
forward_selection = {"key": "fs", "name": "Forward Selection"}
gurobi = {"key": "gu", "name": "Gurobi"}
pipelining = {"key": "pi", "name": "BE + Gurobi"}


def get_available_methods():
    if current_app.config["GUROBI"]:
        return get_all_methods()
    else:
        return {i["key"]: i["name"] for i in [
            backward_elimination,
            forward_selection]}


def get_all_methods():
    return {i["key"]: i["name"] for i in [
        backward_elimination,
        forward_selection,
        gurobi,
        pipelining]}