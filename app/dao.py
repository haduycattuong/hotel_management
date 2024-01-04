from app.models import *
from app import app, db
import hashlib
import re
from sqlalchemy import func
from datetime import datetime








def get_guests():
    return Guest.query.all()

def get_payment():
    return Payment.query.all()

def get_bookings():
    return Booking.query.all()

def get_room_types():
    return RoomType.query.all()

def get_rooms():
    return Room.query.all()

def create_room(name, img, foreigner_rate, type_id, add_price_id):
    room_name = []
    for r in Room.query.all():
        if r.name == room_name:
           room_name.append(r.name) 
    if r.name not in room_name:
            room = Room(name=name, img=img, foreigner_rate=foreigner_rate,
                             type_id=type_id, add_price_id=add_price_id)
            with app.app_context:
                db.session.add(room)
                db.session.commit()
    else:
        raise Exception("Room name is already exists")

def create_room_type(type, img, max_capacity, price):
    room_type = []
    for r in RoomType.query.all():
        if r.type == room_type:
           room_type.append(r.name) 
    if r.type not in room_type:
            room_type = RoomType(type=type, img=img, max_capacity=max_capacity,
                             price=price)
            with app.app_context:
                db.session.add(room_type)
                db.session.commit()
    else:
        raise Exception("Room type is already exists")
    

def create_guest(first_name, last_name, cccd, phone):
    guests = []
    for g in Guest.query.all():
        if g.cccd == guests:
           guests.append(g.cccd) 
    if g.cccd not in guests:
            guest = Guest(first_name=first_name, last_name=last_name,
                          cccd=cccd, phone=phone)
            with app.app_context:
                db.session.add(guest)
                db.session.commit()
    else:
        raise Exception("Guest cccd is already exists")

def create_payment(first_name, last_name, img, cccd, phone):
    guests = []
    for g in Guest.query.all():
        if g.cccd == guests:
           guests.append(g.cccd) 
    if g.cccd not in guests:
            guest = Guest(first_name=first_name, last_name=last_name, img=img,
                          cccd=cccd, phone=phone)
            with app.app_context:
                db.session.add(guest)
                db.session.commit()
    else:
        raise Exception("Guest cccd is already exists")

def create_booking(check_in, check_out, num_guest, has_foreigner, phone):
    date_now = datetime.now() 
    booking = Booking(check_in=check_in, check_out=check_out, num_guest=num_guest,
                          has_foreigner=has_foreigner, phone=phone)
    with app.app_context:
        db.session.add(booking)
        db.session.commit()

def create_booking_status(status):
    status_list = []
    for s in BookingStatus.query.all():
        if s.status == status_list:
           status_list.append(s.status) 
    if s.status not in status_list:
            booking_status = BookingStatus(status=status)
            with app.app_context:
                db.session.add(booking_status)
                db.session.commit()
    else:
        raise Exception("Status is already exists")


def get_rooms_by_types(type_id=None):
    rooms = Room.query.all()
    if type_id:
        rooms = Room.query.filter(Room.type_id.__eq__(type_id))

    return rooms.all()

def get_type_by_price(price=None):
    types = RoomType.query.all()
    if price:
        types = RoomType.query.filter(RoomType.price.__eq__(price))

    return types.all()

def get_rooms_by_id(room_id):
    return Room.query.get(room_id)

def get_rooms_by_kw(kw, room_type_id, page=None):
    rooms = Room.query
    if kw:
        rooms = rooms.filter(Room.name.contains(kw))

    if room_type_id:
        rooms = rooms.filter(Room.type_id.__eq__(room_type_id))

    if page:
        page = int(page)
        page_size = app.config['PAGE_SIZE']
        start = (page - 1)*page_size

        return rooms.slice(start, start + page_size)

    return rooms.all()

    
