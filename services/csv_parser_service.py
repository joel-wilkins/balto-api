import csv
import logging
from models.movie import Movie
from models.genre import Genre
from models.movie_origin import MovieOrigin
from services.director_service import DirectorService
from services.movie_service import MovieService
from services.genre_service import GenreService
from services.origin_service import OriginService
from services.cast_member_service import CastMemberService
from services.movie_cast_member_service import MovieCastMemberService
from services.movie_director_service import MovieDirectorService
import uuid

logger = logging.getLogger("CsvParserService")


class CsvParserService:
    director_service: DirectorService = None
    movie_service: MovieService = None
    genre_service: GenreService = None
    origin_service: OriginService = None
    cast_member_service: CastMemberService = None
    movie_cast_member_service: MovieCastMemberService = None
    movie_director_service: MovieDirectorService = None

    def __init__(self, db):
        self.director_service = DirectorService(db)
        self.movie_service = MovieService(db)
        self.genre_service = GenreService(db)
        self.origin_service = OriginService(db)
        self.cast_member_service = CastMemberService(db)
        self.movie_cast_member_service = MovieCastMemberService(db)
        self.movie_director_service = MovieDirectorService(db)

    def parse_csv_into_movies(self, file_name: str):
        with open(file_name) as csv_file:
            movie_reader = csv.DictReader(csv_file)
            for row in movie_reader:
                self.__parse_and_insert_row(row)

    def __parse_and_insert_row(self, row):
        director_ids = self.__parse_and_insert_director(row)
        genre_id = self.__parse_and_insert_genre(row)
        origin_id = self.__parse_and_insert_origin(row)
        cast_member_ids = self.__parse_and_insert_cast_members(row)

        self.__parse_and_insert_movie(
            row, director_ids, genre_id, origin_id, cast_member_ids
        )

    def __parse_and_insert_director(self, row) -> []:
        directors = row['Director']

        if len(directors) == 0:
            return []

        director_list = self.__sanitize_string(directors).split(',')
        director_ids = []

        for director in director_list:
            if (len(director) > 240):
                continue

            director_record = self.director_service.parse_from_string(
                director.strip())

            if director_record is None:
                continue

            director_id = self.director_service.get_id(director_record)
            if (not director_id):
                director_id = self.director_service.insert(director_record)

            if (not self.__has_item(director_ids, director_id)):
                director_ids.append(director_id)

        return director_ids

    def __parse_and_insert_genre(self, row) -> uuid:
        genre = row['Genre']
        genre_id = self.genre_service.get_id(genre)

        if not genre_id:
            genre_id = self.genre_service.insert(Genre(genre))

        return genre_id

    def __parse_and_insert_origin(self, row) -> uuid:
        origin = row['Origin/Ethnicity']
        origin_id = self.origin_service.get_id(origin)

        if not origin_id:
            origin_id = self.origin_service.insert(MovieOrigin(origin))

        return origin_id

    def __parse_and_insert_cast_members(self, row) -> []:
        cast_members = row['Cast']

        if len(cast_members) == 0:
            return []

        cast_list = self.__sanitize_string(cast_members).split(',')
        cast_ids = []

        for cast in cast_list:
            if (len(cast) > 240):
                continue

            cast_member = self.cast_member_service.parse_from_string(
                cast.strip())

            if cast_member is None:
                continue

            cast_member_id = self.cast_member_service.get_id(cast_member)
            if (not cast_member_id):
                cast_member_id = self.cast_member_service.insert(cast_member)

            if (not self.__has_item(cast_ids, cast_member_id)):
                cast_ids.append(cast_member_id)

        return cast_ids

    def __parse_and_insert_movie(
        self,
        row,
        director_ids: [],
        genre_id: uuid,
        origin_id: uuid,
        cast_ids: []
    ) -> uuid:
        movie_title = row['Title']

        if len(movie_title) > 120:
            movie_title = f'{movie_title[:117]}...'

        release_year = row['Release Year']
        wiki_page = row['Wiki Page']
        plot = row['Plot']

        movie_id = self.movie_service.insert(
            Movie(
                release_year,
                movie_title,
                wiki_page,
                plot,
                origin_id,
                genre_id
            )
        )

        if len(director_ids) > 0:
            self.movie_director_service.insert_many(
                self.movie_director_service.get_list_from_movie_and_director(
                    movie_id, director_ids
                )
            )

        if len(cast_ids) > 0:
            self.movie_cast_member_service.insert_many(
                self.movie_cast_member_service.get_list_from_movie_and_cast(
                    movie_id, cast_ids
                )
            )

        return movie_id

    def __sanitize_string(self, string_to_sanitize: str) -> str:
        return string_to_sanitize.replace(', Jr.', '') \
            .replace('(unconfirmed)', '') \
            .replace(', Sr.', '')

    def __has_item(self, array: [], thing_to_find) -> bool:
        try:
            array.index(thing_to_find)
            return True
        except ValueError:
            return False
