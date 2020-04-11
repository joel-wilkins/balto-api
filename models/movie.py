from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey
from app import db, ma
import uuid


class Movie(db.Model):
    __tablename__ = 'movie'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    release_year = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(120), nullable=False)
    wikipedia_link = db.Column(db.String(500), nullable=True)
    plot = db.Column(db.String(), nullable=False)
    origin_id = db.Column(ForeignKey('movie_origin.id'), nullable=True)
    genre_id = db.Column(ForeignKey('genre.id'), nullable=True)

    def __init__(
            self,
            release_year,
            title,
            wikipedia_link,
            plot,
            origin_id,
            genre_id):
        self.release_year = release_year
        self.title = title
        self.wikipedia_link = wikipedia_link
        self.plot = plot
        self.origin_id = origin_id
        self.genre_id = genre_id


class MovieSchema(ma.Schema):
    class Meta:
        fields = (
            'id', 'release_year', 'title', 'wikipedia_link', 'plot',
            'origin_id', 'genre_id'
        )

    def dump_as_json(self, data):
        from flask import jsonify
        dumped_data = self.dump(data)
        return jsonify(dumped_data)
