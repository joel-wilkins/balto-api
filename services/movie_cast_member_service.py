from models.movie_cast_member import MovieCastMember
import uuid


class MovieCastMemberService():
    db = None

    def __init__(self, db):
        self.db = db

    def get_list_from_movie_and_cast(
        self, movie_id: str, cast_member_ids: []
    ) -> []:
        movie_cast_members = []
        for member_id in cast_member_ids:
            movie_cast_members.append(MovieCastMember(movie_id, member_id))
        return movie_cast_members

    def insert_many(self, movie_cast_members: []) -> None:
        for movie_cast_member in movie_cast_members:
            self.db.session.add(movie_cast_member)

        self.db.session.commit()

    def insert(self, movie_cast_member: MovieCastMember) -> uuid:
        self.db.session.add(movie_cast_member)
        self.db.session.commit()
        return movie_cast_member.id

    def delete_by_movie_id(self, movie_id, commit):
        self.db.session.query(MovieCastMember).filter(
            MovieCastMember.movie_id == movie_id
        ).delete()
        if (commit):
            self.db.session.commit()
