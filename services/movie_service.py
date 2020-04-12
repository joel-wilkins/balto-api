from models.movie import Movie
from sqlalchemy import func
import uuid
from services.movie_director_service import MovieDirectorService
from services.movie_cast_member_service import MovieCastMemberService
from models.movie_cast_member import MovieCastMember
from models.movie_director import MovieDirector


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
        return self.db.session.query(Movie).order_by(
            Movie.release_year.desc(),
            Movie.title
        ).paginate(page, page_size).items

    def get_count(self):
        count_query = self.db.session.query(Movie).statement.with_only_columns(
            [func.count('id')]
        )
        return self.db.session.execute(count_query).scalar()

    def update(self, movie: Movie, args):
        movie.genre_id = args['genre']['id']
        movie.origin_id = args['origin']['id']
        movie.plot = args['plot']
        movie.release_year = args['release_year']
        movie.title = args['title']
        movie.wikipedia_link = args['wikipedia_link']

        cast_member_service = MovieCastMemberService(self.db)
        director_service = MovieDirectorService(self.db)

        cast_member_service.delete_by_movie_id(movie.id, False)
        director_service.delete_by_movie_id(movie.id, False)

        self.db.session.commit()

        if len(args['cast']) > 0:
            movie_cast_records = []
            for cast in args['cast']:
                movie_cast_records.append(
                    MovieCastMember(movie.id, cast['id'])
                )
            cast_member_service.insert_many(movie_cast_records)

        if len(args['directors']) > 0:
            movie_director_records = []
            for director in args['directors']:
                movie_director_records.append(
                    MovieDirector(movie.id, director['id'])
                )
            director_service.insert_many(movie_director_records)

    def delete(self, movie: Movie):
        self.db.session.delete(movie)
        self.db.session.commit()
