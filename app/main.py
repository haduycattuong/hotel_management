from flask import render_template, request, redirect, session, jsonify
from app.models import User, Guest, Room, Booking, Payment
import dao
from app import app, login, db
import hashlib
import math
from flask_login import login_user, logout_user, login_required



@app.route("/")
def index():
    kw = request.args.get('kw')
    room_type_id = request.args.get('room_type_id')
    page = request.args.get('page')

    rooms = dao.get_rooms(kw, room_type_id, page)

    num = dao.count_rooms()
    page_size = app.config['PAGE_SIZE']

    return render_template('index.html',
                           rooms=rooms, pages=math.ceil(num/app.config['PAGE_SIZE']))


@app.route('/api/rooms')
def display_rooms():
    kw = request.args.get('kw')
    type_id = request.args.get('cate_id')
    page = request.args.get('page')

    rooms = dao.get_rooms(kw, type_id, page)
    num = dao.count_rooms()
    
    page_size = app.config['PAGE_SIZE'] 
    return render_template('index.html', rooms=rooms, pages=math.ceil(num/page_size))
    



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
    app.run(debug=True)
