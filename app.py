from flask import Flask, request, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from werkzeug.utils import secure_filename
from config import configure
import os
import logging
from os import path

ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
configure(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)
logger = logging.getLogger('app')

from models import (
    cast_member, director, genre, movie_cast_member, movie_origin,
    movie, movie_director
)


@app.route('/movies', methods=['GET'])
def list_movies():
    from services.movie_service import MovieService
    from models.movie import MovieSchema
    movie_schema = MovieSchema(many=True)
    movie_service = MovieService(db)
    page = 1
    page_size = 100

    if request.args.get('page'):
        index = request.args.get('page')
        if index == 0:
            index = 1

    if request.args.get('page_size'):
        page_size = request.args.get('page_size')
    data = movie_service.get_all(page, page_size)
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
