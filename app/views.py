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
        self.movies = Movies.query
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
            }

    @staticmethod
    def is_activate_filter(form, filter_name):
        list_filter = []
        for filter in form:
            if filter.startswith(filter_name):
                filter_id = filter[len(filter_name):]
                list_filter.append(int(filter_id))

        return list_filter
    
    
    def activate_filter(self, active_reliase, active_genre, active_directors):
        movies = self.movies

        self.context["is_active_years"] = active_reliase
        self.context["is_active_genre"] = active_genre
        self.context["is_active_directors"] = active_directors
      
        if active_reliase:
            movies = self.movies.join(Reliase).filter(Reliase.id.in_(active_reliase))

        if active_genre:
            if movies:
                movies = movies.join(genre_movie).join(Genres).options(joinedload(
                    Movies.genres)).filter(Genres.id.in_(active_genre))
            else:
                movies = self.movies.join(genre_movie).join(Genres).options(joinedload(
                    Movies.genres)).filter(Genres.id.in_(active_genre))
        
        if active_directors:
            if movies:
                movies = movies.join(Directors).filter(Directors.id.in_(active_directors))
            else:
                movies = self.movies.join(Directors).filter(Directors.id.in_(active_directors))
 
        return movies


    def search(self, q):
        return self.movies.filter(Movies.title.ilike(f"%{q}%"))
    

    def is_active_sorted(self, sorted):
        if sorted == self.rating_asc:
            return Movies.query.join(Ratings).filter(Ratings.id==Movies.rating_id).order_by(Ratings.star.asc())
        
        if sorted == self.rating_desc:
            return Movies.query.join(Ratings).filter(Ratings.id==Movies.rating_id).order_by(Ratings.star.desc())
        
        if sorted == self.release_date_asc:
            return Movies.query.join(Reliase).filter(Reliase.id==Movies.reliase_id).order_by(Reliase.year.asc())

        if sorted == self.release_date_desc:
            return Movies.query.join(Reliase).filter(Reliase.id==Movies.reliase_id).order_by(Reliase.year.desc())
        
        if sorted == self.standart:
            return Movies.query.order_by(Movies.id.desc())


@app.route('/', methods=['GET', 'POST'])
def view_movie():
    form = request.form
    base_context_data = BaseContextData(form)
    context = base_context_data.context

    q = request.args.get('q')
    if q:
        movies = base_context_data.search(q)
        context["movies"] = movies
        print(context)
        return render_template('search.html', **context, q=q)

    is_sorted = form.get('sorted')
    print("SORTED -------\n", is_sorted, "\n-----")
    
    is_active_reliase = base_context_data.is_activate_filter(form, 'year_')
    is_active_genre = base_context_data.is_activate_filter(form, 'genre_')
    is_active_directors = base_context_data.is_activate_filter(form, 'director_')

    if is_sorted:
        movies = base_context_data.is_active_sorted(is_sorted)
    else:
        movies = base_context_data.activate_filter(is_active_reliase, is_active_genre, is_active_directors)
        print("MOVIES -------\n", movies, "\n-----")
    
    
    context["movies"] = movies
    print(context)
    return render_template('index.html', **context)

