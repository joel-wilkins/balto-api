from sqlalchemy import ForeignKey
from app import db


class MovieDirector(db.Model):
    __tablename__ = 'movie_director'

    movie_id = db.Column(ForeignKey('movie.id'), primary_key=True)
    director_id = db.Column(ForeignKey('director.id'), primary_key=True)

    def __init__(self, movie_id: str, director_id: str):
        self.movie_id = movie_id
        self.director_id = director_id
