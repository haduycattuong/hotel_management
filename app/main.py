from flask import render_template, request, redirect, session, jsonify, url_for
from app.models import * 
import dao
from wtforms import Form
from app import app, login, db
import hashlib
import math
from flask_login import login_user, logout_user, login_required

#Admin site

@app.route('/admin/rooms', methods=['get', 'post'])
def admin_rooms():
    rooms = dao.get_rooms()
    return render_template('admin/room.html', rooms=rooms)

    
@app.route('/admin/roomtypes', methods=['get', 'post'])
def admin_room_type():
    room_type = dao.get_room_types()
    return render_template('admin/room_type.html', room_type=room_type)


@app.route('/admin/addprice', methods=['get', 'post'])
def admin_add_price():
    add_price = dao.get_add_price()
    return render_template('admin/add_price.html', add_price=add_price)


@app.route('/admin/bookings', methods=['get', 'post'])
def admin_bookings():
    bookings = dao.get_bookings()
    return render_template('admin/booking.html', bookings=bookings)


@app.route('/admin/payments', methods=['get', 'post'])
def admin_payment():
    payments = dao.get_payment()
    return render_template('admin/payment.html', payments=payments)

@app.route('/admin/guests', methods=['get', 'post'])
def admin_guest():
    guests = dao.get_guests()
    return render_template('admin/guest.html', guests=guests)


@app.route('/admin/rooms/update/<int:id>', methods=['get', 'post'])
def update_rooms():
    rooms = None
    if request.method == "POST":
        rooms.name = request.form['name']
        rooms.img = request.form['img']
        rooms.foreigner_rate = request.form['foreigner_rate']
        rooms.type_id = request.form['type_id']
        rooms.add_price_id = request.form['add_price_id']
    
@app.route('/admin/create-room', methods=['get', 'post'])
def admin_create_room():
    err_msg = ""
    name = request.form.get('name')
    img = request.form.get('img')
    foreigner_rate = request.form.get('foreigner_rate')
    room_type_id = request.form.get('room_type_id')
    add_price_id = request.form.get('add_price_id')

    name_exists = Room.query.filter_by(name=name).first() is not None
    room = dao.create_room(name=name, img=img, foreigner_rate=foreigner_rate,
                             type_id=room_type_id, add_price_id=add_price_id)
    err_msg = "Room create successully"
    return render_template('add_room.html', err_msg=err_msg)
    
@app.route('/admin/create-guest', methods=['get', 'post'])
def admin_create_guest():
    err_msg = ""
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    cccd = request.form.get('cccd')
    phone = request.form.get('phone')

    guest_exists = Guest.query.filter_by(cccd=cccd).first() is not None
    guest = dao.create_guest(first_name=first_name, last_name=last_name, 
                             cccd=cccd, phone=phone)
    err_msg = "Guest create successully"
    return render_template('add_guest.html', err_msg=err_msg)

# @app.route('/admin/create-room', methods=['get', 'post'])
# def admin_create_room():
#     err_msg = ""
#     name = request.form.get('name')
#     img = request.form.get('img')
#     foreigner_rate = request.form.get('foreigner_rate')
#     room_type_id = request.form.get('room_type_id')
#     add_price_id = request.form.get('add_price_id')

#     name_exists = Room.query.filter_by(name=name).first() is not None
#     room = dao.create_room(name=name, img=img, foreigner_rate=foreigner_rate,
#                              type_id=room_type_id, add_price_id=add_price_id)
#     err_msg = "Room create successully"
#     return render_template('add_room.html', err_msg=err_msg)

# @app.route('/admin/create-room', methods=['get', 'post'])
# def admin_create_room():
#     err_msg = ""
#     name = request.form.get('name')
#     img = request.form.get('img')
#     foreigner_rate = request.form.get('foreigner_rate')
#     room_type_id = request.form.get('room_type_id')
#     add_price_id = request.form.get('add_price_id')

#     name_exists = Room.query.filter_by(name=name).first() is not None
#     room = dao.create_room(name=name, img=img, foreigner_rate=foreigner_rate,
#                              type_id=room_type_id, add_price_id=add_price_id)
#     err_msg = "Room create successully"
#     return render_template('add_room.html', err_msg=err_msg)

# @app.route('/admin/create-room', methods=['get', 'post'])
# def admin_create_room():
#     err_msg = ""
#     name = request.form.get('name')
#     img = request.form.get('img')
#     foreigner_rate = request.form.get('foreigner_rate')
#     room_type_id = request.form.get('room_type_id')
#     add_price_id = request.form.get('add_price_id')

