from sqlalchemy.dialects.postgresql import UUID
from app import db
import uuid


class Genre(db.Model):
    __tablename__ = 'genre'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    genre = db.Column(db.String(120), nullable=False, unique=True)

    def __init__(self, genre: str):
        self.genre = genre
