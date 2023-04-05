from flask import render_template, request
from app import app
from .models import Users, Movies, Genres, Ratings


@app.route('/search', methods=['GET', 'POST'])
def movie_search():
    q = request.args.get('q')
    if q:
        q = request.args.get('q')
        movies = Movies.query.filter(Movies.title.contains(q))
    else:
        movies = 'No result'

    return render_template('index.html', movies=movies, q=q)


@app.route('/', methods=['GET', 'POST'])
def view_movie():
    movies = Movies.query

    movie_genres = Genres.query.all()

    rating_asc = "rating_asc"
    rating_desc = "rating_desc"
    release_date_asc = "release_date_asc"
    release_date_desc = "release_date_desc"

    data_sorted = [{'value': rating_asc, 'text': 'От мин до мах рейтинга',},
                   {'value': rating_desc, 'text': 'От мах до мин рейтинга',},
                   
                   {'value': release_date_asc, 'text': 'От старых до новых',},
                   {'value': release_date_desc, 'text': 'От новых до старых',},
                ]
    
    context = {
                "title": "ТОП 250 ПО ВЕРСИИ FILMIX.NET",
                "movie_genres": movie_genres,
                "movies_sorted": data_sorted,
            }
    
    selected_item_sorted = release_date_asc

    sorted = request.form.get('sorted')
    print(sorted)

    if sorted:
        if sorted == rating_asc:
            context["movies"] = movies.join(Ratings, Ratings.id==Movies.rating_id).order_by(Ratings.star.asc()).all()
        
        if sorted == rating_desc:
            context["movies"] = movies.join(Ratings, Ratings.id==Movies.rating_id).order_by(Ratings.star.desc()).all()
        
        if sorted == release_date_asc:
            context["movies"] = movies.order_by(Movies.reliase.asc()).all()

        if sorted == release_date_desc:
            context["movies"] = movies.order_by(Movies.reliase.desc()).all()
        
        context["selected_item_sorted"] = sorted
        selected_item_sorted = sorted
            
    else:
        context["selected_item_sorted"] = selected_item_sorted
        context["movies"] = movies.order_by(Movies.id.desc()).all()
    
    # print("context:", context)
    
    
    return render_template('index.html', **context)
