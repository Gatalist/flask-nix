from app import db
from movies_json import movies_list
from app.movies.models import Movies, Directors, Genres, Ratings, Reliase
from app.users.models import Users


def return_last_id_from_the_table(table):
    last_id = table.query.order_by(table.id.desc()).first()
    if last_id == None:
        last_id = 1
    else:
        last_id = last_id.id + 1
    print(f"new id: {last_id}")
    return last_id


def create_user(name:str, email:str):
    last_id = return_last_id_from_the_table(Users)
    try:
        user = Users(id=last_id+1, username=name, email=email)
        db.session.add(user)
        db.session.commit()
        print(f"user '{name}' created")

    except Exception as e:
        print(e)

# create_user('Alex', 'kostenko.alexander2012@gmail.com')
# create_user('Anna', 'anna@gmail.com')
# create_user('Ivan', 'ivan@gmail.com')
# create_user('Admin', 'admin@gmail.com')
# create_user('Nikolay', 'nikolay@gmail.com')
# <---- END user ---->


def get_feature_to_movies(feature, movies_list):
    feature_list = []
    num = 1
    for _ in movies_list:
        feature_movie = movies_list[num].get(feature)
        if type(feature_movie) == list:
            feature_list.extend(feature_movie)
        else:
            feature_list.append(feature_movie)
        num += 1

    feature_movie = set(feature_list)
    print(feature_movie)
    return feature_movie


# all_genres = get_feature_to_movies("Genres", movies_list)
# all_reliase = get_feature_to_movies("reliase", movies_list)
# all_director = get_feature_to_movies("Director", movies_list)
# all_rating = get_feature_to_movies("Rating", movies_list)


def insert_dependens_for_movie(table, dates):
    if table == "Genres":
        for elem in dates:
            try:
                row = Genres(name=elem)
                db.session.add(row)
                db.session.commit()
                print(f"{table} '{row}' created")

            except Exception as e:
                print(e)

    if table == "Directors":
        for elem in dates:
            try:
                row = Directors(name=elem)
                db.session.add(row)
                db.session.commit()
                print(f"{table} '{row}' created")

            except Exception as e:
                print(e)
                   
    elif table == "Ratings":
        for elem in dates:
            try:
                row = Ratings(star=elem)
                db.session.add(row)
                db.session.commit()
                print(f"{table} '{row}' created")

            except Exception as e:
                print(e)
    
    elif table == "Reliase":
        for elem in dates:
            try:
                row = Reliase(year=elem)
                db.session.add(row)
                db.session.commit()
                print(f"{table} '{row}' created")

            except Exception as e:
                print(e)

    
# insert_dependens_for_movie("Reliase", all_reliase)
# insert_dependens_for_movie("Ratings", all_rating)
# insert_dependens_for_movie(Directors, all_director)
# insert_dependens_for_movie(Genres, all_genres)


def genre_add_to_movie(movie, genres):
    print("movie:", movie)
    for elem in genres:
        genre = Genres.query.filter_by(name=elem).first().id
        print("genre:", genre)

        db.engine.execute(f'INSERT INTO "genre_movie" VALUES(%s, %s);', (movie, genre))
        

def create_movie(movies_list):
    num = 1
    for _ in movies_list:
        movie = movies_list[num]

        reliase = Reliase.query.filter_by(year=movie['reliase']).first().id
        director = Directors.query.filter_by(name=movie['Director']).first().id
        rating = Ratings.query.filter_by(star=movie['Rating']).first().id
        user = Users.query.filter_by(username=movie['user']).first().id
        
        mov = Movies(
                title = movie['title'],
                description = movie['description'],
                poster = movie['Poster'],
                reliase_id = reliase,
                director_id = director,
                rating_id = rating,
                user_id = user,
            )

        num += 1
        db.session.add(mov)
        db.session.commit()

        new_mov_id = Movies.query.order_by(Movies.id.desc()).first().id        
        genres = movie['Genres']

        genre_add_to_movie(new_mov_id, genres)


create_movie(movies_list)


