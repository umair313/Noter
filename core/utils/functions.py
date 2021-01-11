from core import mail,bcrypt
from flask_mail import Message


def is_equal(password,confirm_password):
	'''
		Function to check if password and confirm password are equal
	'''
	return password==confirm_password


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
