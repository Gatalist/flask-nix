import random, os
from flask import url_for, redirect, request, abort, jsonify
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, form, helpers, expose, AdminIndexView
from flask_security import SQLAlchemyUserDatastore, Security
from flask_login import current_user, logout_user

from app import app, db
from app.settings import Config
from app.movies.models import Genres, Movies, Ratings, Directors, Reliase
from app.users.models import Users, Role


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, Users, Role)
security = Security(app, user_datastore)



class MovieView(ModelView):
    # pass
    # column_sortable_list = ('name', 'last_name')
    # column_exclude_list = ('last_name', 'email')

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

    def edit_form(self, obj=None):
        print(current_user.id)
        print(obj.user.id)
        if current_user.has_role('admin') or current_user.id == obj.user.id:
            return self._change_path_data(
                super(MovieView, self).edit_form(obj)
            )
        else:
            abort(403)

    def create_form(self, obj=None):
        return self._change_path_data(
            super(MovieView, self).create_form(obj)
        )

    def delete_model(self, obj):
        print("Delete")
        if current_user.has_role('admin') or current_user.id == obj.user.id:
            return self._change_path_data(
                super(MovieView, self).delete_model(obj)
            )
        else:
            abort(403)

# Create customized model view class
class MyModelView(ModelView):

    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and
                current_user.has_role('admin')
                )

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                return redirect(url_for('security.login', next=request.url))


# Переадресация страниц (используется в шаблонах)
class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('.login_page'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_page(self):
        if current_user.is_authenticated:
            return redirect(url_for('.index'))
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_page(self):
        logout_user()
        return redirect(url_for('.index'))

    @expose('/reset/')
    def reset_page(self):
        return redirect(url_for('.index'))


# Create admin
admin_panel = Admin(app, index_view=MyAdminIndexView(), base_template='admin/master-extended.html')

admin_panel.add_view(ModelView(Genres, db.session))
admin_panel.add_view(MovieView(Movies, db.session))
admin_panel.add_view(ModelView(Ratings, db.session))
admin_panel.add_view(ModelView(Directors, db.session))
admin_panel.add_view(ModelView(Reliase, db.session))
admin_panel.add_view(ModelView(Role, db.session))
# admin_panel.add_view(ModelView(Users, db.session))
admin_panel.add_view(MyModelView(Users, db.session))


# define a context processor for merging flask-admin's template context into the
# flask-security views.
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin_panel.base_template,
        admin_view=admin_panel.index_view,
        h=helpers,
        get_url=url_for
    )