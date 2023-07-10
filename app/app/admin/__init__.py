from flask import url_for
from flask_admin import Admin, helpers
from flask_security import SQLAlchemyUserDatastore, Security

from app import app, db
from app.movies.models import Genres, Movies, Ratings, Directors, Reliase
from app.users.models import Users, Role
from .routes import MyAdminIndexView, UsersView
from .routes import MovieView, GenresView, RatingsView, DirectorsView, ReliaseView, RoleView


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, Users, Role)
security = Security(app, user_datastore)


# Create admin
admin_panel = Admin(app, index_view=MyAdminIndexView(), base_template='admin/master-extended.html')


admin_panel.add_view(GenresView(Genres, db.session))
admin_panel.add_view(MovieView(Movies, db.session))
admin_panel.add_view(RatingsView(Ratings, db.session))
admin_panel.add_view(DirectorsView(Directors, db.session))
admin_panel.add_view(ReliaseView(Reliase, db.session))
admin_panel.add_view(RoleView(Role, db.session))
admin_panel.add_view(UsersView(Users, db.session))


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
