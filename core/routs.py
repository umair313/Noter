from datetime import datetime
from flask import render_template ,url_for,redirect,request
from flask_login import login_user, current_user, logout_user,login_required
from core.models import Users, Notes
from core import app,db,login_manager,bcrypt


@app.route('/')
@app.route('/home')
def home():
	if current_user.is_authenticated:
		return redirect(url_for('notes'))
	return render_template("index.html",title = "Home - Noter")

@app.route('/login',methods=["POST","GET"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('notes'))
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


@app.route('/register',methods=["POST","GET"])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('notes'))
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
			return redirect(url_for('login'))
	return render_template("register.html",title= "Register - Noter",error=error)

@app.route('/profile',methods=["POST","GET"])
@login_required
def profile():

	if not current_user.is_authenticated:
		return redirect(url_for('login'))
	notes = Notes.query.filter_by(user_id=current_user.id).order_by(Notes.cd.desc())
	numberOfNotes=notes.count()
	return render_template("profile.html",title = "Profile - Noter",number_of_notes=numberOfNotes)

@app.route('/create/note',methods=["POST","GET"])
@login_required
def new_note():
	if request.method== "POST":
		title = request.form["notetitle"]
		content=request.form["notecontent"]
		note = Notes(title=title,content=content,user_id=current_user.id)
		db.session.add(note)
		db.session.commit()
		return redirect(url_for('notes'))
	return render_template("new_note.html",title = "Create New Note - Noter")

@app.route('/notes')
@login_required
def notes():
	notes = Notes.query.filter_by(user_id=current_user.id).order_by(Notes.cd.desc())
	return render_template("notes.html",title = "All Notes - Noter",notes=notes)

@app.route("/note/delete/<int:id>/<string:title>",methods=["POST","GET"])
def delete_note(id,title):
	note=Notes.query.filter_by(id=id,title=title,user_id=current_user.id).first()
	if note:
		db.session.delete(note)
		db.session.commit()
	return redirect(url_for("notes"))

@app.route('/note/view/<int:id>/<string:title>',methods=["POST","GET"])
def view_note(id,title):
	note=Notes.query.filter_by(id=id,title=title,user_id=current_user.id).first()
	if not note:
		return redirect(url_for('notes'))
	return render_template('view_note.html',title = note.title,note=note)

@app.route('/note/edit/<int:id>/<string:title>',methods=["POST","GET"])
def edit_note(id,title):
	note=Notes.query.filter_by(id=id,title=title,user_id=current_user.id).first()
	if not note:
		return redirect(url_for('notes'))
	elif request.method=="POST":
		note.title = request.form["notetitle"]
		note.content=request.form["notecontent"]
		note.md=datetime.utcnow()
		db.session.commit()
		return redirect(url_for('notes'))
	return render_template("edit_note.html",title=note.title,note=note)

# reset password request
@app.route('/reset_password_request',methods=['POST',"GET"])
def reset_password_request():
	error = {
	"email": False
	}
	data={
	"link" : ""
	}
	if request.method == "POST":
		email=request.form['email']
		user = Users.query.filter_by(email=email).first()
		if user:
			token = user.gen_token()
			data['link'] = f"{url_for('reset_password',token=token,_external=True)}"
			return render_template('go_to_reset_password.html',data=data)
		else: error["email"]=True
	return render_template('reset_password_request.html',title="Reset Password Request",error=error,data=data)


@app.route('/reset_password/<token>',methods=["GET","POST"])
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
			return redirect(url_for('login'))
		else: 
			error["password"]=True
	return	render_template("reset_password.html",title="Reset Password",error=error) 

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('login'))