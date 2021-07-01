from pymongo import MongoClient
from bson import json_util
import uuid
import json
import logging

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
        else:
            logger.info("database credentials loaded")
        self.client = MongoClient(
            "mongodb+srv://" + user +":" + password + "@maincluster.btvwv.mongodb.net"
        )
        logger.info("database responded")
    
    def update_job(job):