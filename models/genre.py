from sqlalchemy.dialects.postgresql import UUID
from app import db
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
import uuid


class Genre(db.Model):
    __tablename__ = 'genre'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    genre = db.Column(db.String(120), nullable=False, unique=True)

    def __init__(self, genre: str):
        self.genre = genre


class GenreSchema(SQLAlchemySchema):
    class Meta:
        model = Genre

    id = auto_field()
    genre = auto_field()
