from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, DateTime, DECIMAL
from sqlalchemy.orm import relationship
from app import db
from flask_login import UserMixin
import enum


class UserRoleEnum(enum.Enum):
    USER = 1
    ADMIN = 2

class Hotel(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(String(100), nullable=True)
    address  = Column(String(100), nullable=True)

    rooms = relationship("Room", backref="hotel")
    User = relationship("User", backref="hotel")

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    hotel_id = Column(Integer, ForeignKey=True, nullable=False)
    full_name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    avatar = Column(String(100),
                    default='https://res.cloudinary.com/dxxwcby8l/image/upload/v1690461425/bqjr27d0xjx4u78ghp3s.jpg')
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.USER)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)

    def __str__(self):
        return self.name


class Guest_Type(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(50), nullable=False, unique=True)
    price = Column(DECIMAL, nullable=False, default=0)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)

    guests = relationship("Guest", backref="guest_type")

class Guest(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    guest_type_id = Column(Integer, ForeignKey(Guest_Type.id), nullable=False)
    full_name = Column(String(100), nullable=False)
    cccd = Column(Integer, nullable=False, unique=True)
    address = Column(String(100), nullable=True)

    bookings = relationship("Booking", backref="guest")

    def __str__(self):
        return self.fullname

class Room_Type(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(50), nullable=False)
    price = Column(DECIMAL, nullable=False, default=0)
    capacity = Column(Integer, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)

    rooms = relationship("Room", backref="room_type")

class Room(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    hotel_id = Column(Integer, ForeignKey(Hotel.id), nullable=False)
    type_id = Column(Integer, ForeignKey(Room_Type.id), nullable=False)
    name = Column(String(50), nullable=False)
    description = Column(String(100), nullable=True)

    booking_room = relationship("Booking_Room", back_populates="room")

    def __str__(self):
        return self.name

class Num_Guest(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    size = Column(Integer, nullable=False)
    price = Column(Float, default=0)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)

class Booking(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    guest_id = Column(Integer, ForeignKey(Guest.id), nullable=False)
    room_id = Column(Integer, ForeignKey(Room.id), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    num_guest_id = Column(Integer, ForeignKey(Num_Guest.id), nullable=False)
    check_in = Column(DateTime, nullable=False)
    check_out = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False)

    booking_room = relationship("Booking_Room", back_populates="booking")



class Booking_Room(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    booking_id = Column(Integer, ForeignKey(Booking.id), nullable=False)
    room_id = Column(Integer, ForeignKey(Room.id), nullable=False)
    created_at = Column(DateTime, nullable=False)

    booking = relationship("Booking", back_populates="booking_room")
    room = relationship("Room", back_populates="booking_room")
    payment = relationship("Payment", back_populates="booking_room")

    
class Payment_Method(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    method = Column(String(50), nullable=False)

    payments = relationship("Payment", backref="payment_method")

    def __str__(self):
        return self.method

class Payment(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    booking_id = Column(Integer, ForeignKey(Booking.id), nullable=False)
    pay_method_id = Column(Integer, ForeignKey(Payment_Method.id), nullable=False)
    created_at = Column(DateTime, nullable=False)
    description = Column(String(100), nullable=True)
    

    def __str__(self):
        return self.name











if __name__ == '__main__':
    from app import app
    with app.app_context():
        db.create_all()

        import hashlib
        u = User(name='Admin', username='admin',
                 password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
                 user_role=UserRoleEnum.ADMIN)
        db.session.add(u)
        db.session.commit()

