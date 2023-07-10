import random, os
from app.settings import Config
from flask_admin import form, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from flask import url_for, redirect, request, abort
from .services import MixinRoleModelView



class MovieView(MixinRoleModelView):
    column_list = ['id', 'title', 'reliase', 'director', 'rating', 'genres', 'user']
    page_size = 20
    form_extra_fields = {
        'file': form.FileUploadField(base_path=Config.MEDIA_PATH)
    }

    def _change_path_data(self, _form):
        try:
            storage_file = _form.file.data

            if storage_file is not None:
                hash = random.getrandbits(128)
                ext = storage_file.filename.split('.')[-1]
                name = f'{hash}.{ext}'
                path_file = os.path.join(Config.MEDIA_PATH, name)
                storage_file.save(
                    path_file
                )
                _form.poster.data = path_file
                del _form.file
        except Exception as ex:
            pass
        return _form
    

class GenresView(ModelView):
   pass


class RatingsView(ModelView):
   pass


class DirectorsView(ModelView):
   pass

class ReliaseView(ModelView):
   pass


class RoleView(ModelView):
   pass


class UsersView(ModelView):
    pass
    # def is_accessible(self):
    #     return (current_user.is_active and
    #             current_user.is_authenticated and
    #             current_user.has_role('Admin')
    #             )

    # def _handle_view(self, name, **kwargs):
    #     """
    #     Override builtin _handle_view in order to redirect users when a view is not accessible.
    #     """
    #     if not self.is_accessible():
    #         if current_user.is_authenticated:
    #             # permission denied
    #             abort(403)
    #         else:
    #             return redirect(url_for('app_users.login', next=request.url))


# Переадресация страниц (используется в шаблонах)
class MyAdminIndexView(AdminIndexView):
    # @expose('/user/profile/')
    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('app_users.profile'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_page(self):
        if current_user.is_authenticated:
            return redirect(url_for('app_users.login'))
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_page(self):
        logout_user()
        return redirect(url_for('app_users.logout'))

