from flask import Blueprint,render_template

errors = Blueprint("errors",__name__)

@errors.app_errorhandler(404)
def error_404(error):
	return render_template('error/404.html'),404