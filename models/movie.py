from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Integer, ForeignKey
from models.base_model import Base
import uuid


class Movie(Base):
    __tablename__ = 'movie'

    id = Column(UUID(as_uuid=True), primary_key=True)
    release_year = Column(Integer, nullable=False)
    title = Column(String(120), nullable=False)
    wikipedia_link = Column(String(500), nullable=True)
    director_id = Column(ForeignKey('director.id'), nullable=True)
    origin_id = Column(ForeignKey('movie_origin.id'), nullable=True)
    genre_id = Column(ForeignKey('genre.id'), nullable=True)
