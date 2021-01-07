from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from core.Config import Config
import os

app = Flask(__name__)

app.config.from_object(Config)
# app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///note.db"

bcrypt=Bcrypt(app)
db=SQLAlchemy(app)
login_manager = LoginManager(app)
#check user access to profile if loged in
login_manager.login_view = 'login'

from core import routs
