from flask import redirect
from flask_admin import Admin, AdminIndexView, expose, BaseView
from flask_admin.contrib.sqla import ModelView
from flask_admin.theme import Bootstrap4Theme
from SaleApp import app, db
from models import Category, Product, UserRole
from flask_login import logout_user, current_user



class MyCategoryView(ModelView):
    column_list = ["id", "name"]
    column_searchable_list = ["name"]
    column_filters = ["name"]

    def is_accessible(self) -> bool:
        return current_user.is_authenticated and current_user.role == UserRole.ADMIN

class MyProductView(ModelView):
    column_list = ["id", "name", "price", "image"]

    def is_accessible(self) -> bool:
        return current_user.is_authenticated

class MyAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        return self.render("admin/index.html")

class MyStatView(BaseView):
    @expose("/")
    def index(self):
        return self.render("admin/stats.html")
    def is_accessible(self) -> bool:
        return current_user.is_authenticated

class MyLogoutView(BaseView):
    @expose("/")
    def index(self):
        logout_user()
        return redirect("/admin")
    def is_accessible(self) -> bool:
        return current_user.is_authenticated

admin = Admin(app=app, name="E-COMMERCE", theme=Bootstrap4Theme(), index_view=MyAdminIndexView())

admin.add_view(MyCategoryView(Category, db.session))
admin.add_view((MyProductView(Product, db.session)))
admin.add_view(MyStatView(name="Thống kê"))
admin.add_view(MyLogoutView(name="Đăng xuất"))