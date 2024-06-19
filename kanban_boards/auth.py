from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import mongo
from . import argon2
from .models import User, UserTasks
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user_data = mongo.db.users.find_one({"email": email})
        remember = True if request.form.get('remember') else False

        if user_data and argon2.check_password_hash(user_data['password'], password):
            user = User(**user_data)
            login_user(user, remember=remember)
            return redirect(url_for('main.kanban'))
        else:
            flash('Login unsuccessful. Check email and password', 'danger')
    
    return render_template('login.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_password = argon2.generate_password_hash(password)
        existing_user = mongo.db.users.find_one({"email": email})

        if existing_user is None:
            user = User.create_user(mongo, username, email, hashed_password)
            user_tasks = UserTasks(user.id)
            user_tasks.save_to_db(mongo)
            flash('Account created successfully!', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Email address already exists', 'danger')
    
    return render_template('signup.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    
    return redirect(url_for('main.index'))
