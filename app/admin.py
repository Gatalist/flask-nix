import random, os
from flask_admin.contrib.sqla import ModelView
from flask_admin import form
from .settings import Config


class GenreView(ModelView):
    pass
    # form_columns = ['name',]


class UserView(ModelView):
    pass
    # form_columns = ['username', 'email',]


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
        return self._change_path_data(
            super(MovieView, self).edit_form(obj)
        )

    def create_form(self, obj=None):
        return self._change_path_data(
            super(MovieView, self).create_form(obj)
        )


class RatingView(ModelView):
    pass
    # form_columns = ['star',]


class DirectorView(ModelView):
    pass
    # form_columns = ['name',]


