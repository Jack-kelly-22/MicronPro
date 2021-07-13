from flask import request, Blueprint, Response
import json
import requests
import os
from time import time
from backend_vars import database_client,workers,WORKER_URL


worker_blueprint = Blueprint("worker_blueprint", __name__)



@worker_blueprint.route("/worker_folders", methods=["POST"])
# @jwt_required()
def get_folders():
    """should get folders of all active workers return folders and files inside"""
    """get folders on specified worker computer"""
    data = request.get_json(force=True)
    req = requests.post(data["url"] + '/folders',data)
    print("JSON: ",req.json())
    return {"folders":req.json()['folders']}

@worker_blueprint.route("/hello", methods=["POST"])
# @jwt_required()
def worker_ping():
    """used by workers to signal online"""
    data = request.get_json(force=True)
    new_worker = {'name': data['self_name'], 'url': data['self_url'],'time':time()}
    workers[new_worker['name']] = new_worker
    for worker in workers.keys():
        if workers[worker]['time'] < time() - 60:
            del workers[worker]
    print("ALIVE WORKER", workers)
    return {"response":"success"}


@worker_blueprint.route("/workers_online", methods=["POST"])
# @jwt_required()
def get_workers_online():
    """return dictionary containing urls and names of active workers"""
    # data = request.get_json(force=True)
    print("workers", workers)
    return {'workers': list(workers.values())}
