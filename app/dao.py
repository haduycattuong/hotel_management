from app.models import User, Room, Room_Type, Booking, Payment, Payment_Method, Guest, Booking_Status, Additional_Price, Room_Img

from app import app, db
import hashlib













def load_rooms():
    return Room.query.all()

def get_user_by_id(id):
    return User.query.get(id)

# def add_user(username, password, avatar):

def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()