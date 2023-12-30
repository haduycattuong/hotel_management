from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, BaseView, expose
from app import app, db
from app.models import *
from flask_login import logout_user, current_user
from flask import redirect


class AuthenticatedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.ADMIN


class AuthenticatedUser(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated



class StatsView(AuthenticatedUser):
    @expose("/")
    def index(self):
        return self.render('admin/stats.html')


class LogoutView(AuthenticatedUser):
    @expose("/")
    def index(self):
        logout_user()
        return redirect('/admin')


admin = Admin(app=app, name='QUẢN TRỊ KHÁCH SẠN', template_mode='bootstrap4')
admin.add_view(ModelView(Room, db.session, name="Phòng"))
admin.add_view(ModelView(RoomType, db.session, name="Loại Phòng"))
admin.add_view(ModelView(Guest, db.session, name="Khách hàng"))
admin.add_view(ModelView(Payment, db.session, name="Thanh toán"))
admin.add_view(ModelView(PaymentMethod, db.session, name="Phương thức thanh toán"))
admin.add_view(ModelView(AdditionalPrice, db.session, name="Giá bổ sung"))
admin.add_view(ModelView(BookedRoom, db.session, name="BookedRoom"))
admin.add_view(ModelView(Booking, db.session, name="Booking"))
admin.add_view(ModelView(BookingStatus, db.session, name="Phương thức book"))
admin.add_view(StatsView(name='Thông kê báo cáo'))
admin.add_view(LogoutView(name='Đăng xuất'))
