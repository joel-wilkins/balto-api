from sqlalchemy.dialects.postgresql import UUID
from app import db
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
import uuid


class CastMember(db.Model):
    __tablename__ = 'cast_member'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = db.Column(db.String(120), unique=False, nullable=False)
    last_name = db.Column(db.String(120), unique=False, nullable=False)
    full_name = db.Column(db.String(240), unique=True, nullable=False)

    def __init__(self, first_name: str, last_name: str, full_name: str):
        self.first_name = first_name
        self.last_name = last_name
        self.full_name = full_name


class CastSchema(SQLAlchemySchema):
    class Meta:
        model = CastMember

    id = auto_field()
    first_name = auto_field()
    last_name = auto_field()
    full_name = auto_field()
