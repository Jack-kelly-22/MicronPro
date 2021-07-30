from pymongo import MongoClient,DESCENDING
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
        print("CLIENT:",self.client.database_names())
        logger.info("database responded")
        print(dict(self.client.micronProDB.stats.find_one()))
    
    def update_stats(self,q):
        self.client.micronProDB.stats.update_one(
            {"_id": "stats"},
            {"$set": q},
            upsert=True
        )
        return self.client.micronProDB.stats.find_one()
    
    def get_stats(self):
        for i in self.client.micronProDB.stats.find({'name': 'stats'}):
            print("STATS:" ,i)
            del i['_id']
            return i
        return {"error":"stats not found"}

    def get_user(self, q=""):
        """Retrieves users from pymongo db"""
        return json.loads(
            json.dumps(list(self.client.Users.users.find(q)), default=json_util.default)
        )

    def add_user(self, new_user=None):
        """Adds a new user to pymongo db"""
        logger.info("trying to add new user")

        if len(self.get_user(q={"user_name": new_user["user_name"]})) != 0:
            return {"result": -1, "msg": "username exists"}

        if self.client.Users.users.insert_one(new_user).inserted_id:
            return {"result": 1, "msg": "successfully inserted"}
        else:
            return {"result": -1, "msg": "failed to inserted"}

    def get_users(self):
        """gets all users from database"""
        users = list(self.client.Users.users.find())
        for user in users:
            del user['_id']
        return users

    def get_job(self,q):
        """gets job from database"""
        print("GETTING JOB WITH ID :",q)
        return self.client.micronProDB.jobs.find_one({"job_id": q})

    def get_jobs(self,q):
        """gathers jobs from cloud mongo db"""
        q2={}
        reverse = 'reverse' in q.keys()
        if 'status' in q.keys() and q['status'] == 'In Progress':
            q2["status"]="In Progress"
        if 'status' in q.keys() and q['status'] == 'Complete':
            q2["status"]="Complete"
        if 'page' in q.keys() and int(q['page']) != 1:
            page=int(q['page'])
        else:
            page=0
        if "name" in q.keys():
            q2["name"]=q['name']

        jobs = list(
            self.client.micronProDB.jobs.find(q2).sort("_id",-1).skip(page*_SIZE).limit(_SIZE)
            .limit((page - 1) * _SIZE + _SIZE)
                )
        jobs.reverse() if reverse else print("not reversed")
        for job in jobs:
            del job['_id']
        return jobs
        
    def post_new_config(self,config):
        """posts new config to database"""
        print("config:",config)
        self.client.micronProDB.configs.insert_one(config)
        return self.client.micronProDB.configs.find_one({"config_name": config["config_name"]})

    def review_images(self,job,images):
        """reviews images in database"""
        for frame in job['frame_ls']:
            for image in frame['image_data']:
                if image['img_name'] in images:
                    image['pass']=True
                    job['img_review'].filter(lambda x: x['img_name'] != image['img_name'])
        self.insert_job(job)
        return 200
                    


    def remove_config(self,config_name):
            """posts new config to database"""
            print("config_name:",config_name)
            self.client.micronProDB.configs.delete_one({"config_name": config_name})
            return True
            

            
        
    def get_configs(self,):
            """gets all configs from database"""
            configs = list(self.client.micronProDB.configs.find())
            for conf in configs:
                del conf['_id']
            return configs

    def insert_job(self,job):
        """inserts job into database"""
        print("JOB:",job)
        self.client.micronProDB.jobs.insert_one(job)
        self.client.micronProDB.stats.update_one({"name":"stats"},{'$inc':{'in_progress':1}})
        return self.client.micronProDB.jobs.find_one({"job_name": job["job_name"]})

    def update_job(self,job_id,job,images=None,action=None):
        """updates job in database"""
        print("UPDATING JOB WITH ID :",job_id)
        if folders:
            self.client.micronProDB.jobs.update_one({"job_id": job_id},{'$set':{"folders":folders}})
        self.client.micronProDB.jobs.update_one({"job_id": job_id},job)
        return self.client.micronProDB.jobs.find_one({"job_id": job_id})

    def add_images(job_id,images):
        """adds images to job in database"""
        print("ADDING IMAGES TO JOB WITH ID :",job_id)
        self.client.micronProDB.jobs.update_one({"job_id": job_id},{'$set':{"status":"image_add_queued"}})
        return self.client.micronProDB.jobs.find_one({"job_id": job_id})

    def delete_job(self,job_id):
        """deletes job from database"""
        print("DELETING JOB WITH ID :",job_id)
        self.client.micronProDB.jobs.delete_one({"job_id": job_id})
        return {'msg':'job deleted from database'}

    def reset_stats(self,q):
        """resets stats"""
        self.client.micronProDB.stats.update_one({"name":"stats"},{'$set':q})
        return self.client.micronProDB.stats.find_one({"name":"stats"})