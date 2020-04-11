from models.genre import Genre
import uuid


class GenreService():
    db = None

    def __init__(self, db):
        self.db = db

    def get_id(self, genre: str) -> uuid:
        return self.db.session.query(Genre.id).filter(
            Genre.genre == genre).scalar()

    def insert(self, genre: Genre) -> uuid:
        self.db.session.add(genre)
        self.db.session.commit()
        return genre.id
