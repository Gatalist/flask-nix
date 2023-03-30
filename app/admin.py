from flask_admin.contrib.sqla import ModelView


class GenreView(ModelView):
    pass
    # form_columns = ['name',]

class UserView(ModelView):
    pass
    # form_columns = ['username', 'email',]

class MovieView(ModelView):
    pass
    # form_columns = ['user_id', 'title', 'reliase', 'ganre', 'director_id', 'rating_id', 'poster', 'description']
    # column_sortable_list = ('name', 'last_name')
    # column_exclude_list = ('last_name', 'email')

class RatingView(ModelView):
    pass
    # form_columns = ['star',]

class DirectorView(ModelView):
    pass
    # form_columns = ['name',]

