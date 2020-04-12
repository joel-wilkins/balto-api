from models.movie_origin import MovieOrigin
import uuid


class OriginService():
    db = None

    def __init__(self, db):
        self.db = db

    def get_id(self, origin: str) -> uuid:
        return self.db.session.query(MovieOrigin.id).filter(
            MovieOrigin.origin == origin).scalar()

    def insert(self, origin: MovieOrigin) -> uuid:
        self.db.session.add(origin)
        self.db.session.commit()
        return origin.id

    def get_all(self):
        return self.db.session.query(MovieOrigin).all()