#     name_exists = Room.query.filter_by(name=name).first() is not None
#     room = dao.create_room(name=name, img=img, foreigner_rate=foreigner_rate,
#                              type_id=room_type_id, add_price_id=add_price_id)
#     err_msg = "Room create successully"
#     return render_template('add_room.html', err_msg=err_msg)

# @app.route('/admin/create-room', methods=['get', 'post'])
# def admin_create_room():
#     err_msg = ""
#     name = request.form.get('name')
#     img = request.form.get('img')
#     foreigner_rate = request.form.get('foreigner_rate')
#     room_type_id = request.form.get('room_type_id')
#     add_price_id = request.form.get('add_price_id')

#     name_exists = Room.query.filter_by(name=name).first() is not None
#     room = dao.create_room(name=name, img=img, foreigner_rate=foreigner_rate,
#                              type_id=room_type_id, add_price_id=add_price_id)
#     err_msg = "Room create successully"
#     return render_template('add_room.html', err_msg=err_msg)

# @app.route('/admin/create-room', methods=['get', 'post'])
# def admin_create_room():
#     err_msg = ""
#     name = request.form.get('name')
#     img = request.form.get('img')
#     foreigner_rate = request.form.get('foreigner_rate')
#     room_type_id = request.form.get('room_type_id')
#     add_price_id = request.form.get('add_price_id')

#     name_exists = Room.query.filter_by(name=name).first() is not None
#     room = dao.create_room(name=name, img=img, foreigner_rate=foreigner_rate,
#                              type_id=room_type_id, add_price_id=add_price_id)
#     err_msg = "Room create successully"
#     return render_template('add_room.html', err_msg=err_msg)
# Booking site
@app.route("/<int:type_id>")
def load_rooms():
    kw = request.args.get('kw')
    room_type_id = request.args.get('room_type_id')
    page = request.args.get('page')

    rooms = dao.get_rooms_by_kw(kw, room_type_id, page)

    num = dao.count_rooms()
    page_size = app.config['PAGE_SIZE']

    return render_template('index.html', 
                           rooms=rooms, pages=math.ceil(num/app.config['PAGE_SIZE']))

@app.route('/hotel')
def hotel_index():
    room_type = dao.get_room_types()
    return render_template('hotel/index.html', room_type=room_type)

@app.route('/bookings')
def booking():
    room_type = dao.get_room_types()
    rooms = dao.get_rooms()
    return render_template('hotel/booking1.html', room_type=room_type)


@app.route("/")
def index():
    kw = request.args.get('kw')
    room_id = request.args.get('room_id')
    page = request.args.get('page')

    room_type = dao.get_room_types_by_kw(kw, room_id, page)
    

    num = dao.count_room_types()
    page_size = app.config['PAGE_SIZE']

    return render_template('index.html',
                           room_type=room_type, pages=math.ceil(num/app.config['PAGE_SIZE']))

@app.route("/rooms")
def room_list():
    room_type_id = request.args.get('room_type_id')

    rooms = dao.get_rooms_by_types(type_id=room_type_id)

    return render_template('hotel/room.html', rooms=rooms)


@app.route('/admin/login', methods=['post'])
@login_required
def login_admin_process():
    username = request.form.get('username')
    password = request.form.get('password')

    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')


@app.route('/register', methods=['get', 'post'])
def register_user():
    err_msg = ""
    name = request.form.get('name')
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_pass = request.form.get('confirm-pass')

    user_exists = User.query.filter_by(username=username).first() is not None
    if password.__eq__(confirm_pass) and user_exists:
        try:
            dao.register(name=name, username=username, password=password)
        except:
            err_msg = 'System Error'
    else:
        err_msg = 'Password didnt match!'
    return render_template('register.html', err_msg=err_msg)


@app.route('/login', methods=['get', 'post'])
def login_user_process():
    ex = ""
    if request.method.__eq__('POST'):
        username = request.form['username']
        password = request.form['password']
        try:
            user = dao.auth_user(username=username, password=password)
            if user:
                login_user(user=user)
                return redirect(url_for('index'))
        except Exception as e:
            ex = str(e)
    return render_template('login.html', ex=ex)

@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)

@app.route('/logout')
@login_required
def user_logout():
    logout_user()
    return redirect('/')

if __name__ == '__main__':
    from app import admin
    app.run(debug=True)
