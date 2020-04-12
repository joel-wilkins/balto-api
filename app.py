from config import configure
from flask import Flask, request, Response
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from os import path
from werkzeug.utils import secure_filename
from webargs.flaskparser import use_args
from request_schemas.movies_request import MoviesRequest
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
from flask.json import jsonify


@app.route('/movies', methods=['GET'])
@use_args(MoviesRequest(), location="query")
def list_movies(args):
    from services.movie_service import MovieService
    from models.movie import MovieSchema
    movie_schema = MovieSchema(many=True)
    movie_service = MovieService(db)

    data = movie_service.get_all(args['page'], args['page_size'])
    return jsonify(movie_schema.dump(data))


@app.route('/movies/count', methods=['GET'])
def get_movie_count():
    from services.movie_service import MovieService
    movie_service = MovieService(db)

    return str(movie_service.get_count())


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


@app.route("/movies/<movie_id>")
def get_movie(movie_id):
    from services.movie_service import MovieService
    from models.movie import MovieSchema

    movie_schema = MovieSchema()
    movie_service = MovieService(db)

    movie_instance = movie_service.get(movie_id)

    if movie_instance is None:
        return Response(status=404)

    return jsonify(movie_schema.dump(movie_instance))


@app.route("/cast")
@use_args({'query': fields.Str(required=True)}, location="query")
def get_cast(args):
    from services.cast_member_service import CastMemberService
    from models.cast_member import CastSchema

    cast_service = CastMemberService(db)
    cast_schema = CastSchema(many=True)

    cast = cast_service.get_all(args['query'])
    return jsonify(cast_schema.dump(cast))


@app.route("/directors")
@use_args({'query': fields.Str(required=True)}, location="query")
def get_directors(args):
    from services.director_service import DirectorService
    from models.director import DirectorSchema

    director_service = DirectorService(db)
    director_schema = DirectorSchema(many=True)

    director = director_service.get_all(args['query'])
    return jsonify(director_schema.dump(director))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() \
        in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run()
