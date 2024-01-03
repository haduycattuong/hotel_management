from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, DateTime, Boolean
from sqlalchemy.orm import relationship 
from flask_login import UserMixin
from app import app, db
from datetime import datetime
import enum

class UserRoleEnum(enum.Enum):
    USER = 1
    ADMIN = 2

class User(db.Model, UserMixin):
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)


    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    avatar = Column(String(100),
                    default='https://res.cloudinary.com/dzvzu6udg/image/upload/v1704092797/pvo703h6r92srmiioym7.jpg')
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.USER)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())
    payment = relationship('Payment', backref='user', lazy=True)
    def __str__(self):
        return self.name


class Guest(db.Model):
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)

    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(100), nullable=True)
    cccd = Column(String(100), nullable=True, unique=True)
    address = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

    bookings = relationship('Booking', backref='guest', lazy=True)

    def __str__(self):
        return self.first_name

class RoomType(db.Model):
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)

    type = Column(String(50), nullable=False)
    price = Column(Float, nullable=False, default=0)
    max_capacity = Column(Integer, nullable=False)
    img = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

    rooms = relationship('Room', backref='roomtype', lazy=False)

    def __str__(self):
        return self.type



class Room(db.Model):
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)

    img = Column(String(100), nullable=True)
    name = Column(String(50), nullable=False)
    description = Column(String(100), nullable=True)
    foreigner_rate = Column(Float,nullable=False, default=1.5)
    is_booked = Column(Boolean, nullable=False, default=False)
    add_price = Column(Float, nullable=False, default=1.25)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

    type_id = Column(Integer, ForeignKey(RoomType.id), nullable=False)
    booked_room = relationship('BookedRoom', backref='room', lazy=False)

    def __str__(self):
        return self.name 

class BookingStatus(db.Model):
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)

    status = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

    bookings = relationship('Booking', backref='bookingstatus', lazy=False)

    def __str__(self):
        return self.status


class Booking(db.Model):
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)

    guest_id = Column(Integer, ForeignKey(Guest.id), nullable=False)
    status_id = Column(Integer, ForeignKey(BookingStatus.id), nullable=False, default=1)
    booked_room = relationship('BookedRoom', backref='booking', lazy=True)

    check_in = Column(DateTime, nullable=False)
    check_out = Column(DateTime, nullable=False)
    has_foreigner = Column(Boolean, nullable=False, default=False)
    num_guest = Column(Integer, nullable=False, default=1)
    booking_price = Column(Float, nullable=False, default=0)
    phone = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())


class BookedRoom(db.Model):
    __table_args__ = {'extend_existing': True}
    booking_id = Column(Integer, ForeignKey(Booking.id), primary_key=True) 
    room_id = Column(Integer, ForeignKey(Room.id), primary_key=True) 

    price = Column(Float, nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())



    
class PaymentMethod(db.Model):
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)

    method = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

    payments = relationship('Payment', backref='paymentmethod', lazy=False)

    def __str__(self):
        return self.method

class Payment(db.Model):
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    booking_id = Column(Integer, ForeignKey(Booking.id), nullable=False)
    pay_method_id = Column(Integer, ForeignKey(PaymentMethod.id), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)

    description = Column(String(100), nullable=True)
    total_price = Column(Float, nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())
    

    def __str__(self):
        return self.name











