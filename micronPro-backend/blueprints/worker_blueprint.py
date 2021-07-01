from flask import request, Blueprint, Response
import json
import requests
import os
from backend_vars import database_client,workers

job_blueprint = Blueprint("worker_blueprint", __name__)



@job_blueprint.route("/get_image_folders", methods=["POST"])
@jwt_required()
def get_folders():
    """get folders on specified worker computer"""
    data = request.get_json(force=true)
    