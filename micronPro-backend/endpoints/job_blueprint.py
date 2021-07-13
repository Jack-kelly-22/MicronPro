from flask import request, Blueprint, Response
import json
import requests
import os
from backend_vars import database_client,workers

job_blueprint = Blueprint("job_blueprint", __name__)



@job_blueprint.route("/new_job", methods=["POST"])
def trigger_new_job():

        job = request.get_json(force=True)

        r = requests.post("http://127.0.0.1:8000"+"/new_job",job)
        job = database_client.insert_job(job)
        return {"message": "created job"}, 200


@job_blueprint.route("/get_stats", methods=["POST"])
def get_stats():
    stats = database_client.get_stats()
    stats["workers_online"]=len(list(workers.keys()))
    return {"stats":stats}

@job_blueprint.route("/get_jobs", methods=["POST"])
def get_jobs():
    """{
        status: finished/inprogress
        name:
        time: epoch
        }"""
    data = request.get_json(force=True)
    jobs = database_client.get_jobs(data)
    return {"jobs":jobs}

@job_blueprint.route("/new_config", methods=["POST"])
def new_config():
    print("DATA", request.get_json(force=True))
    data = request.get_json(force=True)
    database_client.post_new_config(data['config'])
    return {"message": "created config"}, 200


@job_blueprint.route("/remove_config", methods=["POST"])
def remove_config():
    print("DATA", request.get_json(force=True))
    data = request.get_json(force=True)
    if database_client.remove_config(data['config_name']):
        return {"message": "removed config"}, 200

@job_blueprint.route("/get_configs", methods=["POST"])
def get_configs():
    return {"configs": database_client.get_configs()}
   