if __name__ == '__main__':
    from app import app
    with app.app_context():
        db.create_all()

        # import hashlib


        # u = User(name='Tuong', username='admin',
        #          password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #          user_role=UserRoleEnum.ADMIN)
        # db.session.add(u)
        # db.session.commit()
        
        # guest1 = Guest(first_name='Tuong', last_name='Ha Duy Cat')
        # guest2 = Guest(first_name='Khiem', last_name='Bao')
        # db.session.add_all([guest1, guest2])
        # db.session.commit()


        # booking_status1 = BookingStatus(status='PENDING')
        # booking_status2 = BookingStatus(status='CANCELED')
        # booking_status3 = BookingStatus(status='PAID')
        # booking_status4 = BookingStatus(status='RESERVED')
        # db.session.add_all([booking_status1, booking_status2, booking_status3, booking_status4])
        # db.session.commit()

        # room_type1 = RoomType(type='single', price=150, max_capacity=3, img='https://res.cloudinary.com/dzvzu6udg/image/upload/v1704092591/vs2oaxymlefekgmmi6tl.jpg')
        # room_type2 = RoomType(type='double', price=200, max_capacity=3, img='https://res.cloudinary.com/dzvzu6udg/image/upload/v1704092591/knphsg4zwjxpppesksrm.jpg')
        # room_type3 = RoomType(type='premium', price=300, max_capacity=3, img='https://res.cloudinary.com/dzvzu6udg/image/upload/v1704092592/lccma7yonocxj3brpmj8.jpg')
        # room_type4 = RoomType(type='king', price=400, max_capacity=3, img='https://res.cloudinary.com/dzvzu6udg/image/upload/v1704092592/b0letho5eeakz3jawakw.jpg')
        # room_type5 = RoomType(type='vip', price=500, max_capacity=3, img='https://res.cloudinary.com/dzvzu6udg/image/upload/v1704092592/osyhglnk6eerlfgynuiz.jpg')
        # db.session.add_all([room_type1, room_type2, room_type3, room_type4, room_type5])
        # db.session.commit()

        
        # room1 = Room(name='101', foreigner_rate=1.5, type_id=1)
        # room2 = Room(name='102', foreigner_rate=1.5, type_id=2)
        # room3 = Room(name='103', foreigner_rate=1.5, type_id=3)
        # room4 = Room(name='201', foreigner_rate=1.5, type_id=4)
        # room5 = Room(name='202', foreigner_rate=1.5, type_id=2)
        # room6 = Room(name='203', foreigner_rate=1.5, type_id=1)
        # room7 = Room(name='301', foreigner_rate=1.5, type_id=1)
        # room8 = Room(name='302', foreigner_rate=1.5, type_id=5)
        # db.session.add_all([room1, room2, room3, room4, room5, room6, room7, room8])
        # db.session.commit()

        # booking1 = Booking(guest_id=1, status_id=3, check_in='2023-12-24', check_out='2023-12-27',
        #                    num_guest=3, has_foreigner=False)
        # booking2 = Booking(guest_id=1, status_id=3, check_in='2023-12-21', check_out='2023-12-23',
        #                    num_guest=2, has_foreigner=True)
        # booking3 = Booking(guest_id=2, status_id=1, check_in='2024-01-05', check_out='2023-01-08',
        #                    num_guest=3, has_foreigner=True)
        # booking4 = Booking(guest_id=2, status_id=3, check_in='2023-11-20', check_out='2023-11-24',
        #                    num_guest=2, has_foreigner=False)
        # db.session.add_all([booking1, booking2, booking3, booking4])
        # db.session.commit()

        # bookedroom1 = BookedRoom(booking_id=1, room_id=1)
        # bookedroom2 = BookedRoom(booking_id=2, room_id=3)
        # bookedroom3 = BookedRoom(booking_id=3, room_id=4)
        # bookedroom4 = BookedRoom(booking_id=4, room_id=2)
        # db.session.add_all([bookedroom1, bookedroom2, bookedroom3, bookedroom4])
        # db.session.commit()
        
        # pay_method1 = PaymentMethod(method='Credit Card')
        # pay_method2 = PaymentMethod(method='Cash')
        # pay_method3 = PaymentMethod(method='Momo')
        # db.session.add_all([pay_method1, pay_method2, pay_method3])
        # db.session.commit()

        # payment1 = Payment(booking_id=1, user_id=1, pay_method_id=2)
        # payment2 = Payment(booking_id=2, user_id=1, pay_method_id=1)
        # payment3 = Payment(booking_id=4, user_id=1, pay_method_id=2)
        # db.session.add_all([payment1, payment2, payment3])
        # db.session.commit()