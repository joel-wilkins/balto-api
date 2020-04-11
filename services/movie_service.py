from models.movie import Movie
import uuid


class MovieService():
    db = None

    def __init__(self, db):
        self.db = db

    def insert(self, movie: Movie) -> uuid:
        self.db.session.add(movie)
        self.db.session.commit()
        return movie.id
