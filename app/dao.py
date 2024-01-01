from app.models import User, Room, RoomType, Booking, Payment, PaymentMethod, Guest, BookingStatus, AdditionalPrice
from app import app, db
import hashlib
import re
from sqlalchemy import func






def get_add_price():
    return AdditionalPrice.query.all()

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


def get_booked_rooms():
   rooms = Room.query.get(id) 







def add_user(username, password, avatar):
    users = []
    check_pass = password


def strong_pass(client_pass):
    pass_length = len(client_pass) > 8
    pass_up = re.search(r"[A-Z]", client_pass) is not None
    pass_low = re.search(r"[a-z]", client_pass) is not None
    pass_ok = not (pass_length or pass_low or pass_up)
    if (pass_length and pass_low and pass_up):
        return True
    else:
        return False

def check_sdt(client_sdt):
    sdt_length = len(client_sdt) >= 10
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