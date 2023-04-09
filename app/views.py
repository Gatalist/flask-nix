from flask import render_template, request
from app import app
from app import db
from .models import Users, Movies, Genres, Ratings, Reliase, genre_movie, Directors
from sqlalchemy.orm import joinedload


class BaseContextData():
    def __init__(self, request_form):
        self.request_form = request_form
        self.all_directors = Directors.query.all()
        self.all_genres = Genres.query.all()
        self.all_reliase_years = Reliase.query.order_by(Reliase.year.desc())
        # self.movies = Movies.query #.order_by(Movies.id.desc())
        self.movies = Movies.query.all()
        self.standart = "standart"
        self.rating_asc = "rating_asc"
        self.rating_desc = "rating_desc"
        self.release_date_asc = "release_date_asc"
        self.release_date_desc = "release_date_desc"
        self.data_sorted = [
                {'value': self.standart, 'text': 'стандартная',},
                {'value': self.rating_asc, 'text': 'От мин до мах рейтинга',},
                {'value': self.rating_desc, 'text': 'От мах до мин рейтинга',},
                {'value': self.release_date_asc, 'text': 'От старых до новых',},
                {'value': self.release_date_desc, 'text': 'От новых до старых',},
            ]
        
        self.context = {
                "title": "ТОП 250 ПО ВЕРСИИ FILMIX.NET",
                "reliase_data": self.all_reliase_years,
                "all_genres": self.all_genres,
                "all_directors": self.all_directors,
                "movies_sorted": self.data_sorted,
                "is_active_years": self.is_activate_filter(request_form, 'year_'),
                "is_active_genre": self.is_activate_filter(request_form, 'genre_'),
                "is_active_directors": self.is_activate_filter(request_form, 'director_'),
            }

    @staticmethod
    def is_activate_filter(form, filter_name):
        print(form)
        list_filter = []
        for filter in form:
            if filter.startswith(filter_name):
                filter_id = filter[len(filter_name):]
                list_filter.append(int(filter_id))
        print(list_filter)
        return list_filter
    
    def activate_filter_reliase_genre(self, active_reliase, active_genre, active_directors):
        movies = None
      
        if active_reliase and not active_genre and not active_directors:
            # filter relise
            movies = Movies.query.join(Reliase).filter(Reliase.id.in_(active_reliase))

        if not active_reliase and active_genre and not active_directors:
            # filter genre
            movies = Movies.query.join(genre_movie).join(Genres).options(joinedload(
                    Movies.genres)).filter(Genres.id.in_(active_genre))
        
        if not active_reliase and not active_genre and active_directors:
            # filter director
            movies = Movies.query.join(Directors).filter(Directors.id.in_(active_directors))

        if active_reliase and active_genre and not active_directors:
            # filter relise + genre
            movies = Movies.query.join(genre_movie).join(Genres).join(Reliase).options(
                joinedload(Movies.genres)).filter(
                Reliase.id.in_(active_reliase)).filter(
                Genres.id.in_(active_genre))
        
        if active_reliase and not active_genre and active_directors:            
            movies = Movies.query.join(Reliase).join(Directors).filter(
                Reliase.id.in_(active_reliase)).filter(
                Directors.id.in_(active_directors))
        
        if not active_reliase and active_genre and active_directors:
            # filter genre + director
            movies = Movies.query.join(genre_movie).join(Genres).join(Directors).options(
                joinedload(Movies.genres)).filter(
                Genres.id.in_(active_genre)).filter(
                Directors.id.in_(active_directors))

        if active_reliase and active_genre and active_directors:
            # all filters
            movies = Movies.query.join(genre_movie).join(Genres).join(Reliase).join(
            Directors).options(joinedload(Movies.genres)).filter(
            Reliase.id.in_(active_reliase)).filter(
            Genres.id.in_(active_genre)).filter(
            Directors.id.in_(active_directors))

        return movies


    def search(self, q):
        return db.session.query(Movies).filter(Movies.title.ilike(f"%{q}%"))
    

    def is_active_sorted(self, sorted):
        if sorted == self.rating_asc:
            return Movies.query.join(Ratings, Ratings.id==Movies.rating_id).order_by(Ratings.star.asc()) # .all()
        
        if sorted == self.rating_desc:
            return Movies.query.join(Ratings, Ratings.id==Movies.rating_id).order_by(Ratings.star.desc()) # .all()
        
        if sorted == self.release_date_asc:
            return Movies.query.join(Reliase, Reliase.id==Movies.reliase_id).order_by(Reliase.year.asc()) # .all()

        if sorted == self.release_date_desc:
            return Movies.query.join(Reliase, Reliase.id==Movies.reliase_id).order_by(Reliase.year.desc()) # .all()
        
        if sorted == self.standart:
            return Movies.query.order_by(Movies.id.desc())


@app.route('/filter', methods=['GET', 'POST'])
def movie_filter():
    form = request.form
    base_context_data = BaseContextData(form)
    context = base_context_data.context
    movies = Movies.query.all()

    is_sorted = request.form.get('sorted')
    print("1-------\n", is_sorted, "\n-----")
    
    is_active_reliase = base_context_data.is_activate_filter(form, 'year_')
    is_active_genre = base_context_data.is_activate_filter(form, 'genre_')
    is_active_directors = base_context_data.is_activate_filter(form, 'director_')

    if is_sorted and not is_active_reliase and not is_active_genre and not is_active_directors:
        movies = base_context_data.is_active_sorted(is_sorted)
    
    if not is_sorted or is_active_reliase or is_active_genre or is_active_directors:
        movies = base_context_data.activate_filter_reliase_genre(is_active_reliase, is_active_genre, is_active_directors)

    context["movies"] = movies
    print(context)
    return render_template('index.html', **context)


@app.route('/', methods=['GET', 'POST'])
def view_movie():
    base_context_data = BaseContextData(request.form)
    movies = base_context_data.movies
    context = base_context_data.context

    q = request.args.get('q')
    if q:
        movies = base_context_data.search(q)

    context["movies"] = movies
    print(context)

    if q:
        return render_template('search.html', **context, q=q)
    else:
        return render_template('index.html', **context)