from pymongo import MongoClient
from bson import json_util
import uuid
import json
import logging
from os import environ
logger = logging.getLogger("root")


class MicroDatabase:
    def __init__(self,config):
        user, password = (
         
            config["MongoDB"]["user"],
            config["MongoDB"]["password"],
        )
        if (
            user == "YOURUSERHERE"
            or password == "YOURPASSWORDHERE"
        ):
            logger.critical("user or password has not been changed!")
            user = environ.getenv("user") 
            password = environ.getenv("password")
            logger.critical("saved?")
        else:
            logger.info("database credentials loaded")
        self.client = MongoClient(
            "mongodb+srv://" + user +":" + password + "@maincluster.btvwv.mongodb.net"
        )
        logger.info("database responded")
    
    