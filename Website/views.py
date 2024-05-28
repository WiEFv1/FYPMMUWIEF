# views.py

from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import *
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/taskmanagement', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        if 'add_note' in request.form:
            note = request.form.get('note')  # Gets the note from the HTML
            if len(note) < 1:
                flash('Note is too short!', category='error')
            else:
                new_note = Note(data=note, user_id=current_user.id)  # Providing the schema for the note
                db.session.add(new_note)  # Adding the note to the database
                db.session.commit()
                flash('Note added!', category='success')
        
        if 'create_table' in request.form:  # Check if the create table form is submitted
            new_projecttable = Projecttable(user_id=current_user.id, name="Untitled Table", description="Insert Description Here")
            db.session.add(new_projecttable)
            db.session.commit()
            flash('Table Added!', category='success')
        
        if 'add_task' in request.form:
            projecttable_id = request.form.get('projecttable_id')
            new_task = Task(
                user_id=current_user.id,
                projecttable_id=projecttable_id,
                task_name=request.form.get('task_name'),
                task_status=request.form.get('task_status'),
                deadline=request.form.get('deadline'),
                description=request.form.get('description')
            )
            db.session.add(new_task)
            db.session.commit()
            flash('Task Added!', category='success')
        
        if 'delete_task' in request.form:
            task_id = request.form.get('task_id')
            task = Task.query.get(task_id)
            if task and task.user_id == current_user.id:
                db.session.delete(task)
                db.session.commit()
                flash('Task Deleted!', category='success')
                
        if 'edit_task' in request.form:
            task_id = request.form.get('task_id')
            task = Task.query.get(task_id)
            if task:
                task.task_name = request.form.get('task_name')
                task.task_status = request.form.get('task_status')
                task.deadline = request.form.get('deadline')
                task.description = request.form.get('description')
                db.session.commit()
                flash('Task Updated!', category='success')
    
    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)  # This function expects a JSON from the INDEX.js file
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/home')
def mainpage():
    return render_template("taskmanagementweb.html", user=current_user)
