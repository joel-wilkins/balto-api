from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, ForeignKey
from models.base_model import Base
import uuid


class MovieCastMember(Base):
    __tablename__ = 'movie_cast_member'

    movie_id = Column(ForeignKey('movie.id'), primary_key=True)
    cast_member_id = Column(ForeignKey('cast_member.id'), primary_key=True)
