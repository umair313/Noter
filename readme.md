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

you can install all of them by in from terminal using command :
```$ pip install requirements.txt``` 

to run this you may need to set an environment variable `SECRET_KEY` and you can generate secret 
key with `screts` module in python or any other of your likes.
You may also do `export SECRET_KEY="testing"` for testing purpose
and set variable `FLASK_APP=run.py`.

## Update :

after adding Mail server now it requires environment variable named `MAIL_USERNAME`,`MAIL_PASSWORD` should be set before runing application.

MAIL_USERNAME is your email and MAIL_PASSWORD is password for your provided email.
it is required for send email through SMPT (Simple MAIL Transfer protocol).

I am using gmail to send email so I set `MAIL_PORT` to 465
and `MAIL_SERVER` to `'smtp.gmail.com'` if you want to use other service then you can change configuration with provided details.
<br>
!Imporant
in case if using gmail you have to turn on `Less secure app access` from your google account in security if its disable you wont be able so send emails.




