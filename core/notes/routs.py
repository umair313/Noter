from datetime import datetime
from flask import render_template ,url_for,redirect,request,Blueprint
from flask_login import current_user,login_required
from core.utils.functions import get_all_notes,add_note,del_note,get_note,update_note
from core.models import Notes
from core import db

noter_notes= Blueprint('notes',__name__)

@noter_notes.route('/notes')
@login_required
def notes():
	notes = get_all_notes(current_user.id)
	number_of_notes = notes.count()
	return render_template("notes.html",title = "All Notes - Noter",notes=notes,count=number_of_notes)

@noter_notes.route('/create/note',methods=["POST","GET"])
@login_required
def new_note():
	if request.method== "POST":
		title = request.form["notetitle"].replace(" ","-")
		content=request.form["notecontent"]
		add_note(title,content,current_user.id)
		return redirect(url_for('notes.notes'))
	return render_template("new_note.html",title = "Create New Note - Noter")

@noter_notes.route("/note/delete/<int:id>/<string:title>",methods=["POST","GET"])
@login_required
def delete_note(id,title):
	del_note(id,title,current_user.id)
	return redirect(url_for("notes.notes"))

@noter_notes.route('/note/view/<int:id>/<string:title>',methods=["POST","GET"])
@login_required
def view_note(id,title):
	note=get_note(id,title,current_user.id)
	if not note:
		return redirect(url_for('notes.notes'))
	return render_template('view_note.html',title = note.title,note=note)

@noter_notes.route('/note/edit/<int:id>/<string:title>',methods=["POST","GET"])
@login_required
def edit_note(id,title):
	note=get_note(id,title,current_user.id)
	if not note:
		return redirect(url_for('notes.notes'))
	elif request.method=="POST":
		title = request.form["notetitle"].replace(' ','-')
		content=request.form["notecontent"]
		update_note(note,title,content)
		return redirect(url_for('notes.notes'))
	return render_template("edit_note.html",title=note.title,note=note)