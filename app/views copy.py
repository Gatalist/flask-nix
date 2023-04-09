from flask import render_template, request, flash, redirect, url_for, session
# from sqlalchemy import func
from sqlalchemy.sql import func
from app import app
from app import db
from .models import Users, Movies, Genres, Ratings, Reliase, genre_movie, Directors
from sqlalchemy.orm import joinedload


def get_movies_to_genres(list_genre):
    return Movies.query.join(genre_movie).join(Genres).options(joinedload(Movies.genres)).filter(Genres.id.in_(list_genre)).all()


def request_genre(form):
    print(form)
    list_genre = []
    for genre_id in form:
        try:
            list_genre.append(int(genre_id))
        except:
            continue

    return list_genre


@app.route('/filter', methods=['GET', 'POST'])
def movie_filter():
    movie_genres = Genres.query.all()

    list_genre = request_genre(request.form)
    print(list_genre)

    movie_genre = get_movies_to_genres(list_genre)
    print(movie_genre)

    directors = Directors.query.all()

    if movie_genre:
        movies = movie_genre
    else:
        movies = Movies.query.all()

    rating_asc = "rating_asc"
    rating_desc = "rating_desc"
    release_date_asc = "release_date_asc"
    release_date_desc = "release_date_desc"

    reliase_min = db.session.query(func.min(Reliase.year)).first()
    reliase_max = db.session.query(func.max(Reliase.year)).first()

    reliase_diapazon = [year for year in range(reliase_min[0], reliase_max[0])]
    print(reliase_diapazon)
    

    data_sorted = [{'value': rating_asc, 'text': 'От мин до мах рейтинга',},
                   {'value': rating_desc, 'text': 'От мах до мин рейтинга',},
                   
                   {'value': release_date_asc, 'text': 'От старых до новых',},
                   {'value': release_date_desc, 'text': 'От новых до старых',},
                ]
    
    context = {
                "title": "ТОП 250 ПО ВЕРСИИ FILMIX.NET",
                "movie_genres": movie_genres,
                "active_genre": list_genre,
                "movies_sorted": data_sorted,
                "reliase_data": reliase_diapazon,
                # "reliase_min": reliase_min[0],
                # "reliase_max": reliase_max[0],
                "movies": movies,
                "directors": directors,
            }


    return render_template('index.html', **context)



@app.route('/', methods=['GET', 'POST'])
def view_movie():
    rating_asc = "rating_asc"
    rating_desc = "rating_desc"
    release_date_asc = "release_date_asc"
    release_date_desc = "release_date_desc"

    reliase_min = db.session.query(func.min(Reliase.year)).first()
    reliase_max = db.session.query(func.max(Reliase.year)).first()

    directors = Directors.query.all()

    # print(reliase_min, reliase_max)

    movie_genres = Genres.query.all()
    reliase_diapazon = [year for year in range(reliase_min[0], reliase_max[0])]
    print(reliase_diapazon)

    data_sorted = [{'value': rating_asc, 'text': 'От мин до мах рейтинга',},
                   {'value': rating_desc, 'text': 'От мах до мин рейтинга',},
                   
                   {'value': release_date_asc, 'text': 'От старых до новых',},
                   {'value': release_date_desc, 'text': 'От новых до старых',},
                ]
    
    context = {
                "title": "ТОП 250 ПО ВЕРСИИ FILMIX.NET",
                "movie_genres": movie_genres,
                "movies_sorted": data_sorted,
                # "reliase_min": reliase_min[0],
                # "reliase_max": reliase_max[0],
                "reliase_data": reliase_diapazon,
                "directors": directors,
            }

    q = request.args.get('q')
    if q:
        q = request.args.get('q')
        movies = db.session.query(Movies).filter(Movies.title.ilike(f"%{q}%"))
    else:
        movies = Movies.query

    sorted = request.form.get('sorted')

    if sorted:
        if sorted == rating_asc:
            context["movies"] = movies.join(Ratings, Ratings.id==Movies.rating_id).order_by(Ratings.star.asc()).all()
        
        if sorted == rating_desc:
            context["movies"] = movies.join(Ratings, Ratings.id==Movies.rating_id).order_by(Ratings.star.desc()).all()
        
        if sorted == release_date_asc:
            context["movies"] = movies.join(Reliase, Reliase.id==Movies.reliase_id).order_by(Reliase.year.asc()).all()

        if sorted == release_date_desc:
            context["movies"] = movies.join(Reliase, Reliase.id==Movies.reliase_id).order_by(Reliase.year.desc()).all()

    else:
        context["movies"] = movies.order_by(Movies.id.desc()).all()
    
    if q:
        return render_template('search.html', **context, q=q)
    else:
        return render_template('index.html', **context)