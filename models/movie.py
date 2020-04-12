from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow import fields
from app import db
import uuid
from models.genre import GenreSchema
from models.director import DirectorSchema
from models.cast_member import CastSchema
from models.movie_origin import OriginSchema


class Movie(db.Model):
    __tablename__ = 'movie'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    release_year = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(120), nullable=False)
    wikipedia_link = db.Column(db.String(500), nullable=True)
    plot = db.Column(db.String(), nullable=False)
    origin_id = db.Column(ForeignKey('movie_origin.id'), nullable=True)
    genre_id = db.Column(ForeignKey('genre.id'), nullable=True)

    genre = db.relationship('Genre')
    origin = db.relationship('MovieOrigin')
    cast = db.relationship(
        'CastMember', secondary='movie_cast_member'
    )
    directors = db.relationship(
        'Director', secondary='movie_director'
    )

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


class MovieSchema(SQLAlchemySchema):
    class Meta:
        model = Movie
        include_relationships = True

    id = auto_field()
    release_year = auto_field()
    title = auto_field()
    wikipedia_link = auto_field()
    plot = auto_field()
    origin_id = auto_field()
    genre = fields.Nested(GenreSchema)
    directors = fields.Nested(DirectorSchema, many=True)
    cast = fields.Nested(CastSchema, many=True)
    origin = fields.Nested(OriginSchema)
