from flask import render_template, request, redirect, session, jsonify
from models import User, Guest, Room, Room_Type, Booking, Payment
import dao
from app import app, login, db
import hashlib
from flask_login import login_user, logout_user





@app.route('/admin/login', methods=['post'])
def login_admin_process():
    username = request.form.get('username')
    password = request.form.get('password')

    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')

@app.route('/register', methods=['get', 'post'])
def register_user():
    username = request.form.get('username')
    password = request.form.get('password')

    user_exists = User.query.filter_by(username=username).first() is not None
    if user_exists:
        return jsonify({"error": "Username already exists"}), 409

@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == '__main__':
    from app import admin
    app.run(debug=False)
