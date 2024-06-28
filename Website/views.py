#views.py

from flask import Blueprint, redirect, render_template, request, flash, jsonify, url_for
from flask_login import login_required, current_user
from .models import *
from . import db
import json
from flask import jsonify
from collections import Counter


views = Blueprint('views', __name__)

@views.route('/taskmanagement', methods=['GET', 'POST'])
@login_required
def home():
    
    project_id = request.args.get('project_id')
    if project_id:
        project_id = int(project_id)
        
    projects = Project.query.filter_by(id=project_id).first()
    projecttables = Projecttable.query.filter_by(project_id=project_id).all()
    shared_projects = SharedProject.query.filter_by(project_id=project_id).all()
    shared_user_ids = [shared_project.shared_user_id for shared_project in shared_projects]
    shared_users = User.query.filter(User.id.in_(shared_user_ids)).all()
    print("Shared Projects:")
    for shared_project in shared_projects:
        print(f"Shared Project ID: {shared_project.project_id}, Name: {shared_project.project_name}")

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
            new_projecttable = Projecttable(user_id=current_user.id, name="Untitled Table", description="Insert Description Here", project_id=project_id)
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
            return redirect(url_for("views.home", user=current_user,project_id = project_id))

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
            else:
                flash('Task not found or could not be updated.', category='error')

        if 'add_comment' in request.form:
            task_id = request.form.get('task_id')
            comment_detail = request.form.get('comment_detail')
            new_comment = Comment(user_id=current_user.id, tasks_id=task_id, comment_detail=comment_detail)
            db.session.add(new_comment)
            db.session.commit()
            flash('Comment added!', category='success')
            #ADD: A Feature that detects if there's a non-existing user
        if 'invite_user' in request.form:
            user_email= request.form.get('invite_email')
            user = User.query.filter_by(email=user_email).first()
            if current_user.id == user.id:  # Check if the current user is sharing the project with themselves
                flash('Cannot share project with yourself!', category='error')
            else:
                shared_project = SharedProject(project_id=project_id, shared_user_id=user.id,project_name=projects.name,shared_user_role="Member" )
                db.session.add(shared_project)
                db.session.commit()
                flash('Project shared successfully!', category='success')
        if 'change_role' in request.form:
            selected_user_id = request.form.get('selected_user')
            new_role = request.form.get('new_role')
            
            # Update the selected user's role in the database based on the new role
            shared_project = SharedProject.query.filter_by(shared_user_id=selected_user_id).first()
            if shared_project:
                shared_project.shared_user_role = new_role
                db.session.commit()
                flash('User role changed successfully!', category='success')
            else:
                flash('User not found or role not changed.', category='error')
        
        if 'nav_dashboard' in request.form:
            return redirect(url_for('views.dashboard', project_id=project_id, user=current_user,projecttables=projecttables))
            
    return render_template("home.html", user=current_user,project_id = project_id,projecttables=projecttables,shared_projects=shared_projects,shared_users=shared_users)

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

@views.route('/home', methods=['GET', 'POST'])
@login_required
def mainpage():
    projects = Project.query.filter_by(user_id=current_user.id).all()  # Retrieve all projects
    shared_projects = SharedProject.query.filter_by(shared_user_id=current_user.id).all()
    selected_project = None
    selected_shared_project = None
    
    if request.method == 'POST':
        if 'add_project' in request.form:
            project_name = request.form.get('project_name')
            project_description = request.form.get('project_description')
            new_project = Project(name=project_name, description=project_description, user_id=current_user.id)
            db.session.add(new_project)
            db.session.commit()
            project_id = new_project.id
            flash('Project added!', category='success')
            return redirect(url_for('views.home', project_id=project_id, user=current_user))
        if 'select_project' in request.form:
            selected_project_id = request.form.get('selected_project_id')
            return redirect(url_for('views.home', project_id=selected_project_id, user=current_user))
        
            
            
    return render_template("taskmanagementweb.html", user=current_user, projects=projects, selected_project=selected_project,shared_projects=shared_projects, selected_shared_project=selected_shared_project)

@views.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    projects = Project.query.filter_by(user_id=current_user.id).all()  # Retrieve all projects
    shared_projects = SharedProject.query.filter_by(shared_user_id=current_user.id).all()
    project_id = request.args.get('project_id')
    project_id = int(project_id) if project_id else None
    project_tables = Projecttable.query.filter_by(project_id=project_id).all()
    projecttable_id = [projecttable.id for projecttable in project_tables]
    group_task = Task.query.filter(Task.projecttable_id.in_(projecttable_id)).all()
    
    # Extract the task statuses from the 'group_task' data
    task_statuses = [task.task_status for task in group_task]

    # Calculate the count of tasks for each task status
    task_status_counts = dict(Counter(task_statuses))

    # Convert the task status counts into a list of dictionaries for JSON serialization
    group_task_data = [{'task_status': status, 'count': count} for status, count in task_status_counts.items()]
    group_task_data_json = json.dumps(group_task_data)
    group_task_data_parsed = json.loads(group_task_data_json)
    for task_data in group_task_data_parsed:
        print(f'Task Status: {task_data["task_status"]}, Count: {task_data["count"]}')
    
    # Return the JSON-serializable 'group_task_data' to the template
    return render_template("dashboard.html", user=current_user, projects=projects, shared_projects=shared_projects, group_task_data=group_task_data, group_task_data_json=group_task_data_json)

