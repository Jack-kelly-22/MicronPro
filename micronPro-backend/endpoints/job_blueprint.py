from flask import request, Blueprint, Response
import json
import requests
import os
from backend_vars import database_client,workers
from flask_jwt_extended import jwt_required, get_jwt_identity
import uuid

job_blueprint = Blueprint("job_blueprint", __name__)



@job_blueprint.route("/new_job", methods=["POST"])
# @jwt_required()
def trigger_new_job():
        job = request.get_json(force=True)
        print("typed job: ",type(job))
        job_id = str(uuid.uuid4())
        job['job']["job_id"] = job_id
        job['job']["out_path"] = "/job-data/"
        job['job']["version"] = "3.0.3"
        job['job']["num_images"] = 0
        job['job']['simple'] = True
        job['job']['progress'] = 0
        #print("JOB: ", job)
        requests.post(workers[job['job']['worker_name']]['url']+"/new_job",json=job['job'])
        database_client.insert_job(job['job'])
        return {"message": "created job"}, 200


@job_blueprint.route("/delete_job", methods=["POST"])
@jwt_required()
def delete_job():
        data = request.get_json(force=True)
        if "job_id" in data.keys() and database_client.delete_job(data['job_id']):
                requests.post(workers[data['worker_name']]['url']+"/delete_job",json=data)
                return {"message": "deleted job"}, 200
        else:
                return {"message": "job not found"}, 212


@job_blueprint.route("/get_stats", methods=["POST"])
@jwt_required()
def get_stats():
    stats = database_client.get_stats()
    stats["workers_online"]=len(list(workers.keys()))
    return {"stats":stats}

@job_blueprint.route("/get_jobs", methods=["POST"])
@jwt_required()
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
@jwt_required()
def new_config():
    print("DATA", request.get_json(force=True))
    data = request.get_json(force=True)
    database_client.post_new_config(data['config'])
    return {"message": "created config"}, 200


@job_blueprint.route("/remove_config", methods=["POST"])
@jwt_required()
def remove_config():
    print("DATA", request.get_json(force=True))
    data = request.get_json(force=True)
    if database_client.remove_config(data['config_name']):
        return {"message": "removed config"}, 200

@job_blueprint.route("/get_configs", methods=["POST"])
@jwt_required()
def get_configs():
    return {"configs": database_client.get_configs()}
   
