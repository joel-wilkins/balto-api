from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String
from models.base_model import Base
import uuid


class MovieOrigin(Base):
    __tablename__ = 'movie_origin'

    id = Column(UUID(as_uuid=True), primary_key=True)
    origin = Column(String(120), unique=True, nullable=False)
