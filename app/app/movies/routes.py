from flask import render_template
from flask import request
from .services import ServiceMovies
from app.settings import Config
from app.movies import movie
from flask_login import login_required


@movie.route('/search', methods=["POST", "GET"])
def search_movies():
    service_movies = ServiceMovies()
    # дополняем context
    service_movies.context["title"] = "Результат поиска"
    # получаем номер страницы
    page = service_movies.get_page(request)
    # поиск фильма
    search_movie = service_movies.search_movie(request.args.get('q'))
    pages = search_movie.paginate(page=page, per_page=Config.PAGINATE_ITEM_IN_PAGE)
    service_movies.context["movies"] = search_movie
    return render_template('search.html', **service_movies.context, pages=pages, q=request.args.get('q'))


@movie.route('/', methods=["POST", "GET"])
def view_movie():
    service_movies = ServiceMovies()
    # проверяем включены ли фильтра
    is_active_reliase = service_movies.is_activate_filter(request.form, 'year_')
    is_active_genre = service_movies.is_activate_filter(request.form, 'genre_')
    is_active_directors = service_movies.is_activate_filter(request.form, 'director_')
    # дополняем context
    service_movies.context["title"] = "ТОП 250 ПО ВЕРСИИ FILMIX.NET"
    # фильтра
    service_movies.context["is_active_years"] = is_active_reliase
    service_movies.context["is_active_genre"] = is_active_genre
    service_movies.context["is_active_directors"] = is_active_directors
    # получаем номер страницы
    page = service_movies.get_page(request)
    # сортировка или фильтр
    is_sorted = request.form.get('sorted')
    if is_sorted:
        movies = service_movies.is_active_sorted(is_sorted)
    else:
        movies = service_movies.activate_filter(is_active_reliase, is_active_genre, is_active_directors)

    pages = movies.paginate(page=page, per_page=Config.PAGINATE_ITEM_IN_PAGE)
    service_movies.context["movies"] = movies
    return render_template('index.html', **service_movies.context, pages=pages)
