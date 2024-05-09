from flask import Blueprint, flash, render_template, request

auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    data = request.form
    return render_template("login.html")

@auth.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')

        elif len(username) < 2:
            flash('Username must be greater than 1 characters.', category='error')

        elif password != confirm_password:
            flash('Password don\'t match', category='error')

        elif len(password) < 7:
            flash('Password must be greater than 7 characters.', category='error')

        else:
            flash('User has been created', category='success')
            #add user to database
    return render_template("register.html")