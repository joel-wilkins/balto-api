from sqlalchemy import ForeignKey
from app import db


class MovieCastMember(db.Model):
    __tablename__ = 'movie_cast_member'

    movie_id = db.Column(ForeignKey('movie.id'), primary_key=True)
    cast_member_id = db.Column(ForeignKey('cast_member.id'), primary_key=True)

    def __init__(self, movie_id: str, cast_member_id: str):
        self.movie_id = movie_id
        self.cast_member_id = cast_member_id
