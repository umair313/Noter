from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from core.Config import Config
import os

app = Flask(__name__)

app.config.from_object(Config)


bcrypt=Bcrypt(app)
db=SQLAlchemy(app)
login_manager = LoginManager(app)
#check user access to profile if loged in
login_manager.login_view = 'login'

from core.main.routs import noter_main
from core.users.routs import noter_users
from core.notes.routs import noter_notes

app.register_blueprint(noter_main)
app.register_blueprint(noter_users)
app.register_blueprint(noter_notes)

