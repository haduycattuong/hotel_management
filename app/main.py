from flask import render_template, request, redirect, session, jsonify, url_for, sessions
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

    






@app.route('/admin/payments', methods=['get', 'post'])
def admin_payment():
    payments = dao.get_payment()
    return render_template('admin/payment.html', payments=payments)

@app.route('/guests', methods=['get', 'post'])
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
    
# @app.route('/admin/create-guest', methods=['get', 'post'])
# def admin_create_guest():
#     err_msg = ""
#     first_name = request.form.get('first_name')
#     last_name = request.form.get('last_name')
#     cccd = request.form.get('cccd')
#     phone = request.form.get('phone')

#     guest_exists = Guest.query.filter_by(cccd=cccd).first() is not None
#     guest = dao.create_guest(first_name=first_name, last_name=last_name, 
#                              cccd=cccd, phone=phone)
#     err_msg = "Guest create successully"
#     return render_template('add_guest.html', err_msg=err_msg)

# Booking site

@app.route('/hotel')
def hotel_index():
    room_type = dao.get_room_types()
    return render_template('hotel/index.html', room_type=room_type)

@app.route('/bookings')
def booking():
    room_type = dao.get_room_types()
    rooms = dao.get_rooms()
    return render_template('hotel/booking1.html', room_type=room_type, rooms=rooms)

@app.route('/bookings/<int:room_id>')
def booking_room():
    room = dao.get_rooms_by_id()

# @app.route("/")
# def index():
#     kw = request.args.get('kw')
#     room_id = request.args.get('room_id')
#     page = request.args.get('page')

#     room_type = dao.get_room_types_by_kw(kw, room_id, page)
    

#     num = dao.count_room_types()
#     page_size = app.config['PAGE_SIZE']

#     return render_template('index.html',
#                            room_type=room_type, pages=math.ceil(num/app.config['PAGE_SIZE']))

                           
@app.route("/")
def index():
    kw = request.args.get('kw')
    room_type_id = request.args.get('room_type_id')
    room_id = request.args.get('room_id')
    page = request.args.get('page')

    rooms = dao.get_rooms_by_kw(kw, room_type_id, page)

    num = dao.count_rooms()

    return render_template('index.html', 
                           rooms=rooms, pages=math.ceil(num/app.config['PAGE_SIZE']))


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
    err_msg = ""

    if request.method.__eq__('POST'):
        password = request.form.get('password')
        username = request.form.get('username')
        confirm_pass = request.form.get('confirm-pass')
        user_exists = User.query.filter_by(username=username).first is not None
        if password.__eq__(confirm_pass):
            if user_exists:
                try:
                    dao.add_user(name=request.form.get('name'),
                             username=username,
                             password=password)
                    return redirect(url_for('login_user_process'))
                except:
                    err_msg = "System Error"
            else:
                err_msg = "Username already exists"
        else:
            err_msg = "Password didnt match"
    return render_template('register.html', err_msg=err_msg)

@app.route('/booking-guest/create', methods=['get','post'])
def create_booking_guest():
    err_msg = ""
    if request.method.__eq__('POST'):
        first_name= request.form.get('firstname')
        last_name = request.form.get('lastname')
        cccd = request.form.get('cccd')
        phone = request.form.get('phone')
        check_in = datetime.strptime(request.form['checkInDate'], '%d-%m-%Y')
        check_out = datetime.strptime(request.form['checkOutDate'], '%d-%m-%Y')
        room_id = request.args.get('room_id')
        description = request.form.get('description')
        num_guest = request.form.get('num-guest')
        has_foreigner = request.form.get('has-foreigner')
        try:
            dao.add_guest(first_name=first_name, last_name=last_name, 
                          cccd=cccd, phone=phone)
            db.session.flush()
            dao.add_booking(check_in=check_in, check_out=check_out, room_id=room_id,
                            description=description, num_guest=num_guest, has_foreigner=has_foreigner)
        except:
            db.session.rollback()
            err_msg = "System error cant create booking"
    return render_template('hotel/booking1.html', err_msg=err_msg)
    

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
