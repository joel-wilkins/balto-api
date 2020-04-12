from models.movie import Movie
from sqlalchemy import func
import uuid
from services.movie_director_service import MovieDirectorService
from services.movie_cast_member_service import MovieCastMemberService


class MovieService():
    db = None

    def __init__(self, db):
        self.db = db

    def insert(self, movie: Movie) -> uuid:
        self.db.session.add(movie)
        self.db.session.commit()
        return movie.id

    def get(self, movie_id):
        return self.db.session.query(Movie).filter(Movie.id == movie_id) \
            .scalar()

    def get_all(self, page: int, page_size: int):
        return self.db.session.query(Movie).paginate(page, page_size).items

    def get_count(self):
        count_query = self.db.session.query(Movie).statement.with_only_columns(
            [func.count('id')]
        )
        return self.db.session.execute(count_query).scalar()

    def delete(self, movie: Movie):
        self.db.session.delete(movie)
        self.db.session.commit()
