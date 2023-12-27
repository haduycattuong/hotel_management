from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, DateTime, Boolean
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

class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    avatar = Column(String(100),
                    default='https://res.cloudinary.com/dxxwcby8l/image/upload/v1690461425/bqjr27d0xjx4u78ghp3s.jpg')
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.USER)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())
    def __str__(self):
        return self.name


class Guest(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)

    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    cccd = Column(String(100), nullable=True, unique=True)
    address = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())

    bookings = relationship("Booking", backref="guest")

    def __str__(self):
        return self.id + self.full_name + self.cccd

class RoomType(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)

    type = Column(String(50), nullable=False)
    price = Column(Float, nullable=False, default=0)
    max_capacity = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())

    rooms = relationship("Room", backref="roomtype")

    def __str__(self):
        return self.id + self.type + self.price + self.max_capacity

class AdditionalPrice(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)

    price_rate = Column(Float, nullable=False, default=1)
    price_value = Column(Float, nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())

    rooms = relationship("Room", backref="additionalprice")
class RoomImg(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    img_url = Column(String(100), nullable=False) 
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())

    rooms = relationship("Room", backref="roomimg", lazy=True)

class Room(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    type_id = Column(Integer, ForeignKey(RoomType.id), nullable=False)
    img_id = Column(Integer, ForeignKey(RoomImg.id), nullable=False, default=1)
    add_price_id = Column(Integer, ForeignKey(AdditionalPrice.id), nullable=False, default=1)

    booking_room = relationship('BookingRoom', backref='room', lazy=True)
    name = Column(String(50), nullable=False)
    description = Column(String(100), nullable=True)
    foreigner_rate = Column(Float,nullable=False, default=1.5)
    is_booked = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())

    def __str__(self):
        return self.name

class BookingStatus(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)

    status = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())

    bookings = relationship("Booking", backref="bookingstatus")


class Booking(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)

    guest_id = Column(Integer, ForeignKey(Guest.id), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    status_id = Column(Integer, ForeignKey(BookingStatus.id), nullable=False, default=1)
    booking_room = relationship('BookingRoom', backref='booking', lazy=True)

    check_in = Column(DateTime, nullable=False)
    check_out = Column(DateTime, nullable=False)
    has_foreigner = Column(Boolean, nullable=False, default=False)
    num_guest = Column(Integer, nullable=False, default=1)
    booking_price = Column(Float, nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())


class BookingRoom(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)

    booking_id = Column(Integer, ForeignKey(Booking.id), nullable=False) 
    room_id = Column(Integer, ForeignKey(Room.id), nullable=False) 

    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())



    
class PaymentMethod(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)

    method = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())

    payments = relationship("Payment", backref="paymentmethod")

    def __str__(self):
        return self.method

class Payment(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    booking_id = Column(Integer, ForeignKey(Booking.id), nullable=False)
    pay_method_id = Column(Integer, ForeignKey(PaymentMethod.id), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)

    description = Column(String(100), nullable=True)
    price = Column(Float, nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())
    

    def __str__(self):
        return self.name











if __name__ == '__main__':
    from app import app
    with app.app_context():
        db.create_all()

        import hashlib


        # u = User(name='Tuong', username='admin',
        #          password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #          user_role=UserRoleEnum.ADMIN)
        # db.session.add(u)
        # db.session.commit()
        
        # guest1 = Guest(first_name='Tuong', last_name='Ha Duy Cat')
        # guest2 = Guest(first_name='Khiem', last_name='Bao')
        # db.session.add_all([guest1, guest2])
        # db.session.commit()

        # add_price1 = AdditionalPrice(price_rate=1, price_value=0) 
        # add_price2 = AdditionalPrice(price_rate=1.25)
        # db.session.add_all([add_price1, add_price2])
        # db.session.commit()


        # booking_status1 = BookingStatus(status='PENDING')
        # booking_status2 = BookingStatus(status='CANCELED')
        # booking_status3 = BookingStatus(status='PAID')
        # booking_status4 = BookingStatus(status='RESERVED')
        # db.session.add_all([booking_status1, booking_status2, booking_status3, booking_status4])
        # db.session.commit()

        # room_type1 = RoomType(type='single', price=150, max_capacity=3)
        # room_type2 = RoomType(type='double', price=200, max_capacity=3)
        # room_type3 = RoomType(type='premium', price=300, max_capacity=3)
        # room_type4 = RoomType(type='king', price=400, max_capacity=3)
        # db.session.add_all([room_type1, room_type2, room_type3, room_type4])
        # db.session.commit()

        # room_img1 = RoomImg(img_url="wiueqrpoqwuewq")
        # room_img2 = RoomImg(img_url="awoeiruoweurw")
        # db.session.add_all([room_img1, room_img2])
        # db.session.commit()
        
        # room1 = Room(name='101', foreigner_rate=1.5, 
        #              type_id=1, img_id=1, add_price_id=1)
        # room2 = Room(name='102', foreigner_rate=1.5, 
        #              type_id=2, img_id=2, add_price_id=1)
        # room3 = Room(name='103', foreigner_rate=1.5, 
        #              type_id=3, img_id=2, add_price_id=1)
        # room4 = Room(name='201', foreigner_rate=1.5, 
        #              type_id=4, img_id=2, add_price_id=1)
        # room5 = Room(name='202', foreigner_rate=1.5, 
        #              type_id=2, img_id=1, add_price_id=1)
        # room6 = Room(name='203', foreigner_rate=1.5, 
        #              type_id=1, img_id=1, add_price_id=1)
        # room7 = Room(name='301', foreigner_rate=1.5, 
        #              type_id=1, img_id=1, add_price_id=1)
        # db.session.add_all([room1, room2, room3, room4, room5, room6, room7])
        # db.session.commit()

        # # booking1 = Booking()
        
        # pay_method1 = PaymentMethod(method='Credit Card')
        # pay_method2 = PaymentMethod(method='Cash')
        # pay_method3 = PaymentMethod(method='Momo')
        # db.session.add_all([pay_method1, pay_method2, pay_method3])
        # db.session.commit()

        # # payment1 = Payment()
