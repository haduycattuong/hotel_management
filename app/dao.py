from app.models import User, Room, RoomType, Booking, Payment, PaymentMethod, Guest, BookingStatus, AdditionalPrice
from app import app, db
import hashlib







def get_payment():
    return Payment.query.all()

def get_bookings():
    return Booking.query.all()

def get_room_types():
    return RoomType.query.all()

def get_rooms(kw, room_type_id, page=None):
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

def count_rooms():
    return Room.query.count()

def get_user_by_id(id):
    return User.query.get(id)

def add_user(username, password, avatar):
    users = []
    check_pass = password

def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()