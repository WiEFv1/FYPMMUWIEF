from flask import Blueprint, flash, render_template, request, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in Successfully!', category = 'success')
                return redirect(url_for('view.home'))
            else:
                flash('Incorrect password, Try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("login.html")
            
@auth.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        user = User.query.filter_by(username=username).first()
        
        if user:
            flash('User already exist!',category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')

        elif len(username) < 2:
            flash('Username must be greater than 1 characters.', category='error')

        elif password != confirm_password:
            flash('Password don\'t match', category='error')

        elif len(password) < 7:
            flash('Password must be greater than 7 characters.', category='error')

        else:
            new_user = User(email=email, username=username,password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            flash('User has been created', category='success')
            return redirect(url_for('view.home'))
            
            #add user to database
    return render_template("register.html")