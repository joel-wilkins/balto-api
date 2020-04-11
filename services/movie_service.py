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

    def get(self, movie_id):
        return Movie.query.filter(Movie.id == movie_id).scalar()

    def get_all(self, page: int, page_size: int):
        return Movie.query.paginate(page, page_size).items
