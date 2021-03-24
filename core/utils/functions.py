from core import db,mail,bcrypt
from core.models import Users,Notes
from flask_mail import Message
from datetime import datetime


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


def update_user_data(user,paramiter,value):
	if paramiter == 'last_login_dt':
		user.last_login_dt = value
		db.session.commit()
	if paramiter == "password" :
		user.password=encrypt_password(value)
		db.session.commit()
	return

# ############################################################
#  Function related to notes                                 
# ############################################################

def get_all_notes(id):
	'''
		It will return Notes matched with given id will return Notes Object
	'''
	return Notes.query.filter_by(user_id=id).order_by(Notes.cd.desc())

def add_note(title,content,user_id):
	'''
	This function will add new Note into database
	'''
	note = Notes(title=title,content=content,user_id=user_id)
	db.session.add(note)
	db.session.commit()
	return

def del_note(note_id :int,title :str,user_id:int):
	'''
	This Function will delete note from data base
	'''
	note=Notes.query.filter_by(id=note_id,title=title,user_id=user_id).first()
	if note:
		db.session.delete(note)
		db.session.commit()
	return

def get_note(note_id,title,user_id):
	'''
		Return note if found with provided note id,title and user_id othersiwer
		return None 
	'''
	note=Notes.query.filter_by(id=note_id,title=title,user_id=user_id).first()
	return note

def update_note(note,title,content):
	note.title = title
	note.content= content
	note.md = datetime.now()
	db.session.commit()
###############################################################
def encrypt_password(password):
	return bcrypt.generate_password_hash(password).decode('utf-8')

def check_password(user_password,password):
	return bcrypt.check_password_hash(user_password, password)

def is_equal(password,confirm_password):
	'''
		Function to check if password and confirm password are equal
	'''
	return password==confirm_password

def send_mail(url,email):
	msg = Message("Reset Password",
		sender='noreply@noter.com',
		recipients=[email])

	# msg.body = f""

	msg.html =f'''
		<!DOCTYPE html>
		<html>
		<head>
	   <style type="text/css">
	   *{{
	         padding: 0;
	         margin: 0;
	      }}
	      .container{{

	         width: 70%;
	         margin: 0 auto;
	      }}
	      .header{{
	         width: 100%;
	         text-align: center;
	         background: #2c3e50;
	     }}
	      .header #brand{{
	         color: #fff;
	         padding: 10px;
	         line-height: 50px;
	         font-size: 40px;
	      }}
	      a{{
	         text-decoration: none;
	      }}
	      .body{{
	         background: #F6F8FA;
	         width: 100%;
	         margin: 0 auto;
	         text-align: center;
	      }}
	      .body p#reset_pass{{
	         padding-top: 72px;
	        -ms-text-size-adjust: 100%;
	        -webkit-font-smoothing: antialiased;
	        -webkit-text-size-adjust: 100%;
	        color: #000000;
	        font-family: 'lato','Helvetica', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
	            sans-serif;
	        font-size: 48px;
	        font-smoothing: always;
	        font-style: normal;
	        font-weight: 600;
	        line-height: 52px;
	        mso-line-height-rule: exactly;
	   }}

	   #msg,#ignore{{
	   		width:90%;
	      padding-top: 10px;
	      text-align: left;
	      font-size: 15px;
	      margin-left: 20px;


	   }}
	      .btn{{
	         background: #2c3e50;
	         color: #FFFFFF;
	         padding: 10px;
	         display: inline-block;
	         margin: 15px 0;
	         border-radius: 4px;
	      }}

	      a[href]{{
	      color: #FFFFFF;
	      }}
	   </style>
	</head>

	<body>
	  <div class="container">
	      <header class="header">
	      <h1 id="brand">Noter</h1>
	   </header>
	   <article class="body">
	      
	         <p id="reset_pass">Reset Password Request</p>
	         <p id="msg">You're receiving this e-mail because you requested a password reset at 
	   {datetime.now().strftime('%b %d, %Y %I:%M:%S')} for your Noter account.</p>
	      <p id="ignore">if you did't make this request then ignore this email.</p>
	      <a href="{url}" class="btn btn-reset" style="color:#ffffff">Reset Password</a>

	   </article>
	   <footer>
	      
	   </footer>
	  </div>

	</body>
	</html>
	'''
	mail.send(msg)

