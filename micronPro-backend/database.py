from pymongo import MongoClient
from bson import json_util
import uuid
import json
import logging

logger = logging.getLogger("root")


class MicroDatabase:
    def __init__(self,config):
        database, user, password = (
         
            config["MongoDB"]["user"],
            config["MongoDB"]["password"],
        )
        if (
            database == "YOURURLHERE"
            or user == "YOURUSERHERE"
            or password == "YOURPASSWORDHERE"
        ):
        #     logger.critical("user or password has not been changed!")
        # else:
        #     logger.info("database has been successfully hooked up")
        self.client = MongoClient(
            "mongodb+srv://" + user +":" + password + "@maincluster.btvwv.mongodb.net"
        )
    
    