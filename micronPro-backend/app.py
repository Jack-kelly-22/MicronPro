from flask_jwt_extended import JWTManager
from backend_vars import configFile, log

def create_app():
    app = Flask(__name__)

    CORS(app)
    app.config["JWT_SECRET_KEY"] = configFile.get_configuration()["JWT"]["secret"]
    app.register_blueprint(login_blueprint)
    jwt = JWTManager(app)
    

    return app
