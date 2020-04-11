from config import configure
from flask import Flask, request, Response
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
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
    cast_member, director, genre, movie_cast_member, movie_origin,
    movie, movie_director
)


@app.route('/movies', methods=['GET'])
@use_args(MoviesRequest(), location="query")
def list_movies(args):
    from services.movie_service import MovieService
    from models.movie import MovieSchema
    movie_schema = MovieSchema(many=True)
    movie_service = MovieService(db)

    data = movie_service.get_all(args['page'], args['page_size'])
    return movie_schema.dump_as_json(data)


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

    return movie_schema.dump_as_json(movie_instance)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() \
        in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run()