def get_room_types_by_kw(kw, room_id, page=None):
    room_type = RoomType.query
    if kw:
        room_type = room_type.filter(RoomType.type.contains(kw))

    if room_id:
        room_type = room_type.filter(RoomType.rooms.__eq__(room_id))

    if page:
        page = int(page)
        page_size = app.config['PAGE_SIZE']
        start = (page - 1)*page_size

        return room_type.slice(start, start + page_size)

    return room_type.all()

def count_rooms():
    return Room.query.count()

def count_room_types():
    return RoomType.query.count()

    

def get_user_by_id(id):
    return User.query.get(id)

# QUERY DAO
def get_room_type_by_id(id):
    return Room.query.filter(Room.type_id.__eq__(id)).all() 


def revenue_room_type_month(kw=None):
    query = db.session.query(func.extract('month', BookedRoom.created_at),
                            RoomType.type, func.count(Room.id))\
                            .join(RoomType, RoomType.id == Room.type_id)\
                            .join(BookedRoom, BookedRoom.room_id == Room.id)\

    if kw:
        query = query.filter(func.extract('month', BookedRoom.created_at) == kw)
    return query.group_by(func.extract('month', BookedRoom.created_at), Room.id).all()

# def revenue_room_type_month(kw=None):
#     query = db.session.query(func.extract('month', BookedRoom.created_at),
#                             RoomType.type, func.count(Room.id))\
#                             .join(RoomType, RoomType.id == Room.type_id)\
#                             .join(BookedRoom, BookedRoom.room_id == Room.id)
#     if kw:
#         query = query.filter(RoomType.type.contains(kw))
#     return query.group_by(func.extract('month', BookedRoom.created_at), Room.id).all()


def revenue_stats_by_month(kw=None):
    query = db.session.query(func.extract('month', Payment.created_at),
                            func.sum(Payment.total_price))\
                            .join(Booking, Booking.id == Payment.booking_id)
    if kw:
        query = query.filter(func.extract('month', Payment.created_at) == kw)
    return query.group_by(func.extract('month', Payment.created_at)).all()
                            
                            
                            
                            
                            

# def revenue_stats_by_month(year=2024):
#     return db.session.query(func.extract('month', Receipt.created_date),
#                             func.sum(ReceiptDetails.price*ReceiptDetails.quantity))\
#                         .join(ReceiptDetails, ReceiptDetails.receipt_id == Receipt.id)\
#                         .filter(func.extract('year', Receipt.created_date) == year)\
#                         .group_by(func.extract('month', Receipt.created_date)).all()


def get_booked_rooms():
   rooms = Room.query.get(id) 


def create_guest(first_name, last_name, cccd, phone):
    pass

def create_booking(check_in, check_out, phone, room_id):
    room = Room.query.get()




def register(name, username, password, avatar):
    users = []
    check_pass = password
    if not strong_pass(check_pass):
        raise Exception("Password is not strong enough")
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    for u in User.query.all():
        if u.username == username:
            users.append(u.username)
    if username not in users:
        user = User(name=name.strip(), username=username.strip(),
                                password=password, avatar=avatar)
        with app.app_context():
            db.session.add(user)
            db.session.commit()
    else:
        raise Exception("Username is already exists") 



def strong_pass(client_pass):
    pass_length = len(client_pass) > 6
    pass_up = re.search(r"[A-Z]", client_pass) is not None
    pass_low = re.search(r"[a-z]", client_pass) is not None
    pass_num = re.search(r"[0-9]", client_pass) is not None
    pass_ok = not (pass_length or pass_low or pass_up or pass_num)
    if (pass_length and pass_low and pass_up and pass_num):
        return True
    else:
        return False

def check_sdt(client_sdt):
    sdt_length = len(client_sdt) >= 9 
    sdt_char_up = re.search(r"[A-Z]", client_sdt) is None
    sdt_char_spe = re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~" + r'"]', client_sdt) is None
    sdt_char_low = re.search(r"[a-z]", client_sdt) is None
    if sdt_length and sdt_char_low and sdt_char_up and sdt_char_spe:
        return True
    else:
        return False




def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()