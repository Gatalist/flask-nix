from app import db
# from datetime import datetime


genre_movie = db.Table('genre_movie',
    db.Column('movies_id', db.Integer, db.ForeignKey('movies.id')),
    db.Column('genres_id', db.Integer, db.ForeignKey('genres.id'))
)


class Genres(db.Model):
    __tablename__ = 'genres'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return self.name


class Directors(db.Model):
    __tablename__ = 'directors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return self.name


class Ratings(db.Model):
    __tablename__ = 'ratings'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    star = db.Column(db.Float,)

    def __repr__(self):
        return f'{self.star}'


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True,)
    email = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        return self.username


class Movies(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, nullable=False)
    reliase = db.Column(db.Integer)
    director_id = db.Column(db.Integer, db.ForeignKey('directors.id', ondelete="CASCADE"), default='unknown', nullable=False)
    description = db.Column(db.Text())
    rating_id = db.Column(db.Integer, db.ForeignKey('ratings.id'))
    genres_id = db.Column(db.Integer, db.ForeignKey('genres.id'))
    poster = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    genres = db.relationship('Genres', secondary=genre_movie,
        backref=db.backref('movies', lazy='dynamic'))
    
    # director = db.relationship('Directors', cascade='all,delete-orphan')
    director = db.relationship('Directors', cascade='save-update, merge, delete', passive_deletes=True,)
    
    user = db.relationship('Users')
    rating = db.relationship('Ratings', lazy='joined')

    # __table_args__ = (
    #     db.Index('title', "reliase", "rating"),
    # )

    def __repr__(self):
        return self.title
