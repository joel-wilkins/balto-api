from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Integer
from models.base_model import Base
import uuid


class Genre(Base):
    __tablename__ = 'genre'

    id = Column(UUID(as_uuid=True), primary_key=True)
    genre = Column(String(120), nullable=False, unique=True)
