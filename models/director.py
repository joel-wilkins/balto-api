from sqlalchemy.dialects.postgresql import UUID
from app import db
import uuid


class Director(db.Model):
    __tablename__ = 'director'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = db.Column(db.String(120), unique=False, nullable=False)
    last_name = db.Column(db.String(120), unique=False, nullable=False)
    full_name = db.Column(db.String(240), unique=True, nullable=False)

    def __init__(self, first_name, last_name, full_name):
        self.first_name = first_name
        self.last_name = last_name
        self.full_name = full_name
