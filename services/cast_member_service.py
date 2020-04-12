from models.cast_member import CastMember
from sqlalchemy import or_
import uuid


class CastMemberService():
    db = None

    def __init__(self, db):
        self.db = db

    def parse_from_string(self, cast_member_name: str) -> CastMember:
        if (not cast_member_name):
            return None

        split_name = cast_member_name.split(' ')
        first_name = ''
        last_name = ''

        if len(split_name) > 1:
            first_name = split_name[0]
            last_name = split_name[-1]
        else:
            first_name = last_name = cast_member_name

        return CastMember(first_name, last_name, cast_member_name)

    def get_id(self, cast_member: CastMember) -> uuid:
        return self.db.session.query(CastMember.id).filter(
            CastMember.first_name == cast_member.first_name or
            CastMember.last_name == cast_member.last_name or
            CastMember.full_name == cast_member.full_name).scalar()

    def get_all(self, query):
        wildcarded_query = f'{query}%'
        return self.db.session.query(CastMember).filter(
            or_(
                CastMember.first_name.ilike(wildcarded_query),
                CastMember.last_name.ilike(wildcarded_query),
                CastMember.full_name.ilike(wildcarded_query)
            )
        ).all()

    def insert(self, cast_member: CastMember) -> uuid:
        self.db.session.add(cast_member)
        self.db.session.commit()
        return cast_member.id
