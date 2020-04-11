from models.director import Director
import uuid


class DirectorService():
    db = None

    def __init__(self, db):
        self.db = db

    def parse_from_string(self, director_name: str) -> Director:
        if (not director_name):
            return None

        split_name = director_name.split(' ')
        first_name = ''
        last_name = ''

        if len(split_name) > 1:
            first_name = split_name[0]
            last_name = split_name[-1]
        else:
            first_name = last_name = director_name

        return Director(first_name, last_name, director_name)

    def get_id(self, director: Director) -> uuid:
        return self.db.session.query(Director.id).filter(
            Director.first_name == director.first_name or
            Director.last_name == director.last_name or
            Director.full_name == director.full_name).scalar()

    def insert(self, director: Director) -> uuid:
        self.db.session.add(director)
        self.db.session.commit()
        return director.id
