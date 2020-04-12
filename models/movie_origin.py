from sqlalchemy.dialects.postgresql import UUID
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from app import db
import uuid


class MovieOrigin(db.Model):
    __tablename__ = 'movie_origin'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    origin = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, origin: str):
        self.origin = origin


class OriginSchema(SQLAlchemySchema):
    class Meta:
        model = MovieOrigin

    id = auto_field()
    origin = auto_field()
