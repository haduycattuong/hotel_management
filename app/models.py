from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, DateTime, DECIMAL, MetaData, Table, Boolean
from sqlalchemy.orm import relationship, DeclarativeBase
from app import db
from flask_login import UserMixin
from datetime import datetime
import enum


class Base(DeclarativeBase):
    pass
class UserRoleEnum(enum.Enum):
    USER = 1
    ADMIN = 2

class BaseModel(db.Model):
    """The BaseModel class from which future classes will be derived"""
    __abstract__ = True

    id = Column(Integer(60), primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

class Hotel(BaseModel, db.Model):
    name = Column(String(50), nullable=False)
    description = Column(String(100), nullable=True)
    address  = Column(String(100), nullable=True)

    rooms = relationship("Room", backref="hotel")
    users = relationship("User", backref="hotel")

    def __str__(self):
        return self.name


class User(BaseModel, db.Model, UserMixin):
    hotel_id = Column(Integer, ForeignKey=(Hotel.id), nullable=False)
    full_name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    avatar = Column(String(100),
                    default='https://res.cloudinary.com/dxxwcby8l/image/upload/v1690461425/bqjr27d0xjx4u78ghp3s.jpg')
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.USER)

    def __str__(self):
        return self.name


class Guest(BaseModel, db.Model):
    full_name = Column(String(100), nullable=False)
    cccd = Column(Integer, nullable=False, unique=True)
    address = Column(String(100), nullable=True)

    bookings = relationship("Booking", backref="guest")

    def __str__(self):
        return self.fullname

class Room_Type(BaseModel, db.Model):
    type = Column(String(50), nullable=False)
    price = Column(DECIMAL, nullable=False, default=0)
    max_capacity = Column(Integer, nullable=False)

    rooms = relationship("Room", backref="room_type")

class Additional_Price(BaseModel, db.Model):
    price_rate = Column(Float, nullable=False, default=1)

    rooms = relationship("Room", backref="additional_price")
class Room_Img(BaseModel, db.Model):
    img_url = Column(String(100), nullable=False) 

    rooms = relationship("Room", backref="room_img")

class Room(BaseModel, db.Model):
    hotel_id = Column(Integer, ForeignKey(Hotel.id), nullable=False)
    type_id = Column(Integer, ForeignKey(Room_Type.id), nullable=False)
    img_id = Column(Integer, ForeignKey(Room_Img.id), nullable=False)
    add_price_id = Column(Integer, ForeignKey(Additional_Price.id), nullable=False)

    name = Column(String(50), nullable=False)
    description = Column(String(100), nullable=True)
    foreigner_rate = Column(Float,nullable=False, default=1.5)
    is_booked = Column(Boolean, nullable=False, default=False)

    def __str__(self):
        return self.name

class Booking_Status(BaseModel, db.Model):
    status = Column(String(100), nullable=False)

    bookings = relationship("Booking", backref="booking_status")
booking_room = Table("booking_room", Base.metadata,
    Column("booking_id", Integer, 
           ForeignKey("Booking.id", onupdate='CASCADE', ondelete='CASCADE'), primary_key=True),
    Column("room_id", Integer,
           ForeignKey("Room.id", onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
)
class Booking(BaseModel, db.Model):
    guest_id = Column(Integer, ForeignKey(Guest.id), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    rooms = relationship("Room", secondary=booking_room, backref="booking", viewonly=False)

    check_in = Column(DateTime, nullable=False)
    check_out = Column(DateTime, nullable=False)




# class Booking_Room(db.Model):
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     booking_id = Column(Integer, ForeignKey(Booking.id), nullable=False)
#     room_id = Column(Integer, ForeignKey(Room.id), nullable=False)
#     created_at = Column(DateTime, nullable=False)

    
class Payment_Method(BaseModel, db.Model):
    method = Column(String(50), nullable=False)

    payments = relationship("Payment", backref="payment_method")

    def __str__(self):
        return self.method

class Payment(BaseModel, db.Model):
    booking_id = Column(Integer, ForeignKey(Booking.id), nullable=False)
    pay_method_id = Column(Integer, ForeignKey(Payment_Method.id), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)

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

