from .models import Movies, Reliase, Genres, Directors, Ratings, genre_movie
from sqlalchemy.orm import joinedload


def search_movie(q):
    return Movies.query.filter(Movies.title.ilike(f"%{q}%"))


def is_activate_filter(form, filter_name):
    list_activate_filter = []
    for filter in form:
        if filter.startswith(filter_name):
            filter_id = filter[len(filter_name):]
            list_activate_filter.append(int(filter_id))

    return list_activate_filter


def activate_filter(active_reliase, active_genre, active_directors):
    movies = Movies.query
    
    if active_reliase:
        movies_reliase = movies.join(Reliase).filter(Reliase.id.in_(active_reliase))
        # if movies_reliase:
        movies = movies_reliase

    if active_genre:
        movies_genre = movies.join(genre_movie).join(Genres).options(joinedload(
                Movies.genres)).filter(Genres.id.in_(active_genre))
        # if movies_genre:
        movies = movies_genre
    
    if active_directors:
        movies_directors = movies.join(Directors).filter(Directors.id.in_(active_directors))
        # if movies_directors:
        movies = movies_directors

    return movies


def is_active_sorted(sorted):
        if sorted == "rating_asc":
            return Movies.query.join(Ratings).filter(Ratings.id==Movies.rating_id).order_by(Ratings.star.asc())
        
        if sorted == "rating_desc":
            return Movies.query.join(Ratings).filter(Ratings.id==Movies.rating_id).order_by(Ratings.star.desc())
        
        if sorted == "release_date_asc":
            return Movies.query.join(Reliase).filter(Reliase.id==Movies.reliase_id).order_by(Reliase.year.asc())

        if sorted == "release_date_desc":
            return Movies.query.join(Reliase).filter(Reliase.id==Movies.reliase_id).order_by(Reliase.year.desc())
        
        if sorted == "standart":
            return Movies.query.order_by(Movies.id.desc())
