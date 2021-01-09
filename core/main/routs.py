from flask import redirect,render_template,url_for,Blueprint
from flask_login import current_user

noter_main = Blueprint('main',__name__)

@noter_main.route('/')
@noter_main.route('/home')
def home():
	if current_user.is_authenticated:
		return redirect(url_for('notes.notes'))
	return render_template("index.html",title = "Home - Noter")