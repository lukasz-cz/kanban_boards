from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, LoginManager, current_user, logout_user
from . import mongo
from . import argon2
from .models import User, UserTasks
from bson.objectid import ObjectId

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile', methods=['GET'])
@login_required
def profile():
    return render_template('profile.html', username=current_user.username)

@main.route('/reset_password', methods=['POST'])
@login_required
def reset_password():
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')

    user = User.find_by_id(mongo, current_user.id)

    if not user or not argon2.check_password_hash(user.password, current_password):
        flash('Current password is incorrect', 'danger')
        return redirect(url_for('main.profile'))

    new_password_hash = argon2.generate_password_hash(new_password)
    user.reset_password(mongo, new_password_hash)

    flash('Your password has been updated!', 'success')
    
    return redirect(url_for('main.profile'))

@main.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    user = User.find_by_id(mongo, current_user.id)

    if user and user.delete_account(mongo):
        logout_user()
        flash('Your account has been deleted', 'info')
        return redirect(url_for('auth.login'))
    else:
        flash('Account not found', 'danger')
        return redirect(url_for('main.profile'))

@main.route('/kanban')
@login_required
def kanban():
    user_tasks = UserTasks.load_from_db(mongo, current_user.id)
    
    return render_template('kanban.html', username=current_user.username, user_tasks=user_tasks)

@main.route('/update_tasks', methods=['POST'])
@login_required
def update_tasks():
    data = request.get_json()

    if not data:
        return jsonify({"message": "No data provided"}), 400

    user_tasks = UserTasks.load_from_db(mongo, current_user.id)

    user_tasks.backlog = data.get('backlog', [])
    user_tasks.waiting = data.get('waiting', [])
    user_tasks.working = data.get('working', [])
    user_tasks.done = data.get('done', [])

    user_tasks.save_to_db(mongo)
    
    return jsonify({"status": "success", "message": "Tasks updated successfully"}), 200
