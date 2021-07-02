from flask import request, Blueprint, Response
import json
import requests
import os
from backend_vars import database_client

job_blueprint = Blueprint("job_blueprint", __name__)


@job_blueprint.route("/new_job", methods=["POST"])
def trigger_new_job():

        job = request.get_json(force=True)["job"]
        # r = requests.post("http://127.0.0.1:5000/",job)
        return {"job": job, "message": "created job"}, 200

@job_blueprint.route("/get_jobs", methods=["POST"])
def get_jobs():
    """{
        type: finished/inprogress
        name:
        }"""
    data = request.get_json(force=True)


