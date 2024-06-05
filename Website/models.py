from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    shared_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note', foreign_keys='Note.user_id')
    tasks = db.relationship('Task', foreign_keys='Task.user_id')
    comments = db.relationship('Comment', foreign_keys='Comment.user_id')
    project_tables = db.relationship('Projecttable', foreign_keys='Projecttable.user_id')
    project = db.relationship('Project',foreign_keys='Project.user_id')

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(10000))
    task_status = db.Column(db.String(10000))
    deadline = db.Column(db.String(10000))
    description = db.Column(db.String(10000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    projecttable_id = db.Column(db.Integer, db.ForeignKey('projecttable.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))

class Projecttable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10000))  
    description = db.Column(db.String(10000))  
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    tasks = db.relationship('Task', backref='projecttable', foreign_keys='Task.projecttable_id')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comment_detail = db.Column(db.String(10000))
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10000))  
    description = db.Column(db.String(10000))  
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    projecttable = db.relationship('Projecttable', backref='project', foreign_keys='Projecttable.project_id')