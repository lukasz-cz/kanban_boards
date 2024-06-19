import os
import yaml
from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager, UserMixin
from bson.objectid import ObjectId
from flask_argon2 import Argon2

mongo = PyMongo()
argon2 = Argon2()

def load_config(app, config_filename):
    with open(config_filename) as config_file:
        config = yaml.safe_load(config_file)
        for key, value in config.items():
            app.config[key] = value

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')

    config_name = os.getenv('FLASK_CONFIG', 'development')
    config_filename = os.path.join(app.root_path, '..', 'config', f'{config_name}.yaml')
    load_config(app, config_filename)

    mongo.init_app(app)
    argon2.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User
        
    @login_manager.user_loader
    def user_loader(user_id):
        user_data = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        if user_data is not None:
            return User(str(user_data["_id"]), user_data["username"], user_data["email"], user_data["password"])
        return None

    from .auth import auth as auth_blueprint
    from .main import main as main_blueprint
    
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)

    return app
