
import bcrypt
import uuid
import logging
from flask import request, Blueprint, jsonify
from datetime import timedelta
from flask_jwt_extended import create_access_token,get_jwt_identity
from flask_jwt_extended import create_refresh_token,jwt_required
from backend_vars import database_client, log


user_blueprint = Blueprint("user_blueprint", __name__)

logger = logging.getLogger("root")


def new_user_template(user_name):
    """returns dictionary representing a user for creating new user document"""
    user = {
        "user_id": str(uuid.uuid1()),
        "user_name": user_name,
    }
    return user


def create_user_dataframe(data):
    """creates a user dataframe from a dictionary"""
    user_name = data["user_name"]
    password = data["password"]

    password = data["password"]

    if data['user_name'] is None:
        logger.info("invalid user_name")
        return {"msg": "invalid user_name"}, 400

    salt = bcrypt.gensalt()
    pass_hash = bcrypt.hashpw(str.encode(password), salt)
    user = new_user_template(user_name)
    user["pass_hash"] = pass_hash.decode()

    return {"user": user}, 200


@user_blueprint.route("/login", methods=["POST"])
def try_login():
    if request.method == "POST":
        log.info("trying to login")
        data = request.get_json(force=True)
        curr_user = database_client.get_user({"user_name": data.get("user_name")})
        if len(curr_user) == 0:
            return {"msg": "no user found"}, 404

        curr_user = curr_user[0]
        if not bcrypt.checkpw(
            str.encode(data["password"]), str.encode(curr_user["pass_hash"])
        ):
            return {"msg": "password don't match"}, 400

        # clean up user data for less exposure
        curr_user.pop("pass_hash", None)
        curr_user.pop("_id", None)

        access_token = create_access_token(identity=curr_user, fresh=timedelta(minutes=15))
        refresh_token = create_refresh_token(identity=curr_user)
        return {"access_token": access_token,
                "refresh_token": refresh_token,
                "user": curr_user}, 200




@user_blueprint.route("/newUser", methods=["POST"])
def new_user():
    if request.method == "POST":
        log.info("new user")
        data = request.get_json(force=True)

        result =create_user_dataframe(data)
        if 200 not in result:
            return result

        user = result[0]["user"]
        log.info("successfully parsed new user information")

        result = database_client.add_user(user)
        if result["result"] == -1:
            return {"msg": result["msg"]}, 404

        log.info("successfully added new user")
        # clean up user data for less exposure
        user.pop("_id", None)
        user.pop("pass_hash", None)
        access_token = create_access_token(identity=user)
        return {
            "msg": "user successfully added",
            "access_token": access_token,
            "user": user,
        }, 200


@user_blueprint.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity, fresh=False)
    return jsonify(access_token=access_token)