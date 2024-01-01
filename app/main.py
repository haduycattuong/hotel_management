from flask import render_template, request, redirect, session, jsonify
from app.models import * 
import dao
from app import app, login, db
import hashlib
import math
from flask_login import login_user, logout_user, login_required

#Admin site

# @app.route('/admin/rooms', methods=['get', 'post'])
# def admin_rooms():
#     rooms = dao.get_rooms()
#     return render_template('admin/room.html', rooms=rooms)

    
# @app.route('/admin/roomtypes', methods=['get', 'post'])
# def admin_room_type():
#     room_type = dao.get_room_types()
#     return render_template('admin/room_type.html', room_type=room_type)


# @app.route('/admin/addprice', methods=['get', 'post'])
# def admin_add_price():
#     add_price = dao.get_add_price()
#     return render_template('admin/add_price.html', add_price=add_price)


# @app.route('/admin/bookings', methods=['get', 'post'])
# def admin_bookings():
#     bookings = dao.get_bookings()
#     return render_template('admin/booking.html', bookings=bookings)


# @app.route('/admin/payments', methods=['get', 'post'])
# def admin_payment():
#     payments = dao.get_payment()
#     return render_template('admin/payment.html', payments=payments)

# @app.route('/admin/guests', methods=['get', 'post'])
# def admin_guest():
#     guests = dao.get_guests()
#     return render_template('admin/guest.html', guests=guests)


# @app.route('/admin/rooms/update/<int:id>', methods=['get', 'post'])
# def update_rooms():
#     rooms = Room.query.get_or_404()
    
#     if request.method == "POST":
#         rooms.name = request.form['name']
#         rooms.name = request.form['name']
#         rooms.name = request.form['name']
#         rooms.name = request.form['name']
    
    
# Booking site
# @app.route("/")
# def index():
#     kw = request.args.get('kw')
#     room_type_id = request.args.get('room_type_id')
#     page = request.args.get('page')

#     rooms = dao.get_rooms_by_kw(kw, room_type_id, page)

#     num = dao.count_rooms()
#     page_size = app.config['PAGE_SIZE']

#     return render_template('index.html',
#                            rooms=rooms, pages=math.ceil(num/app.config['PAGE_SIZE']))

@app.route('/hotel')
def hotel_index():
    room_type = dao.get_room_types()
    return render_template('hotel/index.html', room_type=room_type)

@app.route('/bookings')
def booking():
    room_type = dao.get_room_types()
    return render_template('hotel/booking1.html', room_type=room_type)


@app.route("/")
def index():
    kw = request.args.get('kw')
    room_id = request.args.get('room_id')
    page = request.args.get('page')

    rooms = dao.get_rooms()
    room_type = dao.get_room_types_by_kw(kw, room_id, page)

    num = dao.count_room_types()
    page_size = app.config['PAGE_SIZE']

    return render_template('index.html', rooms=rooms,
                           room_type=room_type, pages=math.ceil(num/app.config['PAGE_SIZE']))





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
