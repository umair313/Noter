from dotenv import load_dotenv
import os, secrets
load_dotenv()

class Config:
	SECRET_KEY = os.getenv("key")
	SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	MAIL_USERNAME = os.getenv('MAIL_USERNAME')
	MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
	MAIL_PORT = 465
	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_USE_SSL = True
	MAIL_USE_TLS = False