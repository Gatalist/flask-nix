from flask import Blueprint
from flask import render_template
from flask import request
from .services import is_activate_filter, is_active_sorted, activate_filter, search_movie
from .models import Reliase, Genres, Directors
from app.settings import Config

movie = Blueprint('app_movies', __name__, template_folder='templates', static_folder='static')


data_sorted = [
        {'value': "standart", 'text': 'стандартная',},
        {'value': "rating_asc", 'text': 'От мин до мах рейтинга',},
        {'value': "rating_desc", 'text': 'От мах до мин рейтинга',},
        {'value': "release_date_asc", 'text': 'От старых до новых',},
        {'value': "release_date_desc", 'text': 'От новых до старых',},
    ]


@movie.route('/', methods=["POST", "GET"])
def view_movie():
    is_active_reliase = is_activate_filter(request.form, 'year_')
    is_active_genre = is_activate_filter(request.form, 'genre_')
    is_active_directors = is_activate_filter(request.form, 'director_')

    context = {
            "title": "ТОП 250 ПО ВЕРСИИ FILMIX.NET",
            "reliase_data": Reliase.query.order_by(Reliase.year.desc()),
            "all_genres": Genres.query.all(),
            "all_directors": Directors.query.all(),
            "movies_sorted": data_sorted,
            "is_active_years": is_active_reliase,
            "is_active_genre": is_active_genre,
            "is_active_directors": is_active_directors,
        }
    
    page = request.args.get('page')
    if page  and page.isdigit():
        page = int(page)
    else:
        page = 1


    q = request.args.get('q')
    if q:
        movies = search_movie(q)
        pages = movies.paginate(page=page, per_page=Config.PAGINATE_ITEM_IN_PAGE)

        context["movies"] = movies

        print(context)
        return render_template('search.html', **context, pages=pages, q=q)

    is_sorted = request.form.get('sorted')
    print("SORTED -------\n", is_sorted, "\n-----")

    if is_sorted:
        movies = is_active_sorted(is_sorted)
    else:
        movies = activate_filter(is_active_reliase, is_active_genre, is_active_directors)
        print("MOVIES -------\n", movies, "\n-----")
    
    pages = movies.paginate(page=page, per_page=Config.PAGINATE_ITEM_IN_PAGE)
    print(pages)
    context["movies"] = movies

    print(context)
    return render_template('index.html', **context, pages=pages)

