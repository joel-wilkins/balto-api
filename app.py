from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from config import configure
import os
import logging
from os import path

ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
configure(app)
db = SQLAlchemy(app)
logger = logging.getLogger('app')

from models import (cast_member, director, genre,
                    movie_cast_member, movie_origin, movie)


@app.route('/movies', methods=['GET'])
def list_movies():
    return 'no movies yet'


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
    return f'no movie found with id {movie_id}'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() \
        in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run()
