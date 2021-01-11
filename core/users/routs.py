from datetime import datetime
from flask import (
	render_template,redirect,
	url_for,request,
	Blueprint)

from flask_login import (
	current_user,login_user,
	login_required,logout_user)


from core.utils.functions import (
	send_mail,encrypt_password,check_password,is_equal,register_user,get_user,
	user_exit_by_username,user_exit_by_email,update_user_data,get_notes)

from core.models import Users,Notes
from core import db

noter_users=Blueprint('users',__name__)

@noter_users.route('/login',methods=["POST","GET"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('notes.notes'))
	error = {
	"user" : False,
	"password" : False
	}

	if request.method == "POST":
		email = request.form["email"]
		password = request.form["password"]
		user = get_user(email)
		if user:
			if check_password(user.password,password):
				login_user(user)
				update_user_data(user,'last_login_dt',datetime.now())
				return redirect('notes')
			else: error['password'] = True
		else:
			error['user'] = True
	return render_template("login.html",title= "Login - Noter" ,error=error)


@noter_users.route('/register',methods=["POST","GET"])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('notes.notes'))
	error = {
	"email": False,
	"username":False,
	"password":False
	}
	if request.method == "POST":
		username = request.form["username"]
		email = request.form["email"]
		password = request.form["password"]
		c_password= request.form["confirm_password"]

		error['email']= user_exit_by_email(email)
		error['username']=user_exit_by_username(username)
		error['password'] = not is_equal(password,c_password)

		if not error['email'] and not error['username'] and not error['password']:
			user = Users(username=username,email=email,password=encrypt_password(password))
			register_user(user)
			return redirect(url_for('users.login'))
	return render_template("register.html",title= "Register - Noter",error=error)

@noter_users.route('/profile',methods=["GET"])
@login_required
def profile():
	if not current_user.is_authenticated:
		return redirect(url_for('users.login'))
	notes = get_notes(current_user.id)
	numberOfNotes=notes.count()
	return render_template("profile.html",title = "Profile - Noter",number_of_notes=numberOfNotes)

# reset password request
@noter_users.route('/reset_password_request',methods=['POST',"GET"])
def reset_password_request():
	error = {
	"email": False
	}
	data={
	"link" : "",
	"email" : ""
	}
	if request.method == "POST":
		email=request.form['email']
		user = get_user(email)
		if user:
			token = user.gen_token()
			url = data['link'] = f"{url_for('users.reset_password',token=token,_external=True)}"
			data['email'] = email
			send_mail(url,email)
			return render_template('msg.html',title= "Reset Password",email=data['email'])
		else: error["email"]=True
	return render_template('reset_password_request.html',title="Reset Password Request",error=error,data=data)


@noter_users.route('/reset_password/<token>',methods=["GET","POST"])
def reset_password(token):
	error={
	'invalid':False,
	'password':False
	}
	user = Users.verify_token(token)
	if user is None:
		error["invalid"]=True
	if request.method== "POST" and user is not None:
		password = request.form['password']
		c_password = request.form['confirm_password']
		if is_equal(password,c_password):
			update_user_data(user,'password',password)
			return redirect(url_for('users.login'))
		else: 
			error["password"]=True
	return	render_template("reset_password.html",title="Reset Password",error=error)

# route for change user password
@noter_users.route('/change_password',methods=["GET","POST"])
def change_password():
	if not current_user.is_authenticated:
		return redirect(url_for('users.login'))
	error={
	'password':False
	}
	if request.method== "POST":
		password = request.form['password']
		c_password = request.form['confirm_password']
		if is_equal(password,c_password):
			update_user_data(current_user,'password',password)
			return redirect(url_for('users.profile'))
		else: error['password']=True
	return render_template("change_password.html",title="Change Password" ,error=error)

@noter_users.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('users.login'))	