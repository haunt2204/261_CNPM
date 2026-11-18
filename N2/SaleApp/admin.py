from flask_admin.theme import Bootstrap4Theme
from SaleApp import app, db
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from models import Category




class CategoryModelView(ModelView):
    form_columns = ('name', )


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self) -> str:
        return self.render('admin/index.html')


admin = Admin(app, name="E-COMMERCE", theme=Bootstrap4Theme(), index_view=MyAdminIndexView())
admin.add_view(CategoryModelView(Category, db.session))
