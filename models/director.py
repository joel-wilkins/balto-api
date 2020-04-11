from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String
from models.base_model import Base
import uuid


class Director(Base):
    __tablename__ = 'director'

    id = Column(UUID(as_uuid=True), primary_key=True)
    first_name = Column(String(120), unique=True, nullable=False)
    last_name = Column(String(120), unique=True, nullable=False)
    full_name = Column(String(120), unique=True, nullable=False)
