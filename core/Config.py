import os, secrets
os.environ["SECRET_KEY"] = secrets.token_hex(16)
class Config:
	SECRET_KEY = os.environ.get("SECRET_KEY")
	SQLALCHEMY_DATABASE_URI = "sqlite:///note.db"
