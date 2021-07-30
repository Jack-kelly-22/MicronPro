from flask import request, Blueprint, Response
import json
import requests
import os
from time import time
from backend_vars import database_client,workers
from flask_jwt_extended import jwt_required, get_jwt_identity


worker_blueprint = Blueprint("worker_blueprint", __name__)


@worker_blueprint.route("/users", methods=["POST"])
@jwt_required()
def get_users():
    """
    Get all users from the database
    :return:dict of users
    """
    # Get the users from the database
    try:
        users = database_client.get_users()
        # Return the users
        return {'users': users}
    except Exception as e:
        return {'msg': str(e)}


@worker_blueprint.route("/delete", methods=["POST"])
@jwt_required()
def delete():
    """deletes specified folder from the worker"""
    data=request.get_json(force=True)
    print("DATA: ",data)
    if "name" in data.keys() and data["name"] in workers.keys():
        req = requests.post( data['url'] + '/rm_folder',{'folder':data["folder"]})
        return {"msg":"great succuess"}
    else:
        return {"folders": ["no folders found"]}
    

@worker_blueprint.route("/worker_folders", methods=["POST"])
@jwt_required()
def get_folders():
    """should get folders of all active workers return folders and files inside"""
    """get folders on specified worker computer"""
    data = request.get_json(force=True)
    if "name" in data.keys() and data["name"] in workers.keys():
        
        req = requests.post(workers[data["name"]]['url'] + '/folders',data)
        return {"folders":req.json()['folders']}
    else:
        return {"folders": ["no folders found"]}

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
@jwt_required()
def get_workers_online():
    """return dictionary containing urls and names of active workers"""
    # data = request.get_json(force=True)
    print("workers", workers)
    if len(workers.values())==0:
        return {"workers": []}
    return {'workers': list(workers.values())}
