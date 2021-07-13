from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from backend_vars import configFile, log
from endpoints.job_blueprint import job_blueprint
from endpoints.worker_blueprint import worker_blueprint

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config["JWT_SECRET_KEY"] = configFile.get_configuration()["JWT"]["secret"]
    app.register_blueprint(job_blueprint)
    app.register_blueprint(worker_blueprint)
    jwt = JWTManager(app)
    return app
