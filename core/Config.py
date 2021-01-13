import os, secrets
class Config:
	SECRET_KEY = secrets.token_hex(16)
	SQLALCHEMY_DATABASE_URI = "sqlite:///note.db"
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	MAIL_PORT = 465
	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_USE_SSL = True
	MAIL_USE_TLS = False

