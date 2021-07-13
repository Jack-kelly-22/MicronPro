from pymongo import MongoClient
from bson import json_util
import uuid
import json
import logging
from os import environ
logger = logging.getLogger("root")

_SIZE=20

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
            user = environ.get("user") 
            password = environ.get("password")
            logger.critical("saved?")
        else:
            logger.info("database credentials loaded")
        self.client = MongoClient(
            "mongodb+srv://" + user +":" + password + "@maincluster.btvwv.mongodb.net"
        )
        logger.info("database responded")
    
    def get_jobs(self,name="",reverse=False,page=0):
        """gathers jobs from cloud mongo db"""
        
        jobs = list(
            self.client.Podcasts.allPodcasts.find(q)
            .skip((page - 1) * _SIZE)
            .limit((page - 1) * _SIZE + _SIZE)
                )
        jobs.reverse() if reverse else print("not reversed")
        