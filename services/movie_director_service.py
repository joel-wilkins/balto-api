from models.movie_director import MovieDirector
import uuid


class MovieDirectorService():
    db = None

    def __init__(self, db):
        self.db = db

    def get_list_from_movie_and_cast(
        self, movie_id: str, director_id: []
    ) -> []:
        movie_directors = []
        for director_id in director_id:
            movie_directors.append(MovieDirector(movie_id, director_id))

    def insert_many(self, movie_directors: []) -> None:
        for movie_director in movie_directors:
            self.db.session.add(movie_director)

        self.db.session.commit()

    def insert(self, movie_director: MovieDirector) -> uuid:
        self.db.session.add(movie_director)
        self.db.session.commit()
        return movie_director.id
