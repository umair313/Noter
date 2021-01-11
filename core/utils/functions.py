from core import mail
from flask_mail import Message




def send_mail(url,email):
	msg = Message("Reset Password",
		sender='noreply@noter.com',
		recipients=[email])

	msg.body = f"Click on the click to reset reset your Password:{url}"
	mail.send(msg)
