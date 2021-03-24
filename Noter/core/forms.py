from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import Email,EqualTo, DataRequired, ValidationError , Length

class Registeration(FlaskForm):
	username = StringField("User Name",validators=[DataRequired(),Length(min=2,max=20)])
	email = StringField("Email",validators=[DataRequired(),Email()])
	password = PasswordField("Password",validators=[DataRequired()])
	confirm_password = PasswordField("Confirm Password",validators=[DataRequired(),EqualTo('password')])
	submit = SubmitField("Register")

class Login(FlaskForm):
	email = StringField("Email",validators=[DataRequired(),Email()])
	password = PasswordField("Password",validators=[DataRequired()])
	submit = SubmitField("Register")
