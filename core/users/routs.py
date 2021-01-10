from datetime import datetime
from flask import render_template,redirect,url_for,request,Blueprint
from flask_login import current_user,login_user,login_required,logout_user
from core.models import Users,Notes
from core import db,bcrypt

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
		user = Users.query.filter_by(email=email).first()
		if user:
			if bcrypt.check_password_hash(user.password, password):
				login_user(user)
				user.last_login_dt=datetime.utcnow()
				db.session.commit()
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
		user_with_username = Users.query.filter_by(username=username).first()
		user_with_email = Users.query.filter_by(email=email).first()
		if user_with_email: error['email']= True
		if user_with_username: error['username']=True
		if not password == c_password: error['password'] = True
		if not error['email'] and not error['username'] and not error['password']:
			hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
			user = Users(username=username,email=email,password=hashed_password)
			db.session.add(user)
			db.session.commit()
			return redirect(url_for('users.login'))
	return render_template("register.html",title= "Register - Noter",error=error)

@noter_users.route('/profile',methods=["GET"])
@login_required
def profile():
	if not current_user.is_authenticated:
		return redirect(url_for('users.login'))
	notes = Notes.query.filter_by(user_id=current_user.id).order_by(Notes.cd.desc())
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
		user = Users.query.filter_by(email=email).first()
		if user:
			token = user.gen_token()
			data['link'] = f"{url_for('users.reset_password',token=token,_external=True)}"
			data['email'] = email
			return render_template('go_to_reset_password.html',data=data)
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
		if request.form['password'] == request.form["confirm_password"]:
			password = request.form['password']
			user.password = bcrypt.generate_password_hash(password).decode("utf-8")
			db.session.commit()
			return redirect(url_for('users.login'))
		else: 
			error["password"]=True
	return	render_template("reset_password.html",title="Reset Password",error=error)

# route for change user password
@noter_users.route('/change_password',methods=["GET","POST"])
def change_password():
	error={
	'password':False
	}
	user = Users.query.filter_by(id=current_user.id).first()
	if request.method== "POST":
		if request.form['password'] == request.form["confirm_password"]:
			password = request.form['password']
			user.password = bcrypt.generate_password_hash(password).decode("utf-8")
			db.session.commit()
			return redirect(url_for('users.profile'))
		else: error['password']=True
	return render_template("change_password.html",title="Change Password" ,error=error)

@noter_users.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('users.login'))	