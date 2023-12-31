from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, BaseView, expose
from app import app, db
from app.models import *
from flask_login import logout_user, current_user
from flask import redirect, request
from wtforms import fields
import dao



class AuthenticatedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.ADMIN


class AuthenticatedUser(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated



class StatsView(AuthenticatedUser):
    @expose("/")
    def index(self):
        kw = request.args.get("kw")
        return self.render('admin/stats.html',
                           stats=dao.revenue_room_type_month(kw),
                           month_stats=dao.revenue_stats_by_month(kw))


class LogoutView(AuthenticatedUser):
    @expose("/")
    def index(self):
        logout_user()
        return redirect('/admin')
        
class AdminView(AuthenticatedAdmin):
  can_delete = False
  can_edit = False
  can_create = True

class BookingView(AuthenticatedAdmin):
    column_list = ['id', 'guest_id', 'bookingstatus', 'num_guest', 'has_foreigner', 'booking_price',
                   'check_in', 'check_out', 'created_at', 'phone']    
    column_searchable_list = ['guest_id', 'status_id', 'num_guest', 'has_foreigner', 'booking_price',
                   'check_in', 'check_out', 'created_at', 'phone']
    column_editable_list = ['status_id', 'num_guest', 'has_foreigner', 'booking_price', 'created_at']

    can_export = True
    can_delete = True
    can_edit = True

class StatusView(AuthenticatedAdmin):
    column_list = ['id', 'status']    
    column_searchable_list = ['status']
    column_editable_list = ['status']

    can_delete = True
    can_edit = True
    can_create = True
class RoomView(AuthenticatedAdmin):
    column_list = ['id', 'name', 'foreigner_rate', 'roomtype', 'add_price']    
    column_searchable_list = ['name']
    column_editable_list = ['name', 'description', 'foreigner_rate', 'type_id', 'add_price']

    column_display_all_relations = True

class RoomTypeView(AuthenticatedAdmin):
    column_list = ['id', 'type', 'price', 'max_capacity', 'rooms']    
    column_searchable_list = ['type', 'price']
    column_editable_list = ['type', 'price', 'max_capacity', 'rooms']

    can_delete = True
    can_edit = True
    can_create = True

class PaymentView(AuthenticatedAdmin):
    column_list = ['id','description', 'total_price', 'created_at']    
    column_searchable_list = ['id']
    column_editable_list = ['description', 'total_price']

    can_delete = True
    can_edit = True
    can_create = True
    can_export = True

class PaymentMethodView(AuthenticatedAdmin):
    column_list = ['id', 'method']    
    column_searchable_list = ['method']
    column_editable_list = ['method']

    can_delete = True
    can_edit = True
    can_create = True


class GuestView(AuthenticatedAdmin):
    column_list = ['id', 'first_name', 'last_name', 'cccd', 'address', 'bookings']    
    column_searchable_list = ['first_name', 'last_name', 'cccd', 'address']
    column_editable_list = ['first_name', 'last_name', 'cccd', 'address']

    can_delete = False
    can_edit = True
    can_create = True

class BookedRoomView(AuthenticatedAdmin):
    column_list = ['booking_id', 'room_id', 'price', 'created_at']    
    column_searchable_list = ['booking_id', 'room_id', 'price', 'created_at']
    column_editable_list = ['price']

    can_delete = True
    can_edit = True
    can_create = True
    

admin = Admin(app=app, name='HOTEL MANAGEMENT', template_mode='bootstrap4')
admin.add_view(RoomView(Room, db.session))
admin.add_view(RoomTypeView(RoomType, db.session))
admin.add_view(GuestView(Guest, db.session))
admin.add_view(PaymentView(Payment, db.session))
admin.add_view(PaymentMethodView(PaymentMethod, db.session))
admin.add_view(BookedRoomView(BookedRoom, db.session))
admin.add_view(BookingView(Booking, db.session))
admin.add_view(StatusView(BookingStatus, db.session))
admin.add_view(StatsView(name='REPORT'))
admin.add_view(LogoutView(name='Logout'))
