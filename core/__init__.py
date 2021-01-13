from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from core.Config import Config


bcrypt=Bcrypt()
db=SQLAlchemy()
# no track modification
SQLALCHEMY_TRACK_MODIFICATIONS = False
login_manager = LoginManager()
mail=Mail()

#check user access to profile if loged in
login_manager.login_view = 'users.login'

def create_app(config_class=Config):

	app = Flask(__name__)
	app.config.from_object(Config)

	bcrypt.init_app(app)
	db.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)
	
	from core.main.routs import noter_main
	from core.users.routs import noter_users
	from core.notes.routs import noter_notes
	from core.errors.handlers import errors

	app.register_blueprint(noter_main)
	app.register_blueprint(noter_users)
	app.register_blueprint(noter_notes)
	app.register_blueprint(errors)

	return app

def create_db(app,db):
	app.app_context().push()
	db.create_all()



