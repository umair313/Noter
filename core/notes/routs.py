from datetime import datetime
from flask import render_template ,url_for,redirect,request,Blueprint
from flask_login import current_user,login_required
from core.models import Notes
from core import db

noter_notes= Blueprint('notes',__name__)

@noter_notes.route('/notes')
@login_required
def notes():
	notes = Notes.query.filter_by(user_id=current_user.id).order_by(Notes.cd.desc())
	number_of_notes = notes.count()
	return render_template("notes.html",title = "All Notes - Noter",notes=notes,count=number_of_notes)

@noter_notes.route('/create/note',methods=["POST","GET"])
@login_required
def new_note():
	if request.method== "POST":
		title = request.form["notetitle"]
		content=request.form["notecontent"]
		note = Notes(title=title,content=content,user_id=current_user.id)
		db.session.add(note)
		db.session.commit()
		return redirect(url_for('notes.notes'))
	return render_template("new_note.html",title = "Create New Note - Noter")

@noter_notes.route("/note/delete/<int:id>/<string:title>",methods=["POST","GET"])
def delete_note(id,title):
	note=Notes.query.filter_by(id=id,title=title,user_id=current_user.id).first()
	if note:
		db.session.delete(note)
		db.session.commit()
	return redirect(url_for("notes.notes"))

@noter_notes.route('/note/view/<int:id>/<string:title>',methods=["POST","GET"])
def view_note(id,title):
	note=Notes.query.filter_by(id=id,title=title,user_id=current_user.id).first()
	if not note:
		return redirect(url_for('notes.notes'))
	return render_template('view_note.html',title = note.title,note=note)

@noter_notes.route('/note/edit/<int:id>/<string:title>',methods=["POST","GET"])
def edit_note(id,title):
	note=Notes.query.filter_by(id=id,title=title,user_id=current_user.id).first()
	if not note:
		return redirect(url_for('notes.notes'))
	elif request.method=="POST":
		note.title = request.form["notetitle"]
		note.content=request.form["notecontent"]
		note.md=datetime.utcnow()
		db.session.commit()
		return redirect(url_for('notes.notes'))
	return render_template("edit_note.html",title=note.title,note=note)