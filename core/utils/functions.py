from core import db,mail,bcrypt
from core.models import Users,Notes
from flask_mail import Message


def register_user(user):
	'''
		Function will take user object as paramiter 
		add user into database. 
	'''
	db.session.add(user)
	db.session.commit()
	return

def user_exit_by_username(username):
	user = Users.query.filter_by(username=username).first()
	if user:
		return True
	return False

def user_exit_by_email(email):
	user = Users.query.filter_by(email=email).first()
	if user:
		return True
	return False
def get_user(email):
	'''
	return user if found with email
	'''
	return Users.query.filter_by(email=email).first()

def get_notes(id):
	return Notes.query.filter_by(user_id=id).order_by(Notes.cd.desc())

def update_user_data(user,paramiter,value):
	if paramiter == 'last_login_dt':
		user.last_login_dt = value
		db.session.commit()
	if paramiter == "password" :
		user.password=encrypt_password(value)
		db.session.commit()
	return




def encrypt_password(password):
	return bcrypt.generate_password_hash(password).decode('utf-8')

def check_password(user_password,password):
	return bcrypt.check_password_hash(user_password, password)

def send_mail(url,email):
	msg = Message("Reset Password",
		sender='noreply@noter.com',
		recipients=[email])

	msg.body = f"Click on the click to reset reset your Password:{url}"
	mail.send(msg)

def is_equal(password,confirm_password):
	'''
		Function to check if password and confirm password are equal
	'''
	return password==confirm_password