from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as serializer
from core import app,db,login_manager

@login_manager.user_loader
def load_user(user_id):
	return Users.query.get(int(user_id))


class Users(db.Model,UserMixin):
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(20),unique=True,nullable=False)
	email = db.Column(db.String(120),unique=True,nullable=False)
	password = db.Column(db.String(20),nullable=False)
	join_date= db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
	last_login_dt= db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
	notes = db.relationship('Notes',backref='author',lazy=True)
	
	def gen_token(self,expire_sec=1800):
		s= serializer(app.config["SECRET_KEY"], expire_sec)
		return s.dumps({'user_id':self.id}).decode('utf-8')
	@staticmethod
	def verify_token(token):
		s=serializer(app.config["SECRET_KEY"])
		try:
			user_id = s.loads(token)['user_id']
		except:
			return None
		return Users.query.get(user_id)

	def __repr__(self):
		return f"Users('{self.id}','{self.username}','{self.email}')"

class Notes(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
	title = db.Column(db.String(120),nullable=False)
	cd= db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
	md= db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
	content = db.Column(db.Text,nullable=False)

	def __repr__(self):
		return f"Notes('{self.id}','{self.title}','{self.cd}')"




