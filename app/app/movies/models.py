from app import db
from app.users.models import Users


genre_movie = db.Table('genre_movie',
    db.Column('movies_id', db.Integer, db.ForeignKey('movies.id')),
    db.Column('genres_id', db.Integer, db.ForeignKey('genres.id'))
)


class Genres(db.Model):
    __tablename__ = 'genres'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return self.name


class Directors(db.Model):
    __tablename__ = 'directors'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return self.name


class Ratings(db.Model):
    __tablename__ = 'ratings'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    star = db.Column(db.Float)

    def __repr__(self):
        return f'{self.star}'


class Reliase(db.Model):
    __tablename__ = 'reliase'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    year = db.Column(db.Integer, index=True, unique=True)

    def __repr__(self):
        return f'{self.year}'


class Movies(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(64), index=True, nullable=False)
    description = db.Column(db.Text())
    poster = db.Column(db.String())

    reliase_id = db.Column(db.Integer, db.ForeignKey('reliase.id', ondelete='SET NULL'))
    reliase = db.relationship('Reliase', passive_deletes="all")

    director_id = db.Column(db.Integer, db.ForeignKey('directors.id', ondelete='SET NULL'))
    director = db.relationship('Directors', backref=db.backref('movies'), passive_deletes="all") 

    rating_id = db.Column(db.Integer, db.ForeignKey('ratings.id', ondelete='SET NULL'))
    rating = db.relationship('Ratings', backref=db.backref('movies'), passive_deletes="all")

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    user = db.relationship('Users', backref=db.backref('movies'), passive_deletes="all", )

    genres_id = db.Column(db.Integer, db.ForeignKey('genres.id', ondelete='SET NULL'))
    genres = db.relationship('Genres', secondary=genre_movie, backref=db.backref('movies', lazy='dynamic'), passive_deletes="all")

    def __repr__(self):
        return self.title
    

