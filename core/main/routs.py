from flask import redirect,render_template,url_for,Blueprint
from flask_login import current_user
from core import app
noter_main = Blueprint('amin',__name__)

@app.route('/')
@app.route('/home')
def home():
	if current_user.is_authenticated:
		return redirect(url_for('notes'))
	return render_template("index.html",title = "Home - Noter")