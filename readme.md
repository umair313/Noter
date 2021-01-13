# Noter
Noter is a simple note taking web application writen in Flask

## What's in it?
- user can login
- user can register
- user can logout :)
- reset password
- send email when reset password requested
- can write note
	- can provide title for note
	- can provide content for note
- can edit/view/delete notes
- can we all the notes and its dates when created and when modified

if you want to add more functionality you are always welcome. :)

## Requirements

requirements are specified in requirements.txt 
- bcrypt==3.2.0
- cffi==1.14.4
- click==7.1.2
- dnspython==2.1.0
- email-validator==1.1.2
- Flask==1.1.2
- Flask-Bcrypt==0.7.1
- Flask-Login==0.5.0
- Flask-SQLAlchemy==2.4.4
- Flask-WTF==0.14.3
- idna==3.1
- itsdangerous==1.1.0
- Jinja2==2.11.2
- MarkupSafe==1.1.1
- pycparser==2.20
- six==1.15.0
- SQLAlchemy==1.3.22
- Werkzeug==1.0.1
- WTForms==2.3.3

## How to run this?
to run you first need to install all the requiremnts specified above you can do that by using with following command make sure you in `/Noter` directory in you command-line/CMD

<br>command : ```$ pip install -r requirements.txt``` <br>
it will install the requiremetns.<br>
now you need to set some envionment variables in your CMD type the following commands.<br>
<br>
For windows user
`set FLASK_APP=run.py`
Your Email and password for email server with out these you wont be able send email for reset password

`setx MAIL_USERNAME "your gmail"` <br>
`setx MAIL_PASSWORD "YOUR gmail password"`

<br>
!Imporant
in case if using gmail you have to turn on [Less secure app access](https://myaccount.google.com/lesssecureapps) from your google account in security section if its disable you wont be able so send emails.

For linux users
`export FLASK_APP=run.py`
Your Email and password for email server with out these you wont be able send email for reset password

`export MAIL_USERNAME="your gmail"` <br>
`export MAIL_PASSWORD="YOUR gmail password"`


then command `python run.py` will run the server.<br>
you can open it in your browser by visiting [https://localhost:5000/]


