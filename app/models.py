from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app import db
from flask_login import UserMixin
import enum


class UserRoleEnum(enum.Enum):
    USER = 1
    ADMIN = 2


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    avatar = Column(String(100),
                    default='https://res.cloudinary.com/dxxwcby8l/image/upload/v1690461425/bqjr27d0xjx4u78ghp3s.jpg')
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.USER)

    def __str__(self):
        return self.name

class Guest(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    fullname = Column(String(100), nullable=False)
    cccd = Column(Integer, nullable=False)
    address = Column(String(100), nullable=True)

class RoomType(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(50), nullable=False, unique=True)
    price = Column(Float, default=0)

class Hotel(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(String(100), nullable=True)
    address  = Column(String(100), nullable=True)

class Booking(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)

    guest_id = Column(Integer, ForeignKey(Guest.id), nullable=False)

class Room(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(String(100), nullable=True)
    hotel_id = Column(Integer, ForeignKey(Hotel.id), nullable=False)
    type_id = Column(Integer, ForeignKey(RoomType.id), nullable=False)

class Booking_Room(db.Model):
    booking_id = Column(Integer, ForeignKey(Booking.id), nullable=False)
    room_id = Column(Integer, ForeignKey(Room.id), nullable=False)
    booked_date = Column(String(50), nullable=False)













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

