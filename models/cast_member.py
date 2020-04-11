from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String, ForeignKey
from models.base_model import Base
import uuid


class CastMember(Base):
    __tablename__ = 'cast_member'

    id = Column(UUID(as_uuid=True), primary_key=True)
    first_name = Column(String(120), unique=True, nullable=False)
    last_name = Column(String(120), unique=True, nullable=False)
    full_name = Column(String(120), unique=True, nullable=False)
