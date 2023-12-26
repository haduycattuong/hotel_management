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

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

class Hotel(BaseModel, db.Model):
    name = Column(String(100), nullable=False)
    description = Column(String(100), nullable=True)
    address  = Column(String(100), nullable=True)

    rooms = relationship("Room", backref="hotel")
    users = relationship("User", backref="hotel")

    def __str__(self):
        return self.name


class User(BaseModel, db.Model, UserMixin):
    hotel_id = Column(Integer, ForeignKey=(Hotel.id), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    avatar = Column(String(100),
                    default='https://res.cloudinary.com/dxxwcby8l/image/upload/v1690461425/bqjr27d0xjx4u78ghp3s.jpg')
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.USER)

    def __str__(self):
        return self.name


class Guest(BaseModel, db.Model):
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    cccd = Column(Integer, nullable=False, unique=True)
    address = Column(String(100), nullable=True)

    bookings = relationship("Booking", backref="guest")

    def __str__(self):
        return self.id + self.full_name + self.cccd

class Room_Type(BaseModel, db.Model):
    type = Column(String(50), nullable=False)
    price = Column(Float, nullable=False, default=0)
    max_capacity = Column(Integer, nullable=False)

    rooms = relationship("Room", backref="room_type")

    def __str__(self):
        return self.id + self.type + self.price + self.max_capacity

class Additional_Price(BaseModel, db.Model):
    price_rate = Column(Float, nullable=False, default=1)
    price_value = Column(Float, nullable=False, default=0)

    rooms = relationship("Room", backref="additional_price")
class Room_Img(BaseModel, db.Model):
    img_url = Column(String(100), nullable=False) 

    rooms = relationship("Room", backref="room_img")

class Room(BaseModel, db.Model):
    hotel_id = Column(Integer, ForeignKey(Hotel.id), nullable=False)
    type_id = Column(Integer, ForeignKey(Room_Type.id), nullable=False)
    img_id = Column(Integer, ForeignKey(Room_Img.id), nullable=False, default=1)
    add_price_id = Column(Integer, ForeignKey(Additional_Price.id), nullable=False, default=1)

    name = Column(String(50), nullable=False)
    description = Column(String(100), nullable=True)
    foreigner_rate = Column(Float,nullable=False, default=1.5)
    is_booked = Column(Boolean, nullable=False, default=False)

    def __str__(self):
        return self.name

class Booking_Status(BaseModel, db.Model):
    status = Column(String(100), nullable=False)

    bookings = relationship("Booking", backref="booking_status")

#association table
booking_room = Table("booking_room", Base.metadata,
    Column("booking_id", Integer, 
           ForeignKey("Booking.id", onupdate='CASCADE', ondelete='CASCADE'), primary_key=True),
    Column("room_id", Integer,
           ForeignKey("Room.id", onupdate='CASCADE', ondelete='CASCADE'), primary_key=True),
)
class Booking(BaseModel, db.Model):
    guest_id = Column(Integer, ForeignKey(Guest.id), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    status_id = Column(Integer, ForeignKey(Booking_Status.id), nullable=False)
    rooms = relationship("Room", secondary=booking_room, backref="booking")

    check_in = Column(DateTime, nullable=False)
    check_out = Column(DateTime, nullable=False)
    has_foreigner = Column(Boolean, nullable=False, default=False)
    num_guest = Column(Integer, nullable=False, default=1)
    booking_price = Column(Float, nullable=False, default=0)




# class Booking_Room(BaseModel, db.Model):
#     booking_id = Column(Integer, ForeignKey(Booking.id), nullable=False)
#     room_id = Column(Integer, ForeignKey(Room.id), nullable=False)



    
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
    price = Column(Float, nullable=False, default=0)
    

    def __str__(self):
        return self.name











if __name__ == '__main__':
    from app import app
    with app.app_context():
        db.create_all()

        import hashlib
        user_admin = User(name='Admin', username='admin',
                 password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
                 user_role=UserRoleEnum.ADMIN)
        db.session.add(user_admin)
        db.session.commit()

        
        hotel = Hotel(name='Khach san CT', address='15/9 TBT p5 QBT')
        db.session.add(hotel)
        db.session.commit()
        
        guest1 = Guest(first_name='Tuong', last_name='Ha Duy Cat', cccd='079201023111')
        guest2 = Guest(first_name='Khiem', last_name='Bao')
        db.session.add_all(guest1, guest2)
        db.session.commit()

        add_price1 = Additional_Price(price_rate=1, price_value=0) 
        add_price2 = Additional_Price(price_rate=1.25)
        db.session.add_all(add_price1, add_price2)
        db.session.commit()


        booking_status1 = Booking_Status(status='PENDING')
        booking_status2 = Booking_Status(status='CANCELED')
        booking_status3 = Booking_Status(status='PAID')
        booking_status4 = Booking_Status(status='RESERVED')
        db.session.add_all(booking_status1, booking_status2, booking_status3, booking_status4)
        db.session.commit()

        room_type1 = Room_Type(type='single', price=150, max_capacity=3)
        room_type2 = Room_Type(type='double', price=200, max_capacity=3)
        room_type3 = Room_Type(type='premium', price=300, max_capacity=3)
        room_type4 = Room_Type(type='king', price=400, max_capacity=3)
        db.session.add_all(room_type1, room_type2, room_type3, room_type4)
        db.session.commit()

        room_img = Room_Img()
        
        room1 = Room(name='101', foreigner_rate=1.5, 
                     hotel_id=1, type_id=1, img_id=1, add_price_id=1)
        room2 = Room(name='102', foreigner_rate=1.5, 
                     hotel_id=1, type_id=2, img_id=2, add_price_id=1)
        room3 = Room(name='103', foreigner_rate=1.5, 
                     hotel_id=1, type_id=3, img_id=3, add_price_id=1)
        room4 = Room(name='201', foreigner_rate=1.5, 
                     hotel_id=1, type_id=4, img_id=1, add_price_id=1)
        room5 = Room(name='202', foreigner_rate=1.5, 
                     hotel_id=1, type_id=2, img_id=1, add_price_id=1)
        room6 = Room(name='203', foreigner_rate=1.5, 
                     hotel_id=1, type_id=1, img_id=1, add_price_id=1)
        room7 = Room(name='301', foreigner_rate=1.5, 
                     hotel_id=1, type_id=1, img_id=1, add_price_id=1)
        db.session.add_all(room1, room2, room3, room4, room5, room6, room7)
        db.session.commit()

        booking1 = Booking()
        
        pay_method1 = Payment_Method(method='Credit Card')
        pay_method2 = Payment_Method(method='Cash')
        pay_method3 = Payment_Method(method='Momo')
        db.session.add_all(pay_method1, pay_method2, pay_method3)
        db.session.commit()

        payment1 = Payment()
