from config import configure
from flask import Flask, request, Response, jsonify
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from os import path
from werkzeug.utils import secure_filename
from webargs import flaskparser
from webargs.flaskparser import use_args
from request_schemas.movies_request import MoviesRequest, MovieUpsertRequest
import logging
import os

ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
configure(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)
logger = logging.getLogger('app')
CORS(app)

from models import (
    movie, cast_member, director, genre, movie_cast_member,
    movie_origin, movie_director
)

parser = flaskparser.FlaskParser()


@parser.error_handler
def handle_error(error, req, schema, *args, **kwargs):
    print(args)
    print(kwargs)
    raise Exception('DARN')


@app.route('/movies', methods=['GET'])
@parser.use_args(MoviesRequest(), location="query")
def list_movies(args):
    from services.movie_service import MovieService
    from models.movie import MovieSchema
    movie_schema = MovieSchema(many=True)
    movie_service = MovieService(db)

    data = movie_service.get_all(
        args['page'], args['page_size'], args['query']
    )
    return jsonify(movie_schema.dump(data))


@app.route('/movies/count', methods=['GET'])
@parser.use_args({'query': fields.Str(missing=None)}, location="query")
def get_movie_count(args):
    from services.movie_service import MovieService
    movie_service = MovieService(db)

    return str(movie_service.get_count(args['query']))


@app.route('/movies', methods=['PUT'])
def upload_movie_list():
    from services.csv_parser_service import CsvParserService
    file_key = 'movie_csv'
    if file_key not in request.files:
        return Response(status=400)

    file = request.files[file_key]

    if file.filename == '':
        return Response(status=400)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        if not path.exists(app.config["UPLOAD_FOLDER"]):
            os.mkdir(app.config["UPLOAD_FOLDER"])
        try:
            file.save(file_path)
            CsvParserService(db).parse_csv_into_movies(file_path)
            os.remove(file_path)
        except Exception:
            if (path.exists(file_path)):
                os.remove(file_path)
            logger.exception('error inserting new movie details')
            return Response(status=400)

    return 'SUCCESS'


@app.route("/movies", methods=["POST"])
@parser.use_args(MovieUpsertRequest())
def update_movie(args):
    from services.movie_service import MovieService
    from models.movie import MovieSchema

    movie_service = MovieService(db)
    new_movie = movie_service.insert_from_args(args)

    return jsonify(MovieSchema().dump(new_movie))


@app.route("/movies/<movie_id>", methods=["GET"])
def get_movie(movie_id):
    from services.movie_service import MovieService
    from models.movie import MovieSchema

    movie_schema = MovieSchema()
    movie_service = MovieService(db)

    movie_instance = movie_service.get(movie_id)

    if movie_instance is None:
        return Response(status=404)

    return jsonify(movie_schema.dump(movie_instance))


@app.route("/movies/<movie_id>", methods=["DELETE"])
def delete_movie(movie_id):
    from services.movie_service import MovieService
    movie_service = MovieService(db)

    movie_instance = movie_service.get(movie_id)

    if movie_instance is None:
        return Response(status=404)

    movie_service.delete(movie_instance)

    return Response(status=204)


@app.route("/movies/<movie_id>", methods=["PUT"])
@parser.use_args(MovieUpsertRequest())
def insert_movie(args, movie_id):
    from services.movie_service import MovieService
    movie_service = MovieService(db)

    movie_instance = movie_service.get(args['id'])

    if movie_instance is None:
        return Response(status=404)

    movie_service.update(movie_instance, args)

    return Response(status=200)


@app.route("/cast")
@parser.use_args({'query': fields.Str(required=True)}, location="query")
def get_cast(args):
    from services.cast_member_service import CastMemberService
    from models.cast_member import CastSchema

    cast_service = CastMemberService(db)
    cast_schema = CastSchema(many=True)

    cast = cast_service.get_all(args['query'])
    return jsonify(cast_schema.dump(cast))


@app.route("/directors")
@parser.use_args({'query': fields.Str(required=True)}, location="query")
def get_directors(args):
    from services.director_service import DirectorService
    from models.director import DirectorSchema

    director_service = DirectorService(db)
    director_schema = DirectorSchema(many=True)

    directors = director_service.get_all(args['query'])
    return jsonify(director_schema.dump(directors))


@app.route("/genres")
@parser.use_args({'query': fields.Str(required=True)}, location="query")
def get_genres(args):
    from services.genre_service import GenreService
    from models.genre import GenreSchema

    genre_service = GenreService(db)
    genre_schema = GenreSchema(many=True)

    genres = genre_service.get_all(args['query'])
    return jsonify(genre_schema.dump(genres))


@app.route("/origins")
def get_origins():
    from services.origin_service import OriginService
    from models.movie_origin import OriginSchema

    origin_service = OriginService(db)
    origin_schema = OriginSchema(many=True)

    origins = origin_service.get_all()
    return jsonify(origin_schema.dump(origins))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() \
        in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run()
